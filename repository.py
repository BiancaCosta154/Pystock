from typing import List, Optional

from database import conectar
from model import Produto, Movimentacao


def salvar_produto(produto: Produto) -> int:
    """Insere um novo produto no banco e retorna o id gerado."""
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO produtos (nome, categoria, quantidade, preco_custo, preco_venda, estoque_minimo, fornecedor)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (produto.nome, produto.categoria, produto.quantidade, produto.preco_custo,
          produto.preco_venda, produto.estoque_minimo, produto.fornecedor))
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id


def listar_produtos() -> List[Produto]:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, categoria, quantidade, preco_custo, preco_venda, estoque_minimo, fornecedor
        FROM produtos ORDER BY nome
    """)
    linhas = cursor.fetchall()
    conexao.close()
    return [_linha_para_produto(linha) for linha in linhas]


def buscar_produto_por_id(produto_id: int) -> Optional[Produto]:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, categoria, quantidade, preco_custo, preco_venda, estoque_minimo, fornecedor
        FROM produtos WHERE id = ?
    """, (produto_id,))
    linha = cursor.fetchone()
    conexao.close()
    return _linha_para_produto(linha) if linha else None


def buscar_produtos_por_nome(termo: str) -> List[Produto]:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, categoria, quantidade, preco_custo, preco_venda, estoque_minimo, fornecedor
        FROM produtos WHERE nome LIKE ? ORDER BY nome
    """, (f"%{termo}%",))
    linhas = cursor.fetchall()
    conexao.close()
    return [_linha_para_produto(linha) for linha in linhas]


def atualizar_produto(produto: Produto) -> None:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE produtos
        SET nome = ?, categoria = ?, quantidade = ?, preco_custo = ?,
            preco_venda = ?, estoque_minimo = ?, fornecedor = ?
        WHERE id = ?
    """, (produto.nome, produto.categoria, produto.quantidade, produto.preco_custo,
          produto.preco_venda, produto.estoque_minimo, produto.fornecedor, produto.id))
    conexao.commit()
    conexao.close()


def remover_produto(produto_id: int) -> None:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conexao.commit()
    conexao.close()


def _linha_para_produto(linha) -> Produto:
    return Produto(
        id=linha[0],
        nome=linha[1],
        categoria=linha[2],
        quantidade=linha[3],
        preco_custo=linha[4],
        preco_venda=linha[5],
        estoque_minimo=linha[6],
        fornecedor=linha[7],
    )


def salvar_movimentacao(mov: Movimentacao) -> int:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, data, observacao)
        VALUES (?, ?, ?, ?, ?)
    """, (mov.produto_id, mov.tipo, mov.quantidade, mov.data, mov.observacao))
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id


def listar_movimentacoes_por_produto(produto_id: int) -> List[Movimentacao]:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, produto_id, tipo, quantidade, data, observacao
        FROM movimentacoes WHERE produto_id = ? ORDER BY data DESC, id DESC
    """, (produto_id,))
    linhas = cursor.fetchall()
    conexao.close()
    return [
        Movimentacao(id=l[0], produto_id=l[1], tipo=l[2], quantidade=l[3], data=l[4], observacao=l[5])
        for l in linhas
    ]