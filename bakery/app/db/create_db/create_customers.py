import sys
import random
import sqlite3


db_file = sys.argv[1]
dir = sys.argv[2]

conn = sqlite3.connect(db_file)

cur = conn.cursor()

count = 0
for first in open(dir + "/first_names.txt"):
	for last in open(dir + "/last_names.txt"):
		first = first.strip()
		last = last.strip()
		count += 1
		email = first + last + "@gmail.com"
		birthdate = random.randint(-1577923200, 1104537600)
		
		query = "INSERT INTO Customer VALUES (?, ?, ?, ?)"
		query_args = (email, first + " " + last, birthdate, first + last)
		cur.execute(query, query_args)

conn.commit()

print("Added %i values to Coustomers" % count)
