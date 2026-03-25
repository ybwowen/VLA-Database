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


PARADIGMS = [
    {
        "name": "Autoregressive",
        "description": "Action tokens are generated sequentially, typically with a transformer policy.",
    },
    {
        "name": "Diffusion / Flow-based",
        "description": "Action generation relies on diffusion or flow-matching style denoising processes.",
    },
    {
        "name": "Dual System",
        "description": "The model separates slow reasoning/planning from fast execution/control.",
    },
    {
        "name": "Other",
        "description": "A catch-all bucket for models adjacent to standard paradigm categories.",
    },
]

TOPICS = [
    {"name": "object-centric", "description": "Focuses on object-level grounding or manipulation."},
    {"name": "task-centric", "description": "Focuses on task execution conditioned by instructions."},
    {"name": "skill/subtask", "description": "Decomposes behavior into reusable skills or subtasks."},
    {"name": "depth/3D perception", "description": "Explicitly leverages depth or 3D reasoning."},
    {"name": "reasoning", "description": "Uses deliberate reasoning, planning, or semantic decomposition."},
    {"name": "long-horizon", "description": "Targets multi-step or long-horizon manipulation tasks."},
    {
        "name": "generalist manipulation",
        "description": "Aims to solve many tasks rather than a single narrow manipulation setting.",
    },
    {
        "name": "dexterous manipulation",
        "description": "Targets high-DoF or dexterous manipulation scenarios.",
    },
    {"name": "sim2real", "description": "Includes simulation-to-real transfer or cross-embodiment transfer."},
    {"name": "safety", "description": "Explicitly addresses safety or risk-aware control."},
    {"name": "other", "description": "Other topics not covered by the current taxonomy."},
]

DATA_SOURCES = [
    {"name": "real robot", "description": "Trained mainly on real-world robot trajectories."},
    {"name": "simulation", "description": "Trained mainly on simulation data."},
    {"name": "synthetic", "description": "Includes synthetic or programmatically generated data."},
    {"name": "mixed", "description": "Combines multiple source types such as robot data and web-scale data."},
]

BENCHMARKS = [
    {
        "name": "SimplerEnv",
        "category": "simulation",
        "description": "Embodied manipulation benchmark for broad VLA evaluation.",
        "official_url": "https://simpler-env.github.io/",
    },
    {
        "name": "LIBERO",
        "category": "simulation",
        "description": "Language-conditioned lifelong robot manipulation benchmark.",
        "official_url": "https://libero-project.github.io/main.html",
    },
    {
        "name": "LIBERO-plus",
        "category": "simulation",
        "description": "A harder variant extending the LIBERO family.",
        "official_url": None,
    },
    {
        "name": "RoboCasa",
        "category": "simulation",
        "description": "Household manipulation benchmark in realistic simulation.",
        "official_url": "https://robocasa.ai/",
    },
    {
        "name": "RoboTwin",
        "category": "simulation",
        "description": "Digital-twin based robotics benchmark.",
        "official_url": None,
    },
    {
        "name": "BEHAVIOR-1K",
        "category": "simulation",
        "description": "Large-scale household activity benchmark.",
        "official_url": "https://behavior.stanford.edu/",
    },
    {
        "name": "CALVIN",
        "category": "simulation",
        "description": "Long-horizon language-conditioned manipulation benchmark.",
        "official_url": "https://github.com/mees/calvin",
    },
    {
        "name": "VIMA-Bench",
        "category": "simulation",
        "description": "Compositional prompt-based manipulation benchmark introduced with VIMA.",
        "official_url": "https://vimalabs.github.io/",
    },
    {
        "name": "Google 13-Task Real-World Eval",
        "category": "real-world",
        "description": "Internal real-world task suite reported by the RT-1 and RT-2 projects.",
        "official_url": "https://robotics-transformer1.github.io/",
    },
    {
        "name": "Cross-Embodiment Real-World Eval",
        "category": "real-world",
        "description": "A generic bucket for public cross-robot real-world evaluations.",
        "official_url": None,
    },
    {
        "name": "Multi-Task Real-World Eval",
        "category": "real-world",
        "description": "A generic bucket for broad real-world manipulation evaluations.",
        "official_url": None,
    },
]


SEED_MODELS = [
    {
        "name": "RT-1",
        "slug": "rt-1",
        "year": 2022,
        "open_source": True,
        "summary": (
            "A large-scale transformer policy for language-conditioned real-world robot control "
            "trained on roughly 130k episodes across 13 manipulation tasks."
        ),
        "notes": "Original project released code artifacts; pretrained checkpoints are not fully mirrored in this seed.",
        "website_url": "https://robotics-transformer1.github.io/",
        "repo_url": "https://github.com/google-research/robotics_transformer",
        "paradigm": "Autoregressive",
        "paper": {
            "title": "RT-1: Robotics Transformer for Real-World Control at Scale",
            "year": 2022,
            "venue_name": "RSS 2023",
            "publication_type": "conference",
            "publication_status": "published",
            "arxiv_url": "https://arxiv.org/abs/2212.06817",
            "project_url": "https://robotics-transformer1.github.io/",
            "code_url": "https://github.com/google-research/robotics_transformer",
            "notes": "Seed data records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Anthony Brohan",
                "affiliations": ["Google Research"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Noah Brown",
                "affiliations": ["Google Research"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Andy Zeng",
                "affiliations": ["Google DeepMind"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
        ],
        "topics": ["task-centric", "generalist manipulation"],
        "data_sources": [
            {
                "name": "real robot",
                "notes": "Public project page reports large-scale real-robot training data.",
            }
        ],
        "evaluations": [
            {
                "benchmark": "Google 13-Task Real-World Eval",
                "split_name": "seen tasks",
                "metric_name": "success rate",
                "metric_value": 97.0,
                "metric_unit": "%",
                "result_summary": "Reported 97% average success on seen tasks.",
                "source_url": "https://robotics-transformer1.github.io/",
            },
            {
                "benchmark": "Google 13-Task Real-World Eval",
                "split_name": "unseen tasks",
                "metric_name": "zero-shot success rate",
                "metric_value": 76.0,
                "metric_unit": "%",
                "result_summary": "Reported 76% average success on unseen tasks.",
                "source_url": "https://robotics-transformer1.github.io/",
            },
        ],
    },
    {
        "name": "RT-2",
        "slug": "rt-2",
        "year": 2023,
        "open_source": False,
        "summary": (
            "A vision-language-action model that transfers web-scale vision-language knowledge "
            "to robotic control and semantic generalization."
        ),
        "notes": None,
        "website_url": "https://robotics-transformer2.github.io/",
        "repo_url": None,
        "paradigm": "Autoregressive",
        "paper": {
            "title": "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control",
            "year": 2023,
            "venue_name": "CoRL 2023",
            "publication_type": "conference",
            "publication_status": "published",
            "arxiv_url": "https://arxiv.org/abs/2307.15818",
            "project_url": "https://robotics-transformer2.github.io/",
            "code_url": None,
            "notes": "Seed data records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Anthony Brohan",
                "affiliations": ["Google DeepMind"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Noah Brown",
                "affiliations": ["Google DeepMind"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Karol Hausman",
                "affiliations": ["Google DeepMind"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
        ],
        "topics": ["task-centric", "reasoning", "generalist manipulation"],
        "data_sources": [
            {
                "name": "mixed",
                "notes": "Combines robot interaction data with large-scale web-derived vision-language knowledge.",
            }
        ],
        "evaluations": [
            {
                "benchmark": "Google 13-Task Real-World Eval",
                "split_name": "semantic generalization",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": (
                    "Project materials report improved semantic generalization compared with RT-1 "
                    "and other robot baselines."
                ),
                "source_url": "https://robotics-transformer2.github.io/",
            }
        ],
    },
    {
        "name": "VIMA",
        "slug": "vima",
        "year": 2022,
        "open_source": True,
        "summary": (
            "A multimodal prompt-conditioned manipulation agent that generates actions "
            "autoregressively from visual observations and structured prompts."
        ),
        "notes": (
            "Included as a closely related vision-language-action style model. "
            "Some surveys treat it as a precursor rather than a modern large-scale VLA."
        ),
        "website_url": "https://vimalabs.github.io/",
        "repo_url": "https://github.com/vimalabs/VIMA",
        "paradigm": "Autoregressive",
        "paper": {
            "title": "VIMA: General Robot Manipulation with Multimodal Prompts",
            "year": 2022,
            "venue_name": "ICML 2023",
            "publication_type": "conference",
            "publication_status": "published",
            "arxiv_url": "https://arxiv.org/abs/2210.03094",
            "project_url": "https://vimalabs.github.io/",
            "code_url": "https://github.com/vimalabs/VIMA",
            "notes": "Seed omits the full author list because the project focuses on database structure rather than exhaustive metadata capture.",
        },
        "authors": [],
        "topics": [
            "object-centric",
            "task-centric",
            "skill/subtask",
            "generalist manipulation",
        ],
        "data_sources": [{"name": "simulation", "notes": "Benchmarked heavily in simulation."}],
        "evaluations": [
            {
                "benchmark": "VIMA-Bench",
                "split_name": "hardest compositional split",
                "metric_name": "relative improvement",
                "metric_value": 2.9,
                "metric_unit": "x",
                "result_summary": (
                    "Official project page reports about 2.9x improvement over prior methods on the hardest zero-shot setting."
                ),
                "source_url": "https://vimalabs.github.io/",
            }
        ],
    },
    {
        "name": "RoboFlamingo",
        "slug": "roboflamingo",
        "year": 2023,
        "open_source": True,
        "summary": (
            "A Flamingo-style vision-language foundation model adapted for robot imitation learning "
            "and language-conditioned action prediction."
        ),
        "notes": None,
        "website_url": "https://roboflamingo.github.io/",
        "repo_url": "https://github.com/RoboFlamingo/RoboFlamingo",
        "paradigm": "Other",
        "paper": {
            "title": "Vision-Language Foundation Models as Effective Robot Imitators",
            "year": 2023,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": "https://arxiv.org/abs/2311.01378",
            "project_url": "https://roboflamingo.github.io/",
            "code_url": "https://github.com/RoboFlamingo/RoboFlamingo",
            "notes": "Seed data records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Xinghang Li",
                "affiliations": ["ByteDance Research", "Tsinghua University"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Minghuan Liu",
                "affiliations": ["ByteDance Research", "Shanghai Jiao Tong University"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Hanbo Zhang",
                "affiliations": ["ByteDance Research"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
        ],
        "topics": ["task-centric", "long-horizon", "generalist manipulation"],
        "data_sources": [{"name": "simulation", "notes": "Public CALVIN evaluation is simulation based."}],
        "evaluations": [
            {
                "benchmark": "CALVIN",
                "split_name": "long-horizon manipulation",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": (
                    "Project materials report strong long-horizon CALVIN performance among VLM-based robot imitators."
                ),
                "source_url": "https://roboflamingo.github.io/",
            }
        ],
    },
    {
        "name": "GR-1",
        "slug": "gr-1",
        "year": 2023,
        "open_source": True,
        "summary": (
            "A generalist robot policy that combines large-scale video generative pretraining "
            "with visual robot manipulation and autoregressive control."
        ),
        "notes": (
            "Often described as a generalist robot policy rather than a foundation VLA agent, "
            "but still useful in a VLA-system database as a closely related baseline."
        ),
        "website_url": "https://gr1-manipulation.github.io/",
        "repo_url": None,
        "paradigm": "Autoregressive",
        "paper": {
            "title": "Unleashing Large-Scale Video Generative Pre-training for Visual Robot Manipulation",
            "year": 2023,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": None,
            "project_url": "https://gr1-manipulation.github.io/",
            "code_url": None,
            "notes": "Seed omits the full author list and keeps the record focused on model-level metadata.",
        },
        "authors": [],
        "topics": ["task-centric", "long-horizon", "generalist manipulation"],
        "data_sources": [{"name": "mixed", "notes": "Combines large video pretraining with robot manipulation data."}],
        "evaluations": [
            {
                "benchmark": "CALVIN",
                "split_name": "ABC-D long-horizon",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "Project materials report state-of-the-art CALVIN ABC-D results at release time.",
                "source_url": "https://gr1-manipulation.github.io/",
            }
        ],
    },
    {
        "name": "OpenVLA",
        "slug": "openvla",
        "year": 2024,
        "open_source": True,
        "summary": (
            "An open-source VLA model trained on Open X-Embodiment style data for instruction-conditioned robot control."
        ),
        "notes": None,
        "website_url": "https://openvla.github.io/",
        "repo_url": "https://github.com/openvla/openvla",
        "paradigm": "Autoregressive",
        "paper": {
            "title": "OpenVLA: An Open-Source Vision-Language-Action Model",
            "year": 2024,
            "venue_name": "CoRL 2024",
            "publication_type": "conference",
            "publication_status": "published",
            "arxiv_url": "https://arxiv.org/abs/2406.09246",
            "project_url": "https://openvla.github.io/",
            "code_url": "https://github.com/openvla/openvla",
            "notes": "Seed data prioritizes model-level information; author list is intentionally partial.",
        },
        "authors": [
            {
                "full_name": "Moo Jin Kim",
                "affiliations": ["Stanford University"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Chelsea Finn",
                "affiliations": ["Stanford University"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
        ],
        "topics": ["task-centric", "generalist manipulation", "sim2real"],
        "data_sources": [{"name": "real robot", "notes": "Built around large-scale real robot data collections."}],
        "evaluations": [
            {
                "benchmark": "Cross-Embodiment Real-World Eval",
                "split_name": "29-task comparison",
                "metric_name": "absolute task success improvement",
                "metric_value": 16.5,
                "metric_unit": "%",
                "result_summary": (
                    "Paper abstract reports a 16.5% absolute task-success improvement over RT-2-X across 29 tasks."
                ),
                "source_url": "https://openvla.github.io/",
            }
        ],
    },
    {
        "name": "Octo",
        "slug": "octo",
        "year": 2024,
        "open_source": True,
        "summary": (
            "An open-source generalist robot policy oriented toward cross-robot transfer and finetuning "
            "on Open X-Embodiment style data."
        ),
        "notes": (
            "Included as a VLA-adjacent generalist policy. Some literature categorizes Octo separately "
            "from canonical VLA models, so this classification should be read as pragmatic rather than absolute."
        ),
        "website_url": "https://octo-models.github.io/",
        "repo_url": "https://github.com/octo-models/octo",
        "paradigm": "Autoregressive",
        "paper": {
            "title": "Octo: An Open-Source Generalist Robot Policy",
            "year": 2024,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": "https://arxiv.org/abs/2405.12213",
            "project_url": "https://octo-models.github.io/",
            "code_url": "https://github.com/octo-models/octo",
            "notes": "Seed omits the full author list.",
        },
        "authors": [],
        "topics": ["task-centric", "generalist manipulation", "sim2real"],
        "data_sources": [{"name": "real robot", "notes": "Open X-Embodiment data is primarily real-robot data."}],
        "evaluations": [
            {
                "benchmark": "Cross-Embodiment Real-World Eval",
                "split_name": "cross-platform transfer",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "Project materials emphasize transfer across multiple robot platforms after lightweight finetuning.",
                "source_url": "https://octo-models.github.io/",
            }
        ],
    },
    {
        "name": "pi0",
        "slug": "pi0",
        "year": 2024,
        "open_source": False,
        "summary": (
            "A flow-matching vision-language-action model for broad robot control, including dexterous and multi-embodiment settings."
        ),
        "notes": (
            "The model name is often stylized as pi0 or π0. This seed conservatively marks official open-source status as unverified."
        ),
        "website_url": "https://www.physicalintelligence.company/blog/pi0",
        "repo_url": None,
        "paradigm": "Diffusion / Flow-based",
        "paper": {
            "title": "pi0: A Vision-Language-Action Flow Model for General Robot Control",
            "year": 2024,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": None,
            "project_url": "https://www.physicalintelligence.company/blog/pi0",
            "code_url": None,
            "notes": "Seed data records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Kevin Black",
                "affiliations": ["Physical Intelligence"],
                "is_first_author": True,
                "is_corresponding_author": False,
            }
        ],
        "topics": ["reasoning", "generalist manipulation", "dexterous manipulation"],
        "data_sources": [{"name": "real robot", "notes": "Project materials emphasize multi-platform real-robot control."}],
        "evaluations": [
            {
                "benchmark": "Multi-Task Real-World Eval",
                "split_name": "multi-platform deployment",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": (
                    "Project materials describe training across 7 robot platforms and 68 tasks for general robot control."
                ),
                "source_url": "https://www.physicalintelligence.company/blog/pi0",
            }
        ],
    },
    {
        "name": "OpenHelix",
        "slug": "openhelix",
        "year": 2025,
        "open_source": True,
        "summary": (
            "An open-source dual-system VLA model that combines a slow reasoning system with a fast control system for robotic manipulation."
        ),
        "notes": None,
        "website_url": "https://www.dongwang218.com/openhelix/",
        "repo_url": "https://github.com/OpenHelix-robot/OpenHelix",
        "paradigm": "Dual System",
        "paper": {
            "title": "OpenHelix: A Short Survey, Empirical Analysis, and Open-Source Dual-System VLA Model for Robotic Manipulation",
            "year": 2025,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": None,
            "project_url": "https://www.dongwang218.com/openhelix/",
            "code_url": "https://github.com/OpenHelix-robot/OpenHelix",
            "notes": "Seed records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Can Cui",
                "affiliations": ["Westlake University"],
                "is_first_author": True,
                "is_corresponding_author": False,
            }
        ],
        "topics": ["reasoning", "long-horizon", "generalist manipulation"],
        "data_sources": [{"name": "mixed", "notes": "Project positions the model as an open-source dual-system manipulation stack."}],
        "evaluations": [
            {
                "benchmark": "CALVIN",
                "split_name": "ABC-D long-horizon",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "Project page reports strong CALVIN ABC-D long-horizon performance for an open-source dual-system VLA.",
                "source_url": "https://www.dongwang218.com/openhelix/",
            }
        ],
    },
    {
        "name": "Fast-in-Slow",
        "slug": "fast-in-slow",
        "year": 2025,
        "open_source": True,
        "summary": (
            "A dual-system VLA architecture that separates slow semantic reasoning from high-frequency robot control."
        ),
        "notes": None,
        "website_url": None,
        "repo_url": None,
        "paradigm": "Dual System",
        "paper": {
            "title": "Fast-in-Slow: A Dual-System VLA Model Unifying Fast Manipulation within Slow Reasoning",
            "year": 2025,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": None,
            "project_url": None,
            "code_url": None,
            "notes": "Seed records selected authors only because the project emphasizes schema design and queryability.",
        },
        "authors": [
            {
                "full_name": "Hao Chen",
                "affiliations": ["The Chinese University of Hong Kong", "Peking University"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Jiaming Liu",
                "affiliations": ["Peking University", "PKU-Wuhan Institute for Artificial Intelligence"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Shanghang Zhang",
                "affiliations": ["Peking University", "Beijing Academy of Artificial Intelligence"],
                "is_first_author": False,
                "is_corresponding_author": True,
            },
        ],
        "topics": ["reasoning", "long-horizon", "generalist manipulation"],
        "data_sources": [{"name": "mixed", "notes": "Project reports both simulation and real-world gains."}],
        "evaluations": [
            {
                "benchmark": "Multi-Task Real-World Eval",
                "split_name": "simulation",
                "metric_name": "average success improvement",
                "metric_value": 8.0,
                "metric_unit": "%",
                "result_summary": "Project materials report about 8% average success-rate improvement in simulation.",
                "source_url": None,
            },
            {
                "benchmark": "Multi-Task Real-World Eval",
                "split_name": "real-world",
                "metric_name": "average success improvement",
                "metric_value": 11.0,
                "metric_unit": "%",
                "result_summary": "Project materials report about 11% average success-rate improvement on real-world tasks.",
                "source_url": None,
            },
        ],
    },
]


def _get_or_create(session, model_class, defaults=None, **lookup):
    instance = session.query(model_class).filter_by(**lookup).one_or_none()
    if instance is not None:
        return instance

    params = dict(lookup)
    if defaults:
        params.update(defaults)
    instance = model_class(**params)
    session.add(instance)
    session.flush()
    return instance


def load_seed_data(session):
    if session.query(VlaModel.id).first():
        return {
            "seeded": False,
            "message": "Model records already exist. Use --reset to rebuild the database from seed data.",
        }

    paradigms = {
        item["name"]: _get_or_create(
            session,
            Paradigm,
            name=item["name"],
            defaults={"description": item["description"]},
        )
        for item in PARADIGMS
    }

    topics = {
        item["name"]: _get_or_create(
            session,
            Topic,
            name=item["name"],
            defaults={"description": item["description"]},
        )
        for item in TOPICS
    }

    data_sources = {
        item["name"]: _get_or_create(
            session,
            DataSourceType,
            name=item["name"],
            defaults={"description": item["description"]},
        )
        for item in DATA_SOURCES
    }

    benchmarks = {
        item["name"]: _get_or_create(
            session,
            Benchmark,
            name=item["name"],
            defaults={
                "category": item["category"],
                "description": item["description"],
                "official_url": item["official_url"],
            },
        )
        for item in BENCHMARKS
    }

    affiliation_cache = {}

    for model_item in SEED_MODELS:
        paper_item = model_item["paper"]
        paper = _get_or_create(
            session,
            Paper,
            title=paper_item["title"],
            defaults={
                "year": paper_item["year"],
                "venue_name": paper_item["venue_name"],
                "publication_type": paper_item["publication_type"],
                "publication_status": paper_item["publication_status"],
                "arxiv_url": paper_item["arxiv_url"],
                "project_url": paper_item["project_url"],
                "code_url": paper_item["code_url"],
                "notes": paper_item["notes"],
            },
        )

        for index, author_item in enumerate(model_item["authors"], start=1):
            author = _get_or_create(
                session,
                Author,
                full_name=author_item["full_name"],
            )

            for affiliation_name in author_item["affiliations"]:
                affiliation = affiliation_cache.get(affiliation_name)
                if affiliation is None:
                    affiliation = _get_or_create(
                        session,
                        Affiliation,
                        name=affiliation_name,
                    )
                    affiliation_cache[affiliation_name] = affiliation

                _get_or_create(
                    session,
                    AuthorAffiliation,
                    author_id=author.id,
                    affiliation_id=affiliation.id,
                )

            _get_or_create(
                session,
                PaperAuthor,
                paper_id=paper.id,
                author_id=author.id,
                defaults={
                    "author_order": index,
                    "is_first_author": author_item["is_first_author"],
                    "is_corresponding_author": author_item["is_corresponding_author"],
                },
            )

        model = _get_or_create(
            session,
            VlaModel,
            slug=model_item["slug"],
            defaults={
                "name": model_item["name"],
                "year": model_item["year"],
                "open_source": model_item["open_source"],
                "summary": model_item["summary"],
                "notes": model_item["notes"],
                "website_url": model_item["website_url"],
                "repo_url": model_item["repo_url"],
                "paper_id": paper.id,
                "paradigm_id": paradigms[model_item["paradigm"]].id,
            },
        )

        for topic_name in model_item["topics"]:
            _get_or_create(
                session,
                ModelTopic,
                model_id=model.id,
                topic_id=topics[topic_name].id,
            )

        for source_item in model_item["data_sources"]:
            _get_or_create(
                session,
                ModelDataSource,
                model_id=model.id,
                data_source_type_id=data_sources[source_item["name"]].id,
                defaults={"notes": source_item["notes"]},
            )

        for result_item in model_item["evaluations"]:
            session.add(
                EvaluationResult(
                    model_id=model.id,
                    benchmark_id=benchmarks[result_item["benchmark"]].id,
                    split_name=result_item["split_name"],
                    metric_name=result_item["metric_name"],
                    metric_value=result_item["metric_value"],
                    metric_unit=result_item["metric_unit"],
                    result_summary=result_item["result_summary"],
                    source_url=result_item["source_url"],
                )
            )

    session.flush()
    return {
        "seeded": True,
        "message": f"Inserted {len(SEED_MODELS)} models and supporting reference data.",
    }
