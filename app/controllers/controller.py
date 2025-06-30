from flask import Blueprint, request, jsonify #type: ignore
from repositories.produto_repository import ProdutoRepository
from services.produto_service import ProdutoService
from database import getDBSession

prod = Blueprint('product', __name__)

@prod.route("/get-products", methods=["GET"])
def get_products():
    
    # next() é usado para pegar a instancia de Session necessária. Sem ele, retorna apenas o 'generator'
    db = next(getDBSession())
    product = ProdutoRepository(db)
    service = ProdutoService(product)

    product_list = service.get_all()

    if product_list:
        return jsonify([p.to_dict() for p in product_list]), 200 
    
    return jsonify('Erro ao retornar produtos'), 400

@prod.route("/get-result-filtered", method=["POST"])
def get_result_filtered():
    pass