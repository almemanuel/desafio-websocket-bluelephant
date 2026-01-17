from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Mapeia a conexão física ao nome do usuário
        self.active_connections: dict[WebSocket, str] = {}

    def is_user_connected(self, username: str) -> bool:
        # Verifica se o nome já existe entre os valores do dicionário
        return username in self.active_connections.values()

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[websocket] = username

    def disconnect(self, websocket: WebSocket):
        # Remove do dicionário e retorna o nome para usarmos na mensagem de saída
        return self.active_connections.pop(websocket, "Usuário desconhecido")

    async def broadcast(self, message: str):
        for connection in self.active_connections.keys():
            await connection.send_text(message)