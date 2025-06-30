from sqlalchemy.orm import Mapped, mapped_column, relationship #type: ignore
from sqlalchemy import ( #type: ignore
    String, Integer, Enum as SQLAlchemyEnum,
    ForeignKey, DECIMAL, Boolean, UniqueConstraint
)
from database import Base 
from typing import List
from models.enums.enums import TipoNutriEcoScoreDB, TipoNovaScoreDB, TipoTagDB

class Produto(Base):
    __tablename__ = 'produto'

    codigo: Mapped[str] = mapped_column(String(255), primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    
    nutriscore: Mapped[TipoNutriEcoScoreDB] = mapped_column(
        SQLAlchemyEnum(TipoNutriEcoScoreDB, name="tipo_nutri_eco_score")
    )
    ecoscore: Mapped[TipoNutriEcoScoreDB] = mapped_column(
        SQLAlchemyEnum(TipoNutriEcoScoreDB, name="tipo_nutri_eco_score")
    )
    novascore: Mapped[TipoNovaScoreDB] = mapped_column(
        SQLAlchemyEnum(TipoNovaScoreDB, name="tipo_nova_score", values_callable=lambda x: [e.value for e in x])
    )

    produto_marcas: Mapped[List["ProdutoMarca"]] = relationship(
        "ProdutoMarca", back_populates="produto", cascade="all, delete-orphan"
    )
    produto_nutrientes: Mapped[List["ProdutoNutriente"]] = relationship(
        "ProdutoNutriente", back_populates="produto", cascade="all, delete-orphan"
    )
    produto_ingredientes: Mapped[List["ProdutoIngrediente"]] = relationship(
        "ProdutoIngrediente", back_populates="produto", cascade="all, delete-orphan"
    )
    produto_tags: Mapped[List["ProdutoTag"]] = relationship(
        "ProdutoTag", back_populates="produto", cascade="all, delete-orphan"
    )
    produto_categorias: Mapped[List["ProdutoCategoria"]] = relationship(
        "ProdutoCategoria", back_populates="produto", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "nutriscore": self.nutriscore.value if self.nutriscore else None,
            "ecoscore": self.ecoscore.value if self.ecoscore else None,
            "novascore": self.novascore.value if self.novascore else None,
            "produto_marcas": [marca.to_dict() for marca in self.produto_marcas] if self.produto_marcas else None,
            "produto_nutrientes": [nutriente.to_dict() for nutriente in self.produto_nutrientes] if self.produto_nutrientes else None,
            "produto_ingredientes": [ingrediente.to_dict() for ingrediente in self.produto_ingredientes] if self.produto_ingredientes else None,
            "produto_tags": [tag.to_dict() for tag in self.produto_tags] if self.produto_tags else None,
            "produto_categorias": [categoria.to_dict() for categoria in self.produto_categorias] if self.produto_categorias else None
        }


class Marca(Base):
    __tablename__ = 'marca'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    produto_marcas: Mapped[List["ProdutoMarca"]] = relationship("ProdutoMarca", back_populates="marca")

class Nutriente(Base):
    __tablename__ = 'nutriente'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    unidade: Mapped[str] = mapped_column(String(10), nullable=False)
    produto_nutrientes: Mapped[List["ProdutoNutriente"]] = relationship("ProdutoNutriente", back_populates="nutriente")

class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    vegano: Mapped[bool] = mapped_column(Boolean)
    vegetariano: Mapped[bool] = mapped_column(Boolean)
    produto_ingredientes: Mapped[List["ProdutoIngrediente"]] = relationship("ProdutoIngrediente", back_populates="ingrediente")

class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[TipoTagDB] = mapped_column(SQLAlchemyEnum(TipoTagDB, name='tipo_tag', create_type=False), nullable=False)
    produto_tags: Mapped[List["ProdutoTag"]] = relationship("ProdutoTag", back_populates="tag")
    __table_args__ = (UniqueConstraint('nome', 'tipo', name='uq_tag_nome_tipo'),)

class Categoria(Base):
    __tablename__ = 'categoria'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    produto_categorias: Mapped[List["ProdutoCategoria"]] = relationship("ProdutoCategoria", back_populates="categoria")

# Associações

class ProdutoMarca(Base):
    __tablename__ = 'produto_marca'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto_id: Mapped[str] = mapped_column(ForeignKey('produto.codigo', ondelete="CASCADE"), nullable=False)
    marca_id: Mapped[int] = mapped_column(ForeignKey('marca.id', ondelete="RESTRICT"), nullable=False)

    produto: Mapped["Produto"] = relationship("Produto", back_populates="produto_marcas")
    marca: Mapped["Marca"] = relationship("Marca", back_populates="produto_marcas")
    __table_args__ = (UniqueConstraint('produto_id', 'marca_id', name='uq_produto_marca'),)

    def to_dict(self):
        return {
            "produto_id": self.produto_id,
            "marca_id": self.marca_id
        }

class ProdutoNutriente(Base):
    __tablename__ = 'produto_nutriente'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto_id: Mapped[str] = mapped_column(ForeignKey('produto.codigo', ondelete="CASCADE"), nullable=False)
    nutriente_id: Mapped[int] = mapped_column(ForeignKey('nutriente.id', ondelete="RESTRICT"), nullable=False)
    quantidade_100g: Mapped[float] = mapped_column(DECIMAL(6,2))

    produto: Mapped["Produto"] = relationship("Produto", back_populates="produto_nutrientes")
    nutriente: Mapped["Nutriente"] = relationship("Nutriente", back_populates="produto_nutrientes")
    __table_args__ = (UniqueConstraint('produto_id', 'nutriente_id', name='uq_produto_nutriente'),)

    def to_dict(self):
        return {
            "produto_id": self.produto_id,
            "nutriente_id": self.nutriente_id,
            "quantidade_100g": self.quantidade_100g
        }

class ProdutoIngrediente(Base):
    __tablename__ = 'produto_ingrediente'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto_id: Mapped[str] = mapped_column(ForeignKey('produto.codigo', ondelete="CASCADE"), nullable=False)
    ingrediente_id: Mapped[int] = mapped_column(ForeignKey('ingrediente.id', ondelete="RESTRICT"), nullable=False)
    quantidade_estimada: Mapped[float] = mapped_column(DECIMAL(5,2))

    produto: Mapped["Produto"] = relationship("Produto", back_populates="produto_ingredientes")
    ingrediente: Mapped["Ingrediente"] = relationship("Ingrediente", back_populates="produto_ingredientes")
    __table_args__ = (UniqueConstraint('produto_id', 'ingrediente_id', name='uq_produto_ingrediente'),)

    def to_dict(self):
        return {
            "produto_id": self.produto_id,
            "ingrediente_id": self.ingrediente_id,
            "quantidade_estimada": self.quantidade_estimada
        }

class ProdutoTag(Base):
    __tablename__ = 'produto_tag'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto_id: Mapped[str] = mapped_column(ForeignKey('produto.codigo', ondelete="CASCADE"), nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tag.id', ondelete="RESTRICT"), nullable=False)

    produto: Mapped["Produto"] = relationship("Produto", back_populates="produto_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="produto_tags")
    __table_args__ = (UniqueConstraint('produto_id', 'tag_id', name='uq_produto_tag'),)

    def to_dict(self):
        return {
            "produto_id": self.produto_id,
            "tag_id": self.tag_id
        }

class ProdutoCategoria(Base):
    __tablename__ = 'produto_categoria'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto_id: Mapped[str] = mapped_column(ForeignKey('produto.codigo', ondelete="CASCADE"), nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categoria.id', ondelete="RESTRICT"), nullable=False)

    produto: Mapped["Produto"] = relationship("Produto", back_populates="produto_categorias")
    categoria: Mapped["Categoria"] = relationship("Categoria", back_populates="produto_categorias")
    __table_args__ = (UniqueConstraint('produto_id', 'categoria_id', name='uq_produto_categoria'),)

    def to_dict(self):
        return {
            "produto_id": self.produto_id,
            "categoria_id": self.categoria_id
        }