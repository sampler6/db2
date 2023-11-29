import tkinter as tk
from tkinter import ttk
import redis

conn = redis.connection = redis.Redis(host='localhost', password="student")


def update():
    judge_name = judges.get()
    sportsmen_name = sportsmen.get()
    if judge_name not in judges_list or sportsmen_name not in sportsmen_list:
        return
    key = "22304-korzhuk-"
    key += f"{judges.get()}-{sportsmen.get()}"
    print(key)
    conn.set(key, int(score.get()), ex=1000)
    update_listbox()


def update_listbox():
    lstbox.delete(0, "end")
    listscores = list()
    for key1 in sportsmen_list:
        total = 0
        key = "22304-korzhuk-"
        for key2 in judges_list:
            a = conn.get(key+key2+'-'+key1)
            if a is None:
                continue
            total += int(a)
        listscores.append((key1, total))
    listscores.sort(key=lambda x: x[1], reverse=True)
    for i in listscores:
        lstbox.insert("end", f"{i[0]}: {i[1]}")


window = tk.Tk()
window['bg'] = "grey"
window.geometry("1080x720")
window.resizable(False, False)
frm1 = tk.Frame(master=window, width=1080, height=720, background="grey")
frm1.pack()

main_label = tk.Label(master=frm1, text="Монитор соревнований",
                      foreground="black", background="grey", font=("Bold", 14))
main_label.place(relx=0, rely=0, relwidth=1)

judges_list = list()
sportsmen_list = list()
for i in range(3):
    judges_list.append(f"Судья {i+1}")
    sportsmen_list.append(f"Спорстмен {i * 2 + 1}")
    sportsmen_list.append(f"Спорстмен {i * 2 + 2}")

lbl_judges = tk.Label(master=frm1, text="Судья", background="grey", font=("Times", 16))
judges = ttk.Combobox(master=frm1, values=judges_list, font=("Times", 16))
judges.place(relx=0.2, rely=0.2, relwidth=0.16)
lbl_judges.place(relx=0.2, rely=0.15, relwidth=0.16)

lbl_sportsmen = tk.Label(master=frm1, text="Спорстмен", background="grey", font=("Times", 16))
sportsmen = ttk.Combobox(master=frm1, values=sportsmen_list, font=("Times", 16))
lbl_sportsmen.place(relx=0.64, rely=0.15, relwidth=0.16)
sportsmen.place(relx=0.64, rely=0.2, relwidth=0.16)

lbl_score = tk.Label(master=frm1, text="Баллы", background="grey", font=("Times", 16))
score = ttk.Combobox(master=frm1, values=list(map(lambda x: str(x), range(1, 11))), font=("Times", 16))
upd = tk.Button(text="Обновить", command=update)
score.place(relx=0.46, relwidth=0.08, rely=0.2)
lbl_score.place(relx=0.46, rely=0.15, relwidth=0.08)
upd.place(relx=0.46, rely=0.25, relwidth=0.08)

lstbox = tk.Listbox(master=frm1, font=("Times", 16))
lstbox.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.6)

score.set(0)
update_listbox()
window.mainloop()
