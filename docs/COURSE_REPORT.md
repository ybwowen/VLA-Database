# VLA 模型数据库系统课程报告

## 1. 项目名称

VLA（Vision-Language-Action）模型数据库系统

## 2. 项目背景与目标

随着具身智能和机器人领域的发展，VLA 模型越来越多，相关信息通常散落在论文、项目主页、GitHub 仓库和综述表格中。若仅用 Excel 或非结构化笔记维护，存在以下问题：

- 信息字段不统一
- 作者、机构、topic、benchmark 难以规范化管理
- 条件查询和统计分析不方便
- 数据复用性和可扩展性较差

本项目的目标是实现一个可运行的数据库应用原型，用关系数据库系统化管理 VLA 模型信息，并展示数据库课程关注的核心能力：

- 规范化建模
- 实体关系设计
- 多对多关系拆分
- 外键约束与数据一致性
- 查询、筛选、统计与数据录入

## 3. 技术方案

- 后端框架：Flask
- ORM：SQLAlchemy
- 数据库：MySQL 8
- 数据库驱动：PyMySQL
- 前端：HTML + Jinja2 + CSS
- 部署方式：WSL 本地直接部署

选择理由：

- Flask 轻量、便于课程项目快速实现
- MySQL 适合数据库课程演示
- SQLAlchemy 能清晰表达实体关系和中间表
- 服务端渲染模板足够支撑查询和录入功能

## 4. 功能模块

### 4.1 浏览与查询

- 首页：项目简介和关键统计
- 模型列表页：支持按 paradigm、topic、benchmark 和关键词筛选
- 模型详情页：展示模型、论文、作者、机构、topic、数据来源、benchmark 结果
- Benchmark 页：从 benchmark 视角查看对应模型结果
- 统计页：展示聚合查询结果
- Schema 页：展示 ER 设计和关系说明

### 4.2 管理与录入

- 新增模型
- 编辑模型
- 新增论文作者与机构关联
- 删除论文作者关联
- 新增 benchmark 结果
- 删除 benchmark 结果

## 5. 数据库设计

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

### 5.3 关系说明

- `Paradigm -> Model`：一对多
- `Paper -> Model`：一对多
- `Paper <-> Author`：多对多，通过 `paper_authors`
- `Author <-> Affiliation`：多对多，通过 `author_affiliations`
- `Model <-> Topic`：多对多，通过 `model_topics`
- `Model <-> DataSourceType`：多对多，通过 `model_data_sources`
- `Model -> EvaluationResult`：一对多
- `Benchmark -> EvaluationResult`：一对多

## 6. 规范化设计思路

本项目没有把所有信息堆在一张大表中，而是按照实体和关系拆分：

- 模型信息与论文信息分离，避免论文元数据重复
- 作者与机构独立建表，支持跨论文复用
- topic、数据来源、benchmark 采用参考表管理
- 多值属性通过中间表建模，而不是逗号拼接写入单字段
- benchmark 结果单独拆成事实表，方便扩展不同 metric 和 split

这样的设计更符合关系数据库课程中对规范化、可维护性和可扩展性的要求。

## 7. 当前实现的数据范围

当前系统内置了 10 个代表性模型的 seed data，包括：

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

说明：

- 对信息不确定的字段保留为空
- 对有争议是否属于标准 VLA 的模型，在备注中保守说明
- benchmark 数值仅录入相对有把握的公开信息

## 8. 查询与展示能力

系统目前支持以下数据库演示场景：

- 按范式查询模型
- 按 topic 查询模型
- 按 benchmark 查询模型
- 查看某个模型的完整详情
- 统计每种 paradigm 的模型数量
- 统计每个 topic 的覆盖情况
- 统计不同数据来源类型的分布
- 统计 publication type 的分布
- 查看 benchmark 覆盖度
- 查看模型年份分布

## 9. 管理功能演示建议

现场演示时可以按以下顺序：

1. 打开 `/schema` 讲解数据库设计
2. 打开 `/stats` 演示聚合查询
3. 打开 `/models` 和某个详情页演示条件查询与详情查询
4. 在 `/admin/models/new` 新增一个模型
5. 在模型详情页点击 “Add Author / Affiliation”
6. 在模型详情页点击 “Add Benchmark Result”

这样可以同时覆盖：

- 查询
- 插入
- 更新
- 删除
- 关系设计
- 统计分析

## 10. 项目亮点

- 使用 MySQL 实现真实关系数据库后端
- 数据结构规范化，关系清晰
- 既支持浏览查询，也支持后台录入
- 既支持明细展示，也支持统计分析
- 页面简单但完整，适合数据库课程验收

## 11. 不足与后续扩展

目前仍有一些可以继续完善的方向：

- 增加完整的作者列表维护
- 增加 benchmark 结果编辑功能
- 增加删除模型和删除论文的安全流程
- 增加更细粒度的数据校验
- 增加图表导出或 CSV 导出
- 增加管理员登录权限控制

## 12. 结论

本项目实现了一个完整可运行的 VLA 模型数据库原型，满足数据库课程大作业对于“数据库设计与实现”的核心要求。系统已经具备：

- 合理的关系模型
- 可运行的 MySQL 后端
- 可展示的 Web 界面
- 可操作的增删改查能力
- 可答辩的统计与 schema 展示页面

因此，它不仅可以作为课程作业原型，也可以作为后续扩展成更完整 VLA 资料库的基础。
