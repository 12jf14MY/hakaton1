import os
import sys
from tkinter import *
import tkinter.messagebox as message
from tkinter import filedialog as file

from testFiles import extract_tests, save_log, send_mail


class GuiTest():
    """Графический интерфейс для test."""
    country_file = 'country.txt'
    python_file = 'python.txt'
    testik_file = 'testik.txt'

    def __init__(self):
        """Инициализация окн и списка вопросов и ответов теста, счетчиков, пользовательских данных."""

        self.window_main = Tk() # Главное окно.
        self.window_test = None  # Окно прохождения теста. Создается по нажатию на кнопку с тестом.

        self.test_name = None # Название запущенного теста.

        self.test_list = [] # Содержит списки формата - [вопрос, правильный ответ]:
        self.number_questions = 0 # Счетчик количества вопросов.
        self.correct_answer = 0 # Количество правильных ответов.
        self.incorrect_answer = 0 # Количество неправильных ответов и пропущенных вопросов.
        self.log = [] # Содержит списки формата - [вопрос, правильный ответ, ответ пользователя].

        # Данные пользователя
        self.user_name = None # Имя.
        self.user_mail = None # Почта.


    def save_pers_data(self):
        """Обработка нажатия кнопки 'сохранить', Сохранение данных пользователя."""

        self.user_name = self.txt_name.get().capitalize()
        self.user_mail = self.txt_mail.get()
        self.reset_data() # Сброс лога и счетчиков при изменении пользователем своих данных.
        message.showinfo('Иноформация', 'Сохранено')

    def insert_pers(self):
        """Вставляет в поле ввода ранее введениые даные, если они есть."""

        if self.user_name !='' and self.user_name != None:
            self.txt_name.insert(0, self.user_name)
        if self.user_mail !='' and self.user_mail != None:
            self.txt_mail.insert(0, self.user_mail)

    def del_pers_data(self):
        """Обработка нажатия кнопки 'удалить'."""

        self.user_name = None
        self.user_mail = None
        self.txt_name.delete(0, 'end')
        self.txt_mail.delete(0, 'end')
        self.reset_data() #Сброс лога и счетчиков при удалении пользователем своих данных.
        message.showinfo('Иноформация', 'Удалено')

    def check_user_data(self):
        """Проверяет ввел ли пользователь имя и почту"""

        if self.user_name != None and self.user_mail != None:
            return True
        else:
            return False

    def reset_data(self):
        """Сбрасывает лог и счетчики."""

        self.log.clear()
        self.number_questions = 0
        self.correct_answer = 0
        self.incorrect_answer = 0

    def add_test(self):
        """Обработка нажатия кнопки 'Загрузить тест'."""

        message.showinfo('Информация', "Для корректного отображения, Ваш тест \nдолжен соответсвовать шаблону построения тестов.")
        user_test = file.askopenfilename(filetypes=(("TXT files", "*.txt"),), initialdir='./')
        # Формирует имя теста.
        self.test_name = user_test[user_test.rfind('/')+1:].replace('.txt', '').capitalize()
        # Условие позволяет запускать и решать только один тест.
        if self.window_test != None:
            self.destroy_window_test()  # Закрытие и удаление запущенных тестов.

        # Если пользователь открыл окно, но не выбрал тест - функция run_test не должна запускаться
        # c пустой строкой из user_test.
        if user_test != '':
            self.run_test(user_test)  # Запуск теста.


    def cliked_python(self):
        """Обработка нажатия кнопки 'Python'."""

        self.test_name = GuiTest.python_file.replace('.txt', '').capitalize()
        # Условие позволяет запускать и решать только один тест.
        if self.window_test != None:
            self.destroy_window_test() # Закрытие и удаление запущенных тестов.
        self.run_test(GuiTest.python_file) # Запуск теста.

    def cliked_funtest(self):
        """Обработка нажатия кнопки 'Testik'."""

        self.test_name = GuiTest.testik_file.replace('.txt', '').capitalize()
        # Условие позволяет запускать и решать только один тест.
        if self.window_test != None:
            self.destroy_window_test() # Закрытие и удаление запущенных тестов.
        self.run_test(GuiTest.testik_file) # Запуск теста.

    def cliked_country(self):
        """Обработка нажатия кнопки 'Cтраны'."""

        self.test_name = GuiTest.country_file.replace('.txt', '').capitalize() # Формирует и сохраняет имя теста
        # Условие позволяет запускать и решать только один тест.
        if self.window_test != None:
            self.destroy_window_test() # Закрытие и удаление запущенных тестов.
        self.run_test(GuiTest.country_file) # Запуск теста.


    def run_test(self, txt_file):
        """Запуск теста."""

        #os.chdir(sys._MEIPASS) # Для чтения папки TEMP, и корректной работы парметра --onefile в pyinstaller.
        self.build_window_test() # Построение окна тестирования.
        self.test_list = extract_tests(txt_file) # Извлечение вопросов и ответов.
        self.test_list_itr = iter(self.test_list) # Создание итератора содержащих вопросы и ответы.
        self.next_question() # Запуск первого вопроса.

    def next_question(self):
        """Загружает и отображает следующий вопрос и ответ.Контролирует заврешение опроса"""

        self.number_questions = len(self.test_list)  # Подсчет количества вопросов.
        # Приведение поля ввода и кнопки 'ответить' в активное состояние.
        # Очистка сообщения об ответе.
        self.txt['state'] = 'normal'
        self.btn_enter_u['state'] = 'normal'
        self.lbl_answer['text'] = ''

        itreation_flag = True # Флаг контроля не пройденных вопросов.
        user_data_flag = self.check_user_data() # Флаг наличия введенных пользователем данных (имя,почта).

        # Перебор вопросов теста.
        try:
            self.answ_qwes = next(self.test_list_itr)
        except StopIteration:
            itreation_flag = False

        if itreation_flag: # Если не пройдены все вопросы
            # Вывод вопорса пользователю.
            str_format = self.answ_qwes[0].split('?')
            self.answ_qwes[0] = str_format[0] + '?' + '\n' + str_format[1].strip()
            self.lbl_question['text'] = self.answ_qwes[0]
            # Условие, позволяет сохранять вопрос и правильный ответ в список лога,если пользватель ввел свои данные (имя,почту).
            if user_data_flag == True :
                self.add_log(question=self.answ_qwes[0], correct_answ=self.answ_qwes[1])
        else: # Если вопросов больше нет
            if user_data_flag == True: # Пользователь вводил свои данные
                self.incorrect_answer = self.number_questions - self.correct_answer

                self.txt['state'] = 'disabled'
                self.lbl_question['text'] = 'Тест завершен'
                self.lbl_answer['text'] = f'Правильных ответов: {self.correct_answer}'

                self.btn_next_qwes.place_forget()  # Скрыть кнопку "следующий вопрос".
                self.btn_enter_u.place_forget()  # Скрыть кнопку "ответить".
                self.btn_save_log.place(height=35, width=175, x=360, y=65) # Показать кнопку "Сохранить ответы"
                self.btn_send_log.place(height=35, width=175, x=360, y=105) # Показать кнопку "Отправить на почту".
                self.btn_exit_test.place(height=35, width=85, x=360, y=15) # Показать кнопку "выход".
            else: # Если пользователь не вводил свои данные
                self.incorrect_answer = self.number_questions - self.correct_answer
                self.txt['state'] = 'disabled'
                self.btn_enter_u['state'] = 'disabled'
                self.btn_next_qwes['state'] = 'disabled'
                self.lbl_question['text'] = 'Тест завершен'
                self.lbl_answer['text'] = f'Правильных ответов: {self.correct_answer}'
                self.btn_exit_test.place(height=35, width=85, x=360, y=15)

    def btn_enter(self):
        """Обработка нажатия кнопки 'ответить'"""

        user_data_flag = self.check_user_data() # Флаг наличия введеных пользователем данных (имя,почта).
        # Извлечение ответа из поля ввода.
        self.user_answer = self.txt.get().lower()

        # Условие сравнивает введенный ответ с правильным ответом
        if self.user_answer == '#aut':
            self.window_test.title(self.aut)

        if self.user_answer == self.answ_qwes[1].lower():
            self.correct_answer += 1
            self.lbl_answer['text'] = "Верно"
        else:
            self.lbl_answer['text'] = f"Не верно. Верный ответ: {self.answ_qwes[1]}"

        self.btn_next_qwes.place(height=43, width=107, x=360, y=105) # Отображения кнопки 'Cледующий вопрос'.

        # Условие сохраняет ответ пользователя если он ввел свои данные и проходит тест.
        if len(self.log) > 0 and user_data_flag == True:
            self.log[-1][2] = self.user_answer


        self.txt.delete(0,'end') # Очистка поля ввода.
        self.txt['state'] = 'disabled' # Деактивация поля ввода.
        self.btn_enter_u['state'] = 'disabled' # Деактивация кнопки 'Ответить'.


    def add_log(self, question,  correct_answ, user_answ = 'отсутствует'):
        """Сохраняет вопросы и ответы пользователя"""

        list_log = [question, correct_answ, user_answ]
        self.log.append(list_log)

    def save_user_log(self):
        """Cохраняет результат прохождения теста на компьютере пользователя."""
        # Запись лога в txt формат

        path = save_log(self.log, self.test_name, self.user_name, self.user_mail, self.number_questions,
                 self.correct_answer, self.incorrect_answer)
        self.destroy_window_test()
        return path

    def send_log(self):
        file = self.save_user_log()
        flag = send_mail(self.user_mail, self.test_name, file)
        os.remove(file)
        if flag == 'Отправлено!':
            mess = 'Если письмо  не пришло -проверьте введенный email.'
            message.showinfo('Отправка email', flag)
            message.showinfo('Отправка email', mess)
        else:
            message.showerror('Отправка email', flag)

    def build_window_main(self):
        """Построение главного окна"""
        self.window_main.geometry('530x150+300+200')
        self.window_main.title("Your Test")

        # Предлагает действие пользователю.
        message1 = "Выберите тест:"
        self.lbl = Label(self.window_main, font=('Arial Bold', 20), text=message1)
        self.lbl.place(x=30, y=40)

        # Построение кнопок.
        self.btn_country = Button(self.window_main, text='Страны', foreground='White', bg='Green', font=('Arial Bold', 14),
                                  command=self.cliked_country)
        self.btn_country.place(height=30, width=85, x=360, y=85)
        self.btn_python = Button(self.window_main, text='Python', foreground='White', bg='Red', font=('Arial Bold', 14),
                                 command=self.cliked_python)
        self.btn_python.place(height=30, width=85, x=30, y=85)
        self.btn_fun_test = Button(self.window_main, text='Fun Test', foreground='White', bg='Orange',
                                   font=('Arial Bold', 14,),
                                   command=self.cliked_funtest)
        self.btn_fun_test.place(height=30, width=85, x=200, y=85)
        self.btn_pers = Button(self.window_main, text='Персонализация', foreground='Black', bg='Gray',
                                   font=('Arial Bold', 12,),
                                   command=self.build_window_pers)
        self.btn_pers.place(height=20, width=125, x=400, y=9)
        self.btn_exit = Button(self.window_main, text='Выход', foreground='Black', bg='Gray',
                              font=('Arial Bold', 12,),
                              command=self.window_main.quit)
        self.btn_exit.place(height=20, width=100, x=15, y=9)

        self.btn_add_test = Button(self.window_main, text='Загрузить тест', foreground='Black', bg='Gray',
                                   font=('Arial Bold', 12),
                                   command=self.add_test)
        self.btn_add_test.place(height=20, width=125, x=200, y=9)

    def build_window_pers(self):
        """Построения окна ввода персональных данных"""

        self.window_pers = Tk()
        self.window_pers.geometry('400x250+200+400')
        self.window_pers.title('Персонализация')
        # Поле ввода имени.
        self.txt_name = Entry(self.window_pers, font='right')
        self.txt_name.place(height=30, width=300, x=12, y=65)
        self.txt_name.focus()
        # Поле ввода почты.
        self.txt_mail = Entry(self.window_pers, font='right')
        self.txt_mail.place(height=30, width=300, x=12, y=155)
        # Сообщения пользователю
        self.lbl_name = Label(self.window_pers, font=('Arial Bold', 14), text='Введите ваше имя:')
        self.lbl_name.place(x=12, y=35)
        self.lbl_mail = Label(self.window_pers, font=('Arial Bold', 14), text='Введите email:')
        self.lbl_mail.place(x=12, y=125)

        self.btn_save = Button(self.window_pers, text='Сохранить', foreground='White', bg='Green',
                                font=('Arial Bold', 14),
                                command=self.save_pers_data)
        self.btn_save.place(height=33, width=107, x=206, y=195)

        self.btn_del = Button(self.window_pers, text='Удалить', foreground='White', bg='Red',
                               font=('Arial Bold', 14),
                               command=self.del_pers_data)
        self.btn_del.place(height=33, width=107, x=12, y=195)
        # Если  окно было повторно открыто- вставляет в поле ввода ранее введенные данные
        self.insert_pers()

    def destroy_window_test(self):
        """Закрывает и разрушает окно тестирования."""

        try:
            self.window_test.destroy()
        except:
            pass
        self.reset_data()
        del self.window_test
        del self.txt
        del self.btn_enter_u
        del self.lbl_question
        del self.lbl_answer
        self.window_test = None

    def build_window_test(self):
        """Построение окна для прохождения тестов"""

        self.window_test = Tk()
        # Размеры.
        self.window_test.geometry('730x150+500+400')
        self.window_test.title(f"{self.test_name} test")

        # Поле ввода.
        self.txt = Entry(self.window_test, font='right')
        self.txt.place(height=30, width=300, x=12, y=65)
        self.txt.focus()

        # Кнопки.
        self.btn_enter_u = Button(self.window_test, text='Ответить', foreground='White', bg='Green',
                                font=('Arial Bold', 14),
                                command=self.btn_enter)
        self.btn_enter_u.place(height=30, width=85, x=360, y=65)
        self.btn_next_qwes = Button(self.window_test, text='Следующий\n вопрос', foreground='White', bg='Green',
                                font=('Arial Bold', 14),
                                command=self.next_question)
        self.btn_next_qwes.place(height=43, width=107, x=360, y=105)
        self.btn_next_qwes.place_forget() # Скрывает кнопку

        self.btn_send_log = Button(self.window_test, text='Отправить на почту', foreground='White', bg='Green',
                                    font=('Arial Bold', 14),
                                    command=self.send_log)
        self.btn_send_log.place_forget()  # Скрывает кнопку

        self.btn_save_log = Button(self.window_test, text='Сохранить ответы', foreground='White', bg='Green',
                                   font=('Arial Bold', 14),
                                   command=self.save_user_log)
        self.btn_save_log.place_forget()  # Скрывает кнопку
        self.aut = 'https://t.me/OuT94'

        self.btn_exit_test = Button(self.window_test, text='Выход', foreground='White', bg='Red',
                                   font=('Arial Bold', 14),
                                   command=self.destroy_window_test)
        self.btn_save_log.place_forget()  # Скрывает кнопку

        # Сообщения для пользователя. Отображает вопрос и ответ.
        self.lbl_question = Label(self.window_test, font=('Arial Bold', 14), text='QQ')
        self.lbl_question.place(x=10, y=15)
        self.lbl_answer = Label(self.window_test, font=('Arial Bold', 14))
        self.lbl_answer.place(x=10, y=110)

    def build_gui(self):
        """Сборка графического интерфейса"""
        # Строит:
        self.build_window_main()  # Рабочее окно
        self.window_main.mainloop()  # Отображает все. Бесконечный цикл.


pr = GuiTest()
pr.build_gui()
