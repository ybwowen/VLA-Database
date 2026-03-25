# VLA (Vision-Language-Action) Model Database System

## 1. Project Overview

This repository is a database course project for managing information about VLA (Vision-Language-Action) models used in embodied AI and robotic manipulation.

The project focuses on a practical question:

- How can we store, normalize, and query VLA model information in a structured database instead of keeping it in scattered spreadsheets, notes, or survey tables?

The system is designed as a small but complete web prototype that can demonstrate typical database-course capabilities:

- normalized schema design
- entity and relationship modeling
- foreign keys and many-to-many bridge tables
- seed data initialization
- basic query, conditional query, and statistical query
- a simple front end for browsing, filtering, and inspecting records

Important data-handling principle for this project:

- do not fabricate missing facts
- unknown fields should stay empty or `NULL`
- seed data is manually curated and intentionally partial where public information is uncertain

## 2. Core Features

The MVP covers the following functions:

- Model information management
  - model name, release year, open-source status, summary, notes
- Paper information management
  - paper title, venue, publication type, publication status, links
- Author and affiliation management
  - selected authors, author order, first-author flag, corresponding-author flag, affiliations
- Paradigm management
  - `Autoregressive`, `Diffusion / Flow-based`, `Dual System`, `Other`
- Topic classification management
  - `object-centric`, `task-centric`, `skill/subtask`, `depth/3D perception`, `reasoning`, `long-horizon`, `generalist manipulation`, `dexterous manipulation`, `sim2real`, `safety`, `other`
- Data source management
  - `real robot`, `simulation`, `synthetic`, `mixed`
- Benchmark and evaluation result management
  - benchmark name, metric, split/setting, result summary, source link
- Query support
  - browse all models
  - filter by paradigm
  - filter by topic
  - filter by benchmark
  - inspect model details
  - browse benchmark-centric result pages
  - view simple aggregate statistics on the home page
  - use a lightweight admin entry page to insert new model records
  - add paper-author-affiliation links through an admin form
  - add benchmark result rows through an admin form
  - open a dedicated schema page for ER explanation
  - edit model records through an admin form
  - delete selected paper-author links and benchmark-result rows

## 3. Recommended Stack

This project intentionally uses a simple stack that is easy to explain in a course demo.

- Backend: `Python 3.12 + Flask`
- ORM: `SQLAlchemy`
- Database: `MySQL 8.x`
- DB driver: `PyMySQL`
- Frontend: server-rendered `HTML + Jinja2 + CSS`
- Deployment style: direct local deployment in WSL, no Docker required

Why this stack:

- Flask is lightweight and fast to set up
- SQLAlchemy is clear enough to demonstrate relational modeling
- MySQL is suitable for a database course project and reflects a mainstream relational database deployment
- server-rendered templates are enough for browsing and querying data without introducing frontend complexity

## 4. Planned Project Structure

```text
VLA-Database/
├── .env.example
├── .gitignore
├── README.md
├── docs/
│   └── COURSE_REPORT.md
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
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html
│       ├── admin_model_form.html
│       ├── admin_paper_author_form.html
│       ├── admin_result_form.html
│       ├── benchmarks.html
│       ├── index.html
│       ├── models.html
│       ├── model_detail.html
│       ├── schema.html
│       └── stats.html
└── scripts/
    ├── init_db.py
    └── setup_mysql_wsl.sh
```

Directory responsibilities:

- `app/`
  - main application package
- `app/config.py`
  - MySQL connection and runtime configuration
- `app/db.py`
  - SQLAlchemy engine, session, and database bootstrap helpers
- `app/models.py`
  - normalized ORM entity definitions
- `app/routes.py`
  - page routes and query logic
- `app/seed_data.py`
  - curated initial data for representative VLA models
- `app/templates/`
  - Jinja templates for the web pages
- `app/static/css/`
  - project styling
- `scripts/init_db.py`
  - create tables and import seed data
- `scripts/setup_mysql_wsl.sh`
  - helper script to provision the MySQL database and user in WSL
- `run.py`
  - local application entry point
- `docs/COURSE_REPORT.md`
  - submission-ready course report outline in Markdown

## 5. Database Design

The schema is normalized to avoid putting all model information into a single denormalized table.

### Required Core Tables

| Table | Main Fields | Purpose |
| --- | --- | --- |
| `Model` | `id`, `name`, `slug`, `year`, `open_source`, `summary`, `paper_id`, `paradigm_id` | Stores the core VLA model record |
| `Paper` | `id`, `title`, `year`, `venue_name`, `publication_type`, `publication_status`, `arxiv_url`, `project_url`, `code_url` | Stores paper/publication metadata |
| `Author` | `id`, `full_name`, `notes` | Stores authors |
| `Affiliation` | `id`, `name`, `country`, `website_url` | Stores institutions or organizations |
| `PaperAuthor` | `paper_id`, `author_id`, `author_order`, `is_first_author`, `is_corresponding_author` | Bridge table between papers and authors |
| `AuthorAffiliation` | `author_id`, `affiliation_id`, `notes` | Bridge table between authors and institutions |
| `Paradigm` | `id`, `name`, `description` | Stores model paradigm categories |
| `Topic` | `id`, `name`, `description` | Stores research topic tags |
| `ModelTopic` | `model_id`, `topic_id` | Bridge table between models and topics |
| `DataSourceType` | `id`, `name`, `description` | Stores source categories such as real robot or simulation |
| `ModelDataSource` | `model_id`, `data_source_type_id`, `notes` | Bridge table between models and data source types |
| `Benchmark` | `id`, `name`, `category`, `description`, `official_url` | Stores evaluation benchmark definitions |
| `EvaluationResult` | `id`, `model_id`, `benchmark_id`, `metric_name`, `metric_value`, `metric_unit`, `split_name`, `result_summary`, `source_url` | Stores benchmark results or qualitative summaries |

### Design Notes

- `Model` and `Paper` are separated because a paper can conceptually support more than one model/version.
- `PaperAuthor` and `AuthorAffiliation` are separate bridge tables to correctly represent many-to-many relationships.
- `ModelTopic` and `ModelDataSource` are also bridge tables to preserve normalization.
- `EvaluationResult` supports both numeric metrics and textual summaries because many public VLA papers do not report directly comparable benchmark numbers for every model.

## 6. Main Relationships

- `Paradigm` 1-to-many `Model`
- `Paper` 1-to-many `Model`
- `Paper` many-to-many `Author` through `PaperAuthor`
- `Author` many-to-many `Affiliation` through `AuthorAffiliation`
- `Model` many-to-many `Topic` through `ModelTopic`
- `Model` many-to-many `DataSourceType` through `ModelDataSource`
- `Model` 1-to-many `EvaluationResult`
- `Benchmark` 1-to-many `EvaluationResult`

## 7. MVP Scope

The project intentionally starts with a minimum viable version instead of trying to build a complete research database in one step.

MVP includes:

- home page with project introduction and simple database statistics
- model list page
- model detail page
- benchmark result page
- statistics dashboard page
- lightweight admin data-entry page for new models
- admin page for linking authors and affiliations to papers
- admin page for adding benchmark-result rows to models
- admin page for editing existing models
- delete actions for author links and benchmark-result rows
- schema / ER explanation page
- simple filters for `paradigm`, `topic`, and `benchmark`
- seed data for 10 representative models

Seed models currently planned:

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

Notes on scope:

- some models above are adjacent to strict VLA definitions rather than universally agreed canonical VLA models
- such cases are explicitly documented in the seed notes
- uncertain fields are left empty instead of guessed

## 8. Query Scenarios to Demonstrate

This project is suitable for demonstrating the following database operations in class:

- list all models ordered by year
- query all models under a given paradigm
- query all models tagged with `reasoning`
- query all models evaluated on `CALVIN`
- inspect a single model and view its paper, selected authors, affiliations, topics, data sources, and evaluation results
- count how many models belong to each paradigm
- count how many models are associated with each topic
- compare publication-type distribution and benchmark coverage on the statistics page
- create a new model record through the admin form and immediately query it back
- attach a new author and affiliation to an existing paper
- attach a new evaluation result to an existing model
- edit an existing model record and verify the update immediately
- remove an author link or benchmark-result row through the admin interface
- explain the ER design directly from the built-in schema page

## 9. How to Run

### Environment Requirements

- Python `3.12+`
- MySQL `8.x` available inside WSL
- a MySQL user with permission to create tables in the target database

### 1. Install MySQL directly inside WSL

If MySQL is not installed yet:

```bash
sudo apt-get update
sudo apt-get install -y mysql-server
sudo systemctl enable --now mysql
```

If you want a dedicated app user instead of connecting as root, this repository also provides a helper script:

```bash
bash scripts/setup_mysql_wsl.sh
```

The helper script will:

- start the MySQL service
- create the database `vla_database` if missing
- create a dedicated user from environment variables if needed
- grant privileges to that user

If you already have a usable MySQL account, you can skip this helper.

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure MySQL connection

Copy the environment template:

```bash
cp .env.example .env
```

Then edit `.env` with your MySQL account and database name:

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=vla_user
MYSQL_PASSWORD=change_me
MYSQL_DATABASE=vla_database
SECRET_KEY=vla-course-project
```

If you prefer, you can also set a full SQLAlchemy URL directly:

```env
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3306/vla_database?charset=utf8mb4
```

### 4. Initialize schema and seed data

```bash
python3 scripts/init_db.py --reset
```

What this script does:

- connects to MySQL
- creates the database if it does not exist and privileges allow it
- creates all tables
- imports the curated seed data

### 5. Start the web app

```bash
python3 run.py
```

Then open:

```text
http://127.0.0.1:5000
```

Useful pages after startup:

- `/`
- `/models`
- `/models/<slug>`
- `/benchmarks`
- `/stats`
- `/schema`
- `/admin/models/new`
- `/admin/models/<model_id>/edit`
- `/admin/papers/<paper_id>/authors/new`
- `/admin/paper-authors/<paper_id>/<author_id>/delete`
- `/admin/models/<model_id>/results/new`
- `/admin/results/<result_id>/delete`

## 10. Future Extensions

Possible follow-up work after the MVP:

- richer data entry and editing forms
- fuller admin backend for maintaining authors, affiliations, and benchmark results
- more complete author lists and affiliation verification
- more benchmark entries and more rigorous metric normalization
- richer chart-based statistics and trend analysis
- exportable ER diagrams or printable schema handouts
- REST API endpoints for programmatic queries
- export to CSV / JSON
- advanced search with year ranges and multi-tag filters

## 11. Course Presentation Highlights

If this project is used for a final database demo, the most important talking points are:

- the schema is normalized
- many-to-many relationships are modeled correctly with bridge tables
- MySQL is used as the relational backend
- the system already supports browsing, filtering, and statistical summaries
- seed data is realistic but conservative, avoiding fabricated facts
