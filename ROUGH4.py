import customtkinter as ctk

def ph():
    print("checkbox toggled, current value:", check_var.get())

def count(boxes, checkvars):
    total = 0
    for i in range(len(boxes)):
        if check_vars[i].get() == "on":
            total += int(boxes[i].cget("text"))
    print(total)

def alone(check):
    if check.get() == "on":
        check.set(value = "off")
        print("leave me alone")

window = ctk.CTk()
window.geometry("500x600")
check_var = ctk.StringVar(value = "on") #has to match onvalue or automatically off
test = ctk.CTkCheckBox(window, text = "test", command = lambda: ph(), variable = check_var, onvalue = "on", offvalue = "off")
test.grid(row = 0, column = 0)

boxes = []
check_vars = [] # have to have seperate for each or they will all use same
for i in range(10):
    check_vars.append(ctk.StringVar(value = "off"))
    boxes.append(ctk.CTkCheckBox(window, text = f"{i}", command = lambda: count(boxes, check_vars), variable = check_vars[i], onvalue = "on", offvalue = "off"))
    boxes[i].grid(row = i + 1, column = 0)

hide = ctk.CTkLabel(window, text = "Nothing to see here folks")
hide.grid(row = 0, column = 1)

check = ctk.StringVar(value = "off")
no = ctk.CTkCheckBox(window, text = "Don't touch", command = lambda: alone(check), variable = check, onvalue = "on", offvalue = "off")
no.grid(row = 0, column = 1)


window.mainloop()
