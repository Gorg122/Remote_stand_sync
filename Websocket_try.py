import asyncio
# import {io} from socket
#
# const socket = io("ws://localhost:3001/boards/board/3")
# from websockets.sync.client import connect
#
# def hello():
#     with connect("ws://localhost:3001/boards/board/3:8400") as websocket:
#         #websocket.send("Hello world!")
#         message = websocket.recv()
#         print(f"Received: {message}")
#
# hello()


# import socketio
# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
#
# sio = socketio.Client()
#
# http_session = requests.Session()
# http_session.verify = False
# retry = Retry(connect=3, backoff_factor=0.5)
# adapter = HTTPAdapter(max_retries=retry)
# http_session.mount('http://', adapter)
# http_session.mount('https://', adapter)
# sio = socketio.Client(http_session=http_session)
#
# @sio.event
# @sio.event
# def connect():
#     print("I'm connected!")
#
# @sio.event
# def connect_error(data):
#     print("The connection failed!")
#
#
# @sio.on('*')
# def catch_all(event, data):
#     pass
#
# @sio.event
# def disconnect():
#     print("I'm disconnected!")
#
#     print('disconnected from server')
#
# sio.connect('http://localhost:3001/boards/board/3')


# import socketio
# import time
# time.sleep(5)
# socketEndpoint = 'ws://localhost:3000/boards/board/3'
# sio = socketio.Client()
#
# sio.connect(socketEndpoint)
# sio.emit('join', {'channelName': 'message'})
# @sio.on('messaage')
# def on_message(response):
#     print(response.data)






# sio.connect('ws://localhost:3001')
# sio.emit('my response', data1)
# print(data1)
# sio.wait()


# import asyncio
# from websockets.server import serve
#
# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)
#
# async def main():
#     async with serve(echo, "localhost", 8765):
#         await asyncio.Future()  # run forever
#
# asyncio.run(main())

# socket = new WebSocket("wss://javascript.info/article/websocket/demo/hello");
#
# socket.onopen = function(e) {
#   alert("[open] Соединение установлено");
#   alert("Отправляем данные на сервер");
#   socket.send("Меня зовут Джон");
# };
#
# socket.onmessage = function(event) {
#   alert(`[message] Данные получены с сервера: ${event.data}`);
# };
#
# socket.onclose = function(event) {
#   if (event.wasClean) {
#     alert(`[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}`);
#   } else {
#     // например, сервер убил процесс или сеть недоступна
#     // обычно в этом случае event.code 1006
#     alert('[close] Соединение прервано');
#   }
# };
#
# socket.onerror = function(error) {
#   alert(`[error]`);
# };




#!/usr/bin/env python

import asyncio
import websockets

async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def main():
    async with websockets.serve(hello, "wss://localhost:3001/boards/board/3", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())