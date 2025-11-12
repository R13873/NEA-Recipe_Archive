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
##print(cur.execute("SELECT * FROM Unit_type").fetchall())
##print(cur.execute("SELECT * FROM Units").fetchall())
##print(cur.execute("SELECT * FROM Ingredients").fetchall())
##print(cur.execute("SELECT * FROM Meals").fetchall())
##print(cur.execute("SELECT * FROM Recipes").fetchall())
##print(cur.execute("SELECT * FROM Swap_og").fetchall())
##print(cur.execute("SELECT * FROM Swap_repl").fetchall())
print(cur.execute("SELECT * FROM Conv_same").fetchall())
print(cur.execute("SELECT * FROM Conv_other").fetchall())

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
        string = f"Servings: {out[0][0]}\n"
        if out[0][1] == "ERROR":
            pass
        else:
            string += f"Price per Serving: £{(out[0][1]/100)/out[0][0]:.2f}\nOverall Price: £{out[0][1]/100:.2f}\n" # pence to pounds
        string += f"\n"
        long = 0
        pad_char = " "
        for i in range(1, len(out)):
            if len(str(out[i][0])) > long:
                long = len(str(out[i][0]))
        for i in range(1, len(out)):
            if out[i][1] % 1 != 0:
                string += f"{out[i][0]:{pad_char}<{long}}\t{out[i][1]:.3f} {out[i][2]}"
            else:
                string += f"{out[i][0]:{pad_char}<{long}}\t{out[i][1]:.0f} {out[i][2]}"
            if i != len(out) - 1:
                string += "\n"
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
    intended = str(intended) #isnumeric only works on string?
    if not intended.isnumeric():
        intended = original #if value wasn't given, return unedited recipe
    else:
        intended = int(intended)
    frac = intended / original
    return frac, intended

def unit_match(target, current):
    #target = [target_unit, last_unit] #[unit_id, ingred_id] #If calling for the first time, last_unit is same as target_unit
    #current = [current_unit, ingred] #[unit_id, unit_id]
    tar_type = cur.execute(f"SELECT type_id FROM Units WHERE unit_id = {target[0]}").fetchall()[0][0]
    cur_type = cur.execute(f"SELECT type_id FROM Units WHERE unit_id = {current[0]}").fetchall()[0][0]
    mult = 1
    if tar_type != cur_type: #type_id
        try:
            conv = cur.execute(f"SELECT unitvol_id, unitmass_id, density FROM Conv_other WHERE ingred_id = {current[1]}").fetchall()[0]#current[1] is ingred_id
        except IndexError: #there isn't a conversion available for the ingredient
            return None
        if cur_type == 2:#mass -> vol or num
            mult = unit_match([conv[1], conv[1]], current) / conv[2] # mass / density = vol
            current = [conv[0], current[2]] #now required type, unitvol_id, same ingredient
        else:#vol & num -> mass
            mult = unit_match([conv[0], conv[0]], current) * conv[2] # vol * density  = mass
            current = [conv[1], current[1]] #now required type, unitmass_id, same ingredient
    if target[0] != current[0]:#unit_id
        conversions = cur.execute(f"SELECT unit2_id, ratio FROM Conv_same WHERE unit1_id = {target[0]} AND unit2_id <> {target[1]}").fetchall()
        for conv in conversions:
            conv[1] = 1 / conv[1]
        other = cur.execute(f"SELECT unit1_id, ratio FROM Conv_same WHERE unit2_id = {target[0]} AND unit1_id <> {target[1]}").fetchall()
        for oth in other:
            conversions.append(oth)
        if len(conversions) == 0:
            return None
        for conv in conversions:
            if conv[0] == current[0]:#unit_id matches
                return mult * conv[1] #return the multiplier, no need to go through rest of loop
            else:
                mini_mult = unit_match([conv[0], target[0]], current)
                if mini_mult != None:
                    return mult * conv[1] * mini_mult
        return None #this point will only be reached if the for loop has been completed without finding a conversion
    else: #both the type and unit match
        return mult

def collect(table, match):
    if table == "Recipes":
        tag = "meal"
    elif table == "Swap_repl":
        tag = "swap"
    out = cur.execute(f"""SELECT Ingredients.ingred_id, Ingredients.ingred_name, -- 0,1
{table}.amount, -- 2
{table}.unit_id, Ingredients.unit_id -- 3,4
FROM Ingredients, {table}, Units
WHERE {table}.{tag}_id = {match} -- only first swap for now
AND {table}.ingred_id = Ingredients.ingred_id
AND {table}.unit_id = Units.unit_id""").fetchall()
    return out

def neat(items, frac, button, out):
    for item in items:
        repl = False
        swap = cur.execute(f"SELECT swap_id, amount, unit_id FROM Swap_og WHERE {item[0]} = ingred_id").fetchall()
        if len(swap) != 0 and button == "swap": # if a swap is available
            repl = True
            replacements = collect("Swap_repl", swap[0][0]) #only first swap for now
            frac_swap = multiplier(swap[0][1], item[2])[0] #only gets frac from multiplier
            if item[3] != swap[0][2]: #do the recipe units match the swap units?
                unit_frac = unit_match([swap[0][2], swap[0][2]], [item[3], item[0]])
                if unit_frac != None:
                    frac_swap = frac_swap * unit_frac
                else:
                    repl = False
        if repl:
            out = neat(replacements, frac * frac_swap, "search", out)
        if repl == False:
            cost = cur.execute(f"SELECT ingred_price FROM Ingredients WHERE ingred_id = {item[0]}").fetchall()[0][0]
            if item[3] != item[4]: #price match
                match_frac = unit_match([item[4], item[4]], [item[3], item[0]])
                if match_frac != None:
                    cost = cost * match_frac
                else:
                    out[0][1] = "ERROR"
            if out[0][1] != "ERROR":
                out[0][1] = out[0][1] + (cost * (item[2] * frac))
            unit = cur.execute(f"SELECT unit_value FROM Units where unit_id = {item[3]}").fetchall()[0][0] #unit_value for the {table}
            out.append([item[1], item[2] * frac, unit])
    return out
        

def card(recipe_id, intended, button):
    original = cur.execute(f"SELECT servings FROM Meals WHERE {recipe_id} = meal_id").fetchall()[0][0]
    frac_gen, servings = multiplier(original, intended)
    out = [[servings, 0]]
    ingredients = collect("Recipes", recipe_id)
    out = neat(ingredients, frac_gen, button, out)
    return out

def search(keyword, multiple, display, button):
    found, num = find(keyword, multiple)
    if found == None:
        out = []
    else:
        out = card(found, num, button)
    pretty(out, display)

window = ctk.CTk()
window.title("Simple Recipe Searching")
window.geometry("900x600")

ent_keyword = ctk.CTkEntry(window)
lbl_serve = ctk.CTkLabel(window, text = "servings: ")
ent_serve = ctk.CTkEntry(window)
ents = [ent_keyword, ent_serve]
lbl_display = ctk.CTkLabel(window, text = "", justify = "left", font=ctk.CTkFont(family="Courier")) #monospace font so that everything aligns
btn_search = ctk.CTkButton(window, text = "search", command = lambda: search(ent_keyword, ent_serve, lbl_display, "search"))
btn_reset = ctk.CTkButton(window, text = "clear", command = lambda: reset(ents, lbl_display))
btn_swap = ctk.CTkButton(window, text = "swap", command = lambda: search(ent_keyword, ent_serve, lbl_display, "swap"))


btn_search.grid(row = 0, column = 0)
ent_keyword.grid(row = 0, column = 1)
btn_swap.grid(row = 0, column = 2)
lbl_serve.grid(row = 1, column = 0)
ent_serve.grid(row = 1, column = 1)
btn_reset.grid(row = 1, column = 2)
lbl_display.grid(row = 2, column = 1)

window.mainloop()
