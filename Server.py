# import asyncio, socket
# def handle_client(client):
#     request = None
#     while request != 'quit':
#         request = client.recv(255).decode('utf8')
#         response = cmd.run(request)
#         client.send(response.encode('utf8'))
#     client.close()
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(('http://localhost:3001', 15555))
# server.listen(8)
#
# try:
#     while True:
#         client, _ = server.accept()
#         threading.Thread(target=handle_client, args=(client,)).start()
# except KeyboardInterrupt:
#     server.close()

# import asyncio
# import logging
# import websockets
# from websockets import WebSocketClientProtocol
#
# logging. basicConfig(level=logging.INFO)
# #websockets.WebSocketClientProtocol = "ws"
# async def consumer_handler(websocket: WebSocketClientProtocol) -> None:
#     async for message in websocket:
#         log_message(message)
#
# async def consume(hostname: str, port: int) -> None:
#     websocket_resource_url = f"ws://{hostname}:{port}"
#     async with websockets.connect(websocket_resource_url) as websocket:
#         await consumer_handler(websocket)
#
# def log_message(message: str) -> None:
#     logging.info(f"Message: {message}")
#     print(message)
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop( )
#     loop. run_until_complete(consume(hostname="localhost:3000/boards/board/3", port=8400))
#     loop. run_forever( )
#
# import asyncio
# from websockets.server import serve
#
# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)
#         print(message)
#
# async def main():
#     async with serve(echo, "localhost", 8765):
#         await asyncio.Future()  # run forever
#
# asyncio.run(main())

# import socketio
# sio = socketio.Client()
# @sio.event
# def connect():
#
#     print('connection established')

# @sio.event
# def message(data):
#     print('I received a message!')
# @sio.on('switch')
# def on_message(arg1):
#     print('I received a message!')
#     print(arg1)
#     #print('arg2')
#     #print('arg3')

# @sio.on('*')
# def catch_all(event, data):
#     print(event)
#     print(data)
#     pass
# sio.emit('pipster')
#@sio.emit('my message', {'foo': 'bar'})
# def catch_all(event, data):
#     print(event)
#     print(data)
#     pass
# @sio.event
# def my_message(data):
#
#
#     print('message received with ', data)
#
#
#     #sio.emit('my response', {'response': 'my response'})
# @sio.event
# def disconnect():
#
#     print('disconnected from server')
# sio.connect('http://localhost:9999')
# sio.wait()

import socket


from typing import Union
import uvicorn
import shutil
from fastapi import FastAPI, File, UploadFile
from typing_extensions import Annotated

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[Union[bytes, None], File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(file: Union[UploadFile, None] = None):
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         return {"filename": file.filename}
#if name == "Server.py":
#    uvicorn.run(app, host="0.0.0.0", port=9999)
@app.post("/uploadfile/")
async def root(file: UploadFile=File(...)):
    with open('Hex/test_hex', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file.filename