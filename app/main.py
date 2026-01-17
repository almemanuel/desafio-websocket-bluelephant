import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.manager import ConnectionManager

# log no terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebSocketServer")

# servidor
app = FastAPI()
manager = ConnectionManager()

# Monta o diretório estático para servir o HTML, CSS e JS
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def get() -> FileResponse:
    """Rota raíz que serve o servidor principal

    Returns:
        FileResponse: conteúdo da página
    """
    return FileResponse("app/static/index.html")


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str) -> None:
    """Verificação de unicidade do usuário e gerenciamento do pool e do broadcast do WebSocket

    Args:
        websocket (WebSocket): protocolo de comunicação para troca de mensagens real-time
        username (str): nome informado para o usuário
    """
    # Sanitização e limite de caracteres
    username = username.strip()[:20]

    # Garante que o nome não fique vazio após o strip
    if not username:
        username = f"Anonimo_{websocket.client.port}"

    # 1. Verifica se o nome já está sendo usado
    if manager.is_user_connected(username):
        logger.warning(f"\tTentativa de conexão duplicada: {username}")
        await websocket.accept() # Aceita só para poder enviar a mensagem de erro
        await websocket.send_text("ERRO_NOME_DUPLICADO")
        await websocket.close()
        return

    # O manager recebe o nome junto com o socket
    await manager.connect(websocket, username)
    logger.info(f"\tLOGIN: {username}")
    
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        # Recupera o nome que estava no pool antes de apagar
        user_left = manager.disconnect(websocket)
        logger.info(f"\tLOGOUT: {user_left}")
        await manager.broadcast(f"SISTEMA: {user_left} saiu")
    except Exception as e:
        # Tratamento de erros inesperados para evitar conexões penduradas
        logger.error(f"\tErro inesperado com {username}: {e}")
        user_left = manager.disconnect(websocket)
        await manager.broadcast(f"SISTEMA: {user_left} saiu devido a um erro técnico")
