import sys
import random
import sqlite3


db_file = sys.argv[1]
dir = sys.argv[2]

conn = sqlite3.connect(db_file)

cur = conn.cursor()

id = 0
for first in open(dir + "/first_names.txt"):
	for last in open(dir + "/last_names.txt"):
		first = first.strip()
		last = last.strip()

		id += 1
		SSN = random.randint(100000000,999999999);
		
		query = "INSERT INTO Employee VALUES (?, ?, ?, ?)"
		query_args = (id, first + " " + last, SSN, first + last)

		cur.execute(query, query_args)

		if id >= 200:
			break

conn.commit()

print("Added %i values to Employee" % id)
