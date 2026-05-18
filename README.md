# VLA (Vision-Language-Action) Model Database System

## 1. Project Overview

This repository provides a relational database system for managing VLA
(Vision-Language-Action) and closely related robot foundation models used in
embodied AI and robotic manipulation.

The project focuses on a practical database-design question:

- How can VLA model information be stored, normalized, queried, and extended in
  a relational database instead of being scattered across papers, project pages,
  GitHub repositories, model cards, and manually maintained spreadsheets?

The system is a small but complete web prototype that provides:

- normalized schema design
- entity and relationship modeling
- foreign keys and many-to-many bridge tables
- sample data initialization
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

The current build covers the following functions:

- Model information management
  - model name, release year, open-source status, summary, notes
- Paper information management
  - paper title, venue, publication type, publication status, links
- Author and affiliation management
  - paper author lists, author order, first-author flag, corresponding-author
    flag, and source-backed per-paper affiliation snapshots
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
  - filter by year range, paradigm, topic, benchmark, open-source status,
    data-source type, and keyword
  - inspect model details
  - browse benchmark-centric result pages
  - view aggregate statistics
  - view a 2022-2026 timeline page
  - use lightweight admin forms to create and edit model records
  - add paper-author-affiliation links
  - add and delete benchmark result rows
  - open a dedicated schema page for ER explanation
- Frontend presentation
  - dark-blue navigation bar with global model search
  - dashboard-style model browsing page with left filters, central table, and
    right-side statistics/timeline cards
  - static GitHub Pages showcase under `docs/` using the same visual language as
    the Flask app

## 3. Recommended Stack

- Backend: `Python 3.11+ / 3.12 + Flask`
- ORM: `SQLAlchemy`
- Database: `MySQL 8.x`
- DB driver: `PyMySQL`
- Frontend: server-rendered `HTML + Jinja2 + CSS`
- Static project page: GitHub Pages from `docs/`
- Report assets: `python-pptx` plus screenshots from the running frontend
- Deployment style: direct local deployment in WSL, no Docker required

Why this stack:

- Flask keeps the web layer compact and easy to inspect
- SQLAlchemy expresses entity relationships clearly
- MySQL reflects a mainstream relational database deployment
- server-rendered pages are enough for query and CRUD workflows
- generated PPTX assets remain editable after creation

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
│   ├── index.html
│   └── assets/
│       ├── site.css
│       └── er_diagram.svg
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
- `Paper` many-to-many `Topic` through `PaperTopic`
- `Author` many-to-many `Affiliation` through `AuthorAffiliation`
- `Model` many-to-many `Topic` through `ModelTopic`
- `Model` many-to-many `DataSourceType` through `ModelDataSource`
- `Model` 1-to-many `EvaluationResult`
- `Benchmark` 1-to-many `EvaluationResult`

## 6. Data Scope

The database loads a compact core set of hand-checked model records and then
creates additional lightweight model records from explicit `model_names` fields
in the paper index when a paper clearly introduces a VLA model or model-level
method. The current sample data covers more than 150 model records across
2022-2026 and more than 145 VLA model or method papers, including robot
foundation models, language-conditioned
policies, action tokenization, and model-level adaptation or acceleration
methods.

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
- FASTer
- X-VLA
- PixelVLA
- MemoryVLA
- Vlaser

The 2026 records cite public project pages or publication pages through the
paper/model link fields and benchmark `source_url` rows.

The paper index is stored in `data/paper_library.json`. It is imported
idempotently into `papers` and linked to `topics` through `paper_topics`, so
papers can be queried even when they are represented only as lightweight
model/method records. Pure dataset, benchmark, and platform-only entries are
excluded from this file. Author metadata is imported when it is available from
arXiv, CVF, ICLR, PMLR, RSS, or project pages. Affiliations are attached when a
source gives a reliable author-institution mapping; otherwise they are left
empty. Because the normalized schema stores author affiliations globally, the
seed also stores source-backed per-paper affiliation snapshots on the
`paper_authors.notes` bridge row and the detail pages display those first.

## 7. Query Scenarios

The application supports the following database operations:

- list all models ordered by year
- query models released in a single year, such as `2026`
- query models within a year range, such as `2024-2026`
- query all models under a given paradigm
- query all models tagged with `reasoning`, `spatial grounding`, or
  `real-time control`
- query all models evaluated on `CALVIN`, `LIBERO`, or `SimplerEnv`
- query only open-source or closed-source model records
- query models by data-source type, such as `real robot`, `simulation`,
  `synthetic`, or `mixed`
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
SECRET_KEY=vla-database-system
```

Or provide a full SQLAlchemy URL:

```env
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3306/vla_database?charset=utf8mb4
```

### 4. Initialize schema and sample data

```bash
.venv/bin/python scripts/init_db.py --reset
```

### 5. Start the web app

```bash
.venv/bin/python run.py
```

Do not prefix the script name with another interpreter name. For example,
`.venv/bin/python python3 run.py` asks Python to open a local file named
`python3`, which will fail.

Open:

```text
http://127.0.0.1:5000
```

Useful pages:

- `/`
- `/models`
- `/models?year=2026`
- `/models?year_from=2024&year_to=2026`
- `/models?year_from=2024&year_to=2026&open_source=yes`
- `/papers`
- `/papers?year=2025`
- `/queries`
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

- sample-data loading
- paper-index size, unique titles, source links, and PaperTopic coverage
- presence of 2026 models
- topic taxonomy expansion
- public route responses
- model filtering
- representative model detail pages
- basic admin validation

## 10. Visual Materials

The GitHub Pages version lives in `docs/index.html` with styles in
`docs/assets/site.css`. It is a static showcase of the same dashboard-oriented
interface used by the Flask app: dark-blue navigation, model search, filter
sidebar, compact model table, statistics cards, and timeline preview.

Visual-generation assets are kept locally under the ignored `projects/`
directory and are not part of this code push. The Flask routes expose the paper
index, SQL examples, schema, statistics, timeline, and model browsing pages
needed for screenshots.

## 11. System Highlights

- The schema is normalized and avoids repeated denormalized fields.
- Many-to-many relationships are modeled with bridge tables.
- `evaluation_results` is a fact table that supports numeric and qualitative
  benchmark records.
- MySQL is used as the relational backend.
- The frontend provides dashboard-style filtering, paper browsing, details,
  statistics, SQL examples, timeline, and admin CRUD workflows.
- Sample data keeps unknown values empty, and
  benchmark numbers are only stored when public sources support them.
