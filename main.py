from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, Request
from starlette.websockets import WebSocketDisconnect
from typing import List


app = FastAPI()
templates = Jinja2Templates(directory='templates')


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []
        print("Creating a list to active connections", self.connections)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        print("New Active connections are ", self.connections)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)
        print("In broadcast: sent msg to ", connection)


manager = ConnectionManager()


@app.get('/', response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect as e:
        manager.connections.remove(websocket)
        print(f'Connection closed {e.code}')
