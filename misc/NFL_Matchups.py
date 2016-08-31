# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Grab List of Winners for NFL Games of the Week

Input(s): Sports Illustrated URL
Output(s): Winners List

slawler@dewberry.com
Created on Tue Aug 30 09:33:12 2016
"""
#------------Load Python Modules--------------------#

from bs4 import BeautifulSoup
import requests
#------------------------------BEGIN SCRIPT----------------------------------#

url = "http://www.si.com/nfl/scoreboard?week=1%2C2"

teams = ('Eagles', 'Bengals', 'Packers', 'Patriots', 'Falcons', 'Vikings', 'Redskins',
         'Cowboys', 'Chargers', 'Panthers', 'Bills', 'Ravens', 'Buccaneers', 'Texans',
         'Rams', '49ers', 'Steelers', 'Lions','Raiders', 'Bears', 'Browns', 'Seahawks',
         'Jets', 'Dolphins', 'Cardinals', 'Titans', 'Giants', 'Colts', 'Jaguars',
         'Saints', 'Chiefs', 'Broncos')

r = requests.get(url)
data = r.text
soup = BeautifulSoup(data,'lxml')

tables = soup.find_all("a", class_="unskinned")

print('\nThis Weeks Match-Ups\n')

matchups = []
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
