import requests
from bs4 import BeautifulSoup
import csv
import json

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
    # stat architecture each match is different from others
    name_mapping = {
        "Kiểm soát bóng": "possession",
        "Phạm lỗi": "foul",
        "Ném biên": "throw_in",
        "Việt vị": "offside",
        "Chuyền dài": "long_pass",
        "Phạt góc": "corner",
        "Thẻ vàng": "yellow_card",
        "Thẻ đỏ": "red_card",
        "Thẻ vàng thứ 2": "second_yellow_card",
        "Sút trúng đích": "shot_on_target",
        "Sút không trúng đích": "shot_off_target",
        "Cú sút bị chặn": "blocked_shot",
        "Phản công": "counter_attack",
        "Thủ môn cản phá": "goalkeeper_save",
        "Phát bóng": "goal_kick",
        "Chăm sóc y tế": "medical_care",
    }   
    stat_label = ['match_id', 'team']
    get_label = soup.find_all('span', class_ = 'statistics_text')
    for label in get_label:
        stat_label.append(name_mapping[label.text])
    result = dict(zip(stat_label, stat))
    return result

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
        time = event.find('span').text
        type_event = event.find('img')['src'].split('/')[3].split('.')[0] #<img src="/images/icons/yellow_card.png"
        content = event.text.replace(time, '').split('(')
        
        if content[0] != '':
        #<li>Teun Koopmeiners (Thay: Marten De Roon)<span class="ic-the"><img src="/images/icons/substitution.png">46</span></li>
            player = content[0]
            if len(content) == 1:
                detail_event = ''
            else:
                detail_event = content[1][:-1]
        else:
        #<li>(Pen) Lionel Messi<span class="ic-the"><img src="/images/icons/goal.png">34</span></li>
            player = content[1].split(')')[1]
            detail_event = content[1].split(')')[0]

        all_events.append([matchId, teamName, time, type_event, player, detail_event])
    return all_events
        
def get_line_up(soup1, matchId, teamName, id):
    """
    id identify home team or away team, id = 0 is home, id = 1 is away
    """
    match_line_up = [matchId, teamName]
    #<p><strong>Ma rốc (4-3-3): </strong><span>Bono (1), Achraf Hakimi (2), Jawad El Yamiq (18), Romain Saiss (6), Yahia Attiyat Allah (25), Azzedine Ounahi (8), Sofyan Amrabat (4), Selim Amallah (15), Hakim Ziyech (7), Youssef En-Nesyri (19), Sofiane Boufal (17)</span></p>
    try:
        soup = soup1.find_all('div', class_= 'live-content')[-3]
        content = soup.find_all('p')[id].text.split(':')
        # print(soup)
        line_up = content[0].split('(')[1][:-1]
        match_line_up.append(line_up)
        players_start = content[1].split(',')
        for player in players_start:
            #get number of player at start line up
            number = player.split('(')[1][:-1]
            match_line_up.append(number)
        return match_line_up
    except:
        soup = soup1.find_all('div', class_= 'live-content')[-4]
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
    match_stats = {}
    match_events = []
    match_line_ups = []

    #get link of match in data file
    links = []
    with open("./data/links.txt", "r") as f:
        for line in f:
            link = line.strip()
            links.append(link)

    #get data of 64 matches
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
        match_stats[i] = (home_stat)
        match_stats[64+i] = (away_stat)
        match_line_ups.append(home_line_up)
        match_line_ups.append(away_line_up)
        for event in home_event:
            match_events.append(event)
        for event in away_event:
            match_events.append(event)
        print(matchId)

    #store data in csv file
    match_info_label = ['match_id', 'home_team', 'away_team', 'home_score', 'away_score', 'hour', 'date', 'stadium', 'round']
    match_stat_label = ['match_id', 'team', 'possession', 'foul', 'throw_in', 'offside', 'long_pass', 'corner', "yellow_card", "red_card", "second_yellow_card", "shot_on_target", "shot_off_target", "blocked_shot", "counter_attack", "goalkeeper_save", "goal_kick", "medical_care"]
    match_event_label = ['matchId', 'team', 'time', 'type_event', 'player', 'detail_event']
    match_line_up_label = ["match_id", "team", "line_up", "player1", "player2", "player3", "player4", "player5", "player6", "player7", "player8", "player9", "player10", "player11"]

    # write the data to a CSV file
    with open('./data/match_info.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(match_info_label)
        for match in match_infos:
            writer.writerow(match)
    
    # with open('./data/match_stat.csv', 'w', newline='') as csvfile2:
    #     writer = csv.writer(csvfile2)
    #     writer.writerow(match_stat_label)
    #     for match in match_stats:
    #         writer.writerow(match)
    with open('./data/match_stat.json', 'w') as f:
        json.dump(match_stats, f)
    
    with open('./data/match_event.csv', 'w', newline='') as csvfile3:
        writer = csv.writer(csvfile3)
        writer.writerow(match_event_label)
        for match in match_events:
            writer.writerow(match)

    with open('./data/match_line_up.csv', 'w', newline='') as csvfile4:
        writer = csv.writer(csvfile4)
        writer.writerow(match_line_up_label)
        for match in match_line_ups:
            writer.writerow(match)
crawl()


# [Kiểm soát bóng, Phạm lỗi, Ném biên, Việt vị, Chuyền dài, Phạt góc, Thẻ vàng, Thẻ đỏ, Thẻ vàng thứ 2, Sút trúng đích, Sút không trúng đích, Cú sút bị chặn, Phản công, Thủ môn cản phá, Phát bóng, Chăm sóc y tế]