import customtkinter as ctk

class recipe:
    def __init__(self, name):
        self._title = name.lower()
        self._ingredients = []
    def add_ingred(self, amount, unit, item):
        self._ingredients.append([float(amount), unit, item])
    def get_name(self):
        return self._title
    def pretty(self):
        string = ""
        for pair in  self._ingredients:
            string += f"{pair[0]} {pair[1]}\t\t{pair[2]}\n"
        return string

def reset(take, out):
    take.delete(0, ctk.END)
    out.configure(text = "")

def search(keyword, display, collection):
    check = keyword.get()
    found = False
    for val in collection:
        if check.lower() == val.get_name():
            found = True
            string = val.pretty()
    if not found:
        string = "ERROR - recipe not found"
    display.configure(text = string)

recipes = []
recipes.append(recipe("bread"))
recipes[0].add_ingred(600, "g", "flour")
recipes[0].add_ingred(450, "ml", "water")
recipes[0].add_ingred(1, "tsp", "salt")
recipes[0].add_ingred(1, "tsp", "sugar")
recipes[0].add_ingred(1, "tsp", "yeast")
recipes[0].add_ingred(1, "tbsp", "oil")
recipes.append(recipe("brownies"))
recipes[1].add_ingred(2, "", "bananas")
recipes[1].add_ingred(200, "g", "sugar")
recipes[1].add_ingred(130, "g", "melted butter")
recipes[1].add_ingred(95, "g", "flour")
recipes[1].add_ingred(40, "g", "cocoa powder")
recipes[1].add_ingred(1/8, "tsp", "salt")

window = ctk.CTk()
window.title("Test")
window.geometry("600x400")

ent_keyword = ctk.CTkEntry(window)
btn_search = ctk.CTkButton(window, text = "search", command = lambda: search(ent_keyword, lbl_display, recipes))
lbl_display = ctk.CTkLabel(window, text = "")
btn_reset = ctk.CTkButton(window, text = "clear", command = lambda: reset(ent_keyword, lbl_display))
ent_keyword.grid(row = 0, column = 0)
btn_search.grid(row = 0, column = 1)
btn_reset.grid(row = 0, column = 2)
lbl_display.grid(row = 1, column = 0)

window.mainloop()
