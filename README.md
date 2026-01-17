# Desafio Técnico: Comunicação com WebSockets 🚀

Este projeto consiste em uma solução de comunicação bidirecional e persistente utilizando o protocolo WebSocket

A aplicação permite que múltiplos clientes se conectem a um servidor central, onde cada mensagem enviada por um usuário é replicada para todos os outros conectados (broadcast)

## 🛠 Tecnologias Utilizadas

* **Linguagem**: Python 3.10+
* **Backend**: FastAPI (escolhido pela alta performance e suporte nativo a conexões assíncronas).
* **Servidor ASGI**: Uvicorn (com suporte a websockets).
* **Frontend**: HTML5 e JavaScript Vanilla (utilizando a API nativa `WebSocket` do navegador).
* **Padronização**: Commitizen (para garantir o padrão de Conventional Commits).

## 🏗 Arquitetura e Decisões Técnicas

Para atender aos requisitos de qualidade e organização, a solução foi dividida em responsabilidades claras:

1.  **Servidor com Estado (Stateful)**: Diferente do HTTP tradicional, o servidor mantém a referência da conexão de cada cliente ativo.
2.  **Connection Manager**: Implementei uma classe dedicada para gerenciar o **pool de conexões**. Ela abstrai as operações de:
    * **Handshake**: Aceite da conexão inicial via HTTP e upgrade para o código 101.
    * **Broadcast**: Iteração sobre as conexões ativas para garantir a entrega das mensagens a todos os clientes.
3.  **Monitoramento e Logs**: O backend monitora o ciclo de vida das conexões (entrada, troca de mensagens e desconexão). Além das mensagens na UI, também foram utilizados logs no terminal.



## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python instalado.
* Ambiente virtual configurado (recomendado).

### Passo a Passo
1.  **Clonar o repositório**:
    ```bash
    git clone git@github.com:almemanuel/desafio-websocket-bluelephant.git # caso não use ssh, copie o link https do repositório
    cd desafio-websocket-bluelephant
    ```

2.  **Criar e ativar o ambiente virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # No Windows: venv\Scripts\activate
    ```

3.  **Instalar as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Iniciar o servidor**:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

5.  **Acessar a aplicação**:
    Abra `http://localhost:8000` em duas ou mais abas do seu navegador para testar a comunicação em tempo real.

---
Desenvolvido como parte do processo seletivo para a Bluelephant AI.