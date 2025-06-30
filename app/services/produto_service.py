from repositories.produto_repository import ProdutoRepository

class ProdutoService:
    def __init__(self, repo: ProdutoRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.get_all()
