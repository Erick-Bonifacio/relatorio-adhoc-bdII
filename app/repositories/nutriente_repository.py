from sqlalchemy.orm import Session
from models.model import Nutriente
from typing import List, Optional
from sqlalchemy import text

class NutrienteRepository:
    def __init__(self, db: Session):
        self.db = db
        self.TABLES = {
            "nutriente": Nutriente,
        }

    def get_all(self) -> List[Nutriente]:
        return self.db.query(Nutriente).all()

    def get_by_id(self, id: int) -> Optional[Nutriente]:
        return self.db.query(Nutriente).filter(Nutriente.id == id).first()

    def create(self, nutriente: Nutriente) -> Nutriente:
        self.db.add(nutriente)
        self.db.commit()
        self.db.refresh(nutriente)
        return nutriente

    def delete(self, id: int) -> None:
        nutriente = self.get_by_id(id)
        if nutriente:
            self.db.delete(nutriente)
            self.db.commit()

    def _resolve_column(self, col_str, val=None):
        table_name, col_name = col_str.split(".")
        model = self.TABLES[table_name]  # TABLES deve mapear nomes como "marca" -> Marca
        column = getattr(model, col_name)

        return column, val

    def get_filtered_nutriente(self, columns: List[str], filter: List[dict], limit: int = None, order_by: str = None):
        labeled_columns = []
        for col_str in columns:
            col, _ = self._resolve_column(col_str)
            labeled_columns.append(col.label(col_str))

        query = self.db.query(*labeled_columns)

        for f in filter:
            col = getattr(Nutriente, f['column'])
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