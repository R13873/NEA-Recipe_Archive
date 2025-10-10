import sqlite3
import customtkinter as ctk

conn = sqlite3.connect("Recipe_Archive.db")
cur = conn.cursor()

##Unit_type(type_id, type_name)
##Units(unit_id, unit_value, type_id)
##Ingredients(ingred_id, ingred_name, ingred_price, unit_id)
##Meals(meal_id, meal_name, servings)
##Recipes(meal_id,ingred_id, amount, unit_id)
##Swap_og(swap_id, ingred_id, amount, unit_id)
##Swap_repl(swap_id, ingred_id, amount, unit_id)
##Conv_same(unit1_id, unit2_id, ratio)
##Conv_other(ingred_id, unitvol_id, unitmass_id, density)
##print(cur.execute("SELECT * FROM Unit_type".fetchall()))
##print(cur.execute("SELECT * FROM Units".fetchall()))
##print(cur.execute("SELECT * FROM Ingredients".fetchall()))
##print(cur.execute("SELECT * FROM Meals".fetchall()))
##print(cur.execute("SELECT * FROM Recipes".fetchall()))
##print(cur.execute("SELECT * FROM Swap_og".fetchall()))
##print(cur.execute("SELECT * FROM Swap_repl".fetchall()))
##print(cur.execute("SELECT * FROM Conv_same".fetchall()))
##print(cur.execute("SELECT * FROM Conv_other".fetchall()))

meals = cur.execute("SELECT meal_name FROM Meals").fetchall() #returns [[,],[,]] etc.
for meal in meals:
    print(meal[0]) #prints debug list of what can be searched
def place_holder():
    pass

def reset(ins, out): #resets input and output boxes
    for take in ins:
        take.delete(0, ctk.END)
    out.configure(text = "")

def pretty(out, display): #outputs recipe
    if len(out) == 0:
        string = "Error - Recipe Not Found"
    else:
        print(out)
    display.configure(text = string)

def find(keyword, multiple): #gets user inputs
    check = keyword.get()
    num = multiple.get()
    try:
        found = cur.execute(f"SELECT meal_id FROM Meals WHERE \"{check.lower()}\" = meal_name;").fetchall()[0][0]
        #If there are duplicate meals, only the first will be used
    except IndexError: #nothing is found, so there is nothing at [0][0]
        found = None
    return found, num

def multiplier(original, intended):
    if not intended.isnumeric():
        intended = original #if value wasn't given, return unedited recipe
    else:
        intended = int(intended)
    frac = intended / original
    return frac, intended

def neat(items, frac, button, out):
    if button == "swap":
        swap = cur.execute(f"SELECT swap_id, amount FROM Swap_og WHERE {items[0]} = ingred_id").fetchall()
        frac_swap = multiplier(swap[1], items[2])
        replacements = cur.execute(f"""SELECT Ingredients.ingred_id, Ingredients.ingred_name -- 0,1
Swap_repl.amount -- 2
IF (Swap_repl.unit_id = Ingredients.unit_id, "match", "miss") -- 3
Swap_repl.unit_id, Ingredients.unit_id, Units.unit_value -- unit_value for the swap, 4,5,6""").fetchall()
        if len(replacements) != 0: #if a swap was found
            out = neat(replacements, frac * frac_swap, "search", out)
    else:
        for item in items:
            out.append([item[1], item[2] * frac, item[6]])
    return out
        

def card(recipe_id, intended, button):
    original = cur.execute(f"SELECT servings FROM Meals WHERE {recipe_id} = meal_id").fetchall()[0][0]
    frac_gen, servings = multiplier(original, intended)
    out = [[servings]]
    ingredients = cur.execute(f"""SELECT Ingredients.ingred_id, Ingredients.ingred_name, -- 0,1
Recipes.amount, -- 2
IF (Recipes.unit_id = Ingredients.unit_id, "match", "miss") -- 3
Recipes.unit_id, Ingrediets.unit_id, Units.unit_value -- unit_value for the recipe, 4,5,6
FROM Ingredients, Recipes, Units
WHERE Recipes.meal_id = {recipe_id}
AND Recipes.ingred_id = Ingredients.ingred_id
AND Recipes.unit_id = Units.unit_id""").fetchall()
    out = neat(ingredients, frac_gen, button, out)

def search(keyword, multiple, display, button):
    found, num = find(keyword, multiple)
    if found == None:
        out = card(found, num, button)
    else:
        card(found, num, button)
    pretty(out, display)

window = ctk.CTk()
window.title("Simple Recipe Searching")
window.geometry("900x600")

ent_keyword = ctk.CTkEntry(window)
lbl_serve = ctk.CTkLabel(window, text = "servings: ")
ent_serve = ctk.CTkEntry(window)
ents = [ent_keyword, ent_serve]
lbl_display = ctk.CTkLabel(window, text = "")
btn_search = ctk.CTkButton(window, text = "search", command = lambda: search(ent_keyword, ent_serve, lbl_display, "search"))
btn_reset = ctk.CTkButton(window, text = "clear", command = lambda: reset(ents, lbl_display))
btn_swap = ctk.CTkButton(window, text = "swap", command = lambda: search(ent_keyword, ent_serve, lbl_display, "swap"))


ent_keyword.grid(row = 0, column = 1)
btn_search.grid(row = 0, column = 2)
btn_swap.grid(row = 0, column = 3)
lbl_serve.grid(row = 1, column = 0)
ent_serve.grid(row = 1, column = 1)
btn_reset.grid(row = 1, column = 2)
lbl_display.grid(row = 2, column = 1)

window.mainloop()
