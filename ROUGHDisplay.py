import customtkinter as ctk

def tmp(string):
    display = ctk.CTk()
    lbl = ctk.CTkLabel(display, text = f"{string}")
    lbl.grid(row = 0, column = 0)
    display.mainloop()
