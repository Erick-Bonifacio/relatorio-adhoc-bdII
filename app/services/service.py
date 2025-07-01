from repositories.produto_repository import ProdutoRepository
from repositories.ingrediente_repository import IngredienteRepository
from repositories.marca_repository import MarcaRepository
from repositories.nutriente_repository import NutrienteRepository
from repositories.tag_repository import TagRepository
from repositories.categoria_repository import CategoriaRepository
from enum import Enum

class Service:
    def __init__(self, db):
        self.produto_repo = ProdutoRepository(db)
        self.ingrediente_repo = IngredienteRepository(db)
        self.marca_repo = MarcaRepository(db)
        self.nutriente_repo = NutrienteRepository(db)
        self.tag_repo = TagRepository(db)
        self.categoria_repo = CategoriaRepository(db)

    def get_all(self: str):
        return self.produto_repo.get_all()

    def get_filtered_produto(self, tables: list, columns: list, agregations: dict, filters: list, limit=None, order_by='ASC'):
        if 'produto' in tables:
            tables = [t for t in tables if t != 'produto']
        rows = self.produto_repo.get_filtered(tables, columns, agregations, filters, limit, order_by)
        # print(rows)
        return self.rows_to_dicts_product(rows, columns)

    def get_filtered_categoria(self, columns: list, filters: list, limit=None, order_by=None):
        rows = self.categoria_repo.get_filtered_categoria(columns, filters, limit, order_by)
        return self.rows_to_dicts(rows, columns)

    def get_filtered_ingrediente(self, columns: list, filters: list, limit=None, order_by=None):
        rows = self.ingrediente_repo.get_filtered_ingrediente(columns, filters, limit, order_by)
        return self.rows_to_dicts(rows, columns)

    def get_filtered_marca(self, columns: list, filters: list, limit=None, order_by=None):
        rows = self.marca_repo.get_filtered_marca(columns, filters, limit, order_by)
        return self.rows_to_dicts(rows, columns)

    def get_filtered_nutriente(self, columns: list, filters: list, limit=None, order_by=None):
        rows = self.nutriente_repo.get_filtered_nutriente(columns, filters, limit, order_by)
        return self.rows_to_dicts(rows, columns)

    def get_filtered_tag(self, columns: list, filters: list, limit=None, order_by=None):
        rows = self.tag_repo.get_filtered_tag(columns, filters, limit, order_by)
        return self.rows_to_dicts(rows, columns)

    @staticmethod
    def rows_to_dicts(rows, columns):
        result = []
        for row in rows:
            d = {}
            for col in columns:
                val = getattr(row, col, None)
                if isinstance(val, Enum):
                    d[col] = val.name  # ou val.value, dependendo do que prefere
                else:
                    d[col] = val
            result.append(d)
        return result

    @staticmethod
    def rows_to_dicts_product(rows, columns):
        result = []
        for row in rows:
            d = {}
            for col in columns:
                if col in row:
                    val = row[col]
                    if isinstance(val, Enum):
                        d[col] = val.name  # ou val.value, conforme preferir
                    else:
                        d[col] = val
                # Se col não está na dict, não adiciona nada (ou pode colocar None)
            result.append(d)
        return result