import sqlite3


class SistemaEstoque:
    def __init__(self, db_name="estoque.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL
            )
        ''')
        self.conn.commit()

    
    def adicionar_produto(self, nome, quantidade, preco):
        self.cursor.execute('''
            INSERT INTO produtos (nome, quantidade, preco)
            VALUES (?, ?, ?)
        ''', (nome, quantidade, preco))
        self.conn.commit()
        print(f"Produto '{nome}' adicionado com sucesso!")

    def listar_produtos(self):
        self.cursor.execute('SELECT * FROM produtos')
        produtos = self.cursor.fetchall()
        
        if not produtos:
            print("\nEstoque vazio.")
            return

        print("\n--- ESTOQUE ATUAL ---")
        print(f"{'ID':<5} | {'Nome':<20} | {'Qtd':<8} | {'Preço (R$)':<10}")
        print("-" * 50)
        for prod in produtos:
            print(f"{prod[0]:<5} | {prod[1]:<20} | {prod[2]:<8} | R$ {prod[3]:<10.2f}")
        print("-" * 50)

    
    def atualizar_produto(self, id_produto, nova_qtd=None, novo_preco=None):
        if nova_qtd is not None:
            self.cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_qtd, id_produto))
        if novo_preco is not None:
            self.cursor.execute('UPDATE produtos SET preco = ? WHERE id = ?', (novo_preco, id_produto))
        
        self.conn.commit()
        print(f"Produto ID {id_produto} atualizado.")

   
    def deletar_produto(self, id_produto):
        self.cursor.execute('DELETE FROM produtos WHERE id = ?', (id_produto,))
        self.conn.commit()
        print(f"Produto ID {id_produto} removido do estoque.")

    def fechar_conexao(self):
        self.conn.close()