# 🖥️ Sistema de Clipboard Distribuído com Histórico

Este projeto implementa um **sistema cliente-servidor em Python** que permite **compartilhar a área de transferência (clipboard)** entre diferentes máquinas, **mantendo um histórico dos últimos textos copiados**.  

O sistema foi desenvolvido com base no **Tema 05 do Seminário de Sistemas Distribuídos** e utiliza **sockets TCP** para comunicação entre cliente e servidor.

---

## ⚙️ Estrutura do Sistema

O projeto é composto por dois scripts principais:

- `servidor.py` → Responsável por receber textos e manter o histórico.  
- `cliente.py` → Monitora a área de transferência e envia novos textos ao servidor.  

*(O arquivo `ctrl+v.py` pode representar a implementação do lado servidor.)*

---

## 🧩 Funcionalidades

- **📡 Comunicação via Sockets TCP**  
  Garante uma comunicação confiável e orientada à conexão entre cliente e servidor.

- **👥 Suporte a Múltiplos Clientes**  
  O servidor utiliza **threads** para lidar com várias conexões simultaneamente.

- **🧠 Histórico de Clipboard**  
  Mantém uma lista com os **últimos 5 textos copiados**, removendo automaticamente os mais antigos.

- **⌨️ Interface Interativa no Servidor**  
  Permite ao administrador usar comandos diretamente no terminal:
  - `listar` → Exibe o histórico.  
  - `colar <n>` → Copia o item *n* do histórico para a área de transferência local.  
  - `sair` → Encerra o servidor.

- **🔄 Monitoramento Contínuo no Cliente**  
  O cliente verifica a área de transferência a cada segundo sem necessidade de interação manual.

- **🔁 Reconexão Automática**  
  O cliente tenta se reconectar caso a conexão com o servidor seja perdida.

---

## 🧠 Como Funciona

1. O **cliente** monitora continuamente o clipboard do usuário.  
2. Quando um novo texto é copiado (Ctrl+C), ele é **enviado ao servidor**.  
3. O **servidor** recebe o texto, adiciona ao **histórico** e o exibe no terminal.  
4. O administrador pode listar o histórico e copiar qualquer item de volta para o clipboard do servidor.

---

## 🧰 Pré-requisitos

Antes de executar o sistema, certifique-se de ter:

- **Python 3** instalado  
  👉 [Baixar Python](https://www.python.org/downloads/)

- Biblioteca **pyperclip**, usada para manipular o clipboard:

  ```bash
  pip install pyperclip
  ```

---

## ▶️ Como Executar

### 🖥️ 1. Iniciar o Servidor

Na máquina que atuará como servidor:

```bash
python servidor.py
```

Você verá a mensagem:

```bash
[ESCUTANDO] Servidor escutando em 0.0.0.0:65432
```

Agora o servidor está pronto para receber conexões.

💬 **Comandos disponíveis:**

```bash
listar
colar <n>
sair
```

---

### 💻 2. Iniciar o Cliente

Na máquina cliente:

1. Se o cliente e o servidor estiverem em máquinas diferentes, abra o arquivo `cliente.py` e altere o IP:

   ```python
   SERVER_HOST = '192.168.1.10'  # IP do servidor

   ```

   Se estiverem na mesma máquina, mantenha:

   ```python
   SERVER_HOST = '127.0.0.1'
   ```

2. Execute o cliente:

   ```bash
   python cliente.py
   ```

O cliente começará a monitorar a área de transferência e enviará automaticamente os textos copiados ao servidor.

---

## 🧪 Exemplo de Uso

1. Com ambos em execução, copie um texto na máquina cliente (Ctrl+C).  
2. O terminal do cliente exibirá:

   ```bash
   [ENVIADO] Texto enviado ao servidor.
   ```

3. O servidor exibirá:

   ```bash
   [DADO RECEBIDO] Recebido de ('192.168.1.15', 50000): "Texto copiado"
   [HISTÓRICO ATUALIZADO] O histórico agora contém 1 item(ns).
   ```

4. No servidor, digite:

   ```bash
   listar
   ```

   Resultado:

   ```bash
   1: Texto copiado
   ```

5. Para copiar novamente o texto para o clipboard do servidor:

   ```bash
   colar 1
   ```

   Resultado:

   ```bash
   [SUCESSO] Item 1 ("Texto copiado") copiado para a área de transferência do servidor!
   ```

---

## 🧾 Resumo Técnico

| Componente | Descrição | Tecnologias |
|-------------|------------|--------------|
| **Servidor** | Recebe textos, mantém histórico e oferece interface de comandos | Python, Sockets, Threads, Pyperclip |
| **Cliente** | Monitora o clipboard e envia textos automaticamente | Python, Sockets, Pyperclip |

---

## 👨‍💻 Autor

**Paulo Victor Almeida de Oliveira**  
**Igor Cézar da Silva**
Instituto Federal da Bahia — IFBA  
4º semestre de **Sistemas de Informação**  
Projeto desenvolvido para o **Seminário de Sistemas Distribuídos (Tema 05)**
