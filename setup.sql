-- {{{ Clean Up
	DROP TABLE IF EXISTS Ingredients;
	DROP TABLE IF EXISTS Meals;
	DROP TABLE IF EXISTS Recipes;
	DROP TABLE IF EXISTS Unit_type;
	DROP TABLE IF EXISTS Units;
	DROP TABLE IF EXISTS Swap_original;
	DROP TABLE IF EXISTS Swap_replacement;
	DROP TABLE IF EXISTS Conversion_same;
	DROP TABLE IF EXISTS Conversion_other;
-- }}}

-- {{{ Tables
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
	
	CREATE TABLE Unit_type (
		type_id INTEGER PRIMARY KEY,
		type_name TEXT);
	
	CREATE TABLE Units (
		unit_id INTEGER PRIMARY KEY,
		unit_value TEXT,
		type_id INTEGER,
		FOREIGN KEY (type_id) REFERENCES Unit_type (type_id));
	
	CREATE TABLE Recipes (
		meal_id INTEGER,
		ingred_id INTEGER,
		amount DECIMAL,
		unit_id INTEGER,
		FOREIGN KEY (meal_id) REFERENCES Meals (meal_id),
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unit_id) REFERENCES Units (unit_id));
	
	CREATE TABLE Swap_original (
		swap_id INTEGER PRIMARY KEY, -- multiple replacement options
		ingred_id INTEGER,
		amount DECIMAL,
		unit_id INTEGER,
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unit_id) REFERENCES Units (unit_id));
	
	CREATE TABLE Swap_replacement (
		swap_id INTEGER,
		ingred_id INTEGER, -- replacement made up of multiple items
		amount DECIMAL,
		unit_id INTEGER,
		FOREIGN KEY (swap_id) REFERENCES Swap_original (swap_id),
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unit_id) REFERENCES Units (unit_id));
	
	CREATE TABLE Conversion_same (
		unit1_id INTEGER, -- * multiplier -> unit2_id
		unit2_id INTEGER, -- / multiplier -> unit1_id
		type_id INTEGER,
		multiplier DECIMAL,
		FOREIGN KEY (unit1_id) REFERENCES Units (unit_id)
		FOREIGN KEY (unit2_id) REFERENCES Units (unit_id)
		FOREIGN KEY (type_id) REFERENCES Unit_type (type_id));
	
	CREATE TABLE Conversion_other (
		ingred_id INTEGER,
		unit_vol_id INTEGER, -- the naming scheme is a little broken, but if instead of volume, the type is number, this value is still used.
		unit_mass_id INTEGER, -- / density -> unit_vol_id
		density DECIMAL,
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unit_vol_id) REFERENCES Units (unit_id),
		FOREIGN KEY (unit_mass_id) REFERENCES Units (unit_id));
	
-- }}}

-- {{{ Data
.mode csv

.import Ingredients.csv tmp
	INSERT INTO Ingredients (ingred_id, ingred_name, ingred_price, unit_id) SELECT ingred_id, ingred_name, ingred_price, unit_id FROM tmp;
	DROP TABLE tmp;

.import Meals.csv tmp
	INSERT INTO Meals (meal_id, meal_name, servings) SELECT meal_id, meal_name, servings FROM tmp;
	DROP TABLE tmp;

.import Recipes.csv tmp
	INSERT INTO Recipes (meal_id, ingred_id, amount, unit_id) SELECT meal_id, ingred_id, amount, unit_id FROM tmp;
	DROP TABLE tmp;

.import Unit_type.csv tmp
	INSERT INTO Unit_type (type_id, type_name) SELECT type_id, type_name FROM tmp;
	DROP TABLE tmp;

.import Units.csv tmp
	INSERT INTO Units (unit_id, unit_value) SELECT unit_id, unit_value FROM tmp;
	DROP TABLE tmp;

.import Swap_original.csv tmp
	INSERT INTO Swap_original (swap_id, ingred_id, amount, unit_id) SELECT swap_id, ingred_id, amount, unit_id FROM tmp;
	DROP TABLE tmp;

.import Swap_replacement.csv tmp
	INSERT INTO Swap_replacement (swap_id, ingred_id, amount, unit_id) SELECT swap_id, ingred_id, amount, unit_id FROM tmp;
	DROP TABLE tmp;

.import Conversion_same.csv tmp
	INSERT INTO Conversion_same (unit1_id, unit2_id, type_id, multiplier) SELECT unit1_id, unit2_id, type_id, multiplier FROM tmp;
	DROP TABLE tmp;

.import Conversion_other.csv tmp
	INSERT INTO Conversion_other (ingred_id, unit_vol_id, unit_mass_id, density) SELECT ingred_id, unit_vol_id, unit_mass_id, density FROM tmp;
	DROP TABLE tmp;

-- }}}