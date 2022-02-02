import os
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - filepath: str representing a path
    - cur: cursor from a connection to sparkifydb
    - this fonction extract song's metadata and insert them in the songs table.
    - this function extract artist metadata and insert them in the artists 
    table.
    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    # Renaning some columns, inplace is used to update the original
    # instead of creating a copy
    df.rename(columns={'artist_latitude':'latitude',
                       'artist_longitude':'longitude'},
              inplace=True)

    # insert song record
    # Selecting interesting columns, then taking just values instead of
    # the dataframe then converting the numpy array into a list
    song_data = \
        df[['song_id','artist_id','title','duration','year']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','latitude',\
                      'longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - filepath: str representing a path
    - cur: cursor from a connection to sparkifydb
    - this fonction extract log data about the user and insert them 
    in the users table.
    - this function extract log data about when the song was played insert them
    in the time table.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)
    df.rename(columns={'firstName':'first_name',
                       'lastName':'last_name',
                       'itemInSession':'item_in_session',
                       'sessionId':'session_id',
                       'userId':'user_id',
                       'location':'user_location',
                       'userAgent':'user_agent'}, inplace=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    t = df['ts']
    
    # insert time data records
    # FutureWarning: Series.dt.weekofyear and Series.dt.week have been 
    # deprecated. Please use Series.dt.isocalendar().week instead.
    time_data = [t.values,t.dt.hour.values,t.dt.day.values, \
                 t.dt.isocalendar().week.values,t.dt.month.values, \
                 t.dt.year.values,t.dt.weekday.values]
    column_labels = ['start_time','hour','day','week','month','year','weekday']
    time_df = pd.DataFrame(dict(zip(column_labels,time_data))) 

    for i, row in time_df.iterrows():
        # every row in the dataframe gives a tuple to be inserted in the table
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['user_id','first_name','last_name','gender','level']]
    # user_df = user_df.drop_duplicates()
    # ON CONFLICT will take of duplicates

    # insert user records
    for i, row in user_df.iterrows():
        # every row in the dataframe gives a tuple to be inserted in the table
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        # As there are no song_id and no artist_id in the log data
        # let's check if there are song_id and artist_id in song data
        # that match the log data
        # song_select is query by which songs table and artists table are
        # joinned base on title, artist_name and duration
        cur.execute(song_select, (row.song, row.artist,row.length))
        results = cur.fetchone()
        
        if results:
            # 
            song_id, artist_id = results
        else:
            song_id, artist_id = None, None

        # insert songplay record
        songplay_data = (row.user_id,song_id,artist_id,row.ts,row.session_id,\
                         row.user_location,row.user_agent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - extracting all files in the dataset
    - for every song file apply process_song_file function
    - for every log file apply process_log_file function
    """
    # get all files matching extension from directory
    all_files = []
    # At each level of the tree, root is one node , dirs is a list of subfolders 
    # inside that node and files is a list of files inside the same node.
    for root, dirs, files in os.walk(filepath):
        for f in files:
            # looking for JSON files at each level of the tree
            if f.endswith('.json'):
                all_files.append(os.path.join(root,f))

    # get total number of files found
    num_files = len(all_files)
    print(f'{num_files} files found in {filepath}')

    # iterate over files and process, making index to start from 1 instead of 0
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print(f'{i}/{num_files} files processed')


def main():
    """
    - Connecting to sparkifydb 
    - Process all the dataset
    - Inserting data into all tables
    """
    # connecting to sparkifydb database
    conn = psycopg2.connect("host=pgdb dbname=sparkifydb user=student \
                            password=student")
    cur = conn.cursor()
    
    print('\nProcessing song data\n')
    # processing song data and inserting into songs and artists tables
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    
    print('\nProcessing log data\n')
    # processing log data and inserting into time, users and songplays tables
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    
    # closing the connection to sparkifydb database
    conn.close()


if __name__ == "__main__":
    main()