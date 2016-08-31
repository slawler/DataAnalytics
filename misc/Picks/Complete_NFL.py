# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Get Results of Weekly NFL Picks Pool

Input(s): Sports Illustrated URL, Player Picks
Output(s): Winners, Losers, and Competition Rank for each week

slawler@dewberry.com
Created on Tue Aug 30 09:33:12 2016
"""
#------------Load Python Modules--------------------#
from bs4 import BeautifulSoup
import requests
import pandas as pd

#------------------------------BEGIN SCRIPT----------------------------------#
upcoming_games  = "http://www.si.com/nfl/scoreboard?week=1%2C2"
concluded_games = "http://www.si.com/nfl/scoreboard?week=0%2C4"
picks           = r"C:\Users\slawler\Desktop\picks.txt"

#=======================PART 1: Get Upcoming Matchups========================#

teams = ('Eagles', 'Bengals', 'Packers', 'Patriots', 'Falcons', 'Vikings', 'Redskins',
         'Cowboys', 'Chargers', 'Panthers', 'Bills', 'Ravens', 'Buccaneers', 'Texans',
         'Rams', '49ers', 'Steelers', 'Lions','Raiders', 'Bears', 'Browns', 'Seahawks',
         'Jets', 'Dolphins', 'Cardinals', 'Titans', 'Giants', 'Colts', 'Jaguars',
         'Saints', 'Chiefs', 'Broncos')

r = requests.get(concluded_games)
data = r.text
soup = BeautifulSoup(data,'lxml')
tables = soup.find_all("a", class_="unskinned")
matchups = []
print('\nThis Weeks Match-Ups\n')

for table in tables:
    try:
        team = table.contents[1].decode_contents()
        if str(team) in teams:
            matchups.append(str(team))
        else:
            continue
    except:
        continue

for i, matchup in enumerate(matchups):
    if i == 2:
        game = i/2+1
        print game, matchups[i], matchups[i+1]
    elif i%2 == 0:
        game =i/2+1
        print game, matchups[i], matchups[i+1]

#===============PART 2: Concluded Games--Get This Weeks Results==============#

r = requests.get(concluded_games)
data = r.text
soup = BeautifulSoup(data,"lxml")

tables = soup.find_all('table')

print('\nGame Totals\n')
winners = []

def GetWinner(table):
    rows = table.find_all('td')
    j = 0
    for row in rows:
        if j == 0:
            try:
                if row.attrs['class'][0] == 'line-score-team-name':
                    data = row.contents
                    team1 = str(data[0])

                elif 'strong' in row.decode_contents():
                    data = row.findAll()[0].contents
                    score1 = int(data[0])
                    j+=1

            except:
                continue

        else:
            try:
                if row.attrs['class'][0] == 'line-score-team-name':
                    data = row.contents
                    team2 = str(data[0])

                elif 'strong' in row.decode_contents():
                    data = row.findAll()[0].contents
                    score2 = int(data[0])
            except:
                continue

    if score1 > score2:
        winner = team1
    elif score1< score2:
        winner = team2
    else:
        winner = 'TIE'

    print(team1.ljust(10), score1, team2.ljust(10), score2)
    return winner


for i, table in enumerate(tables):
    winner = GetWinner(table)
    print("\t\t\t\tGame {0} Winner:".format(str(i+1)), winner,'\n')
    winners.append(winner)

#===================PART 3: Check Individual Results & Tally Score===========#

df = pd.read_csv(picks, sep = '\t')

score_tally = {}

for picker in df:
    print(picker)
    score_tally[picker] = 0
    for pick in df[picker]:
        if pick in winners:
            score_tally[picker] +=1
   
for picker in sorted(score_tally, key=score_tally.get, reverse=True):
  print picker, score_tally[picker]