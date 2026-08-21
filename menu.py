import services
from services import EstoqueError


def exibir_menu() -> None:
    print("\n===== CHAVERIA - GESTÃO DE ESTOQUE =====")
    print("1. Cadastrar produto")
    print("2. Listar produtos")
    print("3. Buscar produto por nome")
    print("4. Registrar entrada de estoque")
    print("5. Registrar saída de estoque (venda)")
    print("6. Ver histórico de um produto")
    print("7. Relatório de estoque baixo")
    print("8. Ver valor total do estoque")
    print("9. Remover produto")
    print("0. Sair")


def ler_inteiro(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Por favor, digite um número inteiro válido.")


def ler_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Por favor, digite um valor numérico válido (ex: 12.50).")


def opcao_cadastrar_produto() -> None:
    print("\n--- Cadastro de novo produto ---")
    nome = input("Nome do produto: ")
    categoria = input("Categoria (ex: Chaves, Cadeados, Fechaduras, Controles): ")
    quantidade = ler_inteiro("Quantidade inicial em estoque: ")
    preco_custo = ler_float("Preço de custo: R$ ")
    preco_venda = ler_float("Preço de venda: R$ ")
    estoque_minimo = ler_inteiro("Estoque mínimo (alerta): ")
    fornecedor = input("Fornecedor (opcional, ENTER para pular): ") or None

    try:
        produto = services.cadastrar_produto(
            nome, categoria, quantidade, preco_custo, preco_venda, estoque_minimo, fornecedor
        )
        print(f"\nProduto '{produto.nome}' cadastrado com sucesso! (ID {produto.id})")
    except EstoqueError as erro:
        print(f"\nErro ao cadastrar: {erro}")


def opcao_listar_produtos() -> None:
    produtos = services.listar_produtos()
    _imprimir_tabela_produtos(produtos)


def opcao_buscar_produto() -> None:
    termo = input("Digite parte do nome do produto: ")
    produtos = services.buscar_produtos(termo)
    _imprimir_tabela_produtos(produtos)


def opcao_registrar_entrada() -> None:
    produto_id = ler_inteiro("ID do produto: ")
    quantidade = ler_inteiro("Quantidade que está entrando: ")
    observacao = input("Observação (opcional): ")
    try:
        produto = services.registrar_entrada(produto_id, quantidade, observacao)
        print(f"Entrada registrada. Novo estoque de '{produto.nome}': {produto.quantidade}")
    except EstoqueError as erro:
        print(f"Erro: {erro}")


def opcao_registrar_saida() -> None:
    produto_id = ler_inteiro("ID do produto: ")
    quantidade = ler_inteiro("Quantidade que está saindo (venda): ")
    observacao = input("Observação (opcional): ")
    try:
        produto = services.registrar_saida(produto_id, quantidade, observacao)
        print(f"Saída registrada. Novo estoque de '{produto.nome}': {produto.quantidade}")
    except EstoqueError as erro:
        print(f"Erro: {erro}")


def opcao_historico_produto() -> None:
    produto_id = ler_inteiro("ID do produto: ")
    movimentacoes = services.historico_do_produto(produto_id)
    if not movimentacoes:
        print("Nenhuma movimentação encontrada para esse produto.")
        return
    print(f"\n{'Data':<20}{'Tipo':<10}{'Quantidade':<12}Observação")
    print("-" * 60)
    for mov in movimentacoes:
        print(f"{mov.data:<20}{mov.tipo:<10}{mov.quantidade:<12}{mov.observacao or ''}")


def opcao_relatorio_estoque_baixo() -> None:
    produtos = services.produtos_com_estoque_baixo()
    if not produtos:
        print("\nNenhum produto está com estoque baixo. Tudo certo!")
        return
    print("\n--- PRODUTOS COM ESTOQUE BAIXO ---")
    _imprimir_tabela_produtos(produtos)


def opcao_valor_total_estoque() -> None:
    total = services.valor_total_do_estoque()
    print(f"\nValor total do estoque (baseado no preço de custo): R$ {total:.2f}")


def opcao_remover_produto() -> None:
    produto_id = ler_inteiro("ID do produto a remover: ")
    confirmacao = input("Tem certeza? Essa ação não pode ser desfeita (s/n): ")
    if confirmacao.lower() == "s":
        services.remover_produto(produto_id)
        print("Produto removido.")
    else:
        print("Operação cancelada.")


def _imprimir_tabela_produtos(produtos) -> None:
    if not produtos:
        print("\nNenhum produto encontrado.")
        return
    print(f"\n{'ID':<5}{'Nome':<25}{'Categoria':<15}{'Qtd':<6}{'Preço Venda':<12}")
    print("-" * 65)
    for p in produtos:
        alerta = " (!)" if p.esta_com_estoque_baixo() else ""
        print(f"{p.id:<5}{p.nome:<25}{p.categoria:<15}{p.quantidade:<6}R$ {p.preco_venda:<9.2f}{alerta}")


ACOES = {
    "1": opcao_cadastrar_produto,
    "2": opcao_listar_produtos,
    "3": opcao_buscar_produto,
    "4": opcao_registrar_entrada,
    "5": opcao_registrar_saida,
    "6": opcao_historico_produto,
    "7": opcao_relatorio_estoque_baixo,
    "8": opcao_valor_total_estoque,
    "9": opcao_remover_produto,
}


def iniciar() -> None:
    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("\nAté logo!")
            break

        acao = ACOES.get(escolha)
        if acao:
            acao()
        else:
            print("Opção inválida. Tente novamente.")