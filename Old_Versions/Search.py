import sqlite3
import customtkinter as ctk

conn = sqlite3.connect("Recipe_Archive.db")
cur = conn.cursor()

def ph(boxes, check_vars, outputs):
    for i in range(len(boxes)):
        if check_vars[i].get() == "on":
            check.set(value = "off")
            print(outputs[i])


def find(keyword, out):
    global results # global because button can't return value
    global check_vars
    for chk in results:
        chk.grid_remove()
    results = []
    check_vars = []
    out.grid_remove()
    check = keyword.get()
    string = "%" + check.lower() + "%"
    outputs = cur.execute(f"SELECT meal_name, meal_id FROM Meals WHERE meal_name LIKE \"{string}\"").fetchall() # get exact meal name
    if outputs == []:
        out.grid(row = 1, column = 0)
    else:
        for i in range(len(outputs)):
            check_vars.append(ctk.StringVar(value = "off"))
            results.append(ctk.CTkCheckBox(search,
                                           text = f"outputs[i][1]",
                                           command = lambda: ph(results, check_vars, outputs),
                                           variable = check_vars[i],
                                           onvalue = "on",
                                           offvalue = "off"))
            results[i].grid(row = i + 1, column = 0)

search = ctk.CTk()
search.title("Search")
search.geometry("300x400")

ent_keyword = ctk.CTkEntry(search)
btn_search = ctk.CTkButton(search, text = "search", command = lambda: find(ent_keyword, lbl_out))
lbl_out = ctk.CTkLabel(search, text = "No Recipes Found")

ent_keyword.grid(row = 0, column = 0)
btn_search.grid(row = 0, column = 1)
results = [] #will store several buttons pointing to different recipes

search.mainloop()
