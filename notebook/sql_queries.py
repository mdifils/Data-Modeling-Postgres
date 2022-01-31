###################### DROP TABLES ###################################

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop     = "DROP TABLE IF EXISTS users;"
time_table_drop     = "DROP TABLE IF EXISTS time;"
song_table_drop     = "DROP TABLE IF EXISTS songs;"
artist_table_drop   = "DROP TABLE IF EXISTS artists;"

##################### CREATE TABLES ###################################

songplay_table_create = """
    CREATE TABLE IF NOT EXISTS artists (
        artist_id          VARCHAR PRIMARY KEY, 
        artist_name        VARCHAR, 
        artist_location    VARCHAR, 
        latitude           NUMERIC, 
        longitude          NUMERIC
    );
"""

user_table_create = ("""
""")

song_table_create = ("""
""")

artist_table_create = ("""
""")

time_table_create = ("""
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]