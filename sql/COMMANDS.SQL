DROP TABLE COMMANDS;

CREATE TABLE COMMANDS (
        COMMAND_ID int NOT NULL UNIQUE
        , COMMAND_NAME VARCHAR(100)
        , PYTHON_CLASS VARCHAR(100)
        , CMD_TRIGGER VARCHAR(100)
        , OPTIONS VARCHAR(2000)
        , OPTIONS_FROM_DB BOOLEAN
        , UPDATE_ON_CALL BOOLEAN
        , PATTERN VARCHAR(100)
        , AUTHOR_WHITELIST INT
        , HELP VARCHAR(2000)
        , PRIMARY KEY (COMMAND_ID)
);



INSERT INTO COMMANDS (COMMAND_ID, PYTHON_CLASS, CMD_TRIGGER, OPTIONS, OPTIONS_FROM_DB, UPDATE_ON_CALL, PATTERN, AUTHOR_WHITELIST, HELP) VALUES
          (1, 'Reply', '\\U0001F51E', 'https://i.imgur.com/JbVqZOn.jpg', False, False, '(lewd)', NULL,
          '')
        , (2, 'RandomReply', NULL, 'DATA_LEWD', True, False, '(lewd)', NULL,
        '!lewd : Send a random "that''s lewd" reaction image')
        , (3, 'RandomReply', NULL, 'DATA_DABS', True, False, '(dab)', NULL,
        '!dab : Send a random dab reaction image')
        , (4, 'RandomReply', NULL, 'DATA_FORTUNES', True, False, '(fortune)', NULL,
        '!fortune : Send a random fortune cookie message')
        , (5, 'RandomReply', NULL, 'DATA_8BALL', True, False, '(8ball)(?:$| )', NULL,
        '!8ball : Shake the magic 8 Ball and see what it says. You can ask the question after the command if you want.')
        , (6, 'Timecheck', NULL, NULL, False, False, '(timecheck)', NULL,
        '!timecheck : Prints Time and Date in EST and JST')
        , (7, 'Choose', NULL, NULL, False, False, '(choose) (.*)', NULL,
        '!choose <options> : Choose one of a list of options separated by commas for you.')
        , (8, 'Stab', NULL, NULL, False, False, '(stab)', NULL,
        '!stab : Stabs someone at random >:D')
        , (9, 'Command', NULL, NULL, False, True, '(refresh)', 1,
        '!refresh : Reloads data fromt the DB. Just for the Admin!')
        , (10, 'Log', NULL, NULL, False, False, '(log) ([^ ]*)', 1,
        '!log : Outdated, logs an entire channel''s history. for backup purposes.')
        , (11, 'Reply', NULL, 'Nice!', False, False, '[Nn]ice\.? *$', NULL,
        '!nice : Dizzy says Nice!')
        , (12, 'Reply', NULL, 'https://i.imgur.com/55sx3FG.png', False, False, '(tsun)', NULL,
        '!tsun : It''s not like I want you to react with this, baka!')
        , (13, 'Reply', NULL, 'https://i.imgur.com/hXuK1cP.png', False, False, '(hush)', NULL,
        '!hush : *muffled noises*')
        , (14, 'Reply', NULL, 'https://i.imgur.com/gilOf0I.gif', False, False, '(teamwork)', NULL,
        '!teamwork : high fives all around')
        , (15, 'Reply', NULL, 'https://i.imgur.com/no93Chq.png', False, False, '(prick)', NULL,
        '!prick : Only a cactus would use this.')
        , (16, 'Reply', NULL, 'https://i.imgur.com/JxOe5TA.jpg', False, False, '(angryjess)', NULL,
        '!angryjess : Do not anger!')
        , (17, 'Ghost', NULL, NULL, False, False, '(ghost) (.*)', 1,
        '')
        , (18, 'Fudge', NULL, NULL, False, False, '(fudge) ([+-]?[0-9]+)', NULL,
        '!fudge [positive/negative number] : Roll four Fudge dice, adding a number if you give one.')
        , (19, 'Fudge', NULL, NULL, False, False, '(fudge)', NULL, '')
        , (20, 'Roll', NULL, NULL, False, False, '(roll|r) (.*)', NULL,
        '!roll <die code> : Rolls dice you specify. Does advantage/disadvantage (1d20a, 1d20d), top X (4d6^3), fudge (1dF) as special options!')
        , (21, 'Headpat', NULL, 'DATA_HEADPATS', True, True, '(headpat)(.*)', NULL,
        '!headpat <@mention>: Headpat @somebody!')
        , (22, 'IrlRuby', NULL, NULL, False, False, '(irlRuby)(.*)', NULL,
        '')
        , (23, 'QuestionPlease', NULL, 'DATA_WII_QUESTIONS', True, True, '(questionplz)', NULL,
        '!questionplz : Get a question from Wii''s Everybody Votes Channel!')
        , (24, 'CounterIncrement', NULL, 'DATA_COUNTERS', True, True, '(mycounter|globalcounter|counter) (add|sub) ([^ ]+) ([0-9]+)', NULL,
        '!mycounter <add or sub> <name of counter> <amount> : Add or subtract the amount from the named personal counter.\n!counter <add or sub> <name of counter> <amount> : Add or subtract the amount from the named server counter.\n!globalcounter <add or sub> <name of counter> <amount> : Add or subtract the amount from the named global counter.')
        , (25, 'CounterCheck', NULL, 'DATA_COUNTERS', True, False, '(mycounter|globalcounter|counter) (check) ([^ ]+)', NULL,
        '!mycounter check <name of counter> :Show the Value in the named personal counter.\n!counter check <name of counter> :Show the Value in the named server counter.\n!globalcounter check <name of counter> :Show the Value in the named global counter.')
        , (26, 'CounterRemove', NULL, 'DATA_COUNTERS', True, True, '(mycounter|globalcounter|counter) (remove) ([^ ]+)', NULL,
        '!mycounter remove <name of counter> :Remove the named personal counter.\n!counter remove <name of counter> :Remove the named server counter.\n!globalcounter remove <name of counter> :Remove the named global counter.')
        , (27, 'CounterList', NULL, 'DATA_COUNTERS', True, True, '(mycounter|globalcounter|counter) (list) ?(all)?', NULL,
        '!mycounter list : Shows all personal counters you have.\n!counter list : Shows all counters on this server\n!globalcounter list : Shows all global counters.')
        , (28, 'CounterSet', NULL, 'DATA_COUNTERS', True, True, '(mycounter|globalcounter|counter) (set) ([^ ]+) ([0-9]+)', NULL,
        '!mycounter set <name of counter> <amount> : Sets the value of the named personal counter to the amount given.\n!counter set <name of counter> <amount> : Sets the value of the named server counter to the amount given.\n!globalcounter set <name of counter> <amount> : Sets the value of the named global counter to the amount given.')
        , (30, 'FateAccelLoad', NULL, 'DATA_FATE_ACCEL_CHARS', True, True, '(chload) ([^ ]*) (.*)', NULL,
        '!chload <nickname> <character sheet> : Loads a formatted Fate Accelerated Character.')
        , (31, 'FateAccelCheck', NULL, 'DATA_FATE_ACCEL_CHARS', True, False, '(chcheck) ([^ ]*)( raw)?', NULL,
        '!chcheck <nickname> [raw] : Prints the character sheet with the given nickname. If raw added after the name, prints without formatting.')
        , (32, 'CharacterList', NULL, 'DATA_FATE_ACCEL_CHARS', True, False, '(chlist)', NULL,
        '!chlist : Lists all characters on this server.')
        , (33, 'CharacterRoll', NULL, 'DATA_FATE_ACCEL_CHARS', True, False, '(chroll) ([^ ]*) ([^ ]*)', NULL,
        '!chroll <nickname> <stat name> : Rolls the Dice for a given state with a given character''s bonus.')
        , (34, 'CharacterMod', NULL, 'DATA_FATE_ACCEL_CHARS', True, True, '(chmod) ([^ ]*) (?:"(.*)"|([^ ]*)) (.*)', NULL,
        '!chmod <nickname> <stat name> <new value> : Changes the value for nickname character''s stat to new value')
        -- 35 is a separate insert
        , (36, 'RandomReply', NULL, 'DATA_FOOD_PORN', True, False, '(porn)', NULL,
        '!porn : Sends some ~~Food~~ Porn.')
;

INSERT INTO COMMANDS 
    (COMMAND_ID, PYTHON_CLASS, CMD_TRIGGER, OPTIONS, OPTIONS_FROM_DB, UPDATE_ON_CALL, PATTERN, AUTHOR_WHITELIST, HELP) 
VALUES 
    (35, 'Reply', NULL, 'How is everyone today? How are you feeling? \n:heartpulse:: I''m Amazing!\n:heart:: Pretty good.\n:orange_heart:: Good!\n:yellow_heart:: I''m Okay\n:green_heart:: I''m coming back\n:purple_heart:: It''s tough\n:blue_heart:: It''s Awful\n:broken_heart:: I''m completely lost and broken inside\n:black_heart:: I''m having suicidal thoughts', False, False, '(checkin)', NULL, '!checkin : Posts the mental health checkin prompt.');

INSERT INTO COMMANDS 
    (COMMAND_ID, PYTHON_CLASS, CMD_TRIGGER, OPTIONS, OPTIONS_FROM_DB, UPDATE_ON_CALL, PATTERN, AUTHOR_WHITELIST, HELP) 
VALUES 
    (37, 'Reply', NULL, 'https://i.imgur.com/qp1cf60.mp4', False, False, '(surething)', NULL, '!surething : Ironwood says Sure Thing.');

INSERT INTO COMMANDS 
    (COMMAND_ID, PYTHON_CLASS, CMD_TRIGGER, OPTIONS, OPTIONS_FROM_DB, UPDATE_ON_CALL, PATTERN, AUTHOR_WHITELIST, HELP) 
VALUES 
    (38, 'Reply', NULL, 'https://i.imgur.com/V6QA3Nz.gif', False, False, '(clusterfuck)', NULL, '!clusterfuck : Welcome back to tonight''s clusterfuck');

INSERT INTO COMMANDS 
    (COMMAND_ID, PYTHON_CLASS, CMD_TRIGGER, OPTIONS, OPTIONS_FROM_DB, UPDATE_ON_CALL, PATTERN, AUTHOR_WHITELIST, HELP) 
VALUES 
    (39, 'Help', NULL, 'V_COMMAND_HELP', True, False, '(help)', NULL, '!help : You know what this does, don''t you?');

INSERT INTO COMMANDS 
    (COMMAND_ID, PYTHON_CLASS, CMD_TRIGGER, OPTIONS, OPTIONS_FROM_DB, UPDATE_ON_CALL, PATTERN, AUTHOR_WHITELIST, HELP) 
VALUES 
    (40, 'TarotDraw', NULL, 'DATA_TAROT', True, True, '(tarot)( \\d+)?( (?:[M|m]ajor|[M|m]inor))?', NULL, '!tarot : Draw X Tarot cards')
    
INSERT INTO COMMANDS 
    (COMMAND_ID, PYTHON_CLASS, CMD_TRIGGER, OPTIONS, OPTIONS_FROM_DB, UPDATE_ON_CALL, PATTERN, AUTHOR_WHITELIST, HELP) 
VALUES 
    (41, 'RandomReply', NULL, 'DATA_AU_LIST', True, False, '(auidea)', NULL,
        '!porn : Alternate Universe prompt!')