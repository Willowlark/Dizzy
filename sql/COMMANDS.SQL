DROP TABLE COMMANDS;

CREATE TABLE COMMANDS (
        COMMAND_ID int NOT NULL UNIQUE
        , COMMAND_NAME VARCHAR(100)
        , PYTHON_CLASS VARCHAR(100)
        , CMD_TRIGGER VARCHAR(100)
        , OPTIONS VARCHAR(100)
        , OPTIONS_FROM_DB BOOLEAN
        , PATTERN VARCHAR(100)
        , AUTHOR_WHITELIST INT
        , HELP VARCHAR(240)
        , PRIMARY KEY (COMMAND_ID)
);

INSERT INTO COMMANDS (COMMAND_ID, PYTHON_CLASS, CMD_TRIGGER, OPTIONS, OPTIONS_FROM_DB, PATTERN, AUTHOR_WHITELIST) VALUES
          (1, 'Reply', '\\U0001F51E', 'https://i.imgur.com/JbVqZOn.jpg', False, '(lewd)', NULL)
        , (2, 'RandomReply', NULL, 'DATA_LEWD', True, '(lewd)', NULL)
        , (3, 'RandomReply', NULL, 'DATA_DABS', True, '(dab)', NULL)
        , (4, 'RandomReply', NULL, 'DATA_FORTUNES', True, '(fortune)', NULL)
        , (5, 'RandomReply', NULL, 'DATA_8BALL', True, '(8ball)(?:$| )', NULL)
        , (6, 'Timecheck', NULL, NULL, False, '(timecheck)', NULL)
        , (7, 'Choose', NULL, NULL, False, '(choose) (.*)', NULL)
        , (8, 'Stab', NULL, NULL, False, '(stab)', NULL)
        , (9, 'Refresh', NULL, NULL, False, '(refresh)', 1)
        , (10, 'Log', NULL, NULL, False, '(log) ([^ ]*)', 1)
        , (11, 'Reply', NULL, 'Nice!', False, '[Nn]ice\.? *$', NULL)
        , (12, 'Reply', NULL, 'https://i.imgur.com/55sx3FG.png', False, '(tsun)', NULL)
        , (13, 'Reply', NULL, 'https://i.imgur.com/hXuK1cP.png', False, '(hush)', NULL)
        , (14, 'Reply', NULL, 'https://i.imgur.com/gilOf0I.gif', False, '(teamwork)', NULL)
        , (15, 'Reply', NULL, 'https://i.imgur.com/no93Chq.png', False, '(prick)', NULL)
        , (16, 'Reply', NULL, 'https://i.imgur.com/JxOe5TA.jpg', False, '(angryjess)', NULL)
        , (17, 'Ghost', NULL, NULL, False, '(ghost) (.*)', 1)
        , (18, 'Fudge', NULL, NULL, False, '(fudge) ([+-]?[0-9]+)', NULL)
        , (19, 'Fudge', NULL, NULL, False, '(fudge)', NULL)
        , (20, 'Roll', NULL, NULL, False, '(roll|r) (.*)', NULL)
        , (21, 'Headpat', NULL, 'DATA_DIZZY_HEADPATS', True, '(headpat)(.*)', NULL)
        , (22, 'IrlRuby', NULL, NULL, False, '(irlRuby)(.*)', NULL)
        , (23, 'QuestionPlease', NULL, 'DATA_QUESTIONS', True, '(questionplz)', NULL)
        , (24, 'CounterIncrement', NULL, 'DATA_COUNTERS', True, '(counter) (add|sub) ([^ ]+) ([0-9]+)', NULL)
        , (25, 'CounterCheck', NULL, 'DATA_COUNTERS', True, '(counter) (check) ([^ ]+)', NULL)
        , (26, 'CounterRemove', NULL, 'DATA_COUNTERS', True, '(counter) (remove) ([^ ]+)', NULL)
        , (27, 'CounterList', NULL, 'DATA_COUNTERS', True, '(counter) (list)', NULL)
        , (28, 'CounterSet', NULL, 'DATA_COUNTERS', True, '(counter) (set) ([^ ]+) ([0-9]+)', NULL)
        , (30, 'CharacterLoad', NULL, 'DATA_FATE_ACCEL_CHARS', True, '(chload) ([^ ]*) (.*)', NULL)
        , (31, 'CharacterCheck', NULL, 'DATA_FATE_ACCEL_CHARS', True, '(chcheck) ([^ ]*) (.*)', NULL)
        , (32, 'CharacterList', NULL, 'DATA_FATE_ACCEL_CHARS', True, '(chlist)', NULL)
        , (33, 'CharacterRoll', NULL, 'DATA_FATE_ACCEL_CHARS', True, '(chroll) ([^ ]*) ([^ ]*)', NULL)
        , (34, 'CharacterMod', NULL, 'DATA_FATE_ACCEL_CHARS', True, '(chmod) ([^ ]*) ([^ ]*|Fate Points) ([0-9])', NULL)
        -- , (35, 'Reply', NULL, 'How is @everyone today? How are you feeling? \n💛: I''m Amazing!\n:heart:: Pretty good.\n💗: Good!\n💜: I''m Okay\n:orange_heart:: I''m coming back\n💚: It''s tough\n💙: It''s Awful\n💔: I''m completely lost and broken inside\n🖤: I''m having suicidal thoughts', False, '(checkin)', NULL)
;
