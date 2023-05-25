import os
import shutil
import time
import serial
import subprocess
import base64
import configparser

import uvicorn
from fastapi import FastAPI

from Sof_to_FPGA import FPGA_flash
from Find_arduino import Find_Arduino
import cv2
import socketio

app = FastAPI()

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)


image = ""

User_path_to_file = "/home/unit1/Project_main/firmware"
root_path = "/home/unit1/Project_main"

config = configparser.ConfigParser()
config_path = root_path + '/' + "Config.ini"
config.read(config_path)

# Выводим имеющиеся в файле конфигурации ключи
keys = config.keys()
for key in keys:
    print(config[key])

# # Читаем из файла конфигурации текущую папку проекта
root_path = config['Direc']['Path']
start = config['Arduino']['arduino_key']

Arduino_port = Find_Arduino(root_path=root_path)
# Arduino_port = "/dev/ttyUSB0"
print(Arduino_port, '\n')
# GUI.print_log("Порт подключения Ардуино ", Arduino_port)
# print(Arduino_port[0:3], '\n')

# Обрабатываем ошибку поиска порта подключения платы Ардуино
# if Arduino_port[0:3] != 'COM':
#     print("Проблема при передаче управляющих сигналов, свяжитесь с преподавателем\n")

# Скрипт передачи управляющих команд на плату Ардуино
def Serial_delivery(arduino, cur_action, curent_pin, pin_state):
    # Распознаем текущую команду
    if cur_action:
        # Проверяем текущее состояние переключателя
        if pin_state == True:
            comand_sw1 = str(curent_pin) + "L"
            # switches[int(curent_pin)] = 0
        else:
            comand_sw1 = str(curent_pin) + "H"
        arduino.write(bytes(comand_sw1, 'utf-8'))
        #time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        #time.sleep(1)
        print(data, '\n')

    else:
        comand_but1 = str(curent_pin) + "H"
        arduino.write(bytes(comand_but1, 'utf-8'))
        #time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        #time.sleep(1)
        print(data, '\n')

        comand_but2 = str(curent_pin) + "L"
        arduino.write(bytes(comand_but2, 'utf-8'))
        #time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        #time.sleep(1)
        print(data, '\n')


def arduino_serial_work(Arduino_port, command, pin, pin_state):
    # Подключаемся к плату Ардуино через последовательный порт, к заранее определенному COM порту
    arduino = serial.Serial(port=Arduino_port, baudrate=9600, timeout=.1)
    y = 0
    # Ожидаем успешного подключения
    #time.sleep(3)

    # Отправляем контрольную последовательность и ожидаем положительного ответа
    # while y != 1:
    #     poslanie = "Hello"
    #     print("Подключение к плате Ардуино")
    #     # GUI.print_log("Подключение к плате Ардуино")
    #     arduino.write(bytes(poslanie, 'utf-8'))
    #     data = str(arduino.readline().decode().strip('\r\n'))
    #     if str(data).count(start[0]):
    #         print("Контрольная последовательность получена")
    #         y += 1

    # Начало передачи управляющих сигналов на плату Ардуино
    print("Начало передачи сигналов")
    #arduino = Arduino_port
    # GUI.print_log("Начало передачи сигналов")
    # Выполняем проходку по непустым строкам файла сценария
    #i = command
    # Обработка команд управления
    # Обработка нажатия переключателя
    if (command):
        if (pin_state):
            # Проверяем данную команду на предмет установленных задержек
            Serial_delivery(arduino, 1, pin, 0)
            #current_commands += 1
        else:
            Serial_delivery(arduino, 1, pin, 1)
            #current_commands += 1
        # Serial_delivery(arduino, 1, pin, pin_state)
        print(f"Отправлена команда свитч {pin}, c состоянием {pin_state}")

    # Обработка нажатия кнопки
    else:
        # Проверяем данную команду на предмет установленных задержек
        Serial_delivery(arduino, 0, pin, 1)
        #current_commands += 1

    #print("Total_commands = ", current_commands)
    return ("Ok")# current_commands)

# @sio.on("connection")
# # функция настройки платы
# def Conecting(sid):
#     print('I received a message!')
#     # Запускаем процесс обработки пользовательской прошивки
#     # sof_path = "#"
#     # sof_file_name = "#"
#     # Запускаем функцию взаимодействия с платой Ардуино, выводим порт подключения
#
#
#     # Запускаем функцию взаимодействия с платой ПЛИС
#     FPGA_chek, pr_type = FPGA_flash(User_path=User_path_to_file, FPGA_num=1, root_path=root_path)
#     # Производим обработку ошибок компиляции проекта или прошивки платы
#     if FPGA_chek != "OK":
#         returncode = 1
#         errors_ = 1
#         print("Проблема с компиляцией проекта, или прошивкой платы, изучите файлы логов\n")


@sio.on("uploadFile")
# функция загрузки прошивки на плату

@sio.on("switch")
def on_messagee(sid, numberOfSwitch, state, arg3):
    print('THIS IS SWITCH')
    print("arg1 = ", sid)
    print("arg2 = ", numberOfSwitch)
    print("arg3 = ", arg3)
    print("n = ", state)
    # # return 'switch', arg1, arg2, arg3
    arduino_serial_work(Arduino_port, 1, numberOfSwitch, state)


@sio.on("button")
def on_message(arg1, arg2):
    print('THIS IS BUTTON')
    print("arg1 = ", arg1)
    print("arg2 = ", arg2)
    return 'button', arg1, arg2
    arduino_serial_work(arduino_port, 0, arg1, arg2)


@sio.on("getImage")
async def getImage(sid):
    print("start")
    ret, img = cap.read()
    image = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    return image

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)

#     < div
#     className = {css.video} >
#     < video
#     controls
#     poster = "https://archive.org/download/WebmVp8Vorbis/webmvp8.gif"
# >
# < source
# src = {starWarsVideo}
# type = "video/mp4" / >
# Your
# browser
# doesn
# 't support HTML5 video tag.
# < / video >
# < / div >