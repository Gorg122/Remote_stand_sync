import os
import shutil
import re
import time
import serial
import sys
import subprocess
import configparser
import pprint
import win32com.client
from datetime import date
from dateutil import parser
from google.oauth2 import service_account
from googleapiclient.discovery import build

import GUI
from Sof_to_FPGA import FPGA_flash
from Find_arduino import Find_Arduino



def WebSocket_catch():
    print('Kek')



# Скрипт передачи управляющих команд на плату Ардуино
def Serial_delivery(arduino, cur_action, curent_pin):
    # Словарь текущих состояний переключателей
    switches = dict([(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)])
    # Распознаем текущую команду
    if cur_action:
        # Проверяем текущее состояние переключателя
        if switches[int(curent_pin)] == 1:
            comand_sw1 = str(curent_pin) + "L"
            switches[int(curent_pin)] = 0
        else:
            comand_sw1 = str(curent_pin) + "H"
            switches[int(curent_pin)] = 1
        arduino.write(bytes(comand_sw1, 'utf-8'))
        time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        time.sleep(1)
        print(data, '\n')
        GUI.print_log("Номер пина распознанный на плате ", data)
        # Изменяем состояние данного переключателя в словаре на текущее

    else:
        comand_but1 = str(curent_pin) + "H"
        arduino.write(bytes(comand_but1, 'utf-8'))
        time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        time.sleep(1)
        print(data, '\n')
        GUI.print_log("Номер пина распознанный на плате ", data)

        comand_but2 = str(curent_pin) + "L"
        arduino.write(bytes(comand_but2, 'utf-8'))
        time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        time.sleep(1)
        print(data, '\n')
        GUI.print_log("Номер пина распознанный на плате ", data)
        # Запускаем процесс ожидания задержки, указанной пользователем

def Arduino_Serial(command, errs_path, Arduino_port):

    # Подключаемся к плату Ардуино через последовательный порт, к заранее определенному COM порту
    arduino = serial.Serial(port=Arduino_port, baudrate=9600, timeout=.1)
    y = 0
    # Ожидаем успешного подключения
    time.sleep(3)

    # Отправляем контрольную последовательность и ожидаем положительного ответа
    while y != 1:
        poslanie = "Hello"
        print("Подключение к плате Ардуино")
        GUI.print_log("Подключение к плате Ардуино")
        arduino.write(bytes(poslanie, 'utf-8'))
        data = str(arduino.readline().decode().strip('\r\n'))
        if str(data).count(start[0]):
            print("Контрольная последовательность получена")
            GUI.print_log("Контрольная последовательность получена")
            y += 1

    # Начало передачи управляющих сигналов на плату Ардуино
    print("Начало передачи сигналов")
    GUI.print_log("Начало передачи сигналов")
    # Выполняем проходку по непустым строкам файла сценария
    i = command
    while i != "The_end":

        # В случае, если строка не пустая, определяем верно ли указаны номера кнопок и переключателей
        if i != "\n" and i != "":
            numbers = i
            print(numbers)
            GUI.print_log("Номер текущего пина ", numbers)
            if (cur_action != 2):
                # Если номер кнопки или переключателя больше 8 или меньше 1, данная команда не обрабатывается
                if (int(numbers) > 8) or (int(numbers) < 1):
                    i += 1
                    false_pin = True
                    # Запись ошибки невверно указанного номера пина (с указанием конкретной строки)
                    errors_file.write("Количество активных пинов равно 9 (строка " + str(i) + ")\n")
                    print("Неверно указан номер пина\n")
                    GUI.print_log("Неправильно указан номер пина")

        # В случае, если номер пина введен верно, и строка не является пустой, начинаем обработку команды
        elif (false_pin == False):

            # Обработка команд управления
            # Обработка нажатия переключателя
            if (cur_action):
                # Проверяем данную команду на предмет установленных задержек
                Serial_delivery(arduino, 1, num[0], 0, 0)
                current_commands += 1

            # Обработка нажатия кнопки
            else:
                # Проверяем данную команду на предмет установленных задержек
                Serial_delivery(arduino, 0, num[0], 0, 0)
                current_commands += 1

            # Определяем ключ окончания обработки файла сценария
            if (lines[i].count(end[0])):
                print(switches)
                # Закрываем файл сценария пользователя
                input_file.close()
                # Выводим итоговое количество команд в файле сценария

                break
    # Закрываем файл ошибок, и ещё раз закрываем файл сценария
    input_file.close()
    errors_file.close()
    print("Total_commands = ", current_commands)
    GUI.print_log("Всего команд в файле сценария ", current_commands)
    # = current_commands
    return ("Ok", current_commands)


def get_file_metadata(path, filename, metadata):
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path)

    file_metadata = dict()
    item = ns.ParseName(str(filename))
    for ind, attribute in enumerate(metadata):
        attr_value = ns.GetDetailsOf(item, ind)
        if attr_value:
            file_metadata[attribute] = attr_value

    return file_metadata


def File_deleting(folder):
    deleting = True
    while deleting:
        delete = 0
        print("Пробегаю")
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".zip"):
                    file_name = file
                    file_path = root + "/" + file_name
                    print(file_path)
                    filename = file_name
                    metadata = ['Name', 'Size', 'Item type', 'Date modified', 'Date created']
                    try:
                        file_metadata = get_file_metadata(root, filename, metadata)
                        #Метаданные архива
                        # print(file_metadata)
                        date_modify = file_metadata['Date modified']
                    except:
                        file_metadata = {'Name': 1, 'Size': 20, 'Item type': "folder", 'Date modified': "28.05.2022",
                                         'Date created': "28.05.2022"}
                        date_modify = "6.12.2022"
                        GUI.print_log("Данные о времени создания файлов получены")
                    print(date_modify)
                    today = date.today()
                    file_date_str = str(date_modify)
                    file_date = file_date_str.split(" ", 1)[0]
                    print(file_date)
                    today = str(today)
                    old_date = parser.parse(file_date)
                    cur_date = parser.parse(today)
                    print("Old_date = ", old_date)
                    print("Current_date = ", cur_date)
                    print("Difference = ", cur_date - old_date)
                    old_file = cur_date - old_date
                    old_file = str(old_file)
                    print(old_file)
                    old_file = old_file.split(" ", 1)[0]
                    print(old_file)
                    old_file = old_file.split(':', 1)[0]
                    old_file = int(old_file)
                    if old_file > 2:
                        new_path = file_path.split('/')[:-1]
                        new_path = ''.join(new_path)
                        print(new_path)
                        shutil.rmtree(new_path, ignore_errors=True)
                        delete = 1

        deleting = False
        print("Удалять нечего")
        return "Все файлы удалены"


# Главная функция обработки файлов пользователя
def Launch(User_path_to_file, root_path):
    errors_ = 0
    # Перемещаемся в текущую папку проекта
    os.chdir(root_path)

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

    # Созщдаем и открываем файл ошибок
    errs_f = "errors.txt"
    errs_name = root_path + "/" + User_path_to_file
    errs_path = errs_name + '/' + errs_f
    errors_file = open(errs_path, "w")
    delay = ["delay"]

    # Запускаем функцию поиска файла прошивки
    script_file_path, script_file_name = Script_file_detect(User_path_to_file=User_path_to_file,
                                                            root_path=root_path,
                                                            errs_path=errs_path)
    # Выводим результат выполнения данной функции
    print(script_file_path)
    print(script_file_path)
    GUI.print_log("Путь к файлу сценария ", script_file_path)
    # scetch_name = "scetch"

    # Если файл сценария существует
    if os.path.exists(script_file_path):
        # Запускаем процесс обработки пользовательской прошивки
        sof_path = "#"
        sof_file_name = "#"
        # Запускаем функцию взаимодействия с платой Ардуино, выводим порт подключения
        Arduino_port = Find_Arduino(root_path=root_path)
        print(Arduino_port, '\n')
        GUI.print_log("Порт подключения Ардуино ", Arduino_port)
        print(Arduino_port[0:3], '\n')

        # Обрабатываем ошибку поиска порта подключения платы Ардуино
        if Arduino_port[0:3] != 'COM':
            errors_file.write("Проблема при передаче управляющих сигналов, свяжитесь с преподавателем\n")

        # Запускаем функцию взаимодействия с платой ПЛИС
        FPGA_chek, pr_type = FPGA_flash(User_path=User_path_to_file, FPGA_num=1, root_path=root_path)
        # Производим обработку ошибок компиляции проекта или прошивки платы
        if FPGA_chek != "OK":
            returncode = 1
            errors_ = 1
            errors_file.write("Проблема с компиляцией проекта, или прошивкой платы, изучите файлы логов\n")

        # Производим поиск файла прошивки после окончания прошивки платы ПЛИС или компиляции проекта
        for root, dirs, files in os.walk(root_path + '/' + User_path_to_file):
            for file in files:
                if file.endswith(".sof"):
                    sof_file_name = file
                    sof_path = root + '/' + sof_file_name

                    print(sof_path)
                    GUI.print_log("Путь к файлу прошивки ", sof_path)

        # Маркер существования видеофайла
        vid_chek = "video_none"

        # Если файл прошивки существует, и работа с платой ПЛИС успешна, запускаем обработку прошивки пользователя
        if os.path.exists(sof_path) and FPGA_chek == "OK":

            # Открываем файл сценария
            input_file = open(script_file_path)

            # print(len(re.findall(r"[\n']+", open(script_file_path).read())))
            # Построчно читаем файл сценария
            lines = input_file.readlines()
            # Найдем количество не пустых строк в файле сценария
            strings = len(re.findall(r"[\n']+", open(script_file_path).read()))
            print("ВСЕГО НЕ ПУСТЫХ СТРОК = ", strings)
            sleep_timing = 0
            for i in range(strings):
                # Поиск указания временных задержек
                if lines[i].count(delay[0]):
                    # Поиск чисел в конкретной строке файла сценария
                    sleep_num = re.findall(r'\d+', str(lines[i]))
                    for item in sleep_num:
                        sleep_dur = int(item)
                    # Длительность единократной задержки не более 30 секунд
                    if sleep_dur > 30:
                        sleep_dur = 30
                    print("Очередной слип на", sleep_dur)
                    sleep_timing = sleep_timing + sleep_dur
            strings = strings * 2
            # Выводим суммарные тайминги
            print("Время записи видео благодаря командам: ", strings)
            GUI.print_log("Время записи видео благодаря командам: ", strings)
            print("Суммарное время слипов: ", sleep_timing)
            GUI.print_log("Суммарное время слипов: ", sleep_timing)
            strings = strings + sleep_timing
            # Длительностт видео не может быть больше 2 минут
            if strings > 240:
                strings = 240
            # Выводим суммарное время записи видео
            print("Суммарное время записи видео: ", strings)
            GUI.print_log("Суммарное время записи видео: ", strings)

            # Создаем файл временных параметров записи видео
            video_file = open("video_timing.txt", "w")
            # Записываем в данный файо необходимую длительность видео
            video_file.write(str(strings * 2))
            video_file.close()
            input_file.close()
            time.sleep(1)

            # Запускаем функцию записи видео
            video_script_path = root_path + '/' + "Video.py"
            #python_path = "C:/Users/grish/AppData/Local/Programs/Python/Python38/python.exe"
            python_path = "C:/Users/Админ/AppData/Local/Programs/Python/Python38/python.exe"
            Video_chek = subprocess.Popen([python_path, video_script_path])

            # Запускаем функцию последовательной передачи управляющих команд на плату Ардуино
            serial, command_num = Arduino_Serial(script_file_path=script_file_path,
                                                 errs_path=errs_path,
                                                 Arduino_port=Arduino_port)

            # Возвращаем флаг удачного завершения процесса передачи данных
            if serial == "OK":
                print("Передача данных окончена")
                GUI.print_log("Передача данных окончена")

            # Ожидаем окончания процесса записи видео
            Video_chek.wait()
            # Перепроверяем завершился ли процесс записи видео
            while Video_chek.poll() is None:
                time.sleep(0.5)
            # Выводим код возврата процесса записи видео
            print("Запись видео возвращает:", Video_chek.returncode)
            GUI.print_log("Запись видео возвращает:", Video_chek.returncode)
            returncode = Video_chek.returncode
        # Если отсутствует файл прошивки или проект на ПЛИС, ошибка записывается в файл ошибок
        else:
            errors_file.write("Отсутствует файл прошивки или проект на ПЛИС\n")
            errors_ = 1
            # Задаем пустые значения переменных если файла прошивки нет
            sof_file_name = ""
            sof_path = ""
    # Если отсутствует файл сценария, ошибка записывается в файл ошибок
    else:
        errors_file.write("Отправте данные повторно, включая файл сценария\n")
        errors_ = 1
        # Задаем соответствующие значения переменных, если отсутствует файл сценария
        returncode = 1
        script_file_path = ""
        script_file_name = ""
        sof_file_name = ""
        sof_path = ""

    # Закрываем файл ошибок
    errors_file.close()

    # Повторно перепроверяем наличие файла прошивки
    if not (os.path.exists(sof_path)):
        sof_path = "#"
        sof_name = "#"

    # Запускаем функцию копирования файлов отчетности
    if not(User_path_to_file == ""):
        file_work = File_switch(User_path_to_file=User_path_to_file, root_path=root_path,
                                sof_path=sof_path, script_file_path=script_file_path,
                                sof_file_name=sof_file_name,
                                script_file_name=script_file_name,
                                video_return=returncode)

    # Запускаем функциб удаления лишних файлов
    if User_path_to_file != '':
        folder_send, chek_delete = Delete_files(root_path=root_path, User_path_to_file=User_path_to_file)

        # new_path = root_path.replace('\\', '/', 2)
        folder_delete = root_path + '/' + "Archived"
        file_delete = File_deleting(folder=folder_delete)
        print("Результат очистки архива = ", file_delete)
        GUI.print_log("Результат очистки архива = ", file_delete)
        pp = pprint.PrettyPrinter(indent=4)

    # Указание адреса авторизации
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Проверяем наличие файла токена
    token_name = 'ul_cad_1.json'
    token_path = root_path + '/' + token_name
    if not (os.path.exists(token_path)):
        for root, dirs, files in os.walk('C:/'):
            if files.find(token) != -1:
                token_path = root + '/' + files
    elif os.path.exists(token_path):
        SERVICE_ACCOUNT_FILE = token_path

        # Подключаемся к соответствующему сервису с помощью сервисного аккаунта Google
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials, static_discovery=False)

        # Запускаем функцию определения главной папки
        main_folder_id = Get_main_folder_id(service=service)
        print("Id главной папки = ", main_folder_id)
        GUI.print_log("Id главной папки = ", main_folder_id)
        if User_path_to_file == "":
            mail_name = "error_folder"
        else:
            mail_name = User_path_to_file.split('/', 2)[1]
        upload_file = True
        # Запускаем процесс загрузки файлов до положительного исхода
        while upload_file:
            #try:
            # Запускаем функцию создания папки пользователя
            folder_id = Folder_create(service=service, Users_drive=mail_name, main_folder_id=main_folder_id)
            print("Id текущей папки = ", folder_id)
            # Выгружаем файлы из папки, содержащей итоговый архив
            if User_path_to_file == "":
                err_path = root_path + '/student_zip/error.txt'
                err_dir = root_path + '/student_zip'
                error = open(err_path, 'w')
                error.write("Проблема с обработкой архива в письме.\n Отправьте архив в формате zip")
                error.close()
                error_dir = root_path + '/Archived/Error'
                os.mkdir(error_dir)
                os.chdir(error_dir)
                shutil.make_archive('result', 'zip', err_dir)
                time.sleep(1)
                file_link = File_upload(service=service, folder_id=folder_id, file_path=err_path)
                os.chdir(root_path)
                shutil.rmtree(error_dir)
                main_dir = root_path + '/student_zip'
                for root, dirs, files in os.walk(main_dir):
                    for direc in dirs:
                        shutil.rmtree(root + '/' + direc)
                    for file in files:
                        os.remove(root + '/' + file)
                upload_file = False
            else:
                # for folders, file in os.listdir(folder_send):
                #     if file.endswith("zip"):
                #         file_path = folder_send + "/" + file
                print("ТА САМАЯ ЕБАЛА---------------------------------------------")
                print(folder_send)
                print("Конец ебалы---------------------------------------------\n")
                folder_send = "C:/Project_930/Project_main/Archived"
                file_path = Find_files_by_ext(folder_send, "zip")

                # Получаем ссылку на скачивание данного архива
                file_link = File_upload(service=service, folder_id=folder_id, file_path=file_path)
                print("Ссылка на файл = ", file_link)
                GUI.print_log("Ссылка на файл = ", file_link)
                upload_file = False
            delete_chek = Old_files_delete(main_folder_id, service)
            print(delete_chek)
            upload_file = False
            # except:
            #     print("Неудача при загрузке файлов на Google Drive")
            #     GUI.print_log("Неудача при загрузке файлов на Google Drive")
    else:
        print("Отсутствует файл токена")
        GUI.print_log("Отсутствует файл токена")
    return ("OK", pr_type, command_num, file_link, errors_)

# Launch(User_path_to_file="student_zip/grisha.petuxov", root_path="C:/Project_930/Prototype_with_mail_bot_TO_EXE")
