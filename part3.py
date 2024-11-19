from datetime import datetime

def compose_tweet(c, conn, uid, replyID):
    # replyID: ID of tweet being replied to, None if not a reply

    # Get tweet and extract hashtags
    duplicate_hashtag = 1
    while duplicate_hashtag == 1:
        tweet_text = input("Tweet text: ")
        hashtag_list = tweet_text.split()
        position = 0
        while position < len(hashtag_list):
            if hashtag_list[position][0] != '#':
                hashtag_list.pop(position)
                position - 1
            position += 1
        # Check for duplicate hashtags
        duplicate_hashtag = 0
        for h in hashtag_list:
            if hashtag_list.count(h) > 1:
                duplicate_hashtag = 1
                print("Duplicate hashtags, please try again.")
                break
    
    # Set tid to next missing value
    c.execute(''' SELECT tid FROM tweets ORDER BY tid DESC LIMIT 1; ''')
    result = c.fetchone()
    tid = 1
    if result: 
        tid=result[0]+1
    # Insert tweet into table
    # Using local time for the date/time, unsure if this is correct
    current = datetime.now()
    date = current.strftime("%Y-%m-%d")
    time = current.strftime("%H:%M:%S")
    c.execute("""INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid) VALUES (:tid, :uid, :tweet_text, :date, :time, :replyID)""", {"tid": tid, "uid": uid, "tweet_text": tweet_text, "date": date, "time": time, "replyID": replyID})

    # Insert hashtags into table
    for term in hashtag_list:
        c.execute("""INSERT INTO hashtag_mentions (tid, term) VALUES (:tid, :term)""", {"tid": tid, "term": term})
    conn.commit()
    print("Tweet posted!")

    

