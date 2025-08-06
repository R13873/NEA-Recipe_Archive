SELECT Meals.meal_name as Name, Meals.servings as Serves, Ingredients.ingred_name as Ingredient, Recipes.amount as Amount, Units.unit_value as Unit, 0 as Price_per_Serving
FROM Recipes, Meals, Ingredients, Units
WHERE Recipes.meal_id = Meals.meal_id
AND Recipes.ingred_id = Ingredients.ingred_id
AND Recipes.unit_id = Units.unit_id
ORDER BY Meals.meal_id