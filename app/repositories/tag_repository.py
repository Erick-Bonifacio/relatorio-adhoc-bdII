from sqlalchemy.orm import Session
from models.model import Tag
from models.enums.enums import TipoTagDB
from typing import List, Optional
from sqlalchemy import text

class TagRepository:
    def __init__(self, db: Session):
        self.db = db
        self.TABLES = {
            "tag": Tag,
        }
        self.ENUMS_MAP = {
            "tag": TipoTagDB
        }

    def get_all(self) -> List[Tag]:
        return self.db.query(Tag).all()

    def get_by_id(self, id: int) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.id == id).first()

    def create(self, tag: Tag) -> Tag:
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def delete(self, id: int) -> None:
        tag = self.get_by_id(id)
        if tag:
            self.db.delete(tag)
            self.db.commit()

    def _resolve_column(self, col_str, val=None):
        table_name, col_name = col_str.split(".")
        model = self.TABLES[table_name]  # TABLES deve mapear nomes como "marca" -> Marca
        column = getattr(model, col_name)

        # Exemplo para Enums, se precisar
        if col_str in self.ENUMS_MAP:
            enum_class = self.ENUMS_MAP[col_str]
            try:
                val = enum_class[val]
            except KeyError:
                raise ValueError(f"Valor '{val}' inválido para Enum '{enum_class.__name__}'")

        return column, val

    def get_filtered_tag(self, columns: List[str], filter: List[dict], limit: int = None, order_by: str = None):
        labeled_columns = []
        for col_str in columns:
            col, _ = self._resolve_column(col_str)
            labeled_columns.append(col.label(col_str))

        query = self.db.query(*labeled_columns)

        for f in filter:
            col = getattr(Tag, f['column'])
            op = f['operator'].lower()
            val = f['value']

            if op == '=':
                query = query.filter(col == val)
            elif op == '!=':
                query = query.filter(col != val)
            elif op == '>':
                query = query.filter(col > val)
            elif op == '<':
                query = query.filter(col < val)
            elif op == 'like':
                query = query.filter(col.like(f"%{val}%"))
            else:
                raise ValueError(f"Operador inválido: {op}")

        if order_by:
            query = query.order_by(text(order_by))

        if limit:
            query = query.limit(limit)

        return query.all()