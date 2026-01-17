# Desafio Técnico: Comunicação com WebSockets 🚀

Este projeto consiste em uma solução de comunicação bidirecional e persistente utilizando o protocolo WebSocket. 

A aplicação permite que múltiplos clientes se conectem a um servidor central, onde cada mensagem enviada por um usuário é replicada para todos os outros conectados (broadcast) em tempo real.

## 🛠 Tecnologias Utilizadas

* **Linguagem**: Python 3.10+
* **Backend**: FastAPI (escolhido pela alta performance e suporte nativo a conexões assíncronas).
* **Servidor**: Uvicorn (com suporte a websockets).
* **Frontend**: SPA (Single Page Application) com HTML5 e JavaScript Vanilla.
* **Padronização**: Commitizen (padrão Conventional Commits).

## 🏗 Arquitetura e Decisões Técnicas

A solução foi estruturada para ser escalável e fácil de monitorar:

1.  **Servidor Stateful**: Diferente do modelo stateless do HTTP, o servidor mantém conexões persistentes, permitindo o envio de dados via *server-push*.
2.  **Connection Manager**: Classe responsável por gerenciar o ciclo de vida das conexões:
    * **Handshake**: Upgrade do protocolo HTTP para WebSocket (Código 101).
    * **Unicidade**: Validação de nomes de usuário para evitar conflitos no pool de conexões.
    * **Broadcast**: Distribuição eficiente de mensagens para todos os sockets ativos.
3.  **Observabilidade**: Implementação de logs via biblioteca `logging` no backend para monitorar eventos de LOGIN, LOGOUT e erros de conexão no terminal.

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.10+
* Ambiente virtual (venv)

### Passo a Passo
1.  **Clonar o repositório**:
    ```bash
    git clone git@github.com:almemanuel/desafio-websocket-bluelephant.git # ou o link https caso você não utilize ssh
    cd desafio-websocket-bluelephant
    ```

2.  **Ambiente Virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # No Windows (PowerShell): .\venv\Scripts\Activate.ps1
    ```

3.  **Dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Iniciar o servidor**:
    ```bash
    # O host 0.0.0.0 garante a acessibilidade em ambientes virtualizados (WSL, Docker, etc)
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

5.  **Acessar a aplicação**:
    Abra `http://127.0.0.1:8000` em duas ou mais abas para testar o broadcast.

---
Desenvolvido por [Emanuel](https://github.com/almemanuel) como parte do processo seletivo para a [Bluelephant AI](https://bluelephantai.com.br/).