# VLA 模型数据库系统课程报告

## 1. 项目名称

VLA（Vision-Language-Action）模型数据库系统

## 2. 需求分析

随着具身智能和机器人领域快速发展，VLA 模型、机器人基础模型、benchmark 结果和开源资源持续增加。相关信息通常散落在论文、项目主页、GitHub 仓库、Hugging Face 模型卡和综述表格中。如果只使用 Excel 或非结构化笔记维护，会出现以下问题：

- 字段口径不统一，例如模型名称、论文状态、是否开源、benchmark split 的命名不一致。
- 实体关系复杂，例如一篇论文有多个作者，一个作者可能对应多个机构，一个模型也可能对应多个 topic、数据来源和 benchmark 结果。
- 条件查询困难，例如按 paradigm、topic、benchmark、年份或关键词组合筛选时，普通表格不方便表达多表联查。
- 统计分析不方便，例如统计范式分布、topic 覆盖、benchmark 覆盖、年份趋势时，需要重复人工整理。
- 扩展成本高，后续新增模型、作者、机构或评测结果时容易产生重复和不一致。

本项目目标是实现一个可运行的关系数据库应用原型，用 MySQL 系统化管理 VLA 模型信息，并展示数据库课程关注的核心能力：

- 规范化建模
- 实体关系设计
- 多对多关系拆分
- 外键约束与数据一致性
- 条件查询、聚合统计与时间线展示
- 轻量级增删改查流程

## 3. 技术方案

- 后端框架：Flask
- ORM：SQLAlchemy
- 数据库：MySQL 8
- 数据库驱动：PyMySQL
- 前端：HTML + Jinja2 + CSS
- 测试：SQLite in-memory + Flask test client
- Poster：python-pptx 生成可编辑英文 A1 竖版 PPTX
- 部署方式：WSL 本地直接部署

选择理由：

- Flask 轻量，适合课程项目快速实现和现场演示。
- MySQL 是关系数据库课程常见平台，便于展示表、外键和 SQL 查询思想。
- SQLAlchemy 可以清晰表达实体关系和中间表。
- 服务端渲染模板足够支撑浏览、筛选、统计和录入，不引入过重前端复杂度。
- PPTX poster 便于后续人工编辑，截图来自真实运行的前端页面。

## 4. 概念结构设计

系统围绕“模型、论文、作者、机构、分类、数据来源、benchmark 结果”组织数据。

核心实体：

- `Model`：VLA 模型或 VLA-adjacent 机器人基础模型。
- `Paper`：论文和出版信息。
- `Author`：作者。
- `Affiliation`：机构。
- `Paradigm`：模型范式，例如 Autoregressive、Diffusion / Flow-based、Dual System。
- `Topic`：研究主题，例如 reasoning、spatial grounding、real-time control。
- `DataSourceType`：数据来源类型，例如 real robot、simulation、synthetic、mixed。
- `Benchmark`：评测基准。
- `EvaluationResult`：模型在 benchmark 上的评测结果。

主要联系：

- 一个 `Paradigm` 可以对应多个 `Model`。
- 一个 `Paper` 可以对应一个或多个 `Model`。
- 一个 `Paper` 可以有多个 `Author`，一个 `Author` 也可以参与多篇论文。
- 一个 `Author` 可以有多个 `Affiliation`，一个 `Affiliation` 也可以对应多位作者。
- 一个 `Model` 可以对应多个 `Topic` 和多个 `DataSourceType`。
- 一个 `Model` 可以有多条 `EvaluationResult`。
- 一个 `Benchmark` 可以被多条 `EvaluationResult` 引用。

## 5. 逻辑结构设计

### 5.1 核心实体表

- `models`
- `papers`
- `authors`
- `affiliations`
- `paradigms`
- `topics`
- `data_source_types`
- `benchmarks`
- `evaluation_results`

### 5.2 中间表

- `paper_authors`
- `author_affiliations`
- `model_topics`
- `model_data_sources`

### 5.3 关系模式说明

- `models(id, name, slug, year, open_source, summary, notes, website_url, repo_url, paper_id, paradigm_id)`
- `papers(id, title, year, venue_name, publication_type, publication_status, arxiv_url, project_url, code_url, notes)`
- `authors(id, full_name, notes)`
- `affiliations(id, name, country, website_url, notes)`
- `paper_authors(paper_id, author_id, author_order, is_first_author, is_corresponding_author, notes)`
- `author_affiliations(author_id, affiliation_id, notes)`
- `paradigms(id, name, description)`
- `topics(id, name, description)`
- `model_topics(model_id, topic_id)`
- `data_source_types(id, name, description)`
- `model_data_sources(model_id, data_source_type_id, notes)`
- `benchmarks(id, name, category, description, official_url)`
- `evaluation_results(id, model_id, benchmark_id, split_name, metric_name, metric_value, metric_unit, result_summary, source_url, notes)`

## 6. 规范化设计思路

本项目没有把所有信息堆在一张大表中，而是按照实体和关系拆分：

- 模型信息与论文信息分离，避免论文元数据在多个模型记录中重复。
- 作者与机构独立建表，支持跨论文复用。
- topic、数据来源、benchmark 使用参考表统一分类口径。
- 多值属性通过中间表建模，而不是用逗号拼接写入单字段。
- benchmark 结果单独拆成事实表，方便扩展不同 metric、split 和来源链接。
- 数值型结果与文字型摘要同时支持，因为很多 VLA 论文并不提供统一可比的 benchmark 数值。

这种设计符合数据库课程中对规范化、可维护性、可扩展性和查询能力的要求。

## 7. 功能实现

### 7.1 浏览与查询

- 首页 `/`：项目简介、模型数量、论文数量、作者数量、benchmark 数量和代表模型。
- 模型列表 `/models`：支持按关键词、paradigm、topic、benchmark、year 筛选。
- 模型详情 `/models/<slug>`：展示模型、论文、作者、机构、topic、数据来源和 benchmark 结果。
- Benchmark 页 `/benchmarks`：从 benchmark 视角浏览模型结果。
- 统计页 `/stats`：展示范式分布、topic 覆盖、数据来源分布、出版类型分布、benchmark 覆盖和年份趋势。
- 时间线页 `/timeline`：按年份展示 2022-2026 的代表模型和主题演化。
- Schema 页 `/schema`：展示 E-R 图、实体字段和关系说明。

### 7.2 管理与录入

- 新增模型：`/admin/models/new`
- 编辑模型：`/admin/models/<model_id>/edit`
- 新增论文作者与机构关联：`/admin/papers/<paper_id>/authors/new`
- 删除论文作者关联：`/admin/paper-authors/<paper_id>/<author_id>/delete`
- 新增 benchmark 结果：`/admin/models/<model_id>/results/new`
- 删除 benchmark 结果：`/admin/results/<result_id>/delete`

### 7.3 数据校验

系统对管理表单做了基础校验：

- 模型名称不能为空。
- slug 自动生成且不能重复。
- 年份必须是整数。
- paradigm 必须存在。
- publication type/status 必须来自允许列表。
- benchmark result 至少要有 metric 或文字 summary。
- metric value 必须是数值。

## 8. 当前数据范围

当前系统内置 20 个代表性模型，覆盖 2022-2026：

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

数据治理原则：

- 对信息不确定的字段保留为空。
- 对有争议是否属于标准 VLA 的模型，在备注中保守说明。
- benchmark 数值只录入公开来源明确给出的数据。
- 只有定性结果时，写入 `result_summary`，不编造 `metric_value`。
- 每条评测尽量保留 `source_url`，方便追溯。

## 9. 查询示例

系统可以演示以下数据库查询能力：

- 按年份查询：`/models?year=2026`
- 按范式查询：例如查询 Diffusion / Flow-based 模型。
- 按 topic 查询：例如查询 `real-time control`、`spatial grounding`、`reasoning`。
- 按 benchmark 查询：例如查询 `LIBERO`、`CALVIN`、`SimplerEnv`。
- 关键词查询：例如搜索 `Green-VLA` 或 `OpenVLA`。
- 模型详情联查：从 `models` 联查 `papers`、`authors`、`affiliations`、`topics`、`data_source_types`、`evaluation_results`、`benchmarks`。
- 聚合统计：统计 paradigm 分布、topic 覆盖度、benchmark 覆盖度、年份分布。

## 10. 数据来源

项目优先使用官方项目页、论文页、GitHub/Hugging Face 模型卡作为来源，例如：

- RDT-1B：https://rdt-robotics.github.io/rdt-robotics/
- SpatialVLA：https://github.com/SpatialVLA/SpatialVLA
- OpenVLA-OFT：https://github.com/moojink/openvla-oft
- GR00T N1.5：https://research.nvidia.com/labs/gear/gr00t-n1_5/
- pi0.5：https://www.physicalintelligence.company/blog/pi05
- SmolVLA：https://huggingface.co/docs/lerobot/v0.4.3/en/smolvla
- Xiaomi-Robotics-0：https://robotics.xiaomi.com/xiaomi-robotics-0.html
- Green-VLA：https://greenvla.github.io/
- AR-VLA：https://arvla.insait.ai/
- ProgressVLA：https://www.microsoft.com/en-us/research/publication/progressvla-progress-guided-diffusion-policy-for-vision-language-robotic-manipulation/

## 11. 测试验证

项目增加了 SQLite in-memory 测试入口，不依赖真实 MySQL 服务。测试内容包括：

- seed data 能正常加载。
- 模型数量不少于 20。
- 2026 模型 `Xiaomi-Robotics-0`、`Green-VLA`、`AR-VLA`、`ProgressVLA` 存在。
- 新增 topic 分类存在。
- `/`、`/models`、`/models?year=2026`、`/stats`、`/schema`、`/timeline`、`/benchmarks` 返回 200。
- `/models/xiaomi-robotics-0` 能展示论文、topic、数据来源和评测结果。
- 管理端模型创建表单能拦截空模型名、缺失 paradigm、非法年份。

命令：

```bash
python -m pytest -q
```

如果本地虚拟环境没有安装 pytest，需要先安装测试依赖。

## 12. Poster 交付

项目包含一个可编辑英文 A1 竖版 poster 工程：

```text
projects/vla_database_final_poster_a1_20260509/
```

Poster 特点：

- 使用 `python-pptx` 生成 PowerPoint。
- 页面尺寸为 A1 portrait。
- 标题、正文、标签、图例、色块均为可编辑对象。
- 前端截图来自真实运行的 Flask 页面，包括 `/schema`、`/stats`、`/models?year=2026`、`/timeline` 和模型详情页。
- 不把整张 poster 合成为一张不可编辑图片。

## 13. 管理功能演示建议

现场演示顺序：

1. 打开 `/schema` 讲解实体、字段和 cardinality。
2. 打开 `/stats` 展示聚合查询。
3. 打开 `/timeline` 展示 2022-2026 模型演化。
4. 打开 `/models?year=2026` 展示年份筛选。
5. 打开 `/models/xiaomi-robotics-0` 展示详情联查。
6. 在 `/admin/models/new` 新增模型。
7. 在模型详情页点击 “Add Author / Affiliation”。
8. 在模型详情页点击 “Add Benchmark Result”。
9. 删除一条 author link 或 result row，展示 delete 操作。

该流程可以覆盖查询、插入、更新、删除、关系设计和统计分析。

## 14. 项目亮点

- 使用 MySQL 实现真实关系数据库后端。
- 数据结构规范化，关系清晰。
- 多对多关系都通过桥表表达。
- 既支持浏览查询，也支持后台录入。
- 既支持明细展示，也支持统计分析和时间线展示。
- seed data 覆盖 2022-2026，包含当前较新的 2026 条目。
- 数据录入策略保守，不编造未知字段和 benchmark 数值。
- Poster 直接使用项目实际运行截图，适合课程最终展示。

## 15. 不足与后续扩展

- 目前作者列表仍是 selected authors，并非每篇论文完整作者表。
- 管理端还没有登录权限控制。
- benchmark metric 尚未做统一单位规范化。
- 可以继续增加 CSV/JSON 导出。
- 可以增加 REST API 供程序化查询。
- 可以增加更完整的来源审计表和数据更新日志。

## 16. 结论

本项目实现了一个完整可运行的 VLA 模型数据库原型，满足数据库课程大作业对于“数据库设计与实现”的核心要求。系统具备：

- 合理的关系模型
- 可运行的 MySQL 后端
- 可展示的 Web 界面
- 可操作的增删改查能力
- 可答辩的统计、schema 和 timeline 页面
- 可编辑的英文 A1 poster 交付物

因此，它既可以作为数据库课程最终项目，也可以作为后续扩展成更完整 VLA 资料库的基础。
