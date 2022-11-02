from bs4 import BeautifulSoup
import urllib.request
import json

f = open('team.json')
teams = json.load(f)
f.close()

f = open('tournament.json')
tournaments = json.load(f)
f.close()

f = open('tournament_team_mapping.json')
ttm = json.load(f)
f.close()

index = len(ttm) + 1
continue_for = int(input("continue for : "))
for tournament in tournaments:

	if continue_for > 0:
		continue_for -= 1;
		continue;

	print("Working for : ", tournament)
	skip = input("skip dom : ")
	if skip == "1":
		continue

	start = int(input("start team id : "))
	end = int(input("end team id : "))

	for team in teams:
		if team["id"] >= start and team["id"] <= end:
			ttm.append({"id": index, "tournament_id": tournament["id"], "team_id": team["id"]})
			index += 1

	ttm_dump = json.dumps(ttm)
	with open("tournament_team_mapping.json", "w") as outfile:
	    outfile.write(ttm_dump)



