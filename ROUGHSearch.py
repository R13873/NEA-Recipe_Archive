import customtkinter as ctk
import ROUGHDisplay as dsp

def tmp(ent):
    string = ent.get()
    dsp.tmp(string)

search = ctk.CTk()
ent = ctk.CTkEntry(search)
btn = ctk.CTkButton(search, text = "search", command = lambda : tmp(ent))

ent.grid(row = 0, column = 0)
btn.grid(row = 0, column = 1)

search.mainloop()
