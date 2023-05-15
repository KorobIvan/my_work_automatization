import os
from tkinter import *

'''
Добавить проверку на задвоение.
Добавить Диалоговое окно на изменение имени поиска.'''

class ListWithAllFile:
    
    serch_exceptions = ['Исх', 'Приборы', 'Согл', 'Растомат', 'Амортизатор',\
        'Петля', 'Замок', 'Поручень', 'Петля 1032-U1 Emka']  #Сюда заносить все папки исключения

    def __init__(self, way:str, laser_way:str='') -> None:
        self.way = way.strip()
        self.laser_way = laser_way
        self.code_name = ['ЦИУЛ', 'ДИШУ']

    def set_way(self, way):
        self.way = way

    def set_laser_way(self, laser_way):
        self.laser_way = laser_way

    def serch_file_on_dir(self, way:str) -> list:
        '''Возвращает список файлов, находящихся в указанной папке.'''
        list_of_file_on_dir = os.listdir(way)
        return list_of_file_on_dir

    def list_of_dir_on_dir(self, way:str) -> list:
        '''Возвращает список директорий, которые находятся в главной директори.'''
        direct_in_direct = []
        main_dir = self.serch_file_on_dir(way)
        for i in main_dir:
            if '.' not in i and i not in ListWithAllFile.serch_exceptions:
                direct_in_direct.append(i)
        return direct_in_direct

    def list_with_all_dir(self, way:str)-> list:
        '''Возвращает список всех путей вложенных дирректорий(глубина вложенности не имеет значения),
        которые есть в указанной папке.'''
        serche_dir = self.list_of_dir_on_dir(way)
        if serche_dir != []:
            for i in serche_dir:  #Пробирает все папки, которые вложенны в указанную
                if self.list_of_dir_on_dir(f'{way}\\{i}') != []:  
                    for j in self.list_of_dir_on_dir(f'{way}\\{i}'):
                        serche_dir.append(f'{i}\\{j}')             
        return serche_dir

    def all_file_in_all_dir(self, way:str) -> list:
        '''Возвращает все файлы, которые есть во всех вложенных дирректориях.'''
        file = self.serch_file_on_dir(way)
        all_file = []
        for i in self.list_with_all_dir(way):
            file.extend(self.serch_file_on_dir(f'{way}\\{i}'))
        for i in file:
            if '.' in i:
                all_file.append(i)    
        return all_file
    
    def all_file_with_needed_format(self, way:str,  format:str) -> list:
        list_with_format = []
        all_file = self.all_file_in_all_dir(way)
        for i in format.split(', '):
            for j in all_file:
                if i in j:
                    list_with_format.append(j)
        return list_with_format
    
class OpenReport(ListWithAllFile):
    def list_on_txt(self) -> list:
        '''Преобразует информацию из отчета в список с именами, начинающимися на self.code_name.'''
        file = []
        with open(f'{self.way}//Отчет.txt') as file_on_proj:                                                            # Дописать интерфейс с возможностью добавлять имена в поля поиска
            for i in file_on_proj.read().split('\n'):
                if i[:4] in self.code_name:
                    file.append(' '.join(i.split()))
        return file

    def all_file_mark_name(self):
        all_code_name = []
        scip_name = ['', 'Обоз']
        with open(f'{self.way}//Отчет.txt') as file_on_proj:
            for i in file_on_proj.read().split('\n'):
                if i[:4] not in all_code_name and i[:4].strip() not in scip_name:
                    all_code_name.append(i[:4])
        return all_code_name

    def add_mark_name(self, name):
        self.code_name.append(name)

    def del_mark_name(self, name):
        self.code_name.remove(name)

        
class DataCompaere(OpenReport):
    def  compare_plan_with_dir(self) -> tuple:
        '''Сравнивает файлы в папке проекта и в отчете.
        возвращает кортеж с 2 списками:
        [0] - список лишних чертежей.
        [1] - список лишних деталей.'''
        designs_on_dir = self.all_file_with_needed_format(self.way, '.cdw')
        details_on_dir = self.all_file_with_needed_format(self.way, '.m3d')
        compare_with_designs = []
        compare_with_details = []
        report = ' '.join(self.list_on_txt())
        for i in designs_on_dir:
            if i.split()[0] not in report:
                compare_with_designs.append(i)
        for i in details_on_dir:
            if i.split()[0] not in report:
                compare_with_details.append(i)
        return (compare_with_designs, compare_with_details)
        
    def  compare_dir_with_plan(self) -> list:
        '''Сравнивает чертежи в отчете и в папке проекта.
        Возвращает список имен файлов, которые есть в отчете, но нет в папке.'''
        compare_with_designs = []
        all_file = ' '.join(self.all_file_with_needed_format(self.way,'.cdw'))
        for i in self.list_on_txt():
            if i != '' and i.split()[0] not in all_file:
                compare_with_designs.append(i) 
        return compare_with_designs
    
    def compare_dxf_with_plan(self) -> list:
        '''Сравнивает файлы в отчете с файлами, которые лежат в лазерной резке.
         Возвращает список имен файлов, дхф или других рабочих форматов, которых не хвататет.'''
        compare_with_laser_file = []
        all_file = ' '.join(self.all_file_with_needed_format(self.laser_way, '.dxf, .x_t, .stp, .pdf'))
        for i in self.list_on_txt():    
            try:
                if i.split()[0] not in all_file and '.00 ' not in i:
                    compare_with_laser_file.append(i)
            except:
                continue
        return compare_with_laser_file
    
    def compare_plan_with_dxf(self) -> list:
        '''Сравнивает файлы в отчете с файлами, которые лежат в лазерной резке.
         Возвращает список лишних файлов.'''
        compare_laser_file_with_plan = []
        ignore_format = ['xls']
        report = ' '.join(self.list_on_txt())
        for i in self.all_file_in_all_dir(self.laser_way):
            try:
                if i.split()[0] not in report and i[-3:] not in ignore_format:
                    compare_laser_file_with_plan.append(i)
            except:
                continue
        return compare_laser_file_with_plan
    
class Report(DataCompaere):
    def save_report_on_file(self) -> None:
        '''Сохраняет результаты проверок в файл.'''
        try:    
            with open(f'{self.way}\Результат отчета.txt', 'w', encoding='utf-8') as file:
                
                if self.compare_plan_with_dir()[0] != []:
                    file.write(f'Чертежи, которые готовы, но нет в отчете:\n\n')
                    for i in self.compare_plan_with_dir()[0]:
                        file.write(f'{i}\n')
                else:
                    file.write('Лишних чертежей нет!\n')
                
                file.write(f'\n--------------------------------\n\n')

                if self.compare_plan_with_dir()[1] != []:
                    file.write(f'Детали, которые готовы, но нет в отчете:\n\n')
                    for i in self.compare_plan_with_dir()[1]:
                        file.write(f'{i}\n')
                else:
                    file.write('Лишних деталей нет!\n')
                
                file.write(f'\n--------------------------------\n\n')
                
                if self.compare_dir_with_plan() != []:
                    file.write(f'Детали и сборки, которые есть в отчете, но нет чертежей в папке:\n\n')
                    for i in self.compare_dir_with_plan():
                        file.write(f'{i}\n')
                else:
                    file.write('Все чертежи сделаны!')
                
                file.write(f'\n--------------------------------\n\n')

                if self.laser_way != '':
                    if self.compare_dxf_with_plan() != []:
                        file.write(f'Детали которые есть в проекте, но нет Dxf:\n\n')
                        for i in self.compare_dxf_with_plan():
                            file.write(f'{i}\n')
                    else:
                        file.write('Все dxf сделаны!')

                    file.write(f'\n--------------------------------\n\n')

                    if self.compare_plan_with_dxf() != []:
                        file.write(f'Лишние файлы в лазерной резке:\n\n')
                        for i in self.compare_plan_with_dxf():
                            file.write(f'{i}\n')
                    else:
                        file.write('Лишних файлов нет!')
        except FileNotFoundError:
            return 'Убедитесь в правильности указанного пути!'
        else:
            return 'Отчет готов!'


class GUI(Frame):
    
    def __init__(self, window):
        window.title("Отчет по проекту")  
        window.geometry('800x300')

        self.way_label = Label(window, text="Введите ссылку на папку с отчетом")  
        self.way_label.grid(column=0, row=0)
        self.laser_way_label = Label(window, text="Введите ссылку на лазерную резку")  
        self.laser_way_label.grid(column=0, row=1)
        self.result = Label(window)
        self.result.grid(column=1, row=3)

        self.txt = Entry(window,width=60)  
        self.txt.grid(column=1, row=0)
        self.txt1 = Entry(window,width=60)  
        self.txt1.grid(column=1, row=1)

        self.create_file = Button(window, text='Создать отчет', command=self.clicked)  
        self.create_file.grid(column=3, row=3)
        self.close_window = Button(window, text='Закрыть', command=lambda:self.close(window))
        self.close_window.grid(column=3, row=5)
        self.get_new_name = Button(window, text='Проверить наличие других имен', command=self.new_name)
        self.get_new_name.grid(column=3, row=4)

        self.serch_try = None
    
    def way_funk(self):
        way = self.txt.get()
        laser_way = self.txt1.get()
        if self.serch_try == None:
            self.serch_try = Report(way, laser_way)
    
    def clicked(self):
        self.way_funk()
        self.serch_try.save_report_on_file()
        self.result['text'] = self.serch_try.save_report_on_file()

    def new_name(self):
        new_window = Tk()
        new_window.geometry('500x700')
        self.way_funk()
        row_button = len(self.serch_try.all_file_mark_name())
        
        def update_info_funk(*args):
            all_name['text'] = " ".join(self.serch_try.code_name)

        def add_name(i):
            self.serch_try.add_mark_name(i)
            update_info_funk()
            clic_button()
        
        def del_name(i):
            self.serch_try.del_mark_name(i)
            update_info_funk()
            clic_button()

        def clic_button():
            row_count = 0
            for i in self.serch_try.all_file_mark_name():
                add_arg = NORMAL
                del_arg = NORMAL
                if i in self.serch_try.code_name:
                    add_arg = DISABLED 
                if add_arg == NORMAL:
                    del_arg = DISABLED
                if len(self.serch_try.code_name) <= 1:
                    del_arg = DISABLED
                Label(new_window, text=f'{i}', width=20).grid(column=0, row=row_count)
                Button(new_window, text='Добавить', command=lambda i=i:add_name(i), state=add_arg).grid(column=1, row=row_count)
                Button(new_window, text='Удалить', command=lambda i=i:del_name(i), state=del_arg).grid(column=2, row=row_count)
                row_count += 1

        clic_button()
        
        update_line = StringVar()
        update_line.trace_add('write', update_info_funk)

        all_name = Label(new_window,width=30, text=f'{" ".join(self.serch_try.code_name)}')
        all_name.grid(column=1, row=row_button+1)
        close_btn = Button(new_window, text="Закрыть", command=lambda:self.close(new_window))  
        close_btn.grid(column=2, row=row_button+3)
        upd_w = Button(new_window, text="Обновить", command=lambda:self.update_info(new_window))  
        upd_w.grid(column=2, row=row_button+2)

        

    def close(self, name):
        name.destroy()


window = Tk()
invent = GUI(window)
window.mainloop()
