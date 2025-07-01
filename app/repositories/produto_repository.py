from sqlalchemy.orm import Session, aliased #type: ignore
from models.model import Produto, Categoria, ProdutoCategoria, Ingrediente, ProdutoIngrediente, Nutriente, Marca, Tag, ProdutoMarca, ProdutoNutriente, ProdutoTag
from models.enums.enums import TipoNovaScoreDB, TipoNutriEcoScoreDB, TipoTagDB
from typing import List, Optional
from sqlalchemy import select, join, func, and_, or_ , join, Enum as SQLAlchemyEnum #type: ignore
class ProdutoRepository:
    def __init__(self, db: Session):
        self.db = db
        self.TABLES = {
            "produto": Produto,
            "categoria": Categoria,
            "ingrediente": Ingrediente,
            "nutriente": Nutriente,
            "marca": Marca,
            "tag": Tag,
        }
        self.JOINS_MAP = {
            ("produto", "categoria"): lambda base, target: join(
                join(base, ProdutoCategoria, Produto.codigo == ProdutoCategoria.produto_id),
                Categoria, ProdutoCategoria.categoria_id == Categoria.id
            ),
            ("produto", "ingrediente"): lambda base, target: join(
                join(base, ProdutoIngrediente, Produto.codigo == ProdutoIngrediente.produto_id),
                Ingrediente, ProdutoIngrediente.ingrediente_id == Ingrediente.id
            ),
            ("produto", "marca"): lambda base, target: join(
                join(base, ProdutoMarca, Produto.codigo == ProdutoMarca.produto_id),
                Marca, ProdutoMarca.marca_id == Marca.id
            ),
            ("produto", "nutriente"): lambda base, target: join(
                join(base, ProdutoNutriente, Produto.codigo == ProdutoNutriente.produto_id),
                Nutriente, ProdutoNutriente.nutriente_id == Nutriente.id
            ),
            ("produto", "tag"): lambda base, target: join(
                join(base, ProdutoTag, Produto.codigo == ProdutoTag.produto_id),
                Tag, ProdutoTag.tag_id == Tag.id
            ),
        }
        self.ENUMS_MAP = {
            "novascore": TipoNovaScoreDB,
            "nutriecostore": TipoNutriEcoScoreDB,
            "tag": TipoTagDB
        }


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

    def get_filtered(self, tables: list, columns: list, aggregations: dict, filters: list, limit, order_by):
        base_table = Produto
        stmt = select()

        # --- Colunas selecionadas ---
        col_objs = []
        if columns:
            for col_str in columns:
                try:
                    col, val = self._resolve_column(col_str)
                    col_objs.append(col.label(col_str))
                except Exception as e:
                    raise Exception(f"[WARN] Coluna inválida '{col_str}': {e}")

        stmt = stmt.add_columns(*col_objs)

        # --- Agregações ---
        if len(aggregations) > 0:
            agg_objs = []
            for alias, agg_data in aggregations.items():
                func_name, col_str = agg_data
                column, val = self._resolve_column(col_str)
                aggregation = getattr(func, func_name)(column).label(alias)
                agg_objs.append(aggregation)
            stmt = stmt.add_columns(*agg_objs)

        # --- Joins ---
        current_join = base_table
        for table_name in tables:
            if table_name == base_table.__tablename__:
                continue  # evita tentar join com ele mesmo
            target_model = self.TABLES.get(table_name)
            if not target_model:
                raise ValueError(f"Tabela '{table_name}' não encontrada em TABLES.")

            join_key = (base_table.__tablename__, table_name)
            if join_key in self.JOINS_MAP:
                current_join = self.JOINS_MAP[join_key](current_join, target_model)
            else:
                # Se não tiver join explícito, tenta direto (risco se não tiver FK mapeada)
                current_join = current_join.join(target_model)

        stmt = stmt.select_from(current_join)

        # --- Filtros ---
        if filters:
            stmt = stmt.where(self._build_filter_expression(filters))

        # --- Agrupamento ---
        if aggregations and col_objs:
            stmt = stmt.group_by(*col_objs)

        # --- ORDER BY ---
        if order_by:
            try:
                col, _ = self._resolve_column(order_by)
                stmt = stmt.order_by(col)
            except Exception as e:
                raise Exception(f"[WARN] ORDER BY inválido '{order_by}': {e}")

        # --- LIMIT ---
        if limit is not None:
            stmt = stmt.limit(limit)


        # --- Execução ---
        try:
            result = self.db.execute(stmt)
            rows = result.mappings().all()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"[ERRO get_filtered]: {e}")
            return False



    def _resolve_column(self, col_str, val = None):
        table_name, col_name = col_str.split(".")
        model = self.TABLES[table_name]
        column = getattr(model, col_name)

        # Resolve o valor se for Enum
        if col_str in self.ENUMS_MAP:
            enum_class = self.ENUMS_MAP[col_str]
            try:
                val = enum_class[val]
            except KeyError:
                raise ValueError(f"Valor '{val}' inválido para Enum '{enum_class.__name__}'")

        return column, val

    def _resolve_filter(self, filter):
        op = filter["operator"]
        raw_val = filter["value"]
        col_str = filter["column"]

        col, val = self._resolve_column(col_str, raw_val)

        if isinstance(col.type, SQLAlchemyEnum):
            try:
                enum_class = col.type.enum_class
                val = enum_class[val]  # converte a string para Enum
            except Exception as e:
                raise ValueError(f"[Enum] Valor '{val}' inválido para enum {enum_class}: {e}")

        if op == "=":
            return col == val
        elif op == ">":
            return col > val
        elif op == "<":
            return col < val
        elif op == "like":
            return col.like(val)
        elif op == "ilike":
            return col.ilike(val)
        else:
            raise ValueError(f"Operador não suportado: {op}")

    # def _build_filter_expression(self, filter_block):
    #     if "logic" in filter_block:
    #         logic_op = filter_block["logic"].lower()
    #         filters = [self._build_filter_expression(f) for f in filter_block["filters"]]

    #         if logic_op == "and":
    #             return and_(*filters)
    #         elif logic_op == "or":
    #             return or_(*filters)
    #         else:
    #             raise ValueError(f"Operador lógico não suportado: {logic_op}")
    #     else:
    #         return self._resolve_filter(filter_block)

    def _build_filter_expression(self, filters):
        if not filters:
            return None

        expr = self._resolve_filter(filters[0])  # primeiro filtro não depende de lógica

        for f in filters[1:]:
            logic_op = f.get("logic", "and").lower()  # padrão AND se não vier
            next_expr = self._resolve_filter(f)

            if logic_op == "and":
                expr = and_(expr, next_expr)
            elif logic_op == "or":
                expr = or_(expr, next_expr)
            else:
                raise ValueError(f"Operador lógico não suportado: {logic_op}")

        return expr