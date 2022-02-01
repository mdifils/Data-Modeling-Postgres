import os
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - filepath: str representing a path
    - cur: cursor from a connection to sparkifydb
    - this fonction extract song's metadata and insert them in the songs table.
    - this function extract artist metadata and insert them in the artists table.
    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    df.rename(columns={'artist_latitude':'latitude','artist_longitude':'longitude'}, inplace=True)

    # insert song record
    song_data = df[['song_id','artist_id','title','duration','year']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','latitude','longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - filepath: str representing a path
    - cur: cursor from a connection to sparkifydb
    - this fonction extract log data about the user and insert them in the users table.
    - this function extract log data about when the song was played insert them in the time table.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    t = df['ts']
    
    # insert time data records
    # FutureWarning: Series.dt.weekofyear and Series.dt.week have been deprecated. Please use Series.dt.isocalendar().week instead.
    time_data = [t.values,t.dt.hour.values,t.dt.day.values, \
                 t.dt.isocalendar().week.values,t.dt.month.values, \
                 t.dt.year.values,t.dt.weekday.values]
    column_labels = ['start_time','hour','day','week','month','year','weekday']
    time_df = pd.DataFrame(dict(zip(column_labels,time_data))) 

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['user_id','first_name','last_name','gender','user_location','level']]
    user_df = user_df.drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            song_id, artist_id = results
        else:
            song_id, artist_id = None, None

        # insert songplay record
        songplay_data = (row.user_id,song_id,artist_id,row.ts,row.item_in_session,row.session_id)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - extracting all files in the dataset
    - for every song file apply process_song_file function
    - for every log file apply process_log_file function
    """
    # get all files matching extension from directory
    all_files = []
    # At each node of the tree, root is the node , dirs are the subfolders and files is a list of files at the node level
    for root, dirs, files in os.walk(filepath):
        for f in files:
            if f.endswith('.json'):
                all_files.append(os.path.join(root,f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Connecting to sparkifydb 
    - Process all the dataset
    - Inserting data into all tables
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    print('\nProcessing song data\n')
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    
    print('\nProcessing log data\n')
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()