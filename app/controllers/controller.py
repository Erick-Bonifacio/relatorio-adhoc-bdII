from flask import Blueprint, request, jsonify #type: ignore
from repositories.produto_repository import ProdutoRepository
from services.service import Service
from database import getDBSession

prod = Blueprint('product', __name__)

@prod.route("/get-products", methods=["GET"])
def get_products():
    
    # next() é usado para pegar a instancia de Session necessária. Sem ele, retorna apenas o 'generator'
    db = next(getDBSession())
    service = Service(db)

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
    aggregations = data.get('aggregations')
    filters = data.get('filters')
    limit = data.get('limit')
    order_by = data.get('orderBy')

    db = next(getDBSession())
    service = Service(db)
    # Se tiver a tabela produtos, será usada como principal
    if 'produto' in tables:
        res = service.get_filtered_produto(tables, columns, aggregations, filters, limit, order_by) 
        if res:
            return jsonify(res), 200
        if isinstance(res, list):
            return jsonify('No data found'), 201
        return jsonify('Erro ao filtrar dados'), 400

    #se nao, estamos mexendo apenas com uma tabela, logo não haverá joins
    else:
        table = tables[0]
        filter_data = filters

        if table == 'categoria':
            res = service.get_filtered_categoria(columns, filter_data, limit, order_by)
        elif table == 'ingrediente':
            res = service.get_filtered_ingrediente(columns, filter_data, limit, order_by)
        elif table == 'marca':
            res = service.get_filtered_marca(columns, filter_data, limit, order_by)
        elif table == 'nutriente':
            res = service.get_filtered_nutriente(columns, filter_data, limit, order_by)
        elif table == 'tag':
            res = service.get_filtered_tag(columns, filter_data, limit, order_by)
        else:
            return jsonify('Tabela não suportada para filtro direto'), 401

        return jsonify(res), 200 if res else 201


