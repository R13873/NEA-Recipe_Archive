import customtkinter as ctk

extra = []

def debug_print(count):
    val = int(count.cget("text"))
    print(f"test{val}")
    count.configure(text = str(val+1))

def pretty(count, out):
    val = int(count.cget("text"))//10
    out.configure(text = str(val*10))
    if val % 10 == 0:
        lbl_flash.grid(row = 1, column = 3)
    else:
        lbl_flash.grid_remove()
    global extra
    extra.append(str(count.cget("text")))
    extra[-1] = ctk.CTkLabel(window, text = extra[-1])
    extra[-1].grid(row = len(extra) - 1, column = 4)

def test(count, out):
    pretty(count, out)
    debug_print(count)

def reset(count, out):
    global extra
    print(extra)
    for i in range(len(extra)):
        extra[i].grid_remove()
    extra = []
    print(extra)
    count.configure(text = "1")
    pretty(count, out)
    lbl_flash.grid_remove()

window = ctk.CTk()
window.title("Something")
window.geometry("600x400")

lbl_store = ctk.CTkLabel(window, text = "")
lbl_flash = ctk.CTkLabel(window, text = "10")
lbl_hold = ctk.CTkLabel(window, text = "1")
btn_test = ctk.CTkButton(window, text = "test", command = lambda: test(lbl_hold, lbl_dec))
btn_test.grid(row = 0, column = 0)
btn_reset = ctk.CTkButton(window, text = "reset", command = lambda: reset(lbl_hold, lbl_dec))
btn_reset.grid(row = 0, column = 1)
lbl_dec = ctk.CTkLabel(window, text = "0")
lbl_dec.grid(row = 1, column = 0)
lbl_flash.grid(row = 1, column = 3)
lbl_flash.grid_remove()

labels = ["This", "is", "a", "test", "it", "worked"]
for i in range(len(labels)):
    labels[i] = ctk.CTkLabel(window, text = labels[i])
    labels[i].grid(row = i, column = 2)

print(labels)

input("continue ")

window.mainloop()

#This isn't very useful/important, just re-aquainting myself with customtkinter
