import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.manager import ConnectionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebSocketServer")

app = FastAPI()
manager = ConnectionManager()

@app.get("/")
async def get():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    # 1. Verifica se o nome já está sendo usado
    if manager.is_user_connected(username):
        logger.warning(f"\tTentativa de conexão duplicada: {username}")
        await websocket.accept() # Aceita só para poder enviar a mensagem de erro
        await websocket.send_text("ERRO_NOME_DUPLICADO")
        await websocket.close()
        return
    # O manager agora recebe o nome junto com o socket
    await manager.connect(websocket, username)
    logger.info(f"\tLOGIN: {username}")
    
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        # Recuperamos o nome que estava no pool antes de apagar
        user_left = manager.disconnect(websocket)
        logger.info(f"\tLOGOUT: {user_left}")
        await manager.broadcast(f"SISTEMA: {user_left} saiu")