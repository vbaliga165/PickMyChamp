""" 
PickMyChamp is a league of legends utility to help a summoner choose which champion is best for them to play in any given scenario
@ 2018 by Vijay Baliga

This class implements all neccessary data calculated from DataGather.py in an algorithm to decide who is actually the user's best choice champion

"""
from DataGather import champions, opponent_copy, good_pick_champs, bad_pick_champs

import pandas as pd
from pandas import DataFrame
from sklearn import linear_model
import statsmodels.api as sm
import matplotlib.pyplot as plt

names = []
win_rates = []
games = []
kds_ratios = []

for champ in champions:
	names.append(champ.get_name())
	win_rates.append(champ.get_winrate())
	games.append(champ.get_games_played())
	kds_ratios.append(champ.get_kda())



Summoner_Data = { 
	'Name' : names,
	'Win Rate' : win_rates,
	'Games' : games,
	'KDA' : kds_ratios
}

frame = DataFrame(Summoner_Data,columns = ['Name','Win Rate','Games','KDA'])

"""
plt.scatter(frame['Games'], frame['Win Rate'], color='red')
plt.title('Games Played vs Win Rate', fontsize=14)
plt.xlabel('Games Played', fontsize=14)
plt.ylabel('Win Rate', fontsize=14)
plt.grid(True)
plt.show()

plt.scatter(frame['KDA'], frame['Win Rate'], color='green')
plt.title('KDA vs Win Rate', fontsize=14)
plt.xlabel('KDA', fontsize=14)
plt.ylabel('Win Rate', fontsize=14)
plt.grid(True)
plt.show()
"""

X = frame[['Games','KDA']] 
Y = frame['Win Rate']

regr = linear_model.LinearRegression()
regr.fit(X, Y)

""" depiction of intercept and coefficients for summoner data
print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)
"""

predictions = []

for champ in champions:
	Games_Played = champ.get_games_played()
	KDA = champ.get_kda()
	predictions.append(regr.predict([[Games_Played , KDA]]))

	""" table statistics
	X = sm.add_constant(X) 
	 
	model = sm.OLS(Y, X).fit()
	predictions = model.predict(X) 
	 
	print_model = model.summary()
	print(print_model)
	"""

# checks for counters and good picks and changes ratio accordingly
for i in range(len(predictions)):
	for pick in good_pick_champs:
		if champions[i].get_name() == pick:
			predictions[i] = predictions[i]*0.75

for k in range(len(predictions)):
	for pick in bad_pick_champs:
		if champions[k].get_name() == pick:
			predictions[k] = predictions[k]*1.25


predictions, names = (list(t) for t in zip(*sorted(zip(predictions, names))))
print("\nYou might want to try going " + names[len(names)-1] + ", " + names[len(names)-2] + ", or " + names[len(names)-3] + ".")
