import sqlite3
import customtkinter as ctk

conn = sqlite3.connect("Recipe_Archive.db")
cur = conn.cursor()

meals = cur.execute("SELECT * FROM Meals").fetchall()
for meal in meals:
    print(meal[1])
#prints a list for debug so I know what I shoud be searching
##print(cur.execute("SELECT * FROM Ingredients").fetchall())
##print(cur.execute("SELECT * FROM Meals").fetchall())
##print(cur.execute("SELECT * FROM Recipes").fetchall())
##print(cur.execute("SELECT * FROM Units").fetchall())
##print(cur.execute("SELECT * FROM Swap_original").fetchall())
##print(cur.execute("SELECT * FROM Swap_replacement").fetchall())
##print(cur.execute("SELECT * FROM Conversion_same").fetchall())
##print(cur.execute("SELECT * FROM Conversion_other").fetchall())

def reset(ins, out): #resets input and output boxes
    for take in ins:
        take.delete(0, ctk.END)
    out.configure(text = "")

def find(keyword, multiple):
    check = keyword.get()
    num = multiple.get()
    try:
        found = cur.execute(f"SELECT meal_id FROM Meals WHERE \"{check.lower()}\" = meal_name;").fetchall()[0][0]
        #If there are duplicate meals, only the first will be used
    except IndexError:
        found = None
    return found, num

def pretty(string, display):
    display.configure(text = string)

def organise_swap_test(recipe_id, intended):
    original = cur.execute(f"SELECT servings FROM Meals WHERE\"{int(recipe_id)}\" = meal_id;").fetchall()[0][0] #servings is returned as [(?,)]
    if not intended.isnumeric():
        intended = original #if value wasn't given, return unedited recipe
    else:
        intended = int(intended)
    fraction = intended / original
    string = f"Servings:\t {intended}\n"
    #stays the same
    ingredients = cur.execute(f"""SELECT Ingredients.ingred_id, Ingredients.ingred_name, Recipes.amount, Units.unit_value
FROM Recipes, Ingredients, Units
WHERE Recipes.meal_id = {int(recipe_id)}
AND Recipes.ingred_id = Ingredients.ingred_id
AND Recipes.unit_id = Units.unit_id""").fetchall()
    swaps = []
    for ingred in ingredients:
        swaps = cur.execute(f"""SELECT swap_id FROM Swap_original WHERE \"{int(ingred[0])}\" = ingred_id""").fetchall()
        print(swaps)
        swaps = []
##    ingredients = cur.execute(f"""SELECT Ingredients.ingred_name, Recipes.amount, Units.unit_value, IF (Recipes.unit_id = Ingredients.unit_id, "match", "miss")
##FROM Recipes, Ingredients, Units
##WHERE Recipes.meal_id = {recipe_id}
##AND Recipes.ingred_id = Ingredients.ingred_id
##AND Recipes.unit_id = Units.unit_id""").fetchall()
##    for ingred in ingredients:
##        string += f"{ingred[0]}\t{ingred[1] * fraction} {ingred[2]}\t\t{ingred[3]}\n" #At some point, I'll use the match/miss for a simplified price calculation before doing unit conversion
##    return string

def organise(recipe_id, intended):
    original = cur.execute(f"SELECT servings FROM Meals WHERE \"{int(recipe_id)}\" = meal_id;").fetchall()[0][0] #servings is returned as [(?,)]
    if not intended.isnumeric():
        intended = original #if value wasn't given, return unedited recipe
    else:
        intended = int(intended)
    fraction = intended / original
    string = f"Servings:\t {intended}\n"
    ingredients = cur.execute(f"""SELECT Ingredients.ingred_name, Recipes.amount, Units.unit_value, IF (Recipes.unit_id = Ingredients.unit_id, "match", "miss"), Recipes.unit_id, Ingredients.unit_id
FROM Recipes, Ingredients, Units
WHERE Recipes.meal_id = {recipe_id}
AND Recipes.ingred_id = Ingredients.ingred_id
AND Recipes.unit_id = Units.unit_id""").fetchall()
    for ingred in ingredients:
        if ingred[3] == "miss":
            mult = "?"
            print(cur.execute(f"""SELECT multiplier, unit1_id, unit2_id FROM Conversion_same
--WHERE unit1_id = {ingred[4]}
--AND unit2_id = {ingred[5]} -- comments out in SQL
""").fetchall(), ingred[4], ingred[5])
        else:
            mult = 1
        string += f"{ingred[0]}\t{ingred[1] * fraction} {ingred[2]}\t\t{ingred[3]},{mult}\n"
    return string

def search(keyword, multiple, display):
    found, num = find(keyword, multiple)
    if found == None:
        string = "ERROR - recipe not found"
    else:
        string = organise(found, num)
        organise_swap_test(found, num)
    pretty(string, display)

window = ctk.CTk()
window.title("Test")
window.geometry("600x400")

ent_keyword = ctk.CTkEntry(window)
lbl_serve = ctk.CTkLabel(window, text = "servings: ")
ent_serve = ctk.CTkEntry(window)
ents = [ent_keyword, ent_serve]
btn_search = ctk.CTkButton(window, text = "search", command = lambda: search(ent_keyword, ent_serve, lbl_display))
btn_swap = ctk.CTkButton(window, text = "swap", command = lambda: swap(ent_keyword, ent_serve, lbl_display))
lbl_display = ctk.CTkLabel(window, text = "")
btn_reset = ctk.CTkButton(window, text = "clear", command = lambda: reset(ents, lbl_display))

ent_keyword.grid(row = 0, column = 1)
btn_search.grid(row = 0, column = 2)
lbl_serve.grid(row = 1, column = 0)
ent_serve.grid(row = 1, column = 1)
btn_reset.grid(row = 1, column = 2)
lbl_display.grid(row = 2, column = 1)
btn_swap.grid(row = 3, column = 1)

window.mainloop()


