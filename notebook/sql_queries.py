###################### DROP TABLES ###################################

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop     = "DROP TABLE IF EXISTS users;"
time_table_drop     = "DROP TABLE IF EXISTS time;"
song_table_drop     = "DROP TABLE IF EXISTS songs;"
artist_table_drop   = "DROP TABLE IF EXISTS artists;"

##################### CREATE TABLES ###################################

artist_table_create = """
    CREATE TABLE IF NOT EXISTS artists (
        artist_id          VARCHAR PRIMARY KEY, 
        artist_name        VARCHAR NOT NULL, 
        artist_location    VARCHAR, 
        latitude           NUMERIC, 
        longitude          NUMERIC
    );
"""

song_table_create = """
    CREATE TABLE IF NOT EXISTS songs (
        song_id            VARCHAR PRIMARY KEY,
        artist_id          VARCHAR,
        title              VARCHAR NOT NULL,  
        duration           NUMERIC,
        year               INT
    );
"""

time_table_create = """
    CREATE TABLE IF NOT EXISTS time (
        -- Primary key is always unique and not null
        -- if start_time is not null so are hour,day,week,month,year,weekday
        -- because they derive directly from start_time
        start_time  TIMESTAMP PRIMARY KEY, 
        hour        INT NOT NULL, 
        day         INT NOT NULL, 
        week        INT NOT NULL, 
        month       INT NOT NULL, 
        year        INT NOT NULL, 
        weekday     INT NOT NULL
    );
"""

user_table_create = """
    CREATE TABLE IF NOT EXISTS users (
        -- I could have converted user_id into integer
        -- but I kept the original data type 
        user_id           VARCHAR PRIMARY KEY, 
        first_name        VARCHAR, 
        last_name         VARCHAR, 
        gender            VARCHAR, 
        level             VARCHAR
    );
"""

songplay_table_create = """
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id       SERIAL PRIMARY KEY,  
        user_id           VARCHAR NOT NULL REFERENCES users,  
        song_id           VARCHAR REFERENCES songs, 
        artist_id         VARCHAR REFERENCES artists, 
        start_time        TIMESTAMP REFERENCES time,
        session_id        INT,
        user_location     VARCHAR,
        song              VARCHAR NOT NULL -- the song's title is important
);
"""

############################# INSERT RECORDS ###################################

songplay_table_insert = """
    INSERT INTO songplays 
    (user_id, song_id, artist_id, start_time, session_id, user_location, song)
    VALUES (%s,%s,%s,%s,%s,%s,%s);
"""

user_table_insert = """
    INSERT INTO users 
    (user_id, first_name, last_name, gender, level) VALUES (%s,%s,%s,%s,%s)
    ON CONFLICT (user_id) DO NOTHING;
"""

song_table_insert = """
    INSERT INTO 
    songs (song_id, artist_id, title, duration, year) VALUES (%s,%s,%s,%s,%s)
"""

artist_table_insert = """
    INSERT INTO 
    artists (artist_id, artist_name, artist_location, latitude, longitude) 
    VALUES (%s,%s,%s,%s,%s)
    ON CONFLICT (artist_id) DO NOTHING;
"""


time_table_insert = """
    INSERT INTO 
    time (start_time, hour, day, week, month, year, weekday) 
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (start_time) DO NOTHING;
"""

#-------------------------------------------FIND SONGS--------------------------

# Finding the song ID and artist ID based on the title, artist name, 
# and duration of a song
song_select = """
    SELECT song_id, a.artist_id
    FROM songs AS s
    JOIN artists AS a
    ON s.artist_id = a.artist_id
    WHERE s.title = %s
    AND a.artist_name = %s
    AND s.duration = %s;
"""

#----------------------------------------- QUERY LISTS -------------------------

create_table_queries = [
    artist_table_create,
    song_table_create,
    time_table_create,
    user_table_create,
    songplay_table_create
]
drop_table_queries = [
    songplay_table_drop,
    user_table_drop,
    time_table_drop,
    song_table_drop,
    artist_table_drop
]