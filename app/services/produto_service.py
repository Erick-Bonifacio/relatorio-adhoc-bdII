from repositories.produto_repository import ProdutoRepository

class ProdutoService:
    def __init__(self, repo: ProdutoRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.get_all()

    def get_filtered(self, tables :list, columns :list, agregations :dict, filters :list): 
        # preparing data
        tables.remove('produto')

        res = self.repo.get_filtered(tables, columns, agregations, filters)

        if res == []:
            return False
        
        return res