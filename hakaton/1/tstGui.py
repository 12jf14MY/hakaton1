from tkinter import *
from tkinter.ttk import Radiobutton, Progressbar
from tkinter import messagebox, ttk, filedialog


d1 = 'country.txt'
d2 = 'python.txt'
d3 = 'testik.txt'


class GuiTest():
    """Графический интерфейс для test."""

    def __init__(self):
        """Инициализация окна."""
        # Рабочее окно.
        self.window = Tk()
        self.qv = ''
        self.res = ''
        self.ind = 0


    def btn_enter(self):

        self.res = self.txt.get()
        print(self.res, )

        self.lbl1 = Label(self.window, font=('Arial Bold', 15), text=self.qv)
        self.lbl1.place(x=30, y=110)



    def cliked_country(self):

        self.btn_country.destroy()
        self.btn_python.destroy()
        self.btn_fun_test.destroy()
        self.txt = Entry(self.window, font='right')
        self.txt.place(height=30, width=300, x=12, y=65)
        self.txt.focus()
        self.btn_enter = Button(self.window, text='Ответить', foreground='White', bg='Green', font=('Arial Bold', 14),
                                command=self.btn_enter)
        self.btn_enter.place(height=30, width=85, x=360, y=65)

        def test(file):
            kol = 0

            with open(file, 'r', encoding='utf-8') as f:
                vopr_f = f.readlines()

            vsego = int(len(vopr_f) / 2)

            vopr = []
            st = 1
            for i in vopr_f:

                if st == 1:
                    newi = i.replace("\n", "")
                    q = []
                    q.append(newi)
                    st = 2
                else:
                    newi = i.replace("\n", "")
                    q.append(newi)
                    vopr.append(q)
                    st = 1

            #print(vopr)
            i = vopr[self.ind]
            otv = self.res


            self.lbl.config(text=i[0], font=('Arial Bold', 10))
            self.res = self.txt.get()
            if otv.upper() == i[1].upper():
                self.qv = "Верно"
                kol = kol + 1
            else:
                self.qv = (f"Не верно, Верный ответ {i[1]}")

            finish = (kol, " верных ответов из ", vsego)


        test(d1)
    # def question_ans(self):
    #     otv = self.res
    #     self.lbl.config(text=question[0], font=('Arial Bold', 10))
    #     if otv.upper() == question[1].upper():
    #         self.qv = "Верно"
    #         return True
    #     else:
    #         self.qv = (f"Не верно, Верный ответ {question[1]}")
    #         return False


    def cliked_python(self):
        self.btn_country.destroy()
        self.btn_python.destroy()
        self.btn_fun_test.destroy()
        self.txt = Entry(self.window, font='right')
        self.txt.place(height=30, width=300, x=12, y=65)
        self.txt.focus()
        self.btn_enter = Button(self.window, text='Ответить', foreground='White', bg='Green', font=('Arial Bold', 14),
                                command=self.btn_enter)
        self.btn_enter.place(height=30, width=85, x=360, y=65)

        def test(file):
            kol = 0

            with open(file, 'r', encoding='utf-8') as f:
                vopr_f = f.readlines()

            vsego = int(len(vopr_f) / 2)

            vopr = []
            st = 1
            for i in vopr_f:

                if st == 1:
                    newi = i.replace("\n", "")
                    q = []
                    q.append(newi)
                    st = 2
                else:
                    newi = i.replace("\n", "")
                    q.append(newi)
                    vopr.append(q)
                    st = 1

            #print(vopr)
            i = vopr[self.ind]
            otv = self.res
            self.lbl.config(text=i[0], font=('Arial Bold', 10))
            if otv.upper() == i[1].upper():
                self.qv = "Верно"
                kol = kol + 1
            else:
                self.qv = (f"Не верно, Верный ответ {i[1]}")

            finish = (kol, " верных ответов из ", vsego)

        test(d2)

    def cliked_funtest(self):
        self.btn_country.destroy()
        self.btn_python.destroy()
        self.btn_fun_test.destroy()
        self.txt = Entry(self.window, font='right')
        self.txt.place(height=30, width=300, x=12, y=65)
        self.txt.focus()
        self.btn_enter = Button(self.window, text='Ответить', foreground='White', bg='Green', font=('Arial Bold', 14),
                                command=self.btn_enter)
        self.btn_enter.place(height=30, width=85, x=360, y=65)

        def test(file):
            kol = 0

            with open(file, 'r', encoding='utf-8') as f:
                vopr_f = f.readlines()

            vsego = int(len(vopr_f) / 2)

            vopr = []
            st = 1
            for i in vopr_f:

                if st == 1:
                    newi = i.replace("\n", "")
                    q = []
                    q.append(newi)
                    st = 2
                else:
                    newi = i.replace("\n", "")
                    q.append(newi)
                    vopr.append(q)
                    st = 1

            print(vopr)
            i = vopr[self.ind]
            otv = self.res
            self.lbl.config(text=i[0], font=('Arial Bold', 10))
            if otv.upper() == i[1].upper():
                self.qv = "Верно"
                kol = kol + 1
            else:
                self.qv = (f"Не верно, Верный ответ {i[1]}")

            finish = (kol, " верных ответов из ", vsego)

        test(d3)

    def build_window(self):
        """Построение окна интерфейса"""
        self.window.geometry('630x200+300+200')
        self.window.title("Your Test")

    def build_description(self):
        """Построение краткого описания действия для пользвателя"""
        message1 = "Выберите тест:"
        self.lbl = Label(self.window, font=('Arial Bold', 20), text=message1)
        self.lbl.place(x=30, y=25)

    def build_btn(self):
        """Построение конпок"""
        self.btn_country = Button(self.window, text='Страны', foreground='White', bg='Green', font=('Arial Bold', 14),
                                  command=self.cliked_country)
        self.btn_country.place(height=30, width=85, x=360, y=70)
        self.btn_python = Button(self.window, text='Python', foreground='White', bg='Red', font=('Arial Bold', 14),
                                 command=self.cliked_python)
        self.btn_python.place(height=30, width=85, x=30, y=70)
        self.btn_fun_test = Button(self.window, text='Fun Test', foreground='White', bg='Orange',
                                   font=('Arial Bold', 14,),
                                   command=self.cliked_funtest)
        self.btn_fun_test.place(height=30, width=85, x=200, y=70)

    def build_gui(self):
        """Сборка графического интерфейса"""
        # Строит:
        self.build_window()  # Рабочее окно
        self.build_description()  # Краткое описание действий для пользователя
        self.build_btn()  # Кнопки выбора файла и старта

        self.window.mainloop()  # Отображает все.


pr = GuiTest()
pr.build_gui()
