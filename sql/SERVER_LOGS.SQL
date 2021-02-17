DROP TABLE SERVER_LOGS;

CREATE TABLE SERVER_LOGS (
        ID int NOT NULL UNIQUE
        , SERVER_ID INT
        , LOG_TYPE VARCHAR(100)
        , LOG_TARGET VARCHAR(100)
        , PRIMARY KEY (ID)
        , CONSTRAINT FK_SERVER_ID FOREIGN KEY (SERVER_ID) REFERENCES SERVERS(SERVER_ID)
);

INSERT INTO SERVER_LOGS (ID, SERVER_ID, LOG_TYPE, LOG_TARGET) VALUES
        (1, 2, 'local', 'DizzyHoG/logs/The Realm of Aurii'),
        (2, 3, 'local', 'DizzyHoG/logs/Beacon Academy Northeastern Campus'),
        (3, 4, 'local', 'DizzyHoG/logs/ASPN')
;