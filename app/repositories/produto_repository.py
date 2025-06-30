from sqlalchemy.orm import Session #type: ignore
from models.model import Produto
from typing import List, Optional


class ProdutoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Produto]:
        return self.db.query(Produto).all()

    def get_by_codigo(self, codigo: str) -> Optional[Produto]:
        return self.db.query(Produto).filter(Produto.codigo == codigo).first()

    def create(self, produto: Produto) -> Produto:
        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def update(self, codigo: str, data: dict) -> Optional[Produto]:
        produto = self.get_by_codigo(codigo)
        if not produto:
            return None
        for key, value in data.items():
            setattr(produto, key, value)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def delete(self, codigo: str) -> bool:
        produto = self.get_by_codigo(codigo)
        if not produto:
            return False
        self.db.delete(produto)
        self.db.commit()
        return True

