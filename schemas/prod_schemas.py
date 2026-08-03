import uuid

from models.produtos import ProdutoBase

from typing import Optional


class ProdutosCreate(ProdutoBase):
    """ Schema para criar um produto """

    cod_prod: str
    preco_custo: float
    preco_venda: float
    quant_estoque: int
    saidas: int
    saidas_commbo: int


class ProdutosPublic(ProdutoBase):
    """ Schema público para expor dados na API """

    prod_id: uuid
    cod_prod: str
    preco_custo: float
    preco_venda: float
    quant_estoque: int
    saidas: int
    saidas_commbo: int


class ProdutosUpdate(ProdutoBase):
    """ Schema para atualizar produtos """

    cod_prod: Optional[str]
    preco_custo: Optional[float]
    preco_venda: Optional[float]
    quant_estoque: Optional[int]
    saidas: Optional[int]
    saidas_commbo: Optional[int]

