import tkinter as tk
from PIL import Image, ImageTk

# def func():
#     print('popa')
# def text():
#     label = tk.Label(win, text='falsf')
#     label.pack()
# count = 0
# def counter():
#     global count
#     count += 1
#     btn3['text'] = f'Счетчик: {count}'
win = tk.Tk()
# photo = ImageTk.PhotoImage(Image.open('photos/Hand-drawn-facebook-messenger-logo-on-transparent-background-PNG.png'))
# win.iconphoto(False, photo)
# win.config(bg='#3f3f3f')
win.title('Calc')
win.geometry('240x280+100+200')
# win.resizable(True, True)
# win.minsize(400, 500)
# win.maxsize(1920, 1080)

# label_l = tk.Label(win, text='Pisya popa cheeleeen',
#                    bg ='#333f3f',
#                    fg='white',
#                    font=('Arial',20,'bold'),
#                    height=20,
#                    width=60,
#                 #    anchor='center',
#                    padx=10,
#                    pady=10,
#                    relief=tk.RAISED,
#                    )
# label_l.pack()

# btn1 = tk.Button(win, text='Hello',
#                  command=func)
# btn1.pack()
# btn2 = tk.Button(win, text='Нажми',
#                  command=text)
# btn3 = tk.Button(win, text=f'Счетчик: {count}',
#                  command=counter,
#                  foreground='blue'
#                  )
# btn2.pack()
# btn3.pack()

# for i in range(5):
#     for j in range(2):
#         tk.Button(win, text=f'Hello {i} {j}').grid(row=i, column=j, stick='we')

# win.grid_columnconfigure(0, minsize=200)
# win.grid_columnconfigure(1, minsize=200)

# def get_entry():
#     value = name.get()
#     if value:
#         print(value)
#     else:
#         print('Empty')

# def delete_entry():
#     name.delete(0,tk.END)
# def submit():
#     print(name.get())
#     print(password.get())
#     password.delete(0, tk.END)
#     name.delete(0, tk.END)

# tk.Label(win, text='Имя').grid(row=1, column=0, sticky='e')
# tk.Label(win, text='Пароль').grid(row=2, column=0, sticky='e')
# password = tk.Entry(win, show='*')
# name = tk.Entry(win)
# name.grid(row=1, column=1)
# password.grid(row=2, column=1)
# tk.Button(win, text='get',
#           command=get_entry).grid(row=3, column=1, sticky='we')
# tk.Button(win, text='Delete',
#           command=delete_entry).grid(row=3, column=2, sticky='we')
# tk.Button(win, text='Submit',
#           command=submit).grid(row=4, column=1, sticky='we')
# win.grid_columnconfigure(0, minsize=100)
# win.grid_columnconfigure(1, minsize=50)
win['bg'] = '#33ffe6'
def add_digit(digit):
    value = calc.get()
    if value[0] == '0' and len(value) == 1:
        value = value[1:]
    calc.delete(0, tk.END)
    calc.insert(0, value + digit)
def add_operation(operation):
    value = calc.get()
    if value[-1] in '-+/*':
        value = value[:-1]
    elif '+' in value or '-' in value or '*' in value or '/' in value:
        calculate()
        value = calc.get()
    calc.delete(0, tk.END)
    calc.insert(0, value+operation)
def calculate():
    value = calc.get()
    if value[-1] in '+-/*':
        operation = value[-1]
        value = value[:-1] + operation + value[:-1]
    calc.delete(0, tk.END)
    calc.insert(0, eval(value))
def make_digit_button(digit):
    return tk.Button(text=digit, bd=5, font = ('Arial', 13, 'bold'),command=lambda: add_digit(digit))
def clear():
    calc.delete(0, tk.END)
    calc.insert(0, 0)
def make_operation_button(operation):
    return tk.Button(text=operation, bd=5, font = ('Arial', 13, 'bold'),fg='red',command=lambda: add_operation(operation))
def make_calc_button(operation):
    return tk.Button(text=operation, bd=5, font = ('Arial', 13, 'bold'),fg='red',command=calculate)
def make_clear_button(operation):
    return tk.Button(text=operation, bd=5, font = ('Arial', 13, 'bold'),fg='red',command=clear)

win.resizable(False, False)
calc = tk.Entry(win, justify=tk.RIGHT, font=('Arial', 15, 'bold'), width=15)
calc.insert(0, '0')
calc.grid(row=0,column=0, columnspan=4, sticky='we', padx=5, pady=5)
make_digit_button('2').grid(row=1, column=1, sticky='wens', padx=5, pady=5)
make_digit_button('1').grid(row=1, column=0, sticky='wens', padx=5, pady=5)
make_digit_button('3').grid(row=1, column=2, sticky='wens', padx=5, pady=5)
make_digit_button('4').grid(row=2, column=0, sticky='wens', padx=5, pady=5)
make_digit_button('5').grid(row=2, column=1, sticky='wens', padx=5, pady=5)
make_digit_button('6').grid(row=2, column=2, sticky='wens', padx=5, pady=5)
make_digit_button('7').grid(row=3, column=0, sticky='wens', padx=5, pady=5)
make_digit_button('8').grid(row=3, column=1, sticky='wens', padx=5, pady=5)
make_digit_button('9').grid(row=3, column=2, sticky='wens', padx=5, pady=5)
make_digit_button('0').grid(row=4, column=0, sticky='wens', padx=5, pady=5)

make_operation_button('+').grid(row=1, column=3, sticky='wens', padx=5, pady=5)
make_operation_button('-').grid(row=2, column=3, sticky='wens', padx=5, pady=5)
make_operation_button('/').grid(row=3, column=3, sticky='wens', padx=5, pady=5)
make_operation_button('*').grid(row=4, column=3, sticky='wens', padx=5, pady=5)

make_calc_button('=').grid(row=4, column=2, sticky='wens', padx=5, pady=5)
make_clear_button('C').grid(row=4, column=1, sticky='wens', padx=5, pady=5)

win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)
win.grid_rowconfigure(1, minsize=60)
win.grid_rowconfigure(2, minsize=60)
win.grid_rowconfigure(3, minsize=60)
win.grid_rowconfigure(4, minsize=60)

win.mainloop()