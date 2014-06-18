#!/usr/bin/python

import json
import urllib2
import pytz
from prettytable import PrettyTable
from dateutil import parser
from datetime import datetime


########### CONFIG ###########
my_timezone = "US/Pacific"
##############################

def fetch_data():
    url = 'http://worldcup.sfg.io/matches/today/'

    try:
        response = urllib2.urlopen(url).read()
    except urllib2.URLError:
        sys.exit()

    return response

def parse(json_data):
    ## JSON -> Dictionary
    matches = json.loads(json_data)

    ## PrettyTable for a nice printing layout
    table = PrettyTable(["Home", "Away", "Score", "Status"])
    table.align["Home"] = "l"
    table.align["Away"] = "l"

    for i in xrange(len(matches)-1, -1, -1): ## Dirty way of arranging games...
        ## Get game information
        homeTeam = matches[i]['home_team']['country']
        awayTeam = matches[i]['away_team']['country']

        homeGoals = matches[i]['home_team']['goals']
        awayGoals = matches[i]['away_team']['goals']
        combinedScore = str(homeGoals) + "-" + str(awayGoals)

        status = matches[i]['status']
        game_time = parser.parse(matches[i]['datetime'])

        if matches[i]['location'] == "Maracan\u00e3 - Est\u00e1dio Jornalista M\u00e1rio Filho":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Sao_Paulo'))
        elif matches[i]['location'] == "Arena Amazonia":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Manaus'))
        elif matches[i]['location'] == "Estadio Mineirao":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Sao_Paulo'))
        elif matches[i]['location'] == "Estadio Nacional":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Sao_Paulo'))
        elif matches[i]['location'] == "Arena Pantanal":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Cuiaba'))
        elif matches[i]['location'] == "Arena da Baixada":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Sao_Paulo'))
        elif matches[i]['location'] == "Estadio Castelao":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Fortaleza'))
        elif matches[i]['location'] == "Estadio das Dunas":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Fortaleza'))
        elif matches[i]['location'] == "Estadio Beira-Rio":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Sao_Paulo'))
        elif matches[i]['location'] == "Arena Pernambuco":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Recife'))
        elif matches[i]['location'] == "Arena Fonte Nova":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Bahia'))
        elif matches[i]['location'] == "Arena Corinthians":
            game_time = game_time.replace(tzinfo = pytz.timezone('America/Sao_Paulo'))

        if status == "completed":
            status = "DONE"
        elif status == "future":
            status = game_time.astimezone(pytz.timezone(my_timezone)).strftime("%I:%M %p")

        if matches[i]['status'] != "future":
            if homeGoals > awayGoals:
                homeTeam = '\033[92m' + homeTeam + '\033[0m'
                awayTeam = '\033[91m' + awayTeam + '\033[0m'
            elif homeGoals < awayGoals:
                homeTeam = '\033[91m' + homeTeam + '\033[0m'
                awayTeam = '\033[92m' + awayTeam + '\033[0m'
            else:
                homeTeam = '\033[93m' + homeTeam + '\033[0m'
                awayTeam = '\033[93m' + awayTeam + '\033[0m'

        table.add_row([homeTeam, awayTeam, combinedScore, status])

    return table


if __name__ == '__main__':
    response = fetch_data()
    print parse(response)