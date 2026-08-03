import uuid

from typing import Optional

from sqlmodel import SQLModel, Field


class ProdutoBase(SQLModel):
    """ Classe base de um produto para ser reutilizada na API """

    cod_prod: str = Field(nullable=False, index=True, max_length=15)
    # Python float  funciona como umm ddube
    preco_custo: float = Field(nullable=False)
    preco_venda: float = Field(nullable=False)
    quant_estoque: int = Field(nullable=False)
    saidas: int = Field()
    saidas_commbo: int = Field()


class Produto(ProdutoBase, table=True):
    """ Classe que vila tabela no banco de dados (só tem uuid, pois os outros campos vêm por herança) """

    prod_id: Optional[uuid] = Field(default=None, primary_key=True)
