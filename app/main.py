import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.manager import ConnectionManager

# configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebSocketServer")

app = FastAPI()
manager = ConnectionManager()

# rota para carregar o html do cliente
@app.get("/")
async def get():
    with open("app/static/index.html", "r") as f:
        return HTMLResponse(f.read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Realiza o Handshake e adiciona ao pool
    # Ao aceitar a conexão, o FastAPI/Uvicorn envia o código 101 Switching Protocols
    # mantendo o canal TCP aberto para comunicação bidirecional.
    client_id = f"{websocket.client.host}:{websocket.client.port}"
    
    await manager.connect(websocket)
    logger.info(f"\tCliente conectado: {client_id}") # log de entrada

    try:
        while True:
            # Mantém a conexão aberta e escuta mensagens 
            data = await websocket.receive_text()
            logger.info(f"\tMensagem recebida de {client_id}: {data}") # log de mensagem
            # Ao receber, faz o broadcast para todos os clientes 
            await manager.broadcast(f"{data}")
    except WebSocketDisconnect:
        # Monitora a desconexão para limpar o pool 
        manager.disconnect(websocket)
        logger.info(f"\tCliente desconectado: {client_id}") # Log de saída
        # broadcast de saída
        await manager.broadcast(f"SISTEMA: Usuário desconectado")