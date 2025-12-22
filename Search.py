import sqlite3
import customtkinter as ctk

conn = sqlite3.connect("Recipe_Archive.db")
cur = conn.cursor()
def ph():
    print("hello")
##    meal_id = cur.execute(f"SELECT meal_id FROM Meals WHERE meal_name = \"{meal_name}\"").fetchall()[0][0]
##    print(meal_id)


def find(keyword, out):
    global results # global because button can't return value
    for btn in results:
        btn.grid_remove()
    results = []
    out.grid_remove()
    check = keyword.get()
    string = "%" + check.lower() + "%"
    outputs = cur.execute(f"SELECT meal_name FROM Meals WHERE meal_name LIKE \"{string}\"").fetchall() # get exact meal name
    if outputs == []:
        out.grid(row = 1, column = 0)
    else:
        for i in range(len(outputs)):
            results.append(ctk.CTkButton(search, text = outputs[i][0], command = ph))
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
