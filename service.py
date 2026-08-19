
from datetime import datetime
from typing import List, Optional

import repository
from model import Produto, Movimentacao


class EstoqueError(Exception):
    pass


def cadastrar_produto(nome: str, categoria: str, quantidade: int,
                       preco_custo: float, preco_venda: float,
                       estoque_minimo: int = 5, fornecedor: Optional[str] = None) -> Produto:
    if not nome.strip():
        raise EstoqueError("O nome do produto não pode ser vazio.")
    if quantidade < 0:
        raise EstoqueError("A quantidade não pode ser negativa.")
    if preco_custo < 0 or preco_venda < 0:
        raise EstoqueError("Os preços não podem ser negativos.")

    produto = Produto(
        nome=nome.strip(),
        categoria=categoria.strip(),
        quantidade=quantidade,
        preco_custo=preco_custo,
        preco_venda=preco_venda,
        estoque_minimo=estoque_minimo,
        fornecedor=fornecedor,
    )
    produto.id = repository.salvar_produto(produto)

    if quantidade > 0:
        _registrar_movimentacao(produto.id, "ENTRADA", quantidade, "Estoque inicial")

    return produto


def listar_produtos() -> List[Produto]:
    return repository.listar_produtos()


def buscar_produtos(termo: str) -> List[Produto]:
    return repository.buscar_produtos_por_nome(termo)


def atualizar_produto(produto: Produto) -> None:
    repository.atualizar_produto(produto)


def remover_produto(produto_id: int) -> None:
    repository.remover_produto(produto_id)


def registrar_entrada(produto_id: int, quantidade: int, observacao: str = "") -> Produto:
    if quantidade <= 0:
        raise EstoqueError("A quantidade de entrada deve ser maior que zero.")

    produto = repository.buscar_produto_por_id(produto_id)
    if produto is None:
        raise EstoqueError("Produto não encontrado.")

    produto.quantidade += quantidade
    repository.atualizar_produto(produto)
    _registrar_movimentacao(produto_id, "ENTRADA", quantidade, observacao)
    return produto


def registrar_saida(produto_id: int, quantidade: int, observacao: str = "") -> Produto:

    if quantidade <= 0:
        raise EstoqueError("A quantidade de saída deve ser maior que zero.")

    produto = repository.buscar_produto_por_id(produto_id)
    if produto is None:
        raise EstoqueError("Produto não encontrado.")

    if quantidade > produto.quantidade:
        raise EstoqueError(
            f"Estoque insuficiente. Disponível: {produto.quantidade}, solicitado: {quantidade}."
        )

    produto.quantidade -= quantidade
    repository.atualizar_produto(produto)
    _registrar_movimentacao(produto_id, "SAIDA", quantidade, observacao)
    return produto


def historico_do_produto(produto_id: int) -> List[Movimentacao]:
    return repository.listar_movimentacoes_por_produto(produto_id)


def produtos_com_estoque_baixo() -> List[Produto]:
    return [p for p in repository.listar_produtos() if p.esta_com_estoque_baixo()]


def valor_total_do_estoque() -> float:
    return sum(p.valor_total_em_estoque() for p in repository.listar_produtos())


def _registrar_movimentacao(produto_id: int, tipo: str, quantidade: int, observacao: str) -> None:
    
    mov = Movimentacao(
        produto_id=produto_id,
        tipo=tipo,
        quantidade=quantidade,
        data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        observacao=observacao,
    )
    repository.salvar_movimentacao(mov)