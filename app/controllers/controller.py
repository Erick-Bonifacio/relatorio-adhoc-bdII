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
    
    return jsonify('Internal error in solving your request'), 400

@prod.route("/get-result-filtered", methods=["POST"])
def get_result_filtered():
    db = next(getDBSession())

    data = request.json
    tables = data.get('tables')
    columns = data.get('columns')
    agregations = data.get('agregations')
    filters = data.get('filters')

    if not tables  or not filters:
        return jsonify('Missing required fields'), 400
    
    # Se tiver a tabela produtos, será usada como principal
    if 'produto' in tables:
        product = ProdutoRepository(db)
        prodService = ProdutoService(product)
        res = prodService.get_filtered(tables, columns, agregations, filters) 
        if res:
            return jsonify(res), 200
        return jsonify('Erro ao filtrar dados'), 400
    return jsonify('Erro ao filtrar dados'), 400

    

