import requests
from bs4 import BeautifulSoup
import csv

url = "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
soup = soup.find("div", class_="mw-parser-output")

player_list = []

teams = soup.find_all('h3')
tables = soup.find_all('table')

for i in range(32):
    players = tables[i].find_all("tr", class_= 'nat-fs-player')  
    for player in players:
        info = player.find_all('td')
        number = info[0].text[:-1] #remove character not used
        position = info[1].find('a').text
        birth = info[2].find('span').text[2:-1] #remove character not used
        caps = info[3].text[:-1] #remove character not used
        goals = info[4].text[:-1] #remove character not used
        club = info[5].text[1:-1] #remove character not used
        league = info[5].find('a')['title']
        player_name = player.find('th').text[:-1]
        team = teams[i].find('span', class_= 'mw-headline').text
        # if i <
        # team = teams
        # print(player_name)
        player_list.append([team, player_name, number, position, birth, caps, goals, club, league])
# print((teams[0]))
# print(len(player_list))
# write to csv file
label = ['team', 'player_name', 'number', 'position', 'birth', 'caps', 'goals', 'club', 'league']
with open('./data/players_info.csv', 'w', newline='') as csvfile4:
    writer = csv.writer(csvfile4)
    writer.writerow(label)
    for player in player_list:
        writer.writerow(player)