# -*- coding: utf-8 -*-

import socket
import pyperclip # Biblioteca para interagir com a área de transferência
import time

# --- Configurações do Cliente ---
SERVER_HOST = '127.0.0.1'  # Altere para o IP do servidor se estiver em outra máquina
SERVER_PORT = 65432

def connect_to_server():
    """
    Tenta se conectar ao servidor. Se a conexão falhar, tenta novamente a cada 5 segundos.
    """
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"[CONECTADO] Conectado com sucesso ao servidor em {SERVER_HOST}:{SERVER_PORT}")
            return client_socket
        except ConnectionRefusedError:
            print(f"[ERRO] Conexão recusada. O servidor está offline? Tentando novamente em 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f"[ERRO INESPERADO] Ocorreu um erro: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)


def monitor_clipboard_and_send():
    """
    Monitora a área de transferência. Quando um novo texto é copiado, ele o envia para o servidor.
    """
    client_socket = connect_to_server()
    recent_value = ""

    print("\n[MONITORANDO] Monitorando a área de transferência para alterações de texto...")
    print("Copie qualquer texto (Ctrl+C) para enviá-lo ao servidor.")

    try:
        while True:
            # Pega o conteúdo atual da área de transferência
            clipboard_content = pyperclip.paste()

            # Verifica se o conteúdo é texto e se é diferente do último valor enviado
            if isinstance(clipboard_content, str) and clipboard_content != recent_value:
                recent_value = clipboard_content
                print(f"[NOVO TEXTO COPIADO] Enviando: \"{clipboard_content}\"")
                
                try:
                    # Envia o conteúdo codificado em UTF-8 para o servidor
                    client_socket.sendall(clipboard_content.encode('utf-8'))
                except (ConnectionResetError, BrokenPipeError):
                    print("[CONEXÃO PERDIDA] A conexão com o servidor foi perdida. Tentando reconectar...")
                    client_socket.close()
                    client_socket = connect_to_server()
                    # Tenta reenviar o último valor após reconectar
                    client_socket.sendall(clipboard_content.encode('utf-8'))


            # Espera um pouco antes de verificar novamente para não sobrecarregar o processador
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Cliente encerrado.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    monitor_clipboard_and_send()


