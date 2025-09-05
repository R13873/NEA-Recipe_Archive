-- {{{ Clean Up
	DROP TABLE IF EXISTS Ingredients;
	DROP TABLE IF EXISTS Meals;
	DROP TABLE IF EXISTS Recipes;
	DROP TABLE IF EXISTS Units;
	DROP TABLE IF EXISTS Swap_original;
	DROP TABLE IF EXISTS Swap_replacement;
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

	CREATE TABLE Units (
		unit_id INTEGER PRIMARY KEY,
		unit_value TEXT);
	
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
		FOREIGN KEY (meal_id) REFERENCES Meals (meal_id),
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unit_id) REFERENCES Units (unit_id));
	
	CREATE TABLE Swap_replacement (
		swap_id INTEGER,
		ingred_id INTEGER, -- replacement made up of multiple items
		amount DECIMAL,
		unit_id INTEGER,
		FOREIGN KEY (swap_id) REFERENCES Swap_original (swap_id),
		FOREIGN KEY (meal_id) REFERENCES Meals (meal_id),
		FOREIGN KEY (ingred_id) REFERENCES Ingredients (ingred_id),
		FOREIGN KEY (unit_id) REFERENCES Units (unit_id));
	
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

.import Units.csv tmp
	INSERT INTO Units (unit_id, unit_value) SELECT unit_id, unit_value FROM tmp;
	DROP TABLE tmp;

-- }}}