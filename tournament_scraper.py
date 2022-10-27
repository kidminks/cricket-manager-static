from bs4 import BeautifulSoup
import urllib.request
import json

def getType(val):
	if val == "N":
		return "National"
	if val == "C":
		return "Club"
	if val == "S":
		return "State"
	if val == "Z":
		return "Zonal"
	if val == "R":
		return "Regional"
	if val == "SZ":
		return "StateAndZonal"

def getLevel(val):
	if val == "I":
		return "International"
	if val == "D":
		return "Domestic"

def getFormat(val):
	if val == "O":
		return "OneDay"
	if val == "2":
		return "T20"
	if val == "T":
		return "Test"


f = open('tournament.json')
data = json.load(f)
f.close()


with urllib.request.urlopen('https://en.wikipedia.org/wiki/Template:Cricket_in_Zimbabwe') as response:
    soup = BeautifulSoup(response, 'html.parser')
    tables = soup.findAll("table")
    for table in tables:
	    rows = table.findAll("tr")
	    country_id = 12
	    index = len(data)
	    for row in rows:
	    	print(row)
	    	val = input("skip row: ")
	    	if val == "1":
	    		continue
	    	val = input("type: ")
	    	match_type = getType(val)
	    	val = input("level: ")
	    	level = getLevel(val)
	    	td = row.find("td")
	    	links = td.findAll("a")
	    	for link in links:
	    		print(link)
	    		val = input("skip row: ")
		    	if val == "1":
		    		continue
		    	val = input("invitation: ")
	    		invitation = (val == "t")
	    		val = input("format: ")
	    		format = getFormat(val)
	    		val = input("over: ")
	    		over = int(val)
		    	name = link.text
		    	print (index, name, country_id, match_type, invitation, format, over, level, "####")
		    	index += 1
		    	data.append({"id": index, "name": name, "country_id": country_id, "type": match_type, "invitation": invitation, "format": format, "overs": over, "level": level})

data = json.dumps(data)

with open("tournament.json", "w") as outfile:
    outfile.write(data)

