import asyncio
from fastapi import WebSocket

class ConnectionManager:
    """Gerencia as conexões ativas dos WebSockets e os nomes dos usuários associados
    """
    def __init__(self):
        """Mapeia a conexão física ao nome do usuário
        """
        self.active_connections: dict[WebSocket, str] = {}


    def is_user_connected(self, username: str) -> bool:
        """Verifica se o nome já existe entre os valores do dicionário

        Args:
            username (str): nome de usuário recebido pelo websocket

        Returns:
            bool: True se o usuário estiver conectado, False caso contrário
        """
        return username in self.active_connections.values()


    async def connect(self, websocket: WebSocket, username: str) -> None:
        """Aceita a conexão WebSocket e adiciona ao dicionário de conexões ativas

        Args:
            websocket (WebSocket): protocolo do servidor
            username (str): nome do usuário associado à conexão
        """
        await websocket.accept()
        self.active_connections[websocket] = username


    def disconnect(self, websocket: WebSocket) -> str:
        """Remove do dicionário e retorna o nome para usarmos na mensagem de saída

        Args:
            websocket (WebSocket): protocolo do servidor

        Returns:
            str: usuário desconectado
        """
        return self.active_connections.pop(websocket, "Usuário desconhecido")


    async def broadcast(self, message: str) -> None:
        """Transmissão de mensagens de forma assíncrona para todos os usuários

        Args:
            message (str): mensagem a ser transmitida
        """
        if not self.active_connections:
            return

        # lista de tarefas para enviar as mensagens simultaneamente
        # list() nas chaves para evitar erros de mutação durante o loop
        targets = list(self.active_connections.keys())
        
        tasks = [connection.send_text(message) for connection in targets]
        
        # garante que se uma conexão falhar, as outras continuem
        await asyncio.gather(*tasks, return_exceptions=True)
