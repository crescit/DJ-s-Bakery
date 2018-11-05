import sys
import random
import sqlite3


conn = sqlite3.connect(sys.argv[1])

cur = conn.cursor()

cats = ["bread", "white bread", "wheat bread", "gluten", "gluten-free", "whole wheat", \
	"cake", "muffin", "bun", "cupcake", "brownie", "sourdough", "pumpkin", "spice",\
	 "Sweet", "bun", "Cinnamon", "Almond", "Cranberry", "Fruit", "Nut", "cheese", \
	"strawberry", "Holiday", "cheddar", "Filled", "coconut", "flax", "pecan", "pie",\
	 "pudding", "hot", "poppy", "seed", "loaf", "beer", "sandwich", "honey", "breadsticks",\
	 "stuffing", "flour", "soft", "dark", "bananna", "grain", "zucchini", "tea", "wrap", \
	"quinoa", "dinner", "no-kneed", "easy", "harvest", "cream", "pizza", "apple", "grape",\
	 "sour", "PB&J", "russian", "swedish", "bacon", "chive", "party", "tuscan", "lemon", \
	"golden", "tomato", "crust", "tangy", "ham", "olive", "semolina", "butter", "artisan",\
	 "rye", "braided", "pretzel", "barley", "breakfast", "wild", "dried", "favorite",\
	 "pumpernickel", "provolone", "wine", "12-grain", "10-grain", "6-grain", "spread", \
	"parmesan", "pepper", "english", "cherry", "pan", "quick", "Vermont", "peanut", "challah"\
	"caramel", "herb", "maple", "fresh", "deli", "flour", "roast", "mini", "American", "jewish",\
	 "limerick", "no-knead", "honeycomb", "jelly", "whole", "onion", "natural", "rustic",\
	 "double", "garlic", "bread"]

id = 0
for cat in cats:
	id += 1
	query = "INSERT INTO Category VALUES (?, ?)"
	cur.execute(query, (id, cat))

conn.commit()
print("Added %i values to Category" % id)

