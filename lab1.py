import redis
import tkinter as tk

conn = redis.connection = redis.Redis(host='localhost', password="student")
current_user = ""


def show_text():
    text = entry2.get()
    font_settings = entry1.get().split(', ')

    if len(font_settings) < 3 or len(text) == 0:
        lbloutput['text'] = "Заполните поля ввода"
        lbloutput['font'] = ("Times", 20)
        lbloutput['foreground'] = "red"
        return

    lbloutput['text'] = text
    lbloutput['font'] = (font_settings[0], int(font_settings[1]))
    lbloutput['foreground'] = font_settings[2]
    return


def update_entry():
    global current_user, entry1, entry2
    try:
        user = users.selection_get()
    except:
        return
    if user in users.get(0, "end"):
        if current_user != "":
            save_entry(current_user)
        current_user = user

        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
        user = "22304-korzhuk-" + user
        tmp = conn.get(user)
        if tmp is not None:
            data = str(tmp.decode()).split("|")
        else:
            return
        entry1.insert(0, data[0])
        entry2.insert(0, data[1])
        show_text()


def save_entry(key):
    if key in users.get(0, "end"):
        key="22304-korzhuk-" + key
        conn.delete(key)
        conn.set(key, f"{entry1.get()}|{entry2.get()}", ex=1000)


window = tk.Tk()
window['bg'] = "grey"
window.geometry("1080x720")
window.resizable(False, False)
frm1 = tk.Frame(master=window, width=1080, height=720, background="grey")
frm1.pack()

main_label = tk.Label(master=frm1, text="Менеджер для сохранения настроек шрифтов",
                      foreground="black", background="grey", font=("Bold", 14))
main_label.place(relx=0, rely=0, relwidth=1)

lblentry1 = tk.Label(master=frm1, text="Настройки шрифта:", background="grey", anchor="w", font=("Ariel", 14))
entry1 = tk.Entry(master=frm1)
lblentry1.place(relx=0, rely=0.1, relwidth=0.20)
entry1.place(relx=0.20, rely=0.1, relwidth=0.3)

lblentry2 = tk.Label(master=frm1, text="Текст сообщения:", background="grey", anchor="w", font=("Ariel", 14))
entry2 = tk.Entry(master=frm1)
lblentry2.place(relx=0, rely=0.15, relwidth=0.20)
entry2.place(relx=0.20, rely=0.15, relwidth=0.3)

lbloutput = tk.Label(master=frm1, text="", background="white")
lbloutput['text'] = "Заполните поля ввода"
lbloutput['font'] = ("Times", 20)
lbloutput['foreground'] = "red"

#button1 = tk.Button(master=frm1, command=show_text, text="Вывести текст", font=("Times", 14))
#button1.place(relx=0, rely=0.25)

users = tk.Listbox(master=frm1, font=("Times", 16))
users.place(relx=0.6, rely=0.09, relwidth=0.4)
users.bind('<<ListboxSelect>>', lambda event: update_entry())
entry1.bind("<KeyRelease>", lambda event: update_entry())
entry2.bind("<KeyRelease>", lambda event: update_entry())


lbloutput.place(relx=0.0, rely=0.5)

users.insert(0, "Коржук Никита Андреевич")
users.insert(1, "Иванов Иван Иванович")
users.insert(2, "Алексеев Алексей Алексеевич")
users.select_set(0)
update_entry()

window.mainloop()
