# VLA (Vision-Language-Action) Model Database System

## 1. Project Overview

This repository is a database course project for managing VLA
(Vision-Language-Action) and closely related robot foundation models used in
embodied AI and robotic manipulation.

The project focuses on a practical database-design question:

- How can VLA model information be stored, normalized, queried, and extended in
  a relational database instead of being scattered across papers, project pages,
  GitHub repositories, model cards, and manually maintained spreadsheets?

The system is a small but complete web prototype that demonstrates:

- normalized schema design
- entity and relationship modeling
- foreign keys and many-to-many bridge tables
- curated seed data initialization
- basic query, conditional query, statistical query, and timeline query
- a server-rendered web front end for browsing, filtering, inspecting, and
  editing records

Data-handling principle:

- do not fabricate missing facts
- unknown fields stay empty or `NULL`
- numeric benchmark values are recorded only when a public source reports them
- qualitative benchmark rows are allowed when a source describes results without
  directly comparable numbers

## 2. Core Features

The final course-project version covers the following functions:

- Model information management
  - model name, release year, open-source status, summary, notes
- Paper information management
  - paper title, venue, publication type, publication status, links
- Author and affiliation management
  - selected authors, author order, first-author flag, corresponding-author flag,
    affiliations
- Paradigm management
  - `Autoregressive`, `Diffusion / Flow-based`, `Dual System`, `Other`
- Topic classification management
  - object-centric, task-centric, reasoning, long-horizon, generalist
    manipulation, bimanual manipulation, humanoid robotics, spatial grounding,
    real-time control, open-world generalization, progress-aware control, and
    other taxonomy terms
- Data source management
  - `real robot`, `simulation`, `synthetic`, `mixed`
- Benchmark and evaluation result management
  - benchmark name, metric, split/setting, result summary, source link
- Query support
  - browse all models
  - filter by paradigm, topic, benchmark, year, and keyword
  - inspect model details
  - browse benchmark-centric result pages
  - view aggregate statistics
  - view a 2022-2026 timeline page
  - use lightweight admin forms to create and edit model records
  - add paper-author-affiliation links
  - add and delete benchmark result rows
  - open a dedicated schema page for ER explanation

## 3. Recommended Stack

- Backend: `Python 3.11+ / 3.12 + Flask`
- ORM: `SQLAlchemy`
- Database: `MySQL 8.x`
- DB driver: `PyMySQL`
- Frontend: server-rendered `HTML + Jinja2 + CSS`
- Poster generation: `python-pptx` plus screenshots from the running frontend
- Deployment style: direct local deployment in WSL, no Docker required

Why this stack:

- Flask keeps the web layer simple enough for a database course demo
- SQLAlchemy expresses entity relationships clearly
- MySQL reflects a mainstream relational database deployment
- server-rendered pages are enough for query and CRUD demonstration
- a generated PPTX poster remains editable after creation

## 4. Project Structure

```text
VLA-Database/
├── README.md
├── requirements.txt
├── run.py
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── models.py
│   ├── routes.py
│   ├── seed_data.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── img/er_diagram.svg
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── models.html
│       ├── model_detail.html
│       ├── benchmarks.html
│       ├── stats.html
│       ├── schema.html
│       ├── timeline.html
│       └── admin_*.html
├── docs/
│   ├── COURSE_REPORT.md
│   └── index.html
├── projects/
│   └── vla_database_final_poster_a1_20260509/
├── scripts/
│   ├── init_db.py
│   └── setup_mysql_wsl.sh
└── tests/
    └── test_app.py
```

## 5. Database Design

The schema is normalized to avoid putting all model information into one
denormalized table.

| Table | Main Fields | Purpose |
| --- | --- | --- |
| `models` | `id`, `name`, `slug`, `year`, `open_source`, `summary`, `paper_id`, `paradigm_id` | Core VLA model records |
| `papers` | `id`, `title`, `year`, `venue_name`, `publication_type`, `publication_status`, links | Paper/publication metadata |
| `authors` | `id`, `full_name`, `notes` | Author records |
| `affiliations` | `id`, `name`, `country`, `website_url` | Institutions or organizations |
| `paper_authors` | `paper_id`, `author_id`, `author_order`, flags | Paper-author bridge table |
| `author_affiliations` | `author_id`, `affiliation_id`, `notes` | Author-affiliation bridge table |
| `paradigms` | `id`, `name`, `description` | Model paradigm reference table |
| `topics` | `id`, `name`, `description` | Research topic reference table |
| `model_topics` | `model_id`, `topic_id` | Model-topic bridge table |
| `data_source_types` | `id`, `name`, `description` | Source categories |
| `model_data_sources` | `model_id`, `data_source_type_id`, `notes` | Model-source bridge table |
| `benchmarks` | `id`, `name`, `category`, `description`, `official_url` | Benchmark definitions |
| `evaluation_results` | `id`, `model_id`, `benchmark_id`, `metric_name`, `metric_value`, `metric_unit`, `split_name`, `result_summary`, `source_url` | Benchmark result facts |

Main relationships:

- `Paradigm` 1-to-many `Model`
- `Paper` 1-to-many `Model`
- `Paper` many-to-many `Author` through `PaperAuthor`
- `Author` many-to-many `Affiliation` through `AuthorAffiliation`
- `Model` many-to-many `Topic` through `ModelTopic`
- `Model` many-to-many `DataSourceType` through `ModelDataSource`
- `Model` 1-to-many `EvaluationResult`
- `Benchmark` 1-to-many `EvaluationResult`

## 6. Seed Data Scope

The database currently seeds 20 representative models across 2022-2026:

- RT-1
- RT-2
- VIMA
- RoboFlamingo
- GR-1
- OpenVLA
- Octo
- pi0
- OpenHelix
- Fast-in-Slow
- RDT-1B
- SpatialVLA
- OpenVLA-OFT
- GR00T N1.5
- pi0.5
- SmolVLA
- Xiaomi-Robotics-0
- Green-VLA
- AR-VLA
- ProgressVLA

The 2026 records are included to show that the schema can keep up with recent
VLA development. They are seeded conservatively and cite public project pages or
publication pages through `source_url` fields.

## 7. Query Scenarios To Demonstrate

This project is suitable for demonstrating the following database operations:

- list all models ordered by year
- query models released in `2026`
- query all models under a given paradigm
- query all models tagged with `reasoning`, `spatial grounding`, or
  `real-time control`
- query all models evaluated on `CALVIN`, `LIBERO`, or `SimplerEnv`
- inspect a single model and view its paper, selected authors, affiliations,
  topics, data sources, and evaluation results
- count how many models belong to each paradigm
- count how many models are associated with each topic
- compare publication-type distribution, benchmark coverage, and year coverage
  on the statistics page
- view the `/timeline` page to explain model evolution from 2022 to 2026
- create a new model record through the admin form and query it back
- attach a new author and affiliation to an existing paper
- attach a new evaluation result to an existing model
- edit an existing model record and verify the update immediately
- remove an author link or benchmark-result row through the admin interface
- explain the ER design directly from the built-in schema page

## 8. How To Run

### Environment Requirements

- Python `3.11+`
- MySQL `8.x` available inside WSL
- a MySQL user with permission to create tables in the target database

### 1. Install MySQL directly inside WSL

```bash
sudo apt-get update
sudo apt-get install -y mysql-server
sudo systemctl enable --now mysql
```

Optional helper:

```bash
bash scripts/setup_mysql_wsl.sh
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure MySQL connection

```bash
cp .env.example .env
```

Example `.env`:

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=vla_user
MYSQL_PASSWORD=change_me
MYSQL_DATABASE=vla_database
SECRET_KEY=vla-course-project
```

Or provide a full SQLAlchemy URL:

```env
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3306/vla_database?charset=utf8mb4
```

### 4. Initialize schema and seed data

```bash
python3 scripts/init_db.py --reset
```

### 5. Start the web app

```bash
python3 run.py
```

Open:

```text
http://127.0.0.1:5000
```

Useful pages:

- `/`
- `/models`
- `/models?year=2026`
- `/models/<slug>`
- `/benchmarks`
- `/stats`
- `/timeline`
- `/schema`
- `/admin/models/new`
- `/admin/models/<model_id>/edit`
- `/admin/papers/<paper_id>/authors/new`
- `/admin/models/<model_id>/results/new`

## 9. Tests

The test entry point uses SQLite in memory so it does not depend on the local
MySQL service:

```bash
python -m pytest -q
```

The current environment may need `pytest` installed before running the command.
The tests cover:

- seed-data loading
- presence of 2026 models
- topic taxonomy expansion
- public route responses
- model filtering
- representative model detail pages
- basic admin validation

## 10. Poster Output

The final editable poster lives under:

```text
projects/vla_database_final_poster_a1_20260509/
```

The generated file is:

```text
vla_database_final_poster_a1_20260509.pptx
```

Poster characteristics:

- English A1 portrait format
- editable PowerPoint text, shapes, and charts
- frontend screenshots captured from actual Flask routes
- source notes stored in `sources.md`

## 11. Course Presentation Highlights

- The schema is normalized and avoids repeated denormalized fields.
- Many-to-many relationships are modeled with bridge tables.
- `evaluation_results` is a fact table that supports numeric and qualitative
  benchmark records.
- MySQL is used as the relational backend.
- The frontend demonstrates filtering, details, statistics, timeline, and admin
  CRUD workflows.
- Seed data is realistic but conservative: unknown values are not guessed, and
  benchmark numbers are only stored when public sources support them.
