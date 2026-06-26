class SqlQueries:
    songplay_table_insert = ("""
        SELECT
            events.start_time,
            events.userid,
            md5(events.sessionid || events.start_time) AS songplay_id,
            events.level,
            songs.song_id,
            songs.artist_id,
            events.sessionid,
            events.location,
            events.useragent
        FROM (
            SELECT
                *,
                TIMESTAMP 'epoch' + ts / 1000 * INTERVAL '1 second' AS start_time
            FROM staging_events
            WHERE page = 'NextSong'
        ) AS events
        LEFT JOIN staging_songs AS songs
            ON
                events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        SELECT DISTINCT
            userid,
            firstname,
            lastname,
            gender,
            level
        FROM staging_events
        WHERE page = 'NextSong'
    """)

    song_table_insert = ("""
        SELECT DISTINCT
            song_id,
            title,
            artist_id,
            year,
            duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        SELECT DISTINCT
            artist_id,
            artist_name,
            artist_location,
            artist_latitude,
            artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        SELECT
            start_time,
            EXTRACT(HOUR FROM start_time) AS hour,
            EXTRACT(DAY FROM start_time) AS day,
            EXTRACT(WEEK FROM start_time) AS week,
            EXTRACT(MONTH FROM start_time) AS month,
            EXTRACT(YEAR FROM start_time) AS year,
            EXTRACT(DAYOFWEEK FROM start_time) AS dayofweek
        FROM songplays
    """)