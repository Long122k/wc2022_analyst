CREATE TABLE players (
    team VARCHAR(50),
    player_name VARCHAR(100),
    number INT,
    position VARCHAR(50),
    birth DATE,
    caps INT,
    goals INT,
    club VARCHAR(100),
    league VARCHAR(100),
    PRIMARY KEY (team, number)
);

CREATE TABLE match_event (
	id int auto_increment,
    match_id INT,
    team VARCHAR(50),
    time varchar(10),
    type_event VARCHAR(50),
    player varchar(100),
    detail_event VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE TABLE match_stat (
    match_id INT,
    team VARCHAR(50),
    possession INT,
    foul INT,
    throw_in INT,
    offside INT,
    long_pass INT,
    corner INT,
    yellow_card INT,
    red_card INT,
    second_yellow_card INT,
    shot_on_target INT,
    shot_off_target INT,
    blocked_shot INT,
    counter_attack INT,
    goalkeeper_save INT,
    goal_kick INT,
    medical_care INT,
    PRIMARY KEY (match_id, team)
);



CREATE TABLE match_line_up (
    match_id INT,
    team VARCHAR(50),
    line_up VARCHAR(50),
    player1 INT,
    player2 INT,
    player3 INT,
    player4 INT,
    player5 INT,
    player6 INT,
    player7 INT,
    player8 INT,
    player9 INT,
    player10 INT,
    player11 INT,
    PRIMARY KEY (match_id, team),
    FOREIGN KEY (team, player1) REFERENCES players(team, number),
    FOREIGN KEY (team, player2) REFERENCES players(team, number),
    FOREIGN KEY (team, player3) REFERENCES players(team, number),
    FOREIGN KEY (team, player4) REFERENCES players(team, number),
    FOREIGN KEY (team, player5) REFERENCES players(team, number),
    FOREIGN KEY (team, player6) REFERENCES players(team, number),
    FOREIGN KEY (team, player7) REFERENCES players(team, number),
    FOREIGN KEY (team, player8) REFERENCES players(team, number),
    FOREIGN KEY (team, player9) REFERENCES players(team, number),
    FOREIGN KEY (team, player10) REFERENCES players(team, number),
    FOREIGN KEY (team, player11) REFERENCES players(team, number)    
);

CREATE TABLE match_info (
    match_id INT PRIMARY KEY,
    home_team VARCHAR(50),
    away_team VARCHAR(50),
    home_score INT,
    away_score INT,
    hour INT,
    date VARCHAR(20),
    stadium VARCHAR(50),
    round VARCHAR(50),
    FOREIGN KEY (match_id, home_team) REFERENCES match_line_up(match_id, team),
    FOREIGN KEY (match_id, away_team) REFERENCES match_line_up(match_id, team),
    FOREIGN KEY (match_id, home_team) REFERENCES match_stat(match_id, team),
    FOREIGN KEY (match_id, away_team) REFERENCES match_stat(match_id, team)
);