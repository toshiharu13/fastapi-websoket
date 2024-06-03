from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, Request
from starlette.websockets import WebSocketDisconnect


app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.websocket('/ws')
async def websocket_endpoint(websoket: WebSocket):
    await websoket.accept()
    try:
        while True:
            data = await websoket.receive_text()
            await websoket.send_text(data)
    except WebSocketDisconnect as e:
        print(f'Connection closed {e.code}')
