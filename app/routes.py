import re

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy import distinct, func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload

from .db import get_session
from .models import (
    Affiliation,
    Author,
    AuthorAffiliation,
    Benchmark,
    DataSourceType,
    EvaluationResult,
    ModelDataSource,
    ModelTopic,
    Paper,
    PaperAuthor,
    Paradigm,
    Topic,
    VlaModel,
)


bp = Blueprint("main", __name__)

PUBLICATION_TYPES = ["arXiv preprint", "conference", "journal"]
PUBLICATION_STATUSES = ["accepted", "published", "unknown"]


def _lower_like(column, text_value):
    pattern = f"%{text_value.lower()}%"
    return func.lower(column).like(pattern)


def _slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", (value or "").strip().lower())
    return slug.strip("-")


def _optional_text(value):
    cleaned = (value or "").strip()
    return cleaned or None


def _optional_int(value):
    cleaned = (value or "").strip()
    if not cleaned:
        return None
    try:
        return int(cleaned)
    except ValueError:
        return None


def _optional_float(value):
    cleaned = (value or "").strip()
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _bar_rows(rows):
    max_count = max((count for _, count in rows), default=0)
    prepared = []
    for label, count in rows:
        prepared.append(
            {
                "label": label or "Unknown",
                "count": count,
                "width": (count / max_count * 100) if max_count else 0,
            }
        )
    return prepared


def _filter_options(session):
    return {
        "paradigms": session.query(Paradigm).order_by(Paradigm.name.asc()).all(),
        "topics": session.query(Topic).order_by(Topic.name.asc()).all(),
        "benchmarks": session.query(Benchmark).order_by(Benchmark.name.asc()).all(),
    }


def _admin_options(session):
    options = _filter_options(session)
    options["data_source_types"] = (
        session.query(DataSourceType).order_by(DataSourceType.name.asc()).all()
    )
    options["publication_types"] = PUBLICATION_TYPES
    options["publication_statuses"] = PUBLICATION_STATUSES
    return options


def _schema_entities():
    return [
        {
            "name": "Paradigm",
            "role": "Reference",
            "fields": ["id (PK)", "name", "description"],
        },
        {
            "name": "Topic",
            "role": "Reference",
            "fields": ["id (PK)", "name", "description"],
        },
        {
            "name": "DataSourceType",
            "role": "Reference",
            "fields": ["id (PK)", "name", "description"],
        },
        {
            "name": "Benchmark",
            "role": "Reference",
            "fields": ["id (PK)", "name", "category", "official_url"],
        },
        {
            "name": "Paper",
            "role": "Core",
            "fields": ["id (PK)", "title", "year", "venue_name", "publication_type"],
        },
        {
            "name": "Model",
            "role": "Core",
            "fields": ["id (PK)", "name", "slug", "year", "paper_id (FK)", "paradigm_id (FK)"],
        },
        {
            "name": "Author",
            "role": "Core",
            "fields": ["id (PK)", "full_name", "notes"],
        },
        {
            "name": "Affiliation",
            "role": "Core",
            "fields": ["id (PK)", "name", "country", "website_url"],
        },
        {
            "name": "PaperAuthor",
            "role": "Bridge",
            "fields": ["paper_id (FK)", "author_id (FK)", "author_order", "is_first_author"],
        },
        {
            "name": "AuthorAffiliation",
            "role": "Bridge",
            "fields": ["author_id (FK)", "affiliation_id (FK)", "notes"],
        },
        {
            "name": "ModelTopic",
            "role": "Bridge",
            "fields": ["model_id (FK)", "topic_id (FK)"],
        },
        {
            "name": "ModelDataSource",
            "role": "Bridge",
            "fields": ["model_id (FK)", "data_source_type_id (FK)", "notes"],
        },
        {
            "name": "EvaluationResult",
            "role": "Fact",
            "fields": ["id (PK)", "model_id (FK)", "benchmark_id (FK)", "metric_name", "metric_value"],
        },
    ]


def _schema_relationships():
    return [
        ("Paradigm", "Model", "1-to-many", "One paradigm can classify many models."),
        ("Paper", "Model", "1-to-many", "One paper can support one or more model records."),
        ("Paper", "Author", "many-to-many", "Implemented through PaperAuthor."),
        ("Author", "Affiliation", "many-to-many", "Implemented through AuthorAffiliation."),
        ("Model", "Topic", "many-to-many", "Implemented through ModelTopic."),
        ("Model", "DataSourceType", "many-to-many", "Implemented through ModelDataSource."),
        ("Model", "EvaluationResult", "1-to-many", "One model can have many benchmark-result rows."),
        ("Benchmark", "EvaluationResult", "1-to-many", "One benchmark can contain many result rows."),
    ]


def _empty_model_form_data():
    return {
        "name": "",
        "slug": "",
        "year": "",
        "open_source": False,
        "summary": "",
        "notes": "",
        "website_url": "",
        "repo_url": "",
        "paper_title": "",
        "paper_year": "",
        "venue_name": "",
        "publication_type": "",
        "publication_status": "",
        "arxiv_url": "",
        "project_url": "",
        "code_url": "",
        "topic_ids": [],
        "data_source_ids": [],
        "paradigm_id": "",
    }


def _model_form_from_request():
    return {
        "name": (request.form.get("name") or "").strip(),
        "slug": (request.form.get("slug") or "").strip(),
        "year": (request.form.get("year") or "").strip(),
        "open_source": request.form.get("open_source") == "on",
        "summary": (request.form.get("summary") or "").strip(),
        "notes": (request.form.get("notes") or "").strip(),
        "website_url": (request.form.get("website_url") or "").strip(),
        "repo_url": (request.form.get("repo_url") or "").strip(),
        "paper_title": (request.form.get("paper_title") or "").strip(),
        "paper_year": (request.form.get("paper_year") or "").strip(),
        "venue_name": (request.form.get("venue_name") or "").strip(),
        "publication_type": (request.form.get("publication_type") or "").strip(),
        "publication_status": (request.form.get("publication_status") or "").strip(),
        "arxiv_url": (request.form.get("arxiv_url") or "").strip(),
        "project_url": (request.form.get("project_url") or "").strip(),
        "code_url": (request.form.get("code_url") or "").strip(),
        "topic_ids": request.form.getlist("topic_ids"),
        "data_source_ids": request.form.getlist("data_source_ids"),
        "paradigm_id": (request.form.get("paradigm_id") or "").strip(),
    }


def _model_form_from_model(model):
    paper = model.paper
    return {
        "name": model.name or "",
        "slug": model.slug or "",
        "year": str(model.year) if model.year is not None else "",
        "open_source": bool(model.open_source),
        "summary": model.summary or "",
        "notes": model.notes or "",
        "website_url": model.website_url or "",
        "repo_url": model.repo_url or "",
        "paper_title": paper.title if paper else "",
        "paper_year": str(paper.year) if paper and paper.year is not None else "",
        "venue_name": paper.venue_name if paper else "",
        "publication_type": paper.publication_type if paper else "",
        "publication_status": paper.publication_status if paper else "",
        "arxiv_url": paper.arxiv_url if paper else "",
        "project_url": paper.project_url if paper else "",
        "code_url": paper.code_url if paper else "",
        "topic_ids": [str(link.topic_id) for link in model.model_topics],
        "data_source_ids": [str(link.data_source_type_id) for link in model.model_data_sources],
        "paradigm_id": str(model.paradigm_id) if model.paradigm_id is not None else "",
    }


def _parse_selected_ids(raw_values):
    values = []
    for raw_value in raw_values:
        parsed_id = _optional_int(raw_value)
        if parsed_id is not None:
            values.append(parsed_id)
    return sorted(set(values))


def _validate_model_form(session, form_data, current_model=None):
    errors = []
    name = form_data["name"]
    slug = form_data["slug"] or _slugify(name)
    year = _optional_int(form_data["year"])
    paper_year = _optional_int(form_data["paper_year"])
    paradigm_id = _optional_int(form_data["paradigm_id"])
    topic_ids = _parse_selected_ids(form_data["topic_ids"])
    data_source_ids = _parse_selected_ids(form_data["data_source_ids"])

    if not name:
        errors.append("Model name is required.")
    if not slug:
        errors.append("Slug is required. Provide a slug or a valid model name.")
    if not paradigm_id:
        errors.append("Paradigm is required.")
    if form_data["year"] and year is None:
        errors.append("Year must be an integer.")
    if form_data["paper_year"] and paper_year is None:
        errors.append("Paper year must be an integer.")
    if form_data["publication_type"] and form_data["publication_type"] not in PUBLICATION_TYPES:
        errors.append("Publication type is invalid.")
    if form_data["publication_status"] and form_data["publication_status"] not in PUBLICATION_STATUSES:
        errors.append("Publication status is invalid.")

    slug_query = session.query(VlaModel).filter(VlaModel.slug == slug)
    name_query = session.query(VlaModel).filter(VlaModel.name == name)
    if current_model is not None:
        slug_query = slug_query.filter(VlaModel.id != current_model.id)
        name_query = name_query.filter(VlaModel.id != current_model.id)

    if slug_query.first():
        errors.append("Slug already exists. Choose a different slug.")
    if name_query.first():
        errors.append("Model name already exists.")

    return errors, {
        "name": name,
        "slug": slug,
        "year": year,
        "paper_year": paper_year,
        "paradigm_id": paradigm_id,
        "topic_ids": topic_ids,
        "data_source_ids": data_source_ids,
    }


def _resolve_paper_for_model_form(session, form_data, normalized, current_model=None):
    paper_title = form_data["paper_title"]
    if not paper_title:
        return None

    current_paper = current_model.paper if current_model is not None else None
    if current_paper is not None and current_paper.title == paper_title:
        current_paper.year = normalized["paper_year"]
        current_paper.venue_name = _optional_text(form_data["venue_name"])
        current_paper.publication_type = _optional_text(form_data["publication_type"])
        current_paper.publication_status = _optional_text(form_data["publication_status"])
        current_paper.arxiv_url = _optional_text(form_data["arxiv_url"])
        current_paper.project_url = _optional_text(form_data["project_url"])
        current_paper.code_url = _optional_text(form_data["code_url"])
        return current_paper

    paper = session.query(Paper).filter(Paper.title == paper_title).one_or_none()
    if paper is not None:
        return paper

    paper = Paper(
        title=paper_title,
        year=normalized["paper_year"],
        venue_name=_optional_text(form_data["venue_name"]),
        publication_type=_optional_text(form_data["publication_type"]),
        publication_status=_optional_text(form_data["publication_status"]),
        arxiv_url=_optional_text(form_data["arxiv_url"]),
        project_url=_optional_text(form_data["project_url"]),
        code_url=_optional_text(form_data["code_url"]),
    )
    session.add(paper)
    session.flush()
    return paper


def _save_model_form(session, model, form_data, normalized):
    paper = _resolve_paper_for_model_form(session, form_data, normalized, current_model=model)

    model.name = normalized["name"]
    model.slug = normalized["slug"]
    model.year = normalized["year"]
    model.open_source = form_data["open_source"]
    model.summary = _optional_text(form_data["summary"])
    model.notes = _optional_text(form_data["notes"])
    model.website_url = _optional_text(form_data["website_url"])
    model.repo_url = _optional_text(form_data["repo_url"])
    model.paradigm_id = normalized["paradigm_id"]
    model.paper_id = paper.id if paper is not None else None

    if model.id is None:
        session.add(model)
        session.flush()
    else:
        session.flush()

    session.query(ModelTopic).filter_by(model_id=model.id).delete()
    session.query(ModelDataSource).filter_by(model_id=model.id).delete()
    session.flush()

    for topic_id in normalized["topic_ids"]:
        session.add(ModelTopic(model_id=model.id, topic_id=topic_id))

    for data_source_id in normalized["data_source_ids"]:
        session.add(
            ModelDataSource(
                model_id=model.id,
                data_source_type_id=data_source_id,
            )
        )

    return model


@bp.route("/")
def index():
    session = get_session()

    stats = {
        "model_count": session.query(func.count(VlaModel.id)).scalar() or 0,
        "paper_count": session.query(func.count(Paper.id)).scalar() or 0,
        "author_count": session.query(func.count(Author.id)).scalar() or 0,
        "benchmark_count": session.query(func.count(Benchmark.id)).scalar() or 0,
    }

    paradigm_stats = (
        session.query(Paradigm.name, func.count(VlaModel.id))
        .outerjoin(VlaModel, Paradigm.id == VlaModel.paradigm_id)
        .group_by(Paradigm.id)
        .order_by(func.count(VlaModel.id).desc(), Paradigm.name.asc())
        .all()
    )

    topic_stats = (
        session.query(Topic.name, func.count(ModelTopic.model_id))
        .outerjoin(ModelTopic, Topic.id == ModelTopic.topic_id)
        .group_by(Topic.id)
        .order_by(func.count(ModelTopic.model_id).desc(), Topic.name.asc())
        .limit(10)
        .all()
    )

    recent_models = (
        session.query(VlaModel)
        .options(
            joinedload(VlaModel.paradigm),
            joinedload(VlaModel.paper),
            selectinload(VlaModel.model_topics).joinedload(ModelTopic.topic),
        )
        .order_by(VlaModel.year.desc(), VlaModel.name.asc())
        .limit(8)
        .all()
    )

    return render_template(
        "index.html",
        stats=stats,
        paradigm_stats=paradigm_stats,
        topic_stats=topic_stats,
        recent_models=recent_models,
    )


@bp.route("/stats")
def stats_dashboard():
    session = get_session()

    stats = {
        "model_count": session.query(func.count(VlaModel.id)).scalar() or 0,
        "open_source_count": session.query(func.count(VlaModel.id))
        .filter(VlaModel.open_source.is_(True))
        .scalar()
        or 0,
        "result_row_count": session.query(func.count(EvaluationResult.id)).scalar() or 0,
        "paper_count": session.query(func.count(Paper.id)).scalar() or 0,
    }

    paradigm_rows = (
        session.query(Paradigm.name, func.count(VlaModel.id))
        .outerjoin(VlaModel, Paradigm.id == VlaModel.paradigm_id)
        .group_by(Paradigm.id)
        .order_by(func.count(VlaModel.id).desc(), Paradigm.name.asc())
        .all()
    )

    topic_rows = (
        session.query(Topic.name, func.count(ModelTopic.model_id))
        .outerjoin(ModelTopic, Topic.id == ModelTopic.topic_id)
        .group_by(Topic.id)
        .order_by(func.count(ModelTopic.model_id).desc(), Topic.name.asc())
        .all()
    )

    data_source_rows = (
        session.query(DataSourceType.name, func.count(ModelDataSource.model_id))
        .outerjoin(ModelDataSource, DataSourceType.id == ModelDataSource.data_source_type_id)
        .group_by(DataSourceType.id)
        .order_by(func.count(ModelDataSource.model_id).desc(), DataSourceType.name.asc())
        .all()
    )

    publication_rows = (
        session.query(Paper.publication_type, func.count(Paper.id))
        .group_by(Paper.publication_type)
        .order_by(func.count(Paper.id).desc(), Paper.publication_type.asc())
        .all()
    )

    benchmark_rows = (
        session.query(Benchmark.name, func.count(distinct(EvaluationResult.model_id)))
        .outerjoin(EvaluationResult, Benchmark.id == EvaluationResult.benchmark_id)
        .group_by(Benchmark.id)
        .order_by(func.count(distinct(EvaluationResult.model_id)).desc(), Benchmark.name.asc())
        .all()
    )

    year_rows = (
        session.query(VlaModel.year, func.count(VlaModel.id))
        .filter(VlaModel.year.is_not(None))
        .group_by(VlaModel.year)
        .order_by(VlaModel.year.asc())
        .all()
    )

    open_source_ratio = 0
    if stats["model_count"]:
        open_source_ratio = round(stats["open_source_count"] / stats["model_count"] * 100, 1)

    return render_template(
        "stats.html",
        stats=stats,
        open_source_ratio=open_source_ratio,
        paradigm_bars=_bar_rows(paradigm_rows),
        topic_bars=_bar_rows(topic_rows),
        data_source_bars=_bar_rows(data_source_rows),
        publication_bars=_bar_rows(publication_rows),
        benchmark_bars=_bar_rows(benchmark_rows),
        year_bars=_bar_rows([(str(year), count) for year, count in year_rows]),
    )


@bp.route("/schema")
def schema_page():
    session = get_session()

    table_counts = {
        "models": session.query(func.count(VlaModel.id)).scalar() or 0,
        "papers": session.query(func.count(Paper.id)).scalar() or 0,
        "authors": session.query(func.count(Author.id)).scalar() or 0,
        "affiliations": session.query(func.count(Affiliation.id)).scalar() or 0,
        "results": session.query(func.count(EvaluationResult.id)).scalar() or 0,
    }

    diagram_text = """Paradigm 1 --- N Model N --- 1 Paper
Model N --- N Topic           via ModelTopic
Model N --- N DataSourceType  via ModelDataSource
Paper N --- N Author          via PaperAuthor
Author N --- N Affiliation    via AuthorAffiliation
Model 1 --- N EvaluationResult N --- 1 Benchmark"""

    return render_template(
        "schema.html",
        table_counts=table_counts,
        entities=_schema_entities(),
        relationships=_schema_relationships(),
        diagram_text=diagram_text,
    )


@bp.route("/models")
def model_list():
    session = get_session()
    paradigm_id = request.args.get("paradigm", type=int)
    topic_id = request.args.get("topic", type=int)
    benchmark_id = request.args.get("benchmark", type=int)
    keyword = request.args.get("q", "").strip()

    query = session.query(VlaModel).options(
        joinedload(VlaModel.paradigm),
        joinedload(VlaModel.paper),
        selectinload(VlaModel.model_topics).joinedload(ModelTopic.topic),
        selectinload(VlaModel.evaluation_results).joinedload(EvaluationResult.benchmark),
    )

    if paradigm_id:
        query = query.filter(VlaModel.paradigm_id == paradigm_id)

    if topic_id:
        query = query.join(VlaModel.model_topics).filter(ModelTopic.topic_id == topic_id)

    if benchmark_id:
        query = query.join(VlaModel.evaluation_results).filter(
            EvaluationResult.benchmark_id == benchmark_id
        )

    if keyword:
        query = query.outerjoin(VlaModel.paper).filter(
            or_(
                _lower_like(VlaModel.name, keyword),
                _lower_like(Paper.title, keyword),
                _lower_like(VlaModel.summary, keyword),
            )
        )

    models = query.distinct().order_by(VlaModel.year.desc(), VlaModel.name.asc()).all()

    return render_template(
        "models.html",
        models=models,
        filters=_filter_options(session),
        selected={
            "paradigm": paradigm_id,
            "topic": topic_id,
            "benchmark": benchmark_id,
            "q": keyword,
        },
    )


@bp.route("/models/<slug>")
def model_detail(slug):
    session = get_session()

    model = (
        session.query(VlaModel)
        .options(
            joinedload(VlaModel.paradigm),
            joinedload(VlaModel.paper)
            .selectinload(Paper.paper_authors)
            .joinedload(PaperAuthor.author)
            .selectinload(Author.author_affiliations)
            .joinedload(AuthorAffiliation.affiliation),
            selectinload(VlaModel.model_topics).joinedload(ModelTopic.topic),
            selectinload(VlaModel.model_data_sources).joinedload(
                ModelDataSource.data_source_type
            ),
            selectinload(VlaModel.evaluation_results).joinedload(EvaluationResult.benchmark),
        )
        .filter(VlaModel.slug == slug)
        .one_or_none()
    )

    if model is None:
        abort(404)

    results = sorted(
        model.evaluation_results,
        key=lambda item: (
            item.benchmark.name if item.benchmark else "",
            item.split_name or "",
            item.metric_name or "",
        ),
    )

    return render_template("model_detail.html", model=model, results=results)


@bp.route("/benchmarks")
def benchmark_list():
    session = get_session()
    benchmark_id = request.args.get("benchmark", type=int)

    benchmark_query = session.query(Benchmark).options(
        selectinload(Benchmark.evaluation_results)
        .joinedload(EvaluationResult.model)
        .joinedload(VlaModel.paradigm)
    )

    if benchmark_id:
        benchmark_query = benchmark_query.filter(Benchmark.id == benchmark_id)

    benchmarks = benchmark_query.order_by(Benchmark.name.asc()).all()

    benchmark_counts = dict(
        session.query(
            Benchmark.id,
            func.count(distinct(EvaluationResult.model_id)),
        )
        .outerjoin(EvaluationResult, Benchmark.id == EvaluationResult.benchmark_id)
        .group_by(Benchmark.id)
        .all()
    )

    ordered_benchmarks = []
    for benchmark in benchmarks:
        benchmark.evaluation_results.sort(
            key=lambda item: (
                item.model.year if item.model and item.model.year is not None else 0,
                item.model.name if item.model else "",
            ),
            reverse=True,
        )
        ordered_benchmarks.append(benchmark)

    return render_template(
        "benchmarks.html",
        benchmarks=ordered_benchmarks,
        benchmark_counts=benchmark_counts,
        filters=_filter_options(session),
        selected_benchmark=benchmark_id,
    )


@bp.route("/admin/models/new", methods=["GET", "POST"])
def admin_model_create():
    session = get_session()
    options = _admin_options(session)
    form_data = _empty_model_form_data()

    if request.method == "POST":
        form_data = _model_form_from_request()
        errors, normalized = _validate_model_form(session, form_data)

        if not errors:
            try:
                model = _save_model_form(session, VlaModel(), form_data, normalized)
                session.commit()
                flash(f"Model '{model.name}' has been created.", "success")
                return redirect(url_for("main.model_detail", slug=model.slug))
            except IntegrityError:
                session.rollback()
                errors.append("Database constraint error occurred while saving the record.")
            except Exception as exc:
                session.rollback()
                errors.append(f"Failed to create model: {exc}")

        for error in errors:
            flash(error, "error")

    recent_models = (
        session.query(VlaModel)
        .options(joinedload(VlaModel.paradigm), joinedload(VlaModel.paper))
        .order_by(VlaModel.id.desc())
        .limit(6)
        .all()
    )

    return render_template(
        "admin_model_form.html",
        options=options,
        form_data=form_data,
        recent_models=recent_models,
        page_title="Add Model Record",
        page_description=(
            "Lightweight admin entry page for course demos. It creates a new model, "
            "optionally creates or reuses a paper, and links selected topics and data-source categories."
        ),
        submit_label="Create Model",
        current_model=None,
    )


@bp.route("/admin/models/<int:model_id>/edit", methods=["GET", "POST"])
def admin_model_edit(model_id):
    session = get_session()
    model = (
        session.query(VlaModel)
        .options(
            joinedload(VlaModel.paper),
            joinedload(VlaModel.paradigm),
            selectinload(VlaModel.model_topics),
            selectinload(VlaModel.model_data_sources),
        )
        .filter(VlaModel.id == model_id)
        .one_or_none()
    )
    if model is None:
        abort(404)

    options = _admin_options(session)
    form_data = _model_form_from_model(model)

    if request.method == "POST":
        form_data = _model_form_from_request()
        errors, normalized = _validate_model_form(session, form_data, current_model=model)

        if not errors:
            try:
                _save_model_form(session, model, form_data, normalized)
                session.commit()
                flash(f"Model '{model.name}' has been updated.", "success")
                return redirect(url_for("main.model_detail", slug=model.slug))
            except IntegrityError:
                session.rollback()
                errors.append("Database constraint error occurred while updating the record.")
            except Exception as exc:
                session.rollback()
                errors.append(f"Failed to update model: {exc}")

        for error in errors:
            flash(error, "error")

    recent_models = (
        session.query(VlaModel)
        .options(joinedload(VlaModel.paradigm), joinedload(VlaModel.paper))
        .order_by(VlaModel.id.desc())
        .limit(6)
        .all()
    )

    return render_template(
        "admin_model_form.html",
        options=options,
        form_data=form_data,
        recent_models=recent_models,
        page_title=f"Edit Model Record: {model.name}",
        page_description="Update the current model, associated paper metadata, topic links, and data-source links.",
        submit_label="Save Changes",
        current_model=model,
    )


@bp.route("/admin/papers/<int:paper_id>/authors/new", methods=["GET", "POST"])
def admin_paper_author_create(paper_id):
    session = get_session()
    paper = (
        session.query(Paper)
        .options(
            selectinload(Paper.paper_authors)
            .joinedload(PaperAuthor.author)
            .selectinload(Author.author_affiliations)
            .joinedload(AuthorAffiliation.affiliation),
            selectinload(Paper.models),
        )
        .filter(Paper.id == paper_id)
        .one_or_none()
    )
    if paper is None:
        abort(404)

    form_data = {
        "full_name": "",
        "author_order": "",
        "affiliation_names": "",
        "is_first_author": False,
        "is_corresponding_author": False,
        "notes": "",
    }

    if request.method == "POST":
        form_data = {
            "full_name": (request.form.get("full_name") or "").strip(),
            "author_order": (request.form.get("author_order") or "").strip(),
            "affiliation_names": (request.form.get("affiliation_names") or "").strip(),
            "is_first_author": request.form.get("is_first_author") == "on",
            "is_corresponding_author": request.form.get("is_corresponding_author") == "on",
            "notes": (request.form.get("notes") or "").strip(),
        }

        errors = []
        full_name = form_data["full_name"]
        author_order = _optional_int(form_data["author_order"])
        affiliation_names = [
            item.strip()
            for item in re.split(r"[,\n;]+", form_data["affiliation_names"])
            if item.strip()
        ]

        if not full_name:
            errors.append("Author name is required.")
        if author_order is None:
            errors.append("Author order must be an integer.")
        elif author_order <= 0:
            errors.append("Author order must be positive.")

        author = None
        if full_name:
            author = session.query(Author).filter(Author.full_name == full_name).one_or_none()

        if author and session.query(PaperAuthor).filter_by(paper_id=paper.id, author_id=author.id).first():
            errors.append("This author is already linked to the selected paper.")

        if author_order is not None and session.query(PaperAuthor).filter_by(paper_id=paper.id, author_order=author_order).first():
            errors.append("This author order is already used in the selected paper.")

        if not errors:
            try:
                if author is None:
                    author = Author(full_name=full_name)
                    session.add(author)
                    session.flush()

                for affiliation_name in affiliation_names:
                    affiliation = (
                        session.query(Affiliation)
                        .filter(Affiliation.name == affiliation_name)
                        .one_or_none()
                    )
                    if affiliation is None:
                        affiliation = Affiliation(name=affiliation_name)
                        session.add(affiliation)
                        session.flush()

                    if not session.query(AuthorAffiliation).filter_by(
                        author_id=author.id, affiliation_id=affiliation.id
                    ).first():
                        session.add(
                            AuthorAffiliation(
                                author_id=author.id,
                                affiliation_id=affiliation.id,
                                notes=_optional_text(form_data["notes"]),
                            )
                        )

                session.add(
                    PaperAuthor(
                        paper_id=paper.id,
                        author_id=author.id,
                        author_order=author_order,
                        is_first_author=form_data["is_first_author"],
                        is_corresponding_author=form_data["is_corresponding_author"],
                        notes=_optional_text(form_data["notes"]),
                    )
                )
                session.commit()
                flash(f"Author '{author.full_name}' has been linked to the paper.", "success")
                linked_model = paper.models[0] if paper.models else None
                if linked_model is not None:
                    return redirect(url_for("main.model_detail", slug=linked_model.slug))
                return redirect(url_for("main.admin_paper_author_create", paper_id=paper.id))
            except IntegrityError:
                session.rollback()
                errors.append("Database constraint error occurred while saving the author link.")
            except Exception as exc:
                session.rollback()
                errors.append(f"Failed to add author: {exc}")

        for error in errors:
            flash(error, "error")

    current_authors = sorted(paper.paper_authors, key=lambda item: item.author_order)
    linked_model = paper.models[0] if paper.models else None

    return render_template(
        "admin_paper_author_form.html",
        paper=paper,
        current_authors=current_authors,
        linked_model=linked_model,
        form_data=form_data,
    )


@bp.route("/admin/paper-authors/<int:paper_id>/<int:author_id>/delete", methods=["POST"])
def admin_paper_author_delete(paper_id, author_id):
    session = get_session()
    link = (
        session.query(PaperAuthor)
        .options(joinedload(PaperAuthor.paper), joinedload(PaperAuthor.author))
        .filter(PaperAuthor.paper_id == paper_id, PaperAuthor.author_id == author_id)
        .one_or_none()
    )
    if link is None:
        abort(404)

    linked_model = (
        session.query(VlaModel).filter(VlaModel.paper_id == paper_id).order_by(VlaModel.id.asc()).first()
    )
    author = link.author

    try:
        session.delete(link)
        session.flush()

        remaining_links = session.query(PaperAuthor).filter(PaperAuthor.author_id == author_id).count()
        if remaining_links == 0:
            affiliation_links = session.query(AuthorAffiliation).filter(
                AuthorAffiliation.author_id == author_id
            ).all()
            orphan_affiliation_ids = [item.affiliation_id for item in affiliation_links]
            for item in affiliation_links:
                session.delete(item)
            session.flush()

            for affiliation_id in orphan_affiliation_ids:
                if (
                    session.query(AuthorAffiliation)
                    .filter(AuthorAffiliation.affiliation_id == affiliation_id)
                    .count()
                    == 0
                ):
                    affiliation = session.get(Affiliation, affiliation_id)
                    if affiliation is not None:
                        session.delete(affiliation)

            session.delete(author)

        session.commit()
        flash("Author link has been removed.", "success")
    except Exception as exc:
        session.rollback()
        flash(f"Failed to remove author link: {exc}", "error")

    if linked_model is not None:
        return redirect(url_for("main.model_detail", slug=linked_model.slug))
    return redirect(url_for("main.admin_paper_author_create", paper_id=paper_id))


@bp.route("/admin/models/<int:model_id>/results/new", methods=["GET", "POST"])
def admin_result_create(model_id):
    session = get_session()
    model = (
        session.query(VlaModel)
        .options(
            joinedload(VlaModel.paradigm),
            joinedload(VlaModel.paper),
            selectinload(VlaModel.evaluation_results).joinedload(EvaluationResult.benchmark),
        )
        .filter(VlaModel.id == model_id)
        .one_or_none()
    )
    if model is None:
        abort(404)

    benchmarks = session.query(Benchmark).order_by(Benchmark.name.asc()).all()
    form_data = {
        "benchmark_id": "",
        "new_benchmark_name": "",
        "benchmark_category": "",
        "benchmark_official_url": "",
        "split_name": "",
        "metric_name": "",
        "metric_value": "",
        "metric_unit": "",
        "result_summary": "",
        "source_url": "",
        "notes": "",
    }

    if request.method == "POST":
        form_data = {
            "benchmark_id": (request.form.get("benchmark_id") or "").strip(),
            "new_benchmark_name": (request.form.get("new_benchmark_name") or "").strip(),
            "benchmark_category": (request.form.get("benchmark_category") or "").strip(),
            "benchmark_official_url": (request.form.get("benchmark_official_url") or "").strip(),
            "split_name": (request.form.get("split_name") or "").strip(),
            "metric_name": (request.form.get("metric_name") or "").strip(),
            "metric_value": (request.form.get("metric_value") or "").strip(),
            "metric_unit": (request.form.get("metric_unit") or "").strip(),
            "result_summary": (request.form.get("result_summary") or "").strip(),
            "source_url": (request.form.get("source_url") or "").strip(),
            "notes": (request.form.get("notes") or "").strip(),
        }

        errors = []
        benchmark_id = _optional_int(form_data["benchmark_id"])
        metric_value = _optional_float(form_data["metric_value"])
        new_benchmark_name = form_data["new_benchmark_name"]

        if benchmark_id and new_benchmark_name:
            errors.append("Choose an existing benchmark or enter a new benchmark name, not both.")
        if not benchmark_id and not new_benchmark_name:
            errors.append("A benchmark is required.")
        if form_data["metric_value"] and metric_value is None:
            errors.append("Metric value must be numeric.")
        if not form_data["result_summary"] and not form_data["metric_name"] and metric_value is None:
            errors.append("Provide at least a result summary or a metric.")

        benchmark = None
        if benchmark_id:
            benchmark = session.query(Benchmark).filter(Benchmark.id == benchmark_id).one_or_none()
            if benchmark is None:
                errors.append("Selected benchmark does not exist.")

        if not errors:
            try:
                if benchmark is None:
                    benchmark = (
                        session.query(Benchmark)
                        .filter(Benchmark.name == new_benchmark_name)
                        .one_or_none()
                    )
                    if benchmark is None:
                        benchmark = Benchmark(
                            name=new_benchmark_name,
                            category=_optional_text(form_data["benchmark_category"]),
                            official_url=_optional_text(form_data["benchmark_official_url"]),
                        )
                        session.add(benchmark)
                        session.flush()

                session.add(
                    EvaluationResult(
                        model_id=model.id,
                        benchmark_id=benchmark.id,
                        split_name=_optional_text(form_data["split_name"]),
                        metric_name=_optional_text(form_data["metric_name"]),
                        metric_value=metric_value,
                        metric_unit=_optional_text(form_data["metric_unit"]),
                        result_summary=_optional_text(form_data["result_summary"]),
                        source_url=_optional_text(form_data["source_url"]),
                        notes=_optional_text(form_data["notes"]),
                    )
                )
                session.commit()
                flash("Benchmark result has been added.", "success")
                return redirect(url_for("main.model_detail", slug=model.slug))
            except IntegrityError:
                session.rollback()
                errors.append("Database constraint error occurred while saving the result.")
            except Exception as exc:
                session.rollback()
                errors.append(f"Failed to add benchmark result: {exc}")

        for error in errors:
            flash(error, "error")

    current_results = sorted(
        model.evaluation_results,
        key=lambda item: (
            item.benchmark.name if item.benchmark else "",
            item.split_name or "",
            item.metric_name or "",
        ),
    )

    return render_template(
        "admin_result_form.html",
        model=model,
        benchmarks=benchmarks,
        form_data=form_data,
        current_results=current_results,
    )


@bp.route("/admin/results/<int:result_id>/delete", methods=["POST"])
def admin_result_delete(result_id):
    session = get_session()
    result = (
        session.query(EvaluationResult)
        .options(joinedload(EvaluationResult.model), joinedload(EvaluationResult.benchmark))
        .filter(EvaluationResult.id == result_id)
        .one_or_none()
    )
    if result is None:
        abort(404)

    model_id = result.model_id
    model_slug = result.model.slug if result.model is not None else None

    try:
        session.delete(result)
        session.commit()
        flash("Benchmark result row has been removed.", "success")
    except Exception as exc:
        session.rollback()
        flash(f"Failed to remove benchmark result: {exc}", "error")

    if model_slug is not None:
        return redirect(url_for("main.model_detail", slug=model_slug))
    return redirect(url_for("main.admin_result_create", model_id=model_id))
