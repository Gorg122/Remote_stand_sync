import os
import shutil
import time
import serial
import subprocess
import configparser
from Sof_to_FPGA import FPGA_flash
from Find_arduino import Find_Arduino
#from Client import *
import socketio

sio = socketio.Client()


# Скрипт передачи управляющих команд на плату Ардуино
def Serial_delivery(arduino, cur_action, curent_pin, pin_state):
    # Распознаем текущую команду
    if cur_action:
        # Проверяем текущее состояние переключателя
        if pin_state == True:
            comand_sw1 = str(curent_pin) + "L"
            #switches[int(curent_pin)] = 0
        else:
            comand_sw1 = str(curent_pin) + "H"
        arduino.write(bytes(comand_sw1, 'utf-8'))
        time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        time.sleep(1)
        print(data, '\n')

    else:
        comand_but1 = str(curent_pin) + "H"
        arduino.write(bytes(comand_but1, 'utf-8'))
        time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        time.sleep(1)
        print(data, '\n')

        comand_but2 = str(curent_pin) + "L"
        arduino.write(bytes(comand_but2, 'utf-8'))
        time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        time.sleep(1)
        print(data, '\n')



def Arduino_Serial(Arduino_port, command, pin, pin_state):

    # Подключаемся к плату Ардуино через последовательный порт, к заранее определенному COM порту
    arduino = serial.Serial(port=Arduino_port, baudrate=9600, timeout=.1)
    y = 0
    # Ожидаем успешного подключения
    time.sleep(3)

    # Отправляем контрольную последовательность и ожидаем положительного ответа
    while y != 1:
        poslanie = "Hello"
        print("Подключение к плате Ардуино")
        #GUI.print_log("Подключение к плате Ардуино")
        arduino.write(bytes(poslanie, 'utf-8'))
        data = str(arduino.readline().decode().strip('\r\n'))
        if str(data).count(start[0]):
            print("Контрольная последовательность получена")
            y += 1

    # Начало передачи управляющих сигналов на плату Ардуино
    print("Начало передачи сигналов")
    #GUI.print_log("Начало передачи сигналов")
    # Выполняем проходку по непустым строкам файла сценария
    i = command
    while i != "The_end":

            # Обработка команд управления
            # Обработка нажатия переключателя
            if (cur_action):
                if (pin_state):
                    # Проверяем данную команду на предмет установленных задержек
                    Serial_delivery(arduino, 1, pin, 0)
                    current_commands += 1
                else:
                    Serial_delivery(arduino, 1, pin, 1)
                    current_commands += 1

            # Обработка нажатия кнопки
            else:
                # Проверяем данную команду на предмет установленных задержек
                Serial_delivery(arduino, 0, pin, 0, 0)
                current_commands += 1

                break
    print("Total_commands = ", current_commands)
    return ("Ok", current_commands)



def File_deleting(folder):
    deleting = True
    while deleting:
        delete = 0
        print("Пробегаю")
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".sof"):
                    file_name = file
                    file_path = root + "/" + file_name
                    try:
                        shutil.rm(file_path_path, ignore_errors=True)
                    except:
                        print('File delete error')
                    delete = 1
        deleting = False
        print("Удалять нечего")
        return "Все файлы удалены"

# Главная функция обработки файлов пользователя
def Launch(User_path_to_file, root_path):
    
    # Открываем файл настроек
    config = configparser.ConfigParser()
    config_path = root_path + '/' + "Config.ini"
    config.read(config_path)

    # Выводим имеющиеся в файле конфигурации ключи
    keys = config.keys()
    for key in keys:
        print(config[key])

    # Читаем из файла конфигурации текущую папку проекта
    root_path = config['Direc']['Path']

    print(root_path)



    @sio.event(namespace = '/chat')
    def connect():

        print('connection established')
    return 1

    @sio.event
    def my_message(sid, data):
        sio.emit('connection', data, namespace='/chat', skip_sid=sid)

    @sio.event
    def Conecting(sid, data):
        sio.on('hello', data, namespace='/chat', skip_sid=sid)
        print(sid)
        print(data)
        if data == 'world':
            @sio.on('hello', namespace='/chat')
            def on_message(arg1):
                print('I received a message!')
                print(arg1)
                # Запускаем процесс обработки пользовательской прошивки
                #sof_path = "#"
                #sof_file_name = "#"
                # Запускаем функцию взаимодействия с платой Ардуино, выводим порт подключения
                Arduino_port = Find_Arduino(root_path=root_path)
                print(Arduino_port, '\n')
                #GUI.print_log("Порт подключения Ардуино ", Arduino_port)
                print(Arduino_port[0:3], '\n')

                # Обрабатываем ошибку поиска порта подключения платы Ардуино
                if Arduino_port[0:3] != 'COM':
                    print("Проблема при передаче управляющих сигналов, свяжитесь с преподавателем\n")

                # Запускаем функцию взаимодействия с платой ПЛИС
                FPGA_chek, pr_type = FPGA_flash(User_path=User_path_to_file, FPGA_num=1, root_path=root_path)
                # Производим обработку ошибок компиляции проекта или прошивки платы
                if FPGA_chek != "OK":
                    returncode = 1
                    errors_ = 1
                    errors_file.write("Проблема с компиляцией проекта, или прошивкой платы, изучите файлы логов\n")

                # Запускаем функцию записи видео
                video_script_path = root_path + '/' + "Video.py"
                #python_path = "C:/Users/grish/AppData/Local/Programs/Python/Python38/python.exe"
                python_path = "C:/Users/Админ/AppData/Local/Programs/Python/Python38/python.exe"
                Video_chek = subprocess.Popen([python_path, video_script_path])

            @sio.on('switch', namespace='/chat')
            def on_message(arg1, arg2, arg3):
                print('THIS IS SWITCH')
                print("arg1 = ", arg1)
                print("arg2 = ", arg2)
                print("arg3 = ", arg3)
                return 'switch', arg1, arg2, arg3
                Arduino_serial(arduino_port, 1, arg1, arg2, arg3)


            @sio.on('button', namespace='/chat')
            def on_message(arg1, arg2):
                print('THIS IS BUTTON')
                print("arg1 = ", arg1)
                print("arg2 = ", arg2)
                return 'button', arg1, arg2
                Arduino_serial(arduino_port, 0, arg1, arg2)


            # Производим поиск файла прошивки после окончания прошивки платы ПЛИС или компиляции проекта
            for root, dirs, files in os.walk(root_path + '/' + User_path_to_file):
                for file in files:
                    if file.endswith(".sof"):
                        sof_file_name = file
                        sof_path = root + '/' + sof_file_name

                        print(sof_path)
                        #GUI.print_log("Путь к файлу прошивки ", sof_path)

            # Маркер существования видеофайла
            vid_chek = "video_none"


        try:
            sio.connect('http://localhost:9999', namespaces=['/chat'])
        except:
            print('Server is not responding')
            # Если файл прошивки существует, и работа с платой ПЛИС успешна, запускаем обработку прошивки пользователя
            if os.path.exists(sof_path) and FPGA_chek == "OK":



          

                # Запускаем функцию последовательной передачи управляющих команд на плату Ардуино
                serial, command_num = Arduino_Serial(script_file_path=script_file_path,
                                                 errs_path=errs_path,
                                                 Arduino_port=Arduino_port)

            # Возвращаем флаг удачного завершения процесса передачи данных
            if serial == "OK":
                print("Передача данных окончена")
                #GUI.print_log("Передача данных окончена")

            # Ожидаем окончания процесса записи видео
            Video_chek.wait()
            # Перепроверяем завершился ли процесс записи видео
            while Video_chek.poll() is None:
                time.sleep(0.5)
            # Выводим код возврата процесса записи видео
            print("Запись видео возвращает:", Video_chek.returncode)
            #GUI.print_log("Запись видео возвращает:", Video_chek.returncode)
            returncode = Video_chek.returncode
        # Если отсутствует файл прошивки или проект на ПЛИС, ошибка записывается в файл ошибок
        else:
            errors_file.write("Отсутствует файл прошивки или проект на ПЛИС\n")
            errors_ = 1
            # Задаем пустые значения переменных если файла прошивки нет
            sof_file_name = ""
            sof_path = ""
        # Если отсутствует файл сценария, ошибка записывается в файл ошибок
        # else:
        #     errors_file.write("Отправте данные повторно, включая файл сценария\n")
        # errors_ = 1
        # # Задаем соответствующие значения переменных, если отсутствует файл сценария
        #     returncode = 1
        #     script_file_path = ""
        #     script_file_name = ""
        #     sof_file_name = ""
        #     sof_path = ""

    # Закрываем файл ошибок
    errors_file.close()

   
Launch(User_path_to_file="Hex/", root_path="/home/unit1/Project_main")

