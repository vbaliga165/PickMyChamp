""" 
PickMyChamp is a league of legends utility to help a summoner choose which champion is best for them to play in any given scenario
@ 2018 by Vijay Baliga

This class takes the user's input and finds out all important information regarding user/champion stats

"""
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from Champion import Champion
import difflib 

# prints introduction and explains utility
print("Welcome to PickMyChamp: utility to help generate the most applicable champion for a game of LoL\n")

# prompts user to enter champion name, does not need to be word-for-word
opponent = input("Please enter the name of the champion you are laning against (be fairly specific)-> Ex. Lee Sin = Lee):\n")

# gets true website url by appending text to the end of a generic link
def get_true_url(text_to_add, url_to_add, symbol):
	final_url = url_to_add
	if len(text_to_add.split()) == 1:
		final_url = url_to_add + text_to_add
	else:
		words = text_to_add.split()
		i = 0
		for word in words:
			if i < len(words) - 1:
				final_url = final_url + (word + symbol)
			else:
				final_url = final_url + word
			i = i + 1
	return final_url

page_soup = None

# opens up the connection and grabs the page
def open_page(url):
	url_request = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
	page_html = urlopen(url_request).read()

	# parses the html (basically collects all the HTML together in an applicable format for operating)
	global page_soup
	page_soup = soup(page_html,"html.parser")

# gets the real champion given the abbreviated name by searching ChampionList.txt for "good enough" matches
input_file = open("ChampionList.txt","r")
champion_list = []

for line in input_file:
	champion_list.append(line[:-1])

input_file.close()
possible_opponent_champs = difflib.get_close_matches(opponent,champion_list)

opponent_copy = ""
counter_url = ""
for inc in range(len(possible_opponent_champs)):
	is_right_champ = input("\nIs " + possible_opponent_champs[inc] + " the champion you are facing against?\n").strip()
	if difflib.SequenceMatcher(None,is_right_champ,"yes").ratio() > 0.25:
		if "'" in possible_opponent_champs[inc]:
			true_opponent = possible_opponent_champs[inc].replace("'","")
		elif "." in possible_opponent_champs[inc]:
			true_opponent = possible_opponent_champs[inc].replace(".","")
		else:
			true_opponent = possible_opponent_champs[inc]
		opponent_copy = possible_opponent_champs[inc]
		counter_url = get_true_url(true_opponent,"https://www.lolcounter.com/champions/","-")
		break
	elif difflib.SequenceMatcher(None,is_right_champ,"no").ratio() > 0.25:
		continue

# gets list of champions enemy is strong or weak against
def get_counter_list(strength):
	open_page(counter_url + strength)
	all_champ_tag = page_soup.findAll("div",{"class":"name"})
	all_champ_tag.remove(all_champ_tag[0])

	acceptable_picks = []

	for spot in range(len(all_champ_tag)):
		acceptable_picks.append(all_champ_tag[spot].text)

	return acceptable_picks

good_pick_champs = get_counter_list("/strong")
bad_pick_champs = get_counter_list("/weak")

# prompts user to input username
summoner_username = input("\nPlease provide your league of legends username (case sensitive):\n").strip()

# gets the url for the summoner champion page and opens it
summoner_url = get_true_url(summoner_username, "http://na.op.gg/summoner/champions/userName=", "%20")
open_page(summoner_url)

"""" collects each champion played in season 8

Row TopRanker is each of a summoner's "top ranking" champion, 
indicated by amount of games played on any given chamption, as well as win rate for that champion

Row is any other champion played by a summoner, indicated by data for any chamption that is not a 'TopRanker'

Gets rid of row not indicating chamption data (which is the first element in the list)
"""
rows = page_soup.findAll("tr",{"class":"Row TopRanker" and "Row"})
rows.remove(rows[0]);

""" gathers all neccessary data (name, win rate, games played, kda ratio)
	about each champion played to help decide which champion is the best choice
"""

# gets the wins/losses on each champion
def get_games_played(index, counter):
	amount = 0
	try:
		if counter == 0:
			amount = int((rows[index].find('div',class_='Text Left').text)[:-1])
		elif counter == 1:
			amount = int((rows[index].find('div',class_='Text Right').text)[:-1])
	except AttributeError:	
		pass
	return amount

champions = []

for index in range(len(rows)):
	champ_name = rows[index].find('td',class_='ChampionName Cell').text.strip()
	win_ratio = float(rows[index].find('td',class_='RatioGraph Cell')["data-value"])

	games_played = 0

	for x in range(2):
		games_played = games_played + get_games_played(index, x)

	kda_ratio_line = rows[index].find('td',class_='KDA').text.strip()
	try:
		#kda has a decimal (length > 1)
		kda_ratio = float(kda_ratio_line[kda_ratio_line.index(".",len(kda_ratio_line) - 10) - 1:kda_ratio_line.index(":")])
	except ValueError:
		#kda does not have a decimal (length 1)
		kda_ratio = float(kda_ratio_line[kda_ratio_line.index(":",len(kda_ratio_line) - 10) - 1:kda_ratio_line.index(":")])
	
	if games_played > 2:
		champions.append(Champion(champ_name,win_ratio,games_played,kda_ratio))

	#Champion.print_champ_data(champions[index])
