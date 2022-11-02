from bs4 import BeautifulSoup
import urllib.request
import json

f = open('team.json')
teams = json.load(f)
f.close()

f = open('tournament_team_mapping.json')
ttm = json.load(f)
f.close()

f = open('tournament.json')
tournaments = json.load(f)
f.close()

wikiBase = "https://en.wikipedia.org"

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

def selection(val):
	if val == "A":
		return "Ameture"
	if val == "M":
		return "Mature"
	if val == "S":
		return "Skilled"
	if val == "P":
		return "Pro"
	if val == "L":
		return "Legend"


team_index = len(teams)
tournament_index = 0
ttm_index = len(ttm)

continue_for = int(input("continue for : "))
for tournament in tournaments:

	if continue_for > 0:
		continue_for -= 1;
		tournament_index += 1
		continue;

	print("Working for : ", tournament)
	skip = input("skip dom : ")
	if skip == "1":
		tournament_index += 1
		continue

	webPath = input("web path : ")	
	copy_from_tournament = int(input("copy from tournament : "))
	if copy_from_tournament != 0:
		for mapping in ttm:
			if mapping["tournament_id"] == copy_from_tournament:
				ttm_index += 1
				mapping["id"] = ttm_index
				mapping["tournament_id"] = tournament["id"]
				ttm.append(mapping)
		tournament["link"] = webPath
		tournaments[tournament_index] = tournament
	else:
		with urllib.request.urlopen(webPath) as response:
			soup = BeautifulSoup(response, 'html.parser')
			tag = input("tag to find : ")
			doms = soup.findAll(tag)
			for dom in doms:
				print(dom)
				skip = input("skip dom : ")
				if skip == "1":
					continue
				if skip == "E":
					break
				links = dom.findAll("a")
				for link in links:
					print(link)
					skip = input("skip link : ")
					if skip == "1":
						continue
					hiring_cond = selection(input("hiring condition :"))
					type = tournament["type"]
					level = tournament["level"]
					abbr = link.text
					name = link["title"]
					country_id = tournament["country_id"]
					href = wikiBase + link["href"]
					tournament["link"] = webPath
					tournaments[tournament_index] = tournament
					team_index += 1
					ttm_index += 1
					print(tournament)
					print ({"id": team_index, "name": name, "type": type, "country_id": country_id, "level": level,\
					 "abbr": abbr,"hiring_cond": hiring_cond, "link": href})
					teams.append({"id": team_index, "name": name, "type": type, "country_id": country_id, "level": level,\
					 "abbr": abbr,"hiring_cond": hiring_cond, "link": href})
					print({"id": ttm_index, "tournament_id": tournament["id"], "team_id": team_index})
					ttm.append({"id": ttm_index, "tournament_id": tournament["id"], "team_id": team_index})

	tournament_index += 1

	team_dump = json.dumps(teams)
	with open("team.json", "w") as outfile:
		outfile.write(team_dump)

	tournament_dump = json.dumps(tournaments)
	with open("tournament.json", "w") as outfile:
	    outfile.write(tournament_dump)

	ttm_dump = json.dumps(ttm)
	with open("tournament_team_mapping.json", "w") as outfile:
	    outfile.write(ttm_dump)



