import customtkinter as ctk

def debug_print(count):
    val = int(count.cget("text"))
    print(f"test{val}")
    count.configure(text = str(val+1))

def pretty(count, out):
    val = int(count.cget("text"))//10
    out.configure(text = str(val*10))

def test(count, out):
    pretty(count, out)
    debug_print(count)

def reset(count, out):
    count.configure(text = "1")
    pretty(count, out)

window = ctk.CTk()
window.title("Something")
window.geometry("600x400")

lbl_hold = ctk.CTkLabel(window, text = "1")
btn_test = ctk.CTkButton(window, text = "test", command = lambda: test(lbl_hold, lbl_dec))
btn_test.grid(row = 0, column = 0)
btn_reset = ctk.CTkButton(window, text = "reset", command = lambda: reset(lbl_hold, lbl_dec))
btn_reset.grid(row = 0, column = 1)
lbl_dec = ctk.CTkLabel(window, text = "0")
lbl_dec.grid(row = 1, column = 0)

window.mainloop()

#This isn't very useful/important, just re-aquainting myself with customtkinter
