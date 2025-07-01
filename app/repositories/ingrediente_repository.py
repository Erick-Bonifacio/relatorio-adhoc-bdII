from sqlalchemy.orm import Session
from models.model import Ingrediente
from typing import List, Optional
from sqlalchemy import text

class IngredienteRepository:
    def __init__(self, db: Session):
        self.db = db
        self.TABLES = {
            "ingrediente": Ingrediente,
        }

    def get_all(self) -> List[Ingrediente]:
        return self.db.query(Ingrediente).all()

    def get_by_id(self, id: int) -> Optional[Ingrediente]:
        return self.db.query(Ingrediente).filter(Ingrediente.id == id).first()

    def create(self, ingrediente: Ingrediente) -> Ingrediente:
        self.db.add(ingrediente)
        self.db.commit()
        self.db.refresh(ingrediente)
        return ingrediente

    def delete(self, id: int) -> None:
        ingrediente = self.get_by_id(id)
        if ingrediente:
            self.db.delete(ingrediente)
            self.db.commit()

    def _resolve_column(self, col_str, val=None):
        table_name, col_name = col_str.split(".")
        model = self.TABLES[table_name]  # TABLES deve mapear nomes como "marca" -> Marca
        column = getattr(model, col_name)

        return column, val

    def get_filtered_ingrediente(self, columns: List[str], filter: List[dict], limit: int = None, order_by: str = None):
        labeled_columns = []
        for col_str in columns:
            col, _ = self._resolve_column(col_str)
            labeled_columns.append(col.label(col_str))

        query = self.db.query(*labeled_columns)


        for f in filter:
            col = getattr(Ingrediente, f['column'])
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