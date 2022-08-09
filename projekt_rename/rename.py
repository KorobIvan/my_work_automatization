from tkinter import *
import subprocess
import os
import tkinter

  
def clicked():
    '''Use click on button'''  
    def copy_file(dir_1, dir_2, new_number, last_name=''):
        '''Copy and rename file'''
        for i in os.listdir(dir_1):
            way = dir_1 + '\\' + i
            if len(i) == 21 and i[:11] == last_name:
                new_file_name = new_number + i[11:]
                new_way = dir_2 + '\\' + new_file_name
                status = subprocess.call(f'copy {way} {new_way}', shell=True)
            else:
                new_way = dir_2 + '\\' + i
                status = subprocess.call(f'copy {way} {new_way}', shell=True)

    first_dir =  txt.get() 
    new_dir = txt1.get()  
    new_name = txt2.get()  
    last_name = txt3.get()  

    copy_file(first_dir, new_dir, new_name, last_name)


window = Tk()  
window.title("Переименовщик файлов")  
window.geometry('800x300') 

last_way = Label(window, text="Введите ссылку на исходную папку")  
last_way.grid(column=0, row=0)
new_way = Label(window, text="Введите ссылку на новую папку")  
new_way.grid(column=0, row=1)
last_name = Label(window, text="Введите старое имя")  
last_name.grid(column=0, row=2)
new_name = Label(window, text="Введите новое имя")  
new_name.grid(column=0, row=3)  

txt = Entry(window,width=40)  
txt.grid(column=1, row=0)
txt1 = Entry(window,width=40)  
txt1.grid(column=1, row=1)
txt2 = Entry(window,width=40)  
txt2.grid(column=1, row=2)
txt3 = Entry(window,width=40)  
txt3.grid(column=1, row=3)

btn = Button(window, text="Копировать файлы", command=clicked)  
btn.grid(column=5, row=6)

window.mainloop()

