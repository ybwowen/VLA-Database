from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .db import Base


class Paradigm(Base):
    __tablename__ = "paradigms"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    models = relationship("VlaModel", back_populates="paradigm")


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False, unique=True)
    year = Column(Integer)
    venue_name = Column(String(255))
    publication_type = Column(String(50))
    publication_status = Column(String(50))
    arxiv_url = Column(String(512))
    project_url = Column(String(512))
    code_url = Column(String(512))
    notes = Column(Text)

    models = relationship("VlaModel", back_populates="paper")
    paper_authors = relationship(
        "PaperAuthor",
        back_populates="paper",
        cascade="all, delete-orphan",
        order_by="PaperAuthor.author_order",
    )

    @property
    def corresponding_authors(self):
        return [link.author for link in self.paper_authors if link.is_corresponding_author]


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False, unique=True)
    notes = Column(Text)

    paper_authors = relationship(
        "PaperAuthor",
        back_populates="author",
        cascade="all, delete-orphan",
    )
    author_affiliations = relationship(
        "AuthorAffiliation",
        back_populates="author",
        cascade="all, delete-orphan",
    )


class Affiliation(Base):
    __tablename__ = "affiliations"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    country = Column(String(100))
    website_url = Column(String(512))
    notes = Column(Text)

    author_affiliations = relationship(
        "AuthorAffiliation",
        back_populates="affiliation",
        cascade="all, delete-orphan",
    )


class PaperAuthor(Base):
    __tablename__ = "paper_authors"

    paper_id = Column(Integer, ForeignKey("papers.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)
    author_order = Column(Integer, nullable=False)
    is_first_author = Column(Boolean, default=False, nullable=False)
    is_corresponding_author = Column(Boolean, default=False, nullable=False)
    notes = Column(Text)

    paper = relationship("Paper", back_populates="paper_authors")
    author = relationship("Author", back_populates="paper_authors")


class AuthorAffiliation(Base):
    __tablename__ = "author_affiliations"

    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)
    affiliation_id = Column(Integer, ForeignKey("affiliations.id"), primary_key=True)
    notes = Column(Text)

    author = relationship("Author", back_populates="author_affiliations")
    affiliation = relationship("Affiliation", back_populates="author_affiliations")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    model_topics = relationship(
        "ModelTopic",
        back_populates="topic",
        cascade="all, delete-orphan",
    )


class ModelTopic(Base):
    __tablename__ = "model_topics"

    model_id = Column(Integer, ForeignKey("models.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), primary_key=True)

    model = relationship("VlaModel", back_populates="model_topics")
    topic = relationship("Topic", back_populates="model_topics")


class DataSourceType(Base):
    __tablename__ = "data_source_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)

    model_data_sources = relationship(
        "ModelDataSource",
        back_populates="data_source_type",
        cascade="all, delete-orphan",
    )


class ModelDataSource(Base):
    __tablename__ = "model_data_sources"

    model_id = Column(Integer, ForeignKey("models.id"), primary_key=True)
    data_source_type_id = Column(Integer, ForeignKey("data_source_types.id"), primary_key=True)
    notes = Column(Text)

    model = relationship("VlaModel", back_populates="model_data_sources")
    data_source_type = relationship("DataSourceType", back_populates="model_data_sources")


class Benchmark(Base):
    __tablename__ = "benchmarks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    category = Column(String(100))
    description = Column(Text)
    official_url = Column(String(512))

    evaluation_results = relationship(
        "EvaluationResult",
        back_populates="benchmark",
        cascade="all, delete-orphan",
    )


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    benchmark_id = Column(Integer, ForeignKey("benchmarks.id"), nullable=False)
    split_name = Column(String(100))
    metric_name = Column(String(100))
    metric_value = Column(Float)
    metric_unit = Column(String(30))
    result_summary = Column(Text)
    source_url = Column(String(512))
    notes = Column(Text)

    model = relationship("VlaModel", back_populates="evaluation_results")
    benchmark = relationship("Benchmark", back_populates="evaluation_results")


class VlaModel(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=False, unique=True)
    year = Column(Integer)
    open_source = Column(Boolean, nullable=False, default=False)
    summary = Column(Text)
    notes = Column(Text)
    website_url = Column(String(512))
    repo_url = Column(String(512))
    paper_id = Column(Integer, ForeignKey("papers.id"))
    paradigm_id = Column(Integer, ForeignKey("paradigms.id"))

    paper = relationship("Paper", back_populates="models")
    paradigm = relationship("Paradigm", back_populates="models")
    model_topics = relationship(
        "ModelTopic",
        back_populates="model",
        cascade="all, delete-orphan",
    )
    model_data_sources = relationship(
        "ModelDataSource",
        back_populates="model",
        cascade="all, delete-orphan",
    )
    evaluation_results = relationship(
        "EvaluationResult",
        back_populates="model",
        cascade="all, delete-orphan",
    )

    @property
    def topic_names(self):
        return sorted(link.topic.name for link in self.model_topics)

    @property
    def data_source_names(self):
        return sorted(link.data_source_type.name for link in self.model_data_sources)

    @property
    def benchmark_names(self):
        names = {result.benchmark.name for result in self.evaluation_results}
        return sorted(names)
