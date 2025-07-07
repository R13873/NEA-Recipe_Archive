import customtkinter as ctk

class recipe:
    def __init__(self, name, serve):
        self._title = name.lower()
        self._ingredients = []
        self._servings = int(serve)
    def add_ingred(self, amount, unit, item):
        self._ingredients.append([float(amount), unit, item])
    def get_name(self):
        return self._title
    def serving_calc(self, intended):
        return intended / self._servings
    def pretty(self, intended):
        if not intended.isnumeric():
            intended = self._servings
        else:
            intended = int(intended)
        fraction = self.serving_calc(intended)
        string = f"Servings:\t {intended}\n"
        for pair in  self._ingredients:
            string += f"{pair[0] * fraction} {pair[1]}\t\t{pair[2]}\n"
        return string

def reset(ins, out):
    for take in ins:
        take.delete(0, ctk.END)
    out.configure(text = "")

def search(keyword, multiple, display, collection):
    check = keyword.get()
    num = multiple.get()
    found = False
    for val in collection:
        if check.lower() == val.get_name():
            found = True
            string = val.pretty(num)
    if not found:
        string = "ERROR - recipe not found"
    display.configure(text = string)

##file.open(".txt", "r")
##lines = file.readlines()
##for line in lines:
##    print(line.strip())
##file.close

recipes = []
recipes.append(recipe("bread", 7))
doc = open("bread.txt", "r")
lines = doc.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].strip()
    lines[i] = lines[i].split("\t")
    recipes[0].add_ingred(lines[i][0], lines[i][1], lines[i][2])
doc.close()
recipes.append(recipe("brownies", 16))
doc = open("brownies.txt", "r")
lines = doc.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].strip()
    lines[i] = lines[i].split("\t")
    recipes[1].add_ingred(lines[i][0], lines[i][1], lines[i][2])
doc.close()

window = ctk.CTk()
window.title("Test")
window.geometry("600x400")

ent_keyword = ctk.CTkEntry(window)
lbl_serve = ctk.CTkLabel(window, text = "servings: ")
ent_serve = ctk.CTkEntry(window)
ents = [ent_keyword, ent_serve]
btn_search = ctk.CTkButton(window, text = "search", command = lambda: search(ent_keyword, ent_serve, lbl_display, recipes))
lbl_display = ctk.CTkLabel(window, text = "")
btn_reset = ctk.CTkButton(window, text = "clear", command = lambda: reset(ents, lbl_display))
ent_keyword.grid(row = 0, column = 1)
btn_search.grid(row = 0, column = 2)
lbl_serve.grid(row = 1, column = 0)
ent_serve.grid(row = 1, column = 1)
btn_reset.grid(row = 1, column = 2)
lbl_display.grid(row = 2, column = 1)

window.mainloop()
