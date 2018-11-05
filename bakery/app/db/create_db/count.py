
import sys

count = 0
for line in open("king-arthur-recipees_all.txt"):
	if "https://www.kingarthurflour.com/" in line:
		count += 1

print(count)