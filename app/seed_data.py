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
    {
        "name": "bimanual manipulation",
        "description": "Targets coordinated two-arm manipulation or dual-arm robot control.",
    },
    {
        "name": "humanoid robotics",
        "description": "Targets humanoid robot embodiments or humanoid-oriented manipulation skills.",
    },
    {
        "name": "spatial grounding",
        "description": "Uses explicit spatial or 3D representations for action generation.",
    },
    {
        "name": "real-time control",
        "description": "Emphasizes low-latency or asynchronous execution for smooth robot control.",
    },
    {
        "name": "open-world generalization",
        "description": "Focuses on generalization to new scenes, objects, or deployment environments.",
    },
    {
        "name": "progress-aware control",
        "description": "Models task progress or termination explicitly during long-horizon control.",
    },
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
    {
        "name": "ALOHA Bimanual Eval",
        "category": "real-world",
        "description": "Bimanual manipulation evaluations on ALOHA-style dual-arm robot setups.",
        "official_url": "https://tonyzhaozh.github.io/aloha/",
    },
    {
        "name": "Humanoid Real-World Eval",
        "category": "real-world",
        "description": "Instruction-conditioned humanoid robot manipulation evaluations.",
        "official_url": None,
    },
    {
        "name": "E-Commerce Shelf Picking",
        "category": "real-world",
        "description": "Shelf picking and SKU-level target selection in dense retail-like scenes.",
        "official_url": None,
    },
    {
        "name": "Meta-World",
        "category": "simulation",
        "description": "Meta-learning and multi-task robotic manipulation benchmark.",
        "official_url": "https://meta-world.github.io/",
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
    {
        "name": "RDT-1B",
        "slug": "rdt-1b",
        "year": 2024,
        "open_source": True,
        "summary": (
            "A 1.2B-parameter Robotics Diffusion Transformer for bimanual manipulation, "
            "pre-trained on 46 robot datasets with more than one million episodes."
        ),
        "notes": "Recorded as a diffusion-based robot foundation model with strong VLA-adjacent manipulation coverage.",
        "website_url": "https://rdt-robotics.github.io/rdt-robotics/",
        "repo_url": "https://github.com/thu-ml/RoboticsDiffusionTransformer",
        "paradigm": "Diffusion / Flow-based",
        "paper": {
            "title": "RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation",
            "year": 2024,
            "venue_name": "ICLR 2025",
            "publication_type": "conference",
            "publication_status": "published",
            "arxiv_url": "https://arxiv.org/abs/2410.07864",
            "project_url": "https://rdt-robotics.github.io/rdt-robotics/",
            "code_url": "https://github.com/thu-ml/RoboticsDiffusionTransformer",
            "notes": "Seed records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Songming Liu",
                "affiliations": ["Tsinghua University"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Lingxuan Wu",
                "affiliations": ["Tsinghua University"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Jun Zhu",
                "affiliations": ["Tsinghua University"],
                "is_first_author": False,
                "is_corresponding_author": True,
            },
        ],
        "topics": ["bimanual manipulation", "generalist manipulation", "open-world generalization"],
        "data_sources": [
            {
                "name": "mixed",
                "notes": "Pre-trained on large multi-robot datasets and fine-tuned on ALOHA bimanual episodes.",
            }
        ],
        "evaluations": [
            {
                "benchmark": "ALOHA Bimanual Eval",
                "split_name": "few-shot and zero-shot real robot tasks",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": (
                    "Project and paper materials report strong bimanual manipulation, zero-shot generalization, "
                    "and few-shot learning across ALOHA-style tasks."
                ),
                "source_url": "https://rdt-robotics.github.io/rdt-robotics/",
            }
        ],
    },
    {
        "name": "SpatialVLA",
        "slug": "spatialvla",
        "year": 2025,
        "open_source": True,
        "summary": (
            "A spatial-enhanced VLA model using 3D-aware spatial representations and adaptive action grids "
            "for cross-robot manipulation."
        ),
        "notes": None,
        "website_url": "https://spatialvla.github.io/",
        "repo_url": "https://github.com/SpatialVLA/SpatialVLA",
        "paradigm": "Autoregressive",
        "paper": {
            "title": "SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Model",
            "year": 2025,
            "venue_name": "RSS 2025",
            "publication_type": "conference",
            "publication_status": "accepted",
            "arxiv_url": "https://arxiv.org/abs/2501.15830",
            "project_url": "https://spatialvla.github.io/",
            "code_url": "https://github.com/SpatialVLA/SpatialVLA",
            "notes": "Seed records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Delin Qu",
                "affiliations": ["Shanghai AI Laboratory", "Fudan University"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Haoming Song",
                "affiliations": ["Shanghai AI Laboratory", "Shanghai Jiao Tong University"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Dong Wang",
                "affiliations": ["Shanghai AI Laboratory"],
                "is_first_author": False,
                "is_corresponding_author": True,
            },
        ],
        "topics": ["spatial grounding", "depth/3D perception", "generalist manipulation", "sim2real"],
        "data_sources": [
            {
                "name": "real robot",
                "notes": "Project page reports pre-training on 1.1M real-robot demonstrations.",
            }
        ],
        "evaluations": [
            {
                "benchmark": "LIBERO",
                "split_name": "fine-tuned average",
                "metric_name": "success rate",
                "metric_value": 78.1,
                "metric_unit": "%",
                "result_summary": "GitHub results table reports 78.1% average success across LIBERO suites.",
                "source_url": "https://github.com/SpatialVLA/SpatialVLA",
            },
            {
                "benchmark": "SimplerEnv",
                "split_name": "Google Robot visual matching average",
                "metric_name": "success rate",
                "metric_value": 75.1,
                "metric_unit": "%",
                "result_summary": "Reported fine-tuned SpatialVLA average on SimplerEnv Google Robot visual matching tasks.",
                "source_url": "https://github.com/SpatialVLA/SpatialVLA",
            },
        ],
    },
    {
        "name": "OpenVLA-OFT",
        "slug": "openvla-oft",
        "year": 2025,
        "open_source": True,
        "summary": (
            "An optimized fine-tuning recipe for OpenVLA that adds parallel decoding, action chunking, "
            "continuous actions, and regression-based action heads."
        ),
        "notes": "Stored separately from OpenVLA because the OFT recipe changes inference speed and task performance.",
        "website_url": "https://openvla-oft.github.io/",
        "repo_url": "https://github.com/moojink/openvla-oft",
        "paradigm": "Autoregressive",
        "paper": {
            "title": "Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success",
            "year": 2025,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": "https://arxiv.org/abs/2502.19645",
            "project_url": "https://openvla-oft.github.io/",
            "code_url": "https://github.com/moojink/openvla-oft",
            "notes": "Seed records selected authors only.",
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
            {
                "full_name": "Percy Liang",
                "affiliations": ["Stanford University"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
        ],
        "topics": ["task-centric", "real-time control", "bimanual manipulation", "generalist manipulation"],
        "data_sources": [{"name": "mixed", "notes": "Fine-tunes OpenVLA on LIBERO and ALOHA-style task data."}],
        "evaluations": [
            {
                "benchmark": "LIBERO",
                "split_name": "four task-suite average",
                "metric_name": "success rate",
                "metric_value": 97.1,
                "metric_unit": "%",
                "result_summary": "Project page reports 97.1% average success across four LIBERO task suites.",
                "source_url": "https://openvla-oft.github.io/",
            },
            {
                "benchmark": "ALOHA Bimanual Eval",
                "split_name": "OFT+ real-world bimanual tasks",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "Project materials report that OpenVLA-OFT+ outperforms fine-tuned VLAs and imitation-learning baselines on ALOHA tasks.",
                "source_url": "https://openvla-oft.github.io/",
            },
        ],
    },
    {
        "name": "GR00T N1.5",
        "slug": "groot-n1-5",
        "year": 2025,
        "open_source": True,
        "summary": (
            "NVIDIA's improved open foundation model for generalist humanoid robots, built around a dual-system "
            "reasoning-and-action architecture."
        ),
        "notes": "GR00T N1.5 is included to show the humanoid robotics branch of VLA-style robot foundation models.",
        "website_url": "https://research.nvidia.com/labs/gear/gr00t-n1_5/",
        "repo_url": None,
        "paradigm": "Dual System",
        "paper": {
            "title": "GR00T N1.5: An Improved Open Foundation Model for Generalist Humanoid Robots",
            "year": 2025,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": None,
            "project_url": "https://research.nvidia.com/labs/gear/gr00t-n1_5/",
            "code_url": None,
            "notes": "Seed uses the NVIDIA project page as the primary source.",
        },
        "authors": [],
        "topics": ["humanoid robotics", "reasoning", "generalist manipulation", "bimanual manipulation"],
        "data_sources": [{"name": "mixed", "notes": "Combines synthetic, simulation, and real humanoid manipulation data."}],
        "evaluations": [
            {
                "benchmark": "Humanoid Real-World Eval",
                "split_name": "real GR-1 robot and simulated manipulation",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "NVIDIA reports better simulated manipulation and real GR-1 robot performance than GR00T N1.",
                "source_url": "https://research.nvidia.com/labs/gear/gr00t-n1_5/",
            }
        ],
    },
    {
        "name": "pi0.5",
        "slug": "pi0-5",
        "year": 2025,
        "open_source": True,
        "summary": (
            "A Physical Intelligence VLA model focused on open-world generalization to unseen environments, "
            "objects, and long-horizon tasks."
        ),
        "notes": "The upstream project stylizes the name with the pi symbol; ASCII pi0.5 is used in this database for portability.",
        "website_url": "https://www.physicalintelligence.company/blog/pi05",
        "repo_url": "https://github.com/Physical-Intelligence/openpi",
        "paradigm": "Diffusion / Flow-based",
        "paper": {
            "title": "pi0.5: A Vision-Language-Action Model with Open-World Generalization",
            "year": 2025,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": None,
            "project_url": "https://www.physicalintelligence.company/blog/pi05",
            "code_url": "https://github.com/Physical-Intelligence/openpi",
            "notes": "Seed references Physical Intelligence and LeRobot model documentation.",
        },
        "authors": [],
        "topics": ["open-world generalization", "long-horizon", "generalist manipulation", "real-time control"],
        "data_sources": [{"name": "mixed", "notes": "Co-trained on robot demonstrations and large-scale multimodal data."}],
        "evaluations": [
            {
                "benchmark": "LIBERO",
                "split_name": "LeRobot pi0.5 LIBERO checkpoint",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "LeRobot provides pi0.5 LIBERO checkpoints and documents the model as an open-world generalization VLA.",
                "source_url": "https://huggingface.co/docs/lerobot/pi05",
            }
        ],
    },
    {
        "name": "SmolVLA",
        "slug": "smolvla",
        "year": 2025,
        "open_source": True,
        "summary": (
            "A compact 450M-parameter open-source VLA model from Hugging Face, designed for efficient deployment "
            "on accessible robotics hardware."
        ),
        "notes": None,
        "website_url": "https://huggingface.co/docs/lerobot/v0.4.3/en/smolvla",
        "repo_url": "https://huggingface.co/lerobot/smolvla_base",
        "paradigm": "Diffusion / Flow-based",
        "paper": {
            "title": "SmolVLA: An Open-Source Vision-Language-Action Model for Modern Robotics",
            "year": 2025,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": None,
            "project_url": "https://huggingface.co/docs/lerobot/v0.4.3/en/smolvla",
            "code_url": "https://huggingface.co/lerobot/smolvla_base",
            "notes": "Seed uses Hugging Face LeRobot documentation and model card links.",
        },
        "authors": [],
        "topics": ["real-time control", "generalist manipulation", "open-world generalization"],
        "data_sources": [{"name": "mixed", "notes": "Trained on open community LeRobot datasets."}],
        "evaluations": [
            {
                "benchmark": "LIBERO",
                "split_name": "open-source VLA comparison",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "Project materials describe competitive performance on LIBERO-style manipulation tasks with a compact model.",
                "source_url": "https://huggingface.co/lerobot/smolvla_base",
            },
            {
                "benchmark": "Meta-World",
                "split_name": "open-source VLA comparison",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "Public materials describe SmolVLA as a compact model targeting simulated and real-world manipulation benchmarks.",
                "source_url": "https://smolvla.net/index_en.html",
            },
        ],
    },
    {
        "name": "Xiaomi-Robotics-0",
        "slug": "xiaomi-robotics-0",
        "year": 2026,
        "open_source": True,
        "summary": (
            "An open-source 4.7B-parameter VLA model optimized for high performance, asynchronous execution, "
            "and smooth real-time robot control."
        ),
        "notes": "Official materials report results current as of the February 2026 release and April 2026 post-training update.",
        "website_url": "https://robotics.xiaomi.com/xiaomi-robotics-0.html",
        "repo_url": "https://github.com/Xiaomi-Robotics/Xiaomi-Robotics-0",
        "paradigm": "Diffusion / Flow-based",
        "paper": {
            "title": "Xiaomi-Robotics-0: An Open-Sourced Vision-Language-Action Model with Real-Time Execution",
            "year": 2026,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": "https://arxiv.org/abs/2602.12684",
            "project_url": "https://robotics.xiaomi.com/xiaomi-robotics-0.html",
            "code_url": "https://github.com/Xiaomi-Robotics/Xiaomi-Robotics-0",
            "notes": "Seed records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Rui Cai",
                "affiliations": ["Xiaomi Robotics"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Jun Guo",
                "affiliations": ["Xiaomi Robotics"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Xinze He",
                "affiliations": ["Xiaomi Robotics"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
        ],
        "topics": ["real-time control", "bimanual manipulation", "generalist manipulation", "open-world generalization"],
        "data_sources": [
            {
                "name": "mixed",
                "notes": "Official page reports about 200M robot timesteps and over 80M vision-language samples.",
            }
        ],
        "evaluations": [
            {
                "benchmark": "LIBERO",
                "split_name": "average",
                "metric_name": "success rate",
                "metric_value": 98.7,
                "metric_unit": "%",
                "result_summary": "Official page reports 98.7% average success on LIBERO.",
                "source_url": "https://robotics.xiaomi.com/xiaomi-robotics-0.html",
            },
            {
                "benchmark": "SimplerEnv",
                "split_name": "Visual Matching",
                "metric_name": "success rate",
                "metric_value": 85.5,
                "metric_unit": "%",
                "result_summary": "Official page reports 85.5% under SimplerEnv Visual Matching.",
                "source_url": "https://robotics.xiaomi.com/xiaomi-robotics-0.html",
            },
            {
                "benchmark": "SimplerEnv",
                "split_name": "Visual Aggregation",
                "metric_name": "success rate",
                "metric_value": 74.7,
                "metric_unit": "%",
                "result_summary": "Official page reports 74.7% under SimplerEnv Visual Aggregation.",
                "source_url": "https://robotics.xiaomi.com/xiaomi-robotics-0.html",
            },
            {
                "benchmark": "SimplerEnv",
                "split_name": "WidowX",
                "metric_name": "success rate",
                "metric_value": 79.2,
                "metric_unit": "%",
                "result_summary": "Official page reports 79.2% on SimplerEnv WidowX.",
                "source_url": "https://robotics.xiaomi.com/xiaomi-robotics-0.html",
            },
            {
                "benchmark": "CALVIN",
                "split_name": "ABC-D",
                "metric_name": "average length",
                "metric_value": 4.75,
                "metric_unit": "",
                "result_summary": "Official page reports average length 4.75 on CALVIN ABC-D.",
                "source_url": "https://robotics.xiaomi.com/xiaomi-robotics-0.html",
            },
            {
                "benchmark": "CALVIN",
                "split_name": "ABCD-D",
                "metric_name": "average length",
                "metric_value": 4.8,
                "metric_unit": "",
                "result_summary": "Official page reports average length 4.80 on CALVIN ABCD-D.",
                "source_url": "https://robotics.xiaomi.com/xiaomi-robotics-0.html",
            },
        ],
    },
    {
        "name": "Green-VLA",
        "slug": "green-vla",
        "year": 2026,
        "open_source": True,
        "summary": (
            "A staged VLA framework for generalist robots that combines a five-stage training curriculum, "
            "unified action space, progress prediction, and RL alignment."
        ),
        "notes": None,
        "website_url": "https://greenvla.github.io/",
        "repo_url": "https://github.com/greenvla/GreenVLA",
        "paradigm": "Diffusion / Flow-based",
        "paper": {
            "title": "Green-VLA: Staged Vision-Language-Action Model for Generalist Robots",
            "year": 2026,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": "https://arxiv.org/abs/2602.00919",
            "project_url": "https://greenvla.github.io/",
            "code_url": "https://github.com/greenvla/GreenVLA",
            "notes": "Seed records selected authors only.",
        },
        "authors": [
            {
                "full_name": "I. Apanasevich",
                "affiliations": ["Sber Robotics Center"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "M. Artemyev",
                "affiliations": ["Sber Robotics Center"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
            {
                "full_name": "P. Fedotova",
                "affiliations": ["Sber Robotics Center"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
        ],
        "topics": [
            "humanoid robotics",
            "bimanual manipulation",
            "progress-aware control",
            "open-world generalization",
            "real-time control",
        ],
        "data_sources": [{"name": "mixed", "notes": "Project page reports 3,000+ hours of multi-embodiment demonstrations."}],
        "evaluations": [
            {
                "benchmark": "ALOHA Bimanual Eval",
                "split_name": "table cleaning first-item success",
                "metric_name": "success rate",
                "metric_value": 69.5,
                "metric_unit": "%",
                "result_summary": "Project page reports 69.5% first-item success on ALOHA table cleaning at R0.",
                "source_url": "https://greenvla.github.io/",
            },
            {
                "benchmark": "SimplerEnv",
                "split_name": "Google Robot average",
                "metric_name": "success rate",
                "metric_value": 60.2,
                "metric_unit": "%",
                "result_summary": "Project page reports 60.2% average success on Google Robot tasks at R0.",
                "source_url": "https://greenvla.github.io/",
            },
            {
                "benchmark": "CALVIN",
                "split_name": "ABC-D R2",
                "metric_name": "average chain length",
                "metric_value": 4.62,
                "metric_unit": "",
                "result_summary": "Project materials report R2 long-horizon CALVIN performance around 4.62 ACL.",
                "source_url": "https://greenvla.github.io/",
            },
            {
                "benchmark": "Humanoid Real-World Eval",
                "split_name": "Green Robot average",
                "metric_name": "success rate",
                "metric_value": 90.0,
                "metric_unit": "%",
                "result_summary": "Project page reports 90% average humanoid instruction-conditioned manipulation success.",
                "source_url": "https://greenvla.github.io/",
            },
            {
                "benchmark": "E-Commerce Shelf Picking",
                "split_name": "OOD items with guidance",
                "metric_name": "top-1 success rate",
                "metric_value": 72.0,
                "metric_unit": "%",
                "result_summary": "Project page reports OOD shelf picking success improving to 72% with JPM guidance.",
                "source_url": "https://greenvla.github.io/",
            },
        ],
    },
    {
        "name": "AR-VLA",
        "slug": "ar-vla",
        "year": 2026,
        "open_source": True,
        "summary": (
            "An autoregressive action expert for VLA models that maintains long-lived action memory "
            "instead of repeatedly resetting chunk-level context."
        ),
        "notes": "Included as a 2026 architecture-focused entry emphasizing streaming action generation.",
        "website_url": "https://arvla.insait.ai/",
        "repo_url": None,
        "paradigm": "Autoregressive",
        "paper": {
            "title": "AR-VLA: True Autoregressive Action Expert for Vision-Language-Action Models",
            "year": 2026,
            "venue_name": "RSS 2026",
            "publication_type": "conference",
            "publication_status": "accepted",
            "arxiv_url": "https://arxiv.org/abs/2603.10126",
            "project_url": "https://arvla.insait.ai/",
            "code_url": None,
            "notes": "Seed records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Yutong Hu",
                "affiliations": ["INSAIT", "KU Leuven"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Jan-Nico Zaech",
                "affiliations": ["INSAIT"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Danda Paudel",
                "affiliations": ["INSAIT"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
        ],
        "topics": ["real-time control", "long-horizon", "generalist manipulation"],
        "data_sources": [{"name": "mixed", "notes": "Project page describes simulated and real-robot manipulation evaluations."}],
        "evaluations": [
            {
                "benchmark": "Multi-Task Real-World Eval",
                "split_name": "streaming autoregressive action generation",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "Project page reports smoother trajectories and history-aware action generation on simulated and real-robot tasks.",
                "source_url": "https://arvla.insait.ai/",
            }
        ],
    },
    {
        "name": "ProgressVLA",
        "slug": "progressvla",
        "year": 2026,
        "open_source": False,
        "summary": (
            "A progress-guided diffusion policy for VLA manipulation that estimates task progress "
            "and uses differentiable guidance to refine action generation."
        ),
        "notes": "Open-source status is left false because the seed only verifies publication/project information.",
        "website_url": "https://www.microsoft.com/en-us/research/publication/progressvla-progress-guided-diffusion-policy-for-vision-language-robotic-manipulation/",
        "repo_url": None,
        "paradigm": "Diffusion / Flow-based",
        "paper": {
            "title": "ProgressVLA: Progress-Guided Diffusion Policy for Vision-Language Robotic Manipulation",
            "year": 2026,
            "venue_name": None,
            "publication_type": "arXiv preprint",
            "publication_status": "unknown",
            "arxiv_url": "https://arxiv.org/abs/2603.27670",
            "project_url": "https://www.microsoft.com/en-us/research/publication/progressvla-progress-guided-diffusion-policy-for-vision-language-robotic-manipulation/",
            "code_url": None,
            "notes": "Seed records selected authors only.",
        },
        "authors": [
            {
                "full_name": "Hongyu Yan",
                "affiliations": ["Microsoft Research"],
                "is_first_author": True,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Qiwei Li",
                "affiliations": ["Microsoft Research"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
            {
                "full_name": "Jiaolong Yang",
                "affiliations": ["Microsoft Research"],
                "is_first_author": False,
                "is_corresponding_author": False,
            },
        ],
        "topics": ["progress-aware control", "long-horizon", "reasoning", "generalist manipulation"],
        "data_sources": [{"name": "mixed", "notes": "Paper describes large-scale video-text pretraining plus robotic manipulation benchmarks."}],
        "evaluations": [
            {
                "benchmark": "CALVIN",
                "split_name": "progress estimation",
                "metric_name": "prediction residual",
                "metric_value": 0.07,
                "metric_unit": "",
                "result_summary": "Microsoft Research page reports a 0.07 progress prediction residual on a [0, 1] scale in simulation.",
                "source_url": "https://www.microsoft.com/en-us/research/publication/progressvla-progress-guided-diffusion-policy-for-vision-language-robotic-manipulation/",
            },
            {
                "benchmark": "LIBERO",
                "split_name": "long-horizon manipulation",
                "metric_name": None,
                "metric_value": None,
                "metric_unit": None,
                "result_summary": "Publication page reports substantial success-rate and generalization improvements on LIBERO and CALVIN.",
                "source_url": "https://www.microsoft.com/en-us/research/publication/progressvla-progress-guided-diffusion-policy-for-vision-language-robotic-manipulation/",
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
