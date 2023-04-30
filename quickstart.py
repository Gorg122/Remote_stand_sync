from __future__ import print_function

import shutil

import httplib2
import os
import os.path
import io
import zipfile

from googleapiclient.http import MediaIoBaseDownload
from apiclient import discovery
from googleapiclient import discovery
# import googleapiclient.discovery
# from gooleapiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


import GUI
from File_work import Launch
from emailsend import send_email
import pymysql.cursors
import datetime
import time
import sys

from win32com.shell import shell, shellcon  # Импортируем энкодер
from File_work import *  ## Исспользуются переменные:
from GUI import *

thread = 0
######
###### command_num - колличество команд.
######
from Sof_to_FPGA import *  ## Исспользуются переменные:
######
######pr_type - тип проекта
######
######
import requests



def empty(confirm, show_progress, sound):
    recycle_bin_path = "C:\$RECYCLE.BIN"
    for files in os.listdir(recycle_bin_path):
        print(files)
    try:
        flags = 0
        if not confirm:
            flags |= shellcon.SHERB_NOCONFIRMATION
        if not show_progress:
            flags |= shellcon.SHERB_NOPROGRESSUI
        if not sound:
            flags |= shellcon.SHERB_NOSOUND
        shell.SHEmptyRecycleBin(None, None, flags)
        print("Корзина очищена")
        GUI.print_log("Корзина очищена")
    except:
        print("Корзина пуста")
        GUI.print_log("Корзина пуста")


def sub_main(service, root_path):
    while True:
        start_time = time.time()
        # os.chdir(root_path)

            #email_name_cur = str(email.split('@')[0])
            email_name_cur = "grisha.petuxov"
            print(email_name_cur)
            GUI.print_log(email_name_cur)
            file_p = root_path + "/Archived/" + email_name_cur
            launch_stat, pr_type, command_num, URL, errors_ = Launch(User_path_to_file=path_firmware, root_path=root_path)
            print("LAUNCH_STAT = ", launch_stat)
            GUI.print_log("LAUNCH_STAT = ", launch_stat)
            if launch_stat == "OK":
                # new_users_dir = "C:\PROJECT_930\Prototype_new_2\Archived"
                print(send_email(addr_to=email,  # "sasha.lorens@yandex.ru",
                                 msg_subj="Ваша прошивка",
                                 msg_text="Ваши файлы",
                                 files='',
                                 URL=URL,
                                 errors_ = errors_))
                stat_5 = change_status(GLOBAL_PC_ID, 5)[1]
                if path_firmware == "":
                    main_dir = root_path + '/' + 'student_zip'
                else:
                    main_dir = root_path + '/' + path_firmware.split('/')[0]
            if path_firmware != '':
                file_path = root_path + "/" + path_firmware
                file_size = os.path.getsize(file_path)  ##!!!!!!!!!!!!!!

            if main_dir != root_path or main_dir != root_path + '/':
                for dirs in os.listdir(main_dir):
                    # os.rmdir(new_path + main_dir + "/" + dirs)
                    shutil.rmtree(main_dir + '/' + dirs)
            else:
                print("SDFKMSJKFZNKLJFSRHFSRZBLHJFSBRGFLBHGRHLG RSG SRHLJG RLHGJD BGHLJDLJHG")
            empty(confirm=False, show_progress=True, sound=True)
        GUI.print_log("--- %s seconds ---" % (time.time() - start_time))
        while GUI.flag_stop:
            time.sleep(1)
        time.sleep(20)

def Find_files_by_name(dir_path, filename):
    for root, dirs, files in os.walk(dir_path):  # В цикле проходим все папки и файлы в корневой папке
        if filename in files:   # Производим поиск по названию файла
            filepath = os.path.join(root, filename)  # Добавляем в путь папки и необходимый файл
            return filepath
        else:
            return 0

def Find_files_by_ext(dir_path, file_ext):
    for root, dirs, files in os.walk(dir_path):  # В цикле проходим все папки и файлы в корневой папке
        for file in files:
            if file.endswith(file_ext):     # Производим поиск по расширению файла
                filepath = os.path.join(root, file)  # Добавляем в путь папки и необходимый файл
                return filepath
            else:
                return 0

def CAD_LOOP():
    service = main()
    GUI.print_log("Начало работы")

    path = sys.argv[0]
    path_len = len(path.split('/')) - 1
    new_path = path.split('/')[:-1]
    new_str_path = "/".join(new_path)
    print(new_str_path)
    GUI.print_log(new_str_path)
    root_path = new_str_path

    config = configparser.ConfigParser()
    config_dir = root_path + '/' + "Config.ini"
    config.read(config_dir)
    config_path = config['Direc']['path']
    if config_path == root_path:
        print("Путь к папке проекта существует")
    else:
        config['Direc']['path'] = root_path
        with open('Config.ini', 'w') as configfile:
            config.write(configfile)
        print("Путь до текущей директории был изменен")

    print("Root_path = ", root_path)
    sub_main(service, root_path=root_path)


if __name__ == '__main__':
    GUI.main_start_gui()

