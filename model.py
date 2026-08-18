from dataclasses import dataclass
from typing import Optional


@dataclass
class Produto:
    nome: str
    categoria: str
    quantidade: int
    preco_custo: float
    preco_venda: float
    estoque_minimo: int = 5
    fornecedor: Optional[str] = None
    id: Optional[int] = None  

    def conferir_estoque_baixo(self) -> bool: ##Array dentro do banco para verificar se a quantidade do produto é menor ou igual ao estoque mínimo
        if self.quantidade <= self.estoque_minimo:
            print(f"Produto {self.nome} está com estoque baixo: {self.quantidade} unidades restantes.") 
        return self.quantidade <= self.estoque_minimo

    def valor_total_em_estoque(self) -> float:
        return self.quantidade * self.preco_custo


@dataclass
class Movimentacao:

    produto_id: int
    tipo: str  
    quantidade: int
    data: str
    observacao: Optional[str] = None
    id: Optional[int] = None