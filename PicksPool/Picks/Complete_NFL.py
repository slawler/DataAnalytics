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
import fileinput
import operator
import os
import re
#------------------------------BEGIN SCRIPT----------------------------------#
lastweek = str(12)
nextweek = str(13)
upcoming_games  = "http://www.si.com/nfl/scoreboard?week=1%2C{}".format(nextweek)
concluded_games = "http://www.si.com/nfl/scoreboard?week=1%2C{}".format(lastweek)
#picks           = r"C:\Users\slawler\Desktop\picks.txt"

os.chdir(r'C:\Users\sml\Desktop\NFLPICKS')
#---Format tables
wk =lastweek
df = pd.read_csv(r"Week_{}.csv".format(wk))
df.head()
emails = df['E-mail:']
email_list = []

for e in emails:
    if ".com" in e:
        email_list.append(e)

for col in df: 
    if "Game" in col:
        print(df[col]) 
        #df[col] = df[col].map(lambda x: str(x)[:-8])
        df[col] = df[col].map(lambda x: x.split('(')[0].replace(' ',''))

df.to_csv("Week{}_EmailTable.csv".format(wk))

print(email_list)


#=======================PART 1: Get Upcoming Matchups========================#

teams = ('Eagles', 'Bengals', 'Packers', 'Patriots', 'Falcons', 'Vikings', 'Redskins',
         'Cowboys', 'Chargers', 'Panthers', 'Bills', 'Ravens', 'Buccaneers', 'Texans',
         'Rams', '49ers', 'Steelers', 'Lions','Raiders', 'Bears', 'Browns', 'Seahawks',
         'Jets', 'Dolphins', 'Cardinals', 'Titans', 'Giants', 'Colts', 'Jaguars',
         'Saints', 'Chiefs', 'Broncos')

r = requests.get(upcoming_games)
data = r.text
soup = BeautifulSoup(data,'lxml')
tables = soup.find_all("a", class_="unskinned")
matchups = []
records = []
print('\nThis Weeks Match-Ups\n')

# Scrape SI html for Upcoming Match data
for table in tables:
    try:
        team = table.contents[1].decode_contents()
        record = table.contents[3].decode_contents()
        if str(team) in teams:
            matchups.append(str(team))
            records.append(str(record))
            #print team, record
            
        else:
            continue
    except:
        continue

#----With no ties
'''    
for i, matchup in enumerate(matchups):
    if i == 2:
        game = i/2+1
        print(game)
        print(matchups[i], records[i])
        print(matchups[i+1], records[i+1])
        print('\n')
        
    elif i%2 == 0:
        game =i/2+1
        print(game)
        print(matchups[i], records[i])
        print(matchups[i+1], records[i+1])
        print('\n')

'''
#----With ties
regex = '<!--\n-->'  
  
for i, matchup in enumerate(matchups):
    if i == 2:
        game = i/2+1
        print(game)
        rec1,rec2 = records[i],records[i+1]
        print(matchups[i], re.sub(regex,'-',rec1))
        print(matchups[i+1], re.sub(regex,'-',rec2))
        print('\n')
        
    elif i%2 == 0:
        game =i/2+1
        print(game)
        rec1,rec2 = records[i],records[i+1]
        print(matchups[i], re.sub(regex,'-',rec1))
        print(matchups[i+1], re.sub(regex,'-',rec2))
        print('\n')


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

    print(team1.ljust(10), str(score1) + '\t', team2.ljust(10), str(score2), "\tGame {0} Winner:".format(str(i+1)), winner)
    return winner


for i, table in enumerate(tables):
    winner = GetWinner(table)
    winners.append(winner)



#===================PART 3: Check Individual Results & Tally Score===========#

df = pd.read_csv("Week{}_EmailTable.csv".format(wk), sep = ',')
df = df.drop_duplicates(subset = 'Name:')


df_player = df.set_index('Name:').T

df_results = df_player.isin(winners).astype(int)

weekly_totals = {}

for col in df_results:
    weekly_totals[col]= df_results[col].sum()


final = sorted(weekly_totals.items(), key=operator.itemgetter(1),reverse=True)    


for f in final: print(f)
    
