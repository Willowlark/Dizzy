DROP TABLE DATA_8BALL;

CREATE TABLE DATA_8BALL (
        ID int NOT NULL AUTO_INCREMENT
        , REPLY VARCHAR(200) 
        , PRIMARY KEY (ID)
);

INSERT INTO DATA_8BALL (URL) VALUES
        ('It is certain.'),
        ('It is decidedly so.'),
        ('Without a doubt.'),
        ('Yes \u2013 definitely.'),
        ('You may rely on it.'),
        ('As I see it, yes.'),
        ('Most likely.'),
        ('Outlook good.'),
        ('Yes.'),
        ('Signs point to yes.'),
        ('Reply hazy, try again.'),
        ('Ask again later.'),
        ('Better not tell you now.'),
        ('Cannot predict now.'),
        ('Concentrate and ask again.'),
        ('Don\'t count on it.'),
        ('My reply is no.'),
        ('My sources say no.'),
        ('Outlook not so good.'),
        ('Very doubtful.')
;