import pytest

from app import create_app
from app.db import Base, get_engine, get_session, remove_session
from app.models import Paper, PaperTopic, Paradigm, Topic, VlaModel
from app.seed_data import load_seed_data


@pytest.fixture()
def app():
    app = create_app(
        {
            "DATABASE_URL": "sqlite:///:memory:",
            "TESTING": True,
            "SECRET_KEY": "test-secret",
        }
    )
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = get_session()
    try:
        load_seed_data(session)
        session.commit()
    finally:
        session.close()
        remove_session()
    yield app
    Base.metadata.drop_all(bind=engine)
    remove_session()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_demo_data_includes_recent_models(app):
    session = get_session()
    try:
        names = {name for (name,) in session.query(VlaModel.name).all()}
        assert len(names) >= 20
        assert {"Xiaomi-Robotics-0", "Green-VLA", "AR-VLA", "ProgressVLA"} <= names
    finally:
        session.close()
        remove_session()


def test_demo_data_includes_extended_topics(app):
    session = get_session()
    try:
        topic_names = {name for (name,) in session.query(Topic.name).all()}
        assert {
            "bimanual manipulation",
            "humanoid robotics",
            "spatial grounding",
            "real-time control",
            "open-world generalization",
            "progress-aware control",
        } <= topic_names
    finally:
        session.close()
        remove_session()


def test_demo_data_includes_large_paper_index(app):
    session = get_session()
    try:
        papers = session.query(Paper).all()
        titles = [paper.title for paper in papers]
        assert len(papers) >= 110
        assert len(titles) == len(set(titles))
        assert all(paper.arxiv_url or paper.project_url or paper.code_url for paper in papers)
        assert session.query(PaperTopic).count() >= 100
        removed_dataset_only_titles = {
            "DROID: A Large-Scale In-the-Wild Robot Manipulation Dataset",
            "BridgeData V2: A Dataset for Robot Learning at Scale",
            "RoboMIND: Benchmark on Multi-embodiment Intelligence Normative Data for Robot Manipulation",
            "AgiBot World Colosseo: A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems",
        }
        assert removed_dataset_only_titles.isdisjoint(titles)
    finally:
        session.close()
        remove_session()


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/models",
        "/papers",
        "/papers?q=OpenVLA",
        "/papers?year=2025",
        "/queries",
        "/models?year=2026",
        "/stats",
        "/schema",
        "/timeline",
        "/benchmarks",
        "/models/xiaomi-robotics-0",
    ],
)
def test_public_pages_return_200(client, path):
    response = client.get(path)
    assert response.status_code == 200


def test_model_filters_still_work(client):
    assert client.get("/models?q=Green-VLA").status_code == 200
    assert b"Green-VLA" in client.get("/models?q=Green-VLA").data
    assert client.get("/models?topic=1").status_code == 200
    assert client.get("/models?benchmark=1").status_code == 200


def test_xiaomi_detail_has_linked_context(client):
    response = client.get("/models/xiaomi-robotics-0")
    assert response.status_code == 200
    body = response.data
    assert b"Xiaomi-Robotics-0" in body
    assert b"LIBERO" in body
    assert b"real-time control" in body
    assert b"mixed" in body
    assert b"Xiaomi-Robotics-0: An Open-Sourced" in body


def test_admin_model_validation_rejects_empty_name(client):
    response = client.post(
        "/admin/models/new",
        data={"name": "", "paradigm_id": "", "year": "not-a-year"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Model name is required." in response.data
    assert b"Paradigm is required." in response.data
    assert b"Year must be an integer." in response.data


def test_admin_model_validation_rejects_duplicate_slug(client):
    session = get_session()
    try:
        paradigm_id = session.query(Paradigm.id).order_by(Paradigm.id.asc()).first()[0]
    finally:
        session.close()
        remove_session()

    response = client.post(
        "/admin/models/new",
        data={
            "name": "Duplicate Slug Probe",
            "slug": "openvla",
            "year": "2026",
            "paradigm_id": str(paradigm_id),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Slug already exists. Choose a different slug." in response.data
