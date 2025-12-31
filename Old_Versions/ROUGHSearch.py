import customtkinter as ctk
import ROUGHDisplay as dsp
import sqlite3

conn = sqlite3.connect("Recipe_Archive.db")
cur = conn.cursor()

meals = cur.execute("SELECT meal_name FROM Meals").fetchall() #returns [[,],[,]] etc.
for meal in meals:
    print(meal[0]) #prints debug list of what can be searched

def find(keyword): 
    """Get's the user input"""
    check = keyword.get()
    try:
        found = cur.execute(f"SELECT meal_id FROM Meals WHERE \"{check.lower()}\" = meal_name;").fetchall()[0][0]
        #If there are duplicate meals, only the first will be used
    except IndexError: #nothing is found, so there is nothing at [0][0]
        found = ""
    return found

def tmp(ent):
    recipe_id = find(ent)
    dsp.tmp(recipe_id)

search = ctk.CTk()
search.title("Search")
search.geometry("280x28")
ent = ctk.CTkEntry(search)
btn = ctk.CTkButton(search, text = "search", command = lambda : tmp(ent))

ent.grid(row = 0, column = 0)
btn.grid(row = 0, column = 1)

search.mainloop()
