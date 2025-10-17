# -*- coding: utf-8 -*-

import socket
import threading
from collections import deque
import pyperclip # Biblioteca para interagir com a área de transferência

# --- Configurações do Servidor ---
HOST = '0.0.0.0'  # Escuta em todas as interfaces de rede disponíveis
PORT = 65432      # Porta para escutar
MAX_HISTORY_SIZE = 5

# --- Estrutura de Dados para o Histórico ---
# Usamos um deque com tamanho máximo para manter automaticamente apenas os últimos 5 itens.
clipboard_history = deque(maxlen=MAX_HISTORY_SIZE)

# Função para lidar com a conexão de cada cliente em uma thread separada
def handle_client(conn, addr):
    """
    Recebe os dados do cliente e os adiciona ao histórico da área de transferência.
    """
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    try:
        while True:
            # Espera receber dados do cliente (até 1024 bytes)
            data = conn.recv(1024)
            if not data:
                # Se não receber dados, o cliente desconectou
                break
            
            decoded_data = data.decode('utf-8')
            print(f"\n[DADO RECEBIDO] Recebido de {addr}: \"{decoded_data}\"")
            
            # Adiciona o texto recebido ao nosso histórico
            clipboard_history.append(decoded_data)
            
            print(f"[HISTÓRICO ATUALIZADO] O histórico agora contém {len(clipboard_history)} item(ns).")
            print(">>> Digite 'listar' para ver o histórico ou 'colar <numero>' para copiar um item.")
            
    except ConnectionResetError:
        print(f"[CONEXÃO PERDIDA] A conexão com {addr} foi perdida.")
    finally:
        print(f"[CONEXÃO ENCERRADA] {addr} desconectou.")
        conn.close()

# Função para a interface de usuário do servidor (rodará em sua própria thread)
def server_ui():
    """
    Permite que o administrador do servidor visualize o histórico e copie itens para a área de transferência local.
    """
    print("\n--- Interface do Servidor ---")
    print("Comandos disponíveis:")
    print("  listar      - Mostra o histórico dos últimos 5 itens copiados pelo cliente.")
    print("  colar <num> - Copia o item de número <num> para a área de transferência do servidor.")
    print("  sair        - Encerra o servidor.")
    
    while True:
        try:
            cmd = input(">>> ").strip().lower()
            
            if cmd == 'listar':
                if not clipboard_history:
                    print("[HISTÓRICO] O histórico está vazio.")
                else:
                    print("\n--- Histórico da Área de Transferência ---")
                    # Itera de forma reversa para mostrar o mais recente primeiro
                    for i, item in enumerate(reversed(clipboard_history)):
                        print(f"  {i + 1}: {item}")
                    print("-----------------------------------------")

            elif cmd.startswith('colar '):
                try:
                    # Pega o número depois de 'colar '
                    index = int(cmd.split(' ')[1])
                    if 1 <= index <= len(clipboard_history):
                        # Índices da lista reversa
                        item_to_copy = list(reversed(clipboard_history))[index - 1]
                        pyperclip.copy(item_to_copy)
                        print(f"[SUCESSO] Item {index} (\"{item_to_copy}\") copiado para a área de transferência do servidor!")
                    else:
                        print(f"[ERRO] Número inválido. Por favor, escolha um número entre 1 e {len(clipboard_history)}.")
                except (ValueError, IndexError):
                    print("[ERRO] Comando inválido. Use 'colar <numero>', ex: 'colar 1'.")
            
            elif cmd == 'sair':
                print("[ENCERRANDO] O servidor será desligado.")
                # Em uma aplicação real, teríamos uma forma mais elegante de fechar as conexões.
                # Para este exemplo, vamos simplesmente encerrar o processo.
                import os
                os._exit(0)

            else:
                if cmd: # Evita mensagem de erro para input vazio
                    print(f"[ERRO] Comando '{cmd}' não reconhecido.")

        except (KeyboardInterrupt, EOFError):
             print("\n[ENCERRANDO] O servidor foi interrompido.")
             import os
             os._exit(0)


# Função principal para iniciar o servidor
def start_server():
    """
    Inicia o servidor, a interface de usuário e aguarda por conexões de clientes.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # A opção SO_REUSEADDR permite que o servidor reinicie e use a mesma porta rapidamente
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[ESCUTANDO] Servidor escutando em {HOST}:{PORT}")

    # Inicia a thread da interface do servidor
    ui_thread = threading.Thread(target=server_ui, daemon=True)
    ui_thread.start()

    while True:
        # Aceita uma nova conexão
        conn, addr = server_socket.accept()
        # Cria e inicia uma nova thread para lidar com o cliente recém-conectado
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()