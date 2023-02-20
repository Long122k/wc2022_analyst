import requests
from bs4 import BeautifulSoup


def get_match_info(soup, matchId):
    soup = soup.find('div', id='pn-neo')
    #get team name
    teams = soup.find_all("h3", class_="name-tie")
    home_team = teams[0].find('a').text
    away_team = teams[1].find('a').text
    #get score of the match
    score = soup.find('div', class_ = 'c2-result').text
    home_score = score[0]
    away_score = score[-1]
    #get other match info
    info = soup.find_all('div', class_ = 'div-row r1')
    date_time = info[0].text.split(',')[1].split(' ')
    hour = date_time[1]
    date = date_time[2]
    stadium = info[1].text
    round = soup.find('div', class_ = 'div-row l1').text.split('-')[0][:-1]
    return [matchId, home_team, away_team, home_score, away_score, hour, date, stadium, round]

def get_match_stat(soup, matchId, teamName, id):
    """
    id identify home team or away team, id = 1 is home, id = 2 is away
    """
    soup = soup.find('div', class_= 'box-statistics')
    stat = [ matchId, teamName]
    analyst = soup.find_all('span', class_ = 'statistics_number'+ str(id))
    for item in analyst:
        stat.append(item.text)
    return stat

# ["yellow_card", "red_card", "second_yellow_card", "shot_on_target", "shot_off_target", "blocked_shot", "counter_attack", "goalkeeper_save", "goal_kick", "medical_care"]

def get_match_event(soup, matchId, teamName, id):
    """
    id identify home team or away team, id = 0 is home, id = 1 is away
    """
    all_events = []
    soup = soup.find('div', class_= 'live-dien-bien')
    team_events = soup.find_all('ul', class_ = 'ul-live')
    events = team_events[id].find_all('li')
    for event in events:
        #<li>Teun Koopmeiners (Thay: Marten De Roon)<span class="ic-the"><img src="/images/icons/substitution.png">46</span></li>
        time = event.find('span').text
        type_event = event.find('img')['src'].split('/')[3].split('.')[0] #<img src="/images/icons/yellow_card.png"
        content = event.text.replace(time, '').split('(')
        
        if content[0] != '':
            player = content[0]
            if len(content) == 1:
                detail_event = ''
            else:
                detail_event = content[1][:-1]
        else:
            player = content[1].split(')')[1]
            detail_event = content[1].split(')')[0]

        all_events.append([matchId, teamName, time, type_event, player, detail_event])
    return all_events
        
# print(get_match_event(soup, 1, 'hi', 1))
def get_line_up(soup, matchId, teamName, id):
    """
    id identify home team or away team, id = 0 is home, id = 1 is away
    """
    match_line_up = [matchId, teamName]
    #<p><strong>Ma rốc (4-3-3): </strong><span>Bono (1), Achraf Hakimi (2), Jawad El Yamiq (18), Romain Saiss (6), Yahia Attiyat Allah (25), Azzedine Ounahi (8), Sofyan Amrabat (4), Selim Amallah (15), Hakim Ziyech (7), Youssef En-Nesyri (19), Sofiane Boufal (17)</span></p>
    try:
        soup = soup.find_all('div', class_= 'live-content')[-3]
        content = soup.find_all('p')[id].text.split(':')
        line_up = content[0].split('(')[1][:-1]
        match_line_up.append(line_up)
        players_start = content[1].split(',')
        for player in players_start:
            #get number of player at start line up
            number = player.split('(')[1][:-1]
            match_line_up.append(number)
        return match_line_up
    except:
        soup = soup.find_all('div', class_= 'live-content')[-2]
        content = soup.find_all('p')[id].text.split(':')
        line_up = content[0].split('(')[1][:-1]
        match_line_up.append(line_up)
        players_start = content[1].split(',')
        for player in players_start:
            #get number of player at start line up
            number = player.split('(')[1][:-1]
            match_line_up.append(number)
        return match_line_up

def crawl():
    match_infos = []
    match_stats = []
    match_events = []
    match_line_ups = []

    #get link of match in data file
    links = []
    with open("./data/links.txt", "r") as f:
        for line in f:
            link = line.strip()
            links.append(link)
    for i in range(64):
        response = requests.get(links[i])
        soup = BeautifulSoup(response.content, "html.parser")
        matchId = i+1
        match_info = get_match_info(soup, matchId)
        home_stat = get_match_stat(soup, matchId, match_info[1], 1)
        away_stat = get_match_stat(soup, matchId, match_info[2], 2)
        home_event = get_match_event(soup, matchId, match_info[1], 0)
        away_event = get_match_event(soup, matchId, match_info[2], 1)
        home_line_up = get_line_up(soup, matchId, match_info[1], 0)
        away_line_up = get_line_up(soup, matchId, match_info[2], 1)
        match_infos.append(match_info)
        match_stats.append(home_stat)
        match_stats.append(away_stat)
        match_line_ups.append(home_line_up)
        match_line_ups.append(away_line_up)
        # print(match_info)
        # print(home_stat)
        # print(away_stat)
        # print(home_event)
        # print(away_event)
        # print(home_line_up)
        # print(away_line_up)
        for event in home_event:
            match_events.append(event)
        for event in away_event:
            match_events.append(event)
        print(match_events)
        break




crawl()



