from sqlalchemy.orm import Session
from models.model import Categoria
from typing import List, Optional
from sqlalchemy import text

class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db
        self.TABLES = {
            "categoria": Categoria,
        }

    def get_all(self) -> List[Categoria]:
        return self.db.query(Categoria).all()

    def get_by_id(self, id: int) -> Optional[Categoria]:
        return self.db.query(Categoria).filter(Categoria.id == id).first()

    def create(self, categoria: Categoria) -> Categoria:
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def delete(self, id: int) -> None:
        categoria = self.get_by_id(id)
        if categoria:
            self.db.delete(categoria)
            self.db.commit()

    def _resolve_column(self, col_str, val=None):
        table_name, col_name = col_str.split(".")
        model = self.TABLES[table_name]
        column = getattr(model, col_name)

        return column, val


    def get_filtered_categoria(self, columns: List[str], filter: List[dict], limit: int = None, order_by: str = None):
        # Resolve e label as colunas corretamente
        labeled_columns = []
        for col_str in columns:
            col, _ = self._resolve_column(col_str)
            labeled_columns.append(col.label(col_str))

        query = self.db.query(*labeled_columns)

        for f in filter:
            col, val = self._resolve_column(f['campo'], f['valor'])
            op = f['operador'].lower()

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
