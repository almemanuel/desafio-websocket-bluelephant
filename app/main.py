from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Realiza o Handshake e adiciona ao pool
    await manager.connect(websocket)
    try:
        while True:
            # Mantém a conexão aberta e escuta mensagens 
            data = await websocket.receive_text()
            # Ao receber, faz o broadcast para todos os clientes 
            await manager.broadcast(f"Cliente diz: {data}")
    except WebSocketDisconnect:
        # Monitora a desconexão para limpar o pool 
        manager.disconnect(websocket)
        await manager.broadcast("Um cliente saiu do chat.")