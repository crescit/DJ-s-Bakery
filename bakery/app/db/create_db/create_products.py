
import sys
import random
import sqlite3
import string

conn = sqlite3.connect(sys.argv[1])
#conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')

cur = conn.cursor()


recipies = []
categories = []
for val in cur.execute("SELECT CategoryID, CatName FROM Category").fetchall():
	categories.append(val)


# Read king arthur recipies
file = open(sys.argv[2] + "/kaf_recipies.txt")
file.readline()
for line in file:

	line = line.decode('utf-8')

	if not "https://www.kingarthurflour.com/recipes" in line:
		recipies[-1]["text"] += line

	else:
		splitline = line.split(",")

		dic = {}

		dic["title"] = splitline[3]
		dic["text"] = splitline[4]

		recipies.append(dic)

# read home_recipies
file = open(sys.argv[2] + "/home_recipies.txt")
recipies_home = []
for line in file:

	line = line.decode('utf-8')

	if not "https://www.tasteofhome.com/" in line:
		recipies_home[-1]["ingred"] += line

	else:
		splitline = line.split(",")

		dic = {}

		dic["title"] = splitline[3]
		dic["text"] = splitline[4]
		dic["ingred"] = ""

		recipies_home.append(dic)

#fix home recipeies, add to kaf recipies
for r in recipies_home:
	r["text"] = r["ingred"] + r["text"]

recipies.extend(recipies_home)

# replace illegal chars
bad_char = ["\"", "\'"]
for r in recipies:
	r["text"] = r["text"].encode("ascii", errors="ignore").decode()
	r["title"] = r["title"].encode("ascii", errors="ignore").decode()
	for c in bad_char:
		r["text"] = r["text"].replace(c, "")
		r["title"] = r["title"].replace(c, "")
id = 0
rec_count = 0
proCat_count = 0
for r in recipies:
	id += 1
	price = random.gammavariate(2, 3)

	for cat in categories:

		try:
			if cat[1] in r["title"].lower() or cat[1] in r["text"].lower():
				query = "INSERT INTO ProductCategories VALUES (?, ?)"
				cur.execute(query, (id, cat[0]))
				proCat_count += 1
		except Exception as e:

			pass
			

	query = "INSERT INTO Recipe VALUES (?, ?, ?, ?, ?)"
	query_params = (id, id, r["title"], r["text"], 1)
	cur.execute(query, query_params)

	query = "INSERT INTO Product VALUES (?, ?, ?)"
	query_params = (id, r["title"], "%.2f" % price)
	cur.execute(query, query_params)

	rec_count += 1

conn.commit()
print("Added %i values to Recipe" % rec_count)
print("Added %i values to Product" % rec_count)
print("Added %i values to ProductCategories" %proCat_count)






