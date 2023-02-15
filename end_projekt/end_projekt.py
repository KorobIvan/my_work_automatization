import os

'''Необходимо реализовать:
- лишние дхф
- не добавлять в дхф те файлы, которые лежат в других папках (дерево токарка и т.д.)'''


def list_on_txt(way: str) -> list:
    '''Преобразует информацию из отчета в список с именами, начинающимися на ЦИУЛ'''
    file = []
    file_on_proj = open(f'{way}//Отчет.txt')
    for i in file_on_proj.read().split('\n'):
        if 'ЦИУЛ' in i:
            file.append(' '.join(i.split()))
    file_on_proj.close()
    return file


def  compare_plan_with_dir(way: str) -> list|str:
    '''Сравнивает файлы в отчете и в папке проекта.'''
    file_on_dir =  os.listdir(way)
    not_end = []
    for i in file_on_dir:
        z = i
        if ' СБ ' in i:
            z = i.replace(' СБ ', ' ')
        if  '.cdw' in z and z[:-4] not in list_on_txt(way):
            not_end.append(i)
    if not_end == []:
        return 'Все dxf сделаны!'
    else:    
        return not_end

def  compare_dir_with_plan(way: str) -> list|str:
    '''Сравнивает файлы в папке проекта и в отчете.'''
    file_on_dir =  os.listdir(way)
    not_end = []
    for i in list_on_txt(way):
        if i + '.cdw' not in file_on_dir :#and i.split()[0] + ' СБ ' + i.split()[1] + '.cdw' not in file_on_dir:
            not_end.append(i)
    if not_end == []:
        return 'Все чертежи сделаны!'
    else:    
        return not_end

def compare_dxf_with_plan(laser_way: str) -> list|str:
    '''Сравнивает файлы в отчете с файлами, 
    которые лежат в лазерной резке и говорит каких дхф не хвататет.'''
    file_on_dir =  os.listdir(f'{laser_way}')
    not_end = []
    for i in list_on_txt(way):
        if i + '.dxf' not in file_on_dir and '.00 ' not in i:
            not_end.append(i)
    if not_end == []:
        return 'Все dxf сделаны!'
    else:    
        return not_end

def compare_plan_with_dxf(laser_way: str) -> list|str:
    ''''''
    pass

def res() -> None:
    '''Сохраняет результаты сравнений в файл.'''
    file = open(f'{way}\Результат отчета.txt', 'w', encoding='utf-8')
    if compare_plan_with_dir(way) != 'Все чертежи сделаны!':
        file.write(f'Чертежи, которые готовы, но нет в отчете:\n\n')
        for i in compare_plan_with_dir(way):
            file.write(f'{i}\n')
    else:
        file.write(compare_plan_with_dir(way))
    file.write(f'--------------------------------\n')
    if compare_dir_with_plan(way) != 'Все чертежи сделаны!':
        file.write(f'Детали и сборки, которые есть в отчете, но нет чертежей в папке:\n\n')
        for i in compare_dir_with_plan(way):
            file.write(f'{i}\n')
    else:
        file.write(compare_dir_with_plan(way))
    file.write(f'--------------------------------\n')
    if compare_dxf_with_plan(laser_way) != 'Все dxf сделаны!':
        file.write(f'Детали которые есть в проекте, но нет Dxf:\n\n')
        for i in compare_dxf_with_plan(laser_way):
            file.write(f'{i}\n')
    file.close()


way = r'L:\ПК\Конструкторский отдел\2. КОНСОЛИ\ВНИИР\Пр. 20386\ДВИЕ.469151.299СБ(ЦИУЛ.204520.00.00) Резервный пульт управления движением'
laser_way = r'L:\Drawings\Лазерная резка\25. ПК\2.КОНСОЛИ\ВНИИР\Пр. 20386\ДВИЕ.469151.299СБ(ЦИУЛ.204520.00.00) Резервный пульт управления движением'

res()

