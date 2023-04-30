import os.path
import subprocess
import configparser
#from quickstart import Find_files_by_name, Find_files_by_ext
#import GUI

global pr_type
pr_type = 100

def Find_files_by_name(dir_path, filename):
    for root, dirs, files in os.walk(dir_path):  # В цикле проходим все папки и файлы в корневой папке
        if filename in files:   # Производим поиск по названию файла
            filepath = os.path.join(root, name)  # Добавляем в путь папки и необходимый файл
            return filepath

    print("Такого файла нет")
    return 0

def Find_files_by_ext(dir_path, file_ext):
    for root, dirs, files in os.walk(dir_path):  # В цикле проходим все папки и файлы в корневой папке
        for file in files:
            if file.endswith(file_ext):     # Производим поиск по расширению файла
                filepath = os.path.join(root, file)  # Добавляем в путь папки и необходимый файл
                return filepath

    print("Такого файла нет")
    return 0

def FPGA_flash(User_path, FPGA_num, root_path):
    global pr_type
    # Задаем ключ успешной прошивки платы
    main_key = ["Quartus Prime Programmer was successful. 0 errors"]

    # Обращаемся к файлу настроек
    config = configparser.ConfigParser()
    config_path = root_path + '/' + "Config.ini"
    config.read(config_path)

    # Задаем директории исполняемых файлов quartus
    Quartus_pgm_path = config['Quartus']['quartus_pgm_path']
    Quartus_sh_path = config['Quartus']['quartus_sh_path']
    root_directory = config['Direc']['Path']

    # Задаем заглушки путей к основным файлам
    qpf_path = "Not_yet"
    qsf_path = "Not_yet"
    sof_path = "Not_yet"

    # Создаем файл отчета о прошивке платы ПЛИС
    log_file = open(root_directory + '/' + User_path + "/JTAG_config.txt", "w")

    # Проверка существования пути к quartus_pgm.exe
    if os.path.exists(Quartus_pgm_path):  # Проверяем существует ли данный путь исполняемых файлов
        Quartus_pgm_path = Quartus_pgm_path

    # В случае если такого пути нет, производим поиск пути исполняемых файлов в корневой папке
    else:
        # Задаем корневую папку
        find_in = "C:/intelFPGA_lite"
        name = "quartus_pgm.exe"
        Find_files_by_name(find_in, name)
        # Обновляем в файле настроек путь до quartus_pgm.exe
        config['Quartus']['quartus_pgm_path'] = Quartus_pgm_path
        with open('Config.ini', 'w') as configfile:
            config.write(configfile)
        print("Текущий путь к quartus_pgm.exe = ", Quartus_sh_path)
        #GUI.print_log("Текущий путь к quartus_pgm.exe = ", Quartus_sh_path)

    # Проверяем существует ли данный путь исполняемых файлов
    if os.path.exists(Quartus_sh_path):
        Quartus_sh_path = Quartus_sh_path

    # В случае, если такого пути не существует производим поиск в корневой папке
    else:
        find_in = "C:/intelFPGA_lite"  # Задаем корневую папку
        name = "quartus_sh.exe"
        Find_files_by_name(find_in, name)
        config['Quartus']['quartus_sh_path'] = Quartus_sh_path
        # Обновляем в файле настроек путь до quartus_sh.exe
        with open('Config.ini', 'w') as configfile:
            config.write(configfile)
        print("Текущий путь к quartus_sh.exe = ", Quartus_sh_path)
        #GUI.print_log("Текущий путь к quartus_sh.exe = ", Quartus_sh_path)

    # Производим поиск файла с расширением qpf
    users_directory = root_directory + '/' + User_path
    found = Find_files_by_ext(users_directory, '.qpf')
    if found:
        pr_type = 0
        qpf_path = found
        print("Путь к qpf файлу пользователя = ", qpf_path, '\n')
        #GUI.print_log("Путь к qpf файлу пользователя = ", qpf_path)

    # Производим поиск файла с расширением qsf
    found = Find_files_by_ext(users_directory, '.qsf')
    if found:
        pr_type = 0
        qsf_path = found
        print("Путь к qsf файлу пользователя = ", qsf_path, '\n')
        #GUI.print_log("Путь к qsf файлу пользователя = ", qsf_path)

    # Производим поиск файла с расширением sof
    found = Find_files_by_ext(users_directory, '.sof')
    if found:
        pr_type = 1
        sof_path = found
        print("Путь к sof файлу пользователя = ", sof_path)
        #GUI.print_log("Путь к sof файлу пользователя = ", sof_path)

    # Если пользователь отправил проект, в котором есть qpf и qsf файлы
    if (os.path.exists(qpf_path)) and (os.path.exists(qsf_path)) and not (os.path.exists(sof_path)):
        # Задаем название файла отчета о компиляции проекта
        Compil_file = "Proj_compil_result.txt"
        # Команда компиляции прокта средствами quartus_sh.exe
        command = "{0} --flow compile <{1}> [-c {2}] >{3}".format(Quartus_sh_path, qpf_path, qsf_path, Compil_file)
        # Изменяем директорию на папку пользователя, чтобы компиляция проекта производилась в ней
        os.chdir(root_directory + '/' + User_path)
        print(root_directory + '/' + User_path)

        print("Проект ПЛИС компилируется\n")
        #GUI.print_log("Проект ПЛИС компилируется")
        # Начинаем процесс компиляции проекта пользователя
        Project_compilation1 = subprocess.run(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE, shell=True)
        # Печатаем вывод консоли, и возвращаемое значение данной функции
        print(Project_compilation1.stdout, '\n')
        print(Project_compilation1, '\n')
        print("Компиляция окончена\n")
        #GUI.print_log("Компиляция проекта ПЛИС окончена")
        #GUI.print_log(Project_compilation1.stdout, '\n')
        # Изменяем дирректорию на изначальную
        os.chdir(root_directory)

    # Произвводим поиск файла с расширением sof в папке пользователя
    sof_path = Find_files_by_ext(users_directory, '.sof')
    print(sof_path)

    # Если файл прошивки существует, начинаем поиск подключенной платы ПЛИС
    if os.path.exists(sof_path):
        print("Выводим список подключенных устройств")
        # Выводим список всех подключенных плат средствами quartus_pgm.exe
        curent_FPGA = subprocess.run(Quartus_pgm_path + " -l", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     shell=True, text=True)
        print(curent_FPGA, "\n")
        # print(curent_FPGA.returncode,"\n") # флаг успешного выполнения команды
        # print(curent_FPGA.stdout,"\n") # Вывод консоли
        fpga_list = curent_FPGA.stdout.split("Info: Processing started:", 2)[0]
        #GUI.print_log("Список подключенных устройств\n", fpga_list)

        if not curent_FPGA:
            #GUI.print_log("Плата ПЛИС не найдена")
            raise IOError("Плата ПЛИС не найдена")


        # Получаем номер той платы, которую в данный момент необходимо прошивать
        FPGA_num = FPGA_num
        str = "{}) ".format(FPGA_num)
        # В случае, если плата с заданным номером существует, определяем порт её подключения как основной
        if curent_FPGA.stdout.find(str) != -1:
            curent_port = curent_FPGA.stdout.split(str, 2)[1]
            curent_port = curent_port.split('\n', 1)[0]
            print(curent_port)
        # Если такой платы не существует, выводим соответствую ошибку
        else:
            #GUI.print_log("Плата ПЛИС с заданым индексом не найдена")
            raise IOError("Плата ПЛИС с заданным индексом не найдена")


        # Выводим список устроств, подключенных к данному порту платы
        modules_FPGA = subprocess.run("{0} -c \"{1}\" -a".format(Quartus_pgm_path, curent_port), stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, shell=True, text=True)
        i = 0

        # Отделяем от всего вывода консоли информацию о подключенных устроствах
        cur_dev = modules_FPGA.stdout.rsplit('Info: ***************', 2)[0]
        device_numbers = cur_dev.split('\n')

        # В случае, если плата ПЛИс имеет более 1 ядра
        if len(device_numbers) > 4:
            curent_device = modules_FPGA.stdout.split('\n', 3)[2]
            #################### Обратить внимание при использовании DE10-NANO ##########################
            curent_device = str(curent_device[12:36])
            print("Текущая плата =", curent_device)
            #GUI.print_log("Текущая плата =", curent_device)
            print("Несколько ядер")
            #GUI.print_log("Плата ПЛИС имеет несколько ядер")
            # Производим прошивку необходимого ядра платы ПЛИС
            result = subprocess.run(
                '{0} -m JTAG -c "{1}" -o p;{2}@{3}'.format(Quartus_pgm_path, curent_port, sof_path, i),
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
            fpga_flashed = result.stdout.split("Info: Processing started:", 2)[1]
            print(fpga_flashed, '\n')  # Вывод консоли
            #GUI.print_log(fpga_flashed)
            # Записываем вывод консоли в файл отчета о прошивке платы ПЛИС
            log_file.write(fpga_flashed)
            log_file.close()
            # Обрабатываем 2 состояния завершения прошивки платы
            if result.stdout.count(main_key[0]):
                print("Прошивка платы ПЛИС окончена")
                #GUI.print_log("Прошивка платы ПЛИС окончена")
                return ("OK", pr_type)
            else:
                print("Прошивка платы ПЛИС заверщилась неудачей")
                #GUI.print_log("Прошивка платы ПЛИС заверщилась неудачей")
                return ("Neok")


        # Если плата ПЛИС имеет одно ядро
        else:
            print("Плата ПЛИС имеет одно ядро\n")
            #GUI.print_log("Плата ПЛИС имеет одно ядро")
            print(sof_path, "\n")
            # Производим прошивку платы ПЛИС без указания ядра назначения
            result = subprocess.run('{0} -m JTAG -c "{1}" -o p;{2}'.format(Quartus_pgm_path, curent_port, sof_path),
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                    text=True)
            print("###############################################")
            print(result.stdout)
            print("##################################")
            try:
                fpga_flashed = result.stdout.split("Info: Processing started:", 2)[1]
                print(fpga_flashed, '\n')  # Вывод консоли
                #GUI.print_log(fpga_flashed)
            except:
                fpga_flashed = "Ошибка при прошивке платы ПЛИС"
            print("FPGA FLASHED = ", fpga_flashed)
            # Записываем вывод консоли в файл отчета о прошивке платы ПЛИС
            log_file.write(fpga_flashed)
            log_file.close()
            # print(result.stdout,'\n') # Вывод консоли

            # Обрабатываем 2 состояния завершения прошивки платы
            if result.stdout.count(main_key[0]):
                print("Прошивка платы ПЛИС окончена")
                #GUI.print_log("Прошивка платы ПЛИС окончена")
                return ("OK", pr_type)
            else:
                return ("Прошить плату не удалось", pr_type)

# FPGA_flash(User_path="student_zip/grisha.petuxov", FPGA_num = 1)
