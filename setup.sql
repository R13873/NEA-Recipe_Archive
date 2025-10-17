-- {{{ Clean Up
	DROP TABLE IF EXISTS Unit_type;
	DROP TABLE IF EXISTS Units;
	DROP TABLE IF EXISTS Conv_same;
	DROP TABLE IF EXISTS Ingredients;
	DROP TABLE IF EXISTS Meals;
	DROP TABLE IF EXISTS Recipes;
	DROP TABLE IF EXISTS Swap_og;
	DROP TABLE IF EXISTS Swap_repl;
	DROP TABLE IF EXISTS Conv_other;
-- }}}

-- {{{ Tables
	CREATE TABLE Unit_type (
		type_id INTEGER PRIMARY KEY,
		type_name TEXT); -- mass, volume, other
	
	CREATE TABLE Units (
		unit_id INTEGER PRIMARY KEY,
		unit_value TEXT,
		type_id INTEGER,
		FOREIGN KEY (type_id) REFERENCES Unit_type (type_id));
	
	CREATE TABLE Conv_same (
		unit1_id INTEGER, -- * ratio -> unit2_id
		unit2_id INTEGER, -- / ratio -> unit1_id
		ratio DECIMAL, -- unit2/unit1
		FOREIGN KEY (unit1_id) REFERENCES Units (unit_id),
		FOREIGN KEY (unit2_id) REFERENCES Units (unit_id));
	
	CREATE TABLE Ingredients (
		ingred_id INTEGER PRIMARY KEY,
		ingred_name TEXT,
		ingred_price DECIMAL, -- price in pence per unit
		unit_id INTEGER,
		FOREIGN KEY (unit_id) REFERENCES Units (unit_id));
	
	CREATE TABLE Meals (
		meal_id INTEGER PRIMARY KEY,
		meal_name TEXT,
		servings INTEGER);
	
	CREATE TABLE Recipes (
		meal_id INTEGER,
		ingred_id INTEGER,
		amount DECIMAL,
		unit_id INTEGER,
		FOREIGN KEY (meal_id) REFERENCES Meals (meal_id),
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unit_id) REFERENCES Units (unit_id));
	
	CREATE TABLE Swap_og (
		swap_id INTEGER PRIMARY KEY, -- multiple replacement options
		ingred_id INTEGER,
		amount DECIMAL,
		unit_id INTEGER,
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unit_id) REFERENCES Units (unit_id));
	
	CREATE TABLE Swap_repl (
		swap_id INTEGER,
		ingred_id INTEGER, -- replacement made up of multiple items
		amount DECIMAL,
		unit_id INTEGER,
		FOREIGN KEY (swap_id) REFERENCES Swap_og (swap_id),
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unit_id) REFERENCES Units (unit_id));
	
	CREATE TABLE Conv_other (
		ingred_id INTEGER,
		unitvol_id INTEGER, -- the naming scheme is a little broken, but if instead of volume, the type is number, this value is still used.
		unitmass_id INTEGER, -- / density -> unitvol_id
		density DECIMAL, -- density = mass/vol
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unitvol_id) REFERENCES Units (unit_id),
		FOREIGN KEY (unitmass_id) REFERENCES Units (unit_id));
	
-- }}}

-- {{{ Data
.mode csv

.import Unit_type.csv tmp
	INSERT INTO Unit_type (type_id, type_name) SELECT type_id, type_name FROM tmp;
	DROP TABLE tmp;

.import Units.csv tmp
	INSERT INTO Units (unit_id, unit_value, type_id) SELECT unit_id, unit_value, type_id FROM tmp;
	DROP TABLE tmp;

.import Conv_same.csv tmp
	INSERT INTO Conv_same (unit1_id, unit2_id, ratio) SELECT unit1_id, unit2_id, ratio FROM tmp;
	DROP TABLE tmp;

.import Ingredients.csv tmp
	INSERT INTO Ingredients (ingred_id, ingred_name, ingred_price, unit_id) SELECT ingred_id, ingred_name, ingred_price, unit_id FROM tmp;
	DROP TABLE tmp;

.import Meals.csv tmp
	INSERT INTO Meals (meal_id, meal_name, servings) SELECT meal_id, meal_name, servings FROM tmp;
	DROP TABLE tmp;

.import Recipes.csv tmp
	INSERT INTO Recipes (meal_id, ingred_id, amount, unit_id) SELECT meal_id, ingred_id, amount, unit_id FROM tmp;
	DROP TABLE tmp;

.import Swap_og.csv tmp
	INSERT INTO Swap_og (swap_id, ingred_id, amount, unit_id) SELECT swap_id, ingred_id, amount, unit_id FROM tmp;
	DROP TABLE tmp;

.import Swap_repl.csv tmp
	INSERT INTO Swap_repl (swap_id, ingred_id, amount, unit_id) SELECT swap_id, ingred_id, amount, unit_id FROM tmp;
	DROP TABLE tmp;

.import Conv_other.csv tmp
	INSERT INTO Conv_other (ingred_id, unitvol_id, unitmass_id, density) SELECT ingred_id, unitvol_id, unitmass_id, density FROM tmp;
	DROP TABLE tmp;

-- }}}