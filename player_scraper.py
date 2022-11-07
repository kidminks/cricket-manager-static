import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import json

f = open('team.json')
teams = json.load(f)
f.close()

f = open('player.json')
players = json.load(f)
f.close()

f = open('player_team_mapping.json')
ptm = json.load(f)
f.close()

wikiBase = "https://en.wikipedia.org"

player_index = len(players) + 1
ptm_index = len(ptm) + 1

def findOrInsert(row, country, name_index):
	for player in players:
		if player["name"] == row[name_index] and player["country"] == country:
			return player["id"]
	return -1

continue_for = int(input("continue for : "))
for team in teams:

	if continue_for > 0:
		continue_for -= 1;
		continue;

	print("Working for : ", team)

	skip = input("skip dom : ")
	if skip == "1":
		continue


	nationality_index = -1
	country = "Sri Lanka"
	# if nationality_index == -1:		
	# 	country = input("country : ")	

	with urllib.request.urlopen(team['link']) as response:
		soup = BeautifulSoup(response, 'html.parser')
		tables=soup.findAll('table',{'class':"wikitable"})
		for table in tables:
			print(table)
			skip = input("skip dom : ")
			if skip == "1":
				continue

			name_index = int(input("name index :"))
			batting_style_index = int(input("Batting style index :"))
			bowling_style_index = int(input("Bowling stype index :"))	
			notes_index = int(input("notes index : "))

			df=pd.read_html(str(table))
			df=pd.DataFrame(df[0])

			player_type = "Batsmen"

			for row in df.itertuples(index=False):
				print(row)
				if row[1] == row[2]:
					player_type = row[1]
					continue
				if nationality_index != -1:
					country = row[nationality_index]
				player_id = findOrInsert(row, country, name_index)
				if player_id == -1:
					note = ""
					if not pd.isna(row[notes_index]):
						note += row[notes_index]
					players.append({"id": player_index, "name": row[name_index], "country": country, \
						"batting_style": row[batting_style_index], "bowling_style": row[bowling_style_index], "player_type": player_type, \
						 "notes": note + ":::" + player_type})
					player_id = player_index
					print({"id": player_index, "name": row[name_index], "country": country, \
						"batting_style": row[batting_style_index], "bowling_style": row[bowling_style_index], "player_type": player_type, \
						 "notes": note + ":::" + player_type})
					player_index += 1
				ptm.append({"id": ptm_index, "player_id": player_id, "team_id": team["id"]})
				print({"id": ptm_index, "player_id": player_id, "team_id": team["id"]})
				ptm_index += 1


	player_dump = json.dumps(players)
	with open("player.json", "w") as outfile:
	    outfile.write(player_dump)

	ptm_dump = json.dumps(ptm)
	with open("player_team_mapping.json", "w") as outfile:
	    outfile.write(ptm_dump)



