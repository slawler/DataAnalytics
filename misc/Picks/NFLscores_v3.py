# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Grab List of Winners for NFL Games of the Week

Input(s):  SI URL
Output(s): Winners List

slawler@dewberry.com
Created on Tue Aug 30 09:33:12 2016
"""
#------------Load Python Modules--------------------#

from bs4 import BeautifulSoup
import requests
#------------------------------BEGIN SCRIPT----------------------------------#

#url = "http://www.si.com/nfl/scoreboard?week=0%2C2"
url = "http://www.si.com/nfl/scoreboard?week=0%2C4"

r = requests.get(url)
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


