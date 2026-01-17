from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # pool de conexões exigido
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Aceita a conexão inicial (handshake)
        await websocket.accept()
        # Adiciona ao pool para monitoramento
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # Remove do pool quando a conexão é encerrada
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # Envia a mensagem para todos os outros clientes 
        for connection in self.active_connections:
            await connection.send_text(message)