import customtkinter as ctk
import sqlite3

conn = sqlite3.connect("Recipe_Archive.db")
cur = conn.cursor()

def multiplier(original, intended):
    """Finds the fraction by which to multiply the original value to get the intended value"""
    intended = str(intended) #isnumeric only works on string?
    if not intended.isnumeric():
        intended = original #if value wasn't given, return unedited recipe
    else:
        intended = int(intended)
    frac = intended / original
    return frac, intended

def unit_match(target, current):
    """Finds the value by which to multiply the current value to change units
    target = [target_unit, last_unit] OR [unit_id, unit_id]
    If calling for the first time, last_unit is same as target_unit
    current = [current_unit, ingred] OR [unit_id, ingred_id]
    If it can't find a conversion rate, it will return None"""
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

def pretty(out, widgets, offset_x, offset_y, window):
    """takes in a 2D array (out) and generates the recipe page"""
    display = widgets[0]
    if len(out) == 0:
        display[0].configure(text = "Error - Recipe Not Found")
    else:
        string = f"Servings: {out[0][0]}\n"
        if out[0][1] == "ERROR":
            string += f"ERROR - price can't be calculated"
        else:
            string += f"Price per Serving: £{(out[0][1]/100)/out[0][0]:.2f}\nOverall Price: £{out[0][1]/100:.2f}" # pence to pounds
        display[0].configure(text = string)
        string = ""
        long = 0
        pad_char = " "
        for i in range(1, len(out)):
            if len(str(out[i][0])) > long:
                long = len(str(out[i][0]))
        for i in range(1, len(out)):
            if out[i][1] % 1 != 0:
                string += f"{out[i][0]:{pad_char}<{long}}\t{out[i][1]:.3f} {out[i][2]}\n"
            else:
                string += f"{out[i][0]:{pad_char}<{long}}\t{out[i][1]:.0f} {out[i][2]}\n"
        display[1].configure(text = string)
        string = "Make the thing :)"
        display[2].configure(text = string)

    for i in range(3): #placement math
        display[i].place(x = 0, y = offset_y)
        window.update_idletasks()
        offset_y += display[i].winfo_height()
        tmp = display[i].winfo_width()
        if tmp > offset_x:
            offset_x = tmp
    widgets[3].place(x = 0, y = offset_y)
    window.update_idletasks()
    tmp = widgets[3].winfo_width()
    widgets[4].place(x = tmp, y = offset_y)
    window.update_idletasks()
    tmp += widgets[4].winfo_width()
    if tmp > offset_x:
        offset_x = tmp
    widgets[1].place(x = offset_x, y = 0)
    window.update_idletasks()
    offset_y = widgets[1].winfo_height()
    pad_x = 20
    for swaps in widgets[2]:
        swaps[0].place(x = offset_x, y = offset_y)
        window.update_idletasks()
        offset_y += swaps[0].winfo_height()
        for swap in swaps[1][1]:
            swap.place(x = offset_x + pad_x, y = offset_y)
            window.update_idletasks()
            offset_y += swap.winfo_height()

def collect(table, match):
    """Collects the list of ingredients
Takes in the table and ID (recipe or swap)"""
    if table == "Recipes":
        tag = "meal"
    elif table == "Swap_repl":
        tag = "swap"
    out = cur.execute(
            f"""SELECT Ingredients.ingred_id, Ingredients.ingred_name, -- 0,1
{table}.amount, -- 2
{table}.unit_id, Ingredients.unit_id -- 3,4
FROM Ingredients, {table}
WHERE {table}.{tag}_id = {match}
AND {table}.ingred_id = Ingredients.ingred_id""").fetchall()
    return out

def replace(swaps):
    """Returns which ingredients should be replaced with which selected substitute"""
    repls = []
    for swap in swaps: #each item that can be replaced
        count = 0
        for i in range(len(swap[1][0])):
            if swap[1][0][i].get() == "on":
                count += 1
                repl = swap[1][2][i]
        if count == 1: #only one substite can be selected for any ingredient
                repls.append(repl)
        else: #if more than one selected, reset
            for check in swap[1][0]:
                    check.set(value = "off")
    return(repls)

def price(items, frac, out):
    """Collects all ingredients into a neat list & calculates the price"""
    for item in items:
        cost = cur.execute(
            f"""SELECT ingred_price
FROM Ingredients
WHERE ingred_id = {item[0]}""").fetchall()[0][0]
        if item[3] != item[4]: #price match
            match_frac = unit_match([item[4], item[4]], [item[3], item[0]])
            if match_frac != None:
                cost = cost * match_frac
            else:
                out[0][1] = "ERROR"
        if out[0][1] != "ERROR":
            out[0][1] = out[0][1] + (cost * (item[2] * frac))
        unit = cur.execute(
            f"""SELECT unit_value
FROM Units
WHERE unit_id = {item[3]}""").fetchall()[0][0]
        out.append([item[1], item[2] * frac, unit])
    return out

def neat(meal_id, intended, repls):
    """Prepends the list of ingredients with the servings"""
    num = intended.get()
    original = cur.execute(
        f"""SELECT servings
FROM Meals
WHERE {meal_id} = meal_id""").fetchall()[0][0]
    frac, servings = multiplier(original, num)
    out = [[servings, 0]]
    ingredients = collect("Recipes", meal_id)
    new = []
    for p in range(len(ingredients)):
        ingred = ingredients[p]
        swaps = cur.execute(f"SELECT swap_id, amount, unit_id FROM Swap_og WHERE {ingred[0]} = ingred_id").fetchall()
        if len(swaps) != 0 and len(repls) != 0:
            for i in range(len(swaps)):
                swap_id = swaps[i][0]
                if swap_id in repls:
                    swap = collect("Swap_repl", swap_id)
                    frac_swap = multiplier(swaps[i][1], ingred[2])[0]
                    if ingred[3] != swaps[i][2]:
                        unit_frac = unit_match([swaps[i][2], swaps[i][2]], [ingred[3], ingred[0]])
                        if unit_frac != None:
                            frac_swap = frac_swap * unit_frac
                    for i2 in range(len(swap)):
                        swap[i2] = [swap[i2][0], swap[i2][1], swap[i2][2] * frac_swap, swap[i2][3], swap[i2][4]]
                    new.append([p, swap]) #index of ingredient to be replaced, and relplacement
    o = 0 #offset
    i = 0
    while len(new) != 0:
        if i == new[0][0]: #ingredient index == replacement location
            ingredients = ingredients[:i+o] + new[0][1] + ingredients[i+o+1:]
            o += len(new[0][1]) - 1
            new = new[1:]
        i += 1
    out = price(ingredients, frac, out)
    return out

def recalc(meal_id, ent_serv, widgets, offset_x, offset_y, window, swaps):
    """Recalculates recipe"""
    repls = replace(swaps)
    out = neat(meal_id, ent_serv, repls)
    pretty(out, widgets, offset_x, offset_y, window)

def download(meal_id, ent_serv, swaps):
    """Downloads the recipe as a txt file"""
    repls = replace(swaps)
    out = neat(meal_id, ent_serv, repls)
    no = []
    for swap in swaps: #each item that can be replaced
        repl = False
        for i in range(len(swap[1][0])):
            if swap[1][0][i].get() == "on":
                repl = True
        if repl:
            no.append(swap[0].cget("text"))
    og = [cur.execute(f"""SELECT meal_name FROM Meals WHERE {meal_id} = meal_id""").fetchall()[0][0]]
    words = og + no
    name = ""
    for i in range(len(words)):
        if i !=0:
            name += "_NO_"
        for c in words[i]:
            c = c.lower()
            if c == " ":
                name += ("_")
            elif c in "abcdefghijklmnopqrstuvwxyz":
                name += (c)
            else:
                name += ("X")
    if len(out) == 0:
        string = "No recipe :("
    else:
        string = f"Servings: {out[0][0]}\n"
        if out[0][1] == "ERROR":
            string += f"ERROR - price can't be calculated"
        else:
            string += f"Price per Serving: £{(out[0][1]/100)/out[0][0]:.2f}\nOverall Price: £{out[0][1]/100:.2f}\n" # pence to pounds
        string += "\n"
        long = 0
        pad_char = " "
        for i in range(1, len(out)):
            if len(str(out[i][0])) > long:
                long = len(str(out[i][0]))
        for i in range(1, len(out)):
            if out[i][1] % 1 != 0:
                string += f"{out[i][0]:{pad_char}<{long}}\t{out[i][1]:.3f} {out[i][2]}\n"
            else:
                string += f"{out[i][0]:{pad_char}<{long}}\t{out[i][1]:.0f} {out[i][2]}\n"
        string += "\n"
        string += "Make the thing :)"
    file = open(f"{name}.txt", "w")
    file.write(string)
    file.close()
    confirm = ctk.CTk()
    confirm.title(f"{name}-download")
    lbl = ctk.CTkLabel(confirm, text = "Download successful!")
    lbl.grid(row = 0, column = 0)
    confirm.mainloop()
    

def check(meal_id, window):
    """Checks which ingredients can be swapped and generates a list of checkboxes
[[lbl,[[chk_var,...],[chk_box,...],[swap_id,...]]],...]"""
    swaps = []
    ingreds = collect("Recipes", meal_id)
    for ingred in ingreds:
        repls = cur.execute(f"SELECT swap_id FROM Swap_og WHERE {ingred[0]} = ingred_id").fetchall()
        if len(repls) != 0: #is there a swap available?
            swaps.append([ctk.CTkLabel(window, text = ingred[1]), [[], [], []]]) #the ingredient being replaced
            for i in range(len(repls)):
                repl = repls[i][0]
                items = collect("Swap_repl", repl)
                string = ""
                for item in items:
                    string += str(item[1]) + " + "
                string = string[:-3] #cuts of the excess " + "
                swaps[-1][1][0].append(ctk.StringVar(value = "off"))
                swaps[-1][1][1].append(ctk.CTkCheckBox(window,
                                                    text = string,
                                                    command = lambda: replace(swaps),
                                                    variable = swaps[-1][1][0][i],
                                                    onvalue = "on",
                                                    offvalue = "off"))
                swaps[-1][1][2].append(repl)
    return swaps

def page(meal_id):
    """Generates the recipe page"""
    name, serve = cur.execute(
        f"""SELECT meal_name, servings
        FROM Meals
        WHERE {meal_id} = meal_id""").fetchall()[0]
    
    window = ctk.CTk()
    window.title(name)
    window.geometry("800x500")
    widgets = []
    offset_x = 0
    offset_y = 0

    lbl_serv = ctk.CTkLabel(window, text = "Servings:")
    ent_serv = ctk.CTkEntry(window, placeholder_text = str(serve))

    lbl_extra = ctk.CTkLabel(window, text = "") #for servings, prices, etc.
    lbl_ingred = ctk.CTkLabel(window, text = "")
    lbl_instruct = ctk.CTkLabel(window, text = "")
    display = [lbl_extra, lbl_ingred, lbl_instruct]

    lbl_swap = ctk.CTkLabel (window, text = "Replacements")
    swaps = check(meal_id, window) #will hold all possible swaps for recipe
    
    btn_calc = ctk.CTkButton(window, text = "Recalculate",
                             command = lambda: recalc(meal_id,
                                                      ent_serv,
                                                      widgets,
                                                      offset_x,
                                                      offset_y,
                                                      window,
                                                      swaps))
    btn_print = ctk.CTkButton(window, text = "Download",
                              command = lambda: download(meal_id,
                                                      ent_serv,
                                                      swaps))

    widgets = [display, lbl_swap, swaps, btn_calc, btn_print] #placement varies depending on content

    lbl_serv.place(x = 0, y = 0)
    window.update_idletasks() #calls all the events that are pending without processing any other events or callback
    offset_x = lbl_serv.winfo_width()
    ent_serv.place(x = offset_x, y = 0)
    window.update_idletasks() #in this case it forces ctk to calculate the geometry
    offset_x += ent_serv.winfo_width()
    offset_y = lbl_serv.winfo_height()
    tmp = ent_serv.winfo_height()
    if tmp > offset_y:
        offset_y = tmp

    recalc(meal_id, ent_serv, widgets, offset_x, offset_y, window, swaps)
    window.mainloop()
