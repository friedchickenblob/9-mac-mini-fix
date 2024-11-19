import datetime
from part3 import compose_tweet

def search_tweet(c, conn, uid, kw):
    #kw = string of keywords inputted - inputted using commas in one single string
    kw = kw.split(',')
    
    for elem in kw:
        elem = elem.strip() #avoids extra whitespace
        tweets = [] #List of lists where each list is of type (type, date, time, text, tid, writer_id)
        #tid is needed for statistics, writer_id needed for retweet

        if len(elem) == 0: #Only whitespace entered as works
            print("Invalid Input.")
            continue

        #Using Python to order by Date and Time here since difficult to establish a type column using current properties in SQLite queries
        #Assuming Tweets "Currently in view" for user means to view 5 tweets per view
        #Assuming it DOES NOT MEAN that the scope is the person's OWN tweets + People it follows' tweets. However, the queries could've been implemented by adding 
        # "AND t1.writer_id IN (SELECT flwee FROM follows WHERE flwer = {uid}) OR writer_id = {uid}" and "AND r1.retweeter_id IN (SELECT flwee FROM follows WHERE flwer = {uid})" 
        
        if elem[0] == "#":
            #Assuming hashtag_mentions table ONLY has the term
            #2 lists, queries from tweets + queries from retweets, combined and ordered using sorted() for datetime, reverse = True
            
            c.execute(f'''SELECT t1.tdate, t1.ttime, t1.text, t1.tid, t1.writer_id FROM tweets t1, hashtag_mentions h1 WHERE t1.tid = h1.tid AND LOWER(h1.term) = "{elem.lower()}"''')
            tl = c.fetchall()
            for tup in tl:
                tweets.append(['t', tup[0], tup[1], tup[2], tup[3], tup[4]])

            c.execute(f'''SELECT r1.rdate, t1.text, r1.tid, r1.writer_id FROM retweets r1, tweets t1, hashtag_mentions h1 WHERE r1.tid = t1.tid AND t1.tid = h1.tid AND LOWER(h1.term) = "{elem.lower()}"''')
            rtl = c.fetchall()
            for tup in rtl:
                #Added retweet date, not original post date
                #Storing 00:00:00 for time in Retweets since retweets table doesnt store time retweeted
                tweets.append(['rt', tup[0], '00:00:00', tup[1], tup[2], tup[3]])

            tweets = sorted(tweets, key=lambda x: f"{x[1]} {x[2]}", reverse=True)
            #lambda helps avoid creation of extra function to return each subarray's relevant data
            
        else:
            '''LIKE Operator shortlists queries without the element in it
            We use Python to remove values where its present in the wrong format. 
            This could be done in SQL using LIKE and declaring which characters to consider,
            but this is notably more static and slow than Python's methods.
            For example "Hello world" does not contain keyword "He" as per clarification announcement.
            However, "#He" or "He," or "He!" are some examples where the keyword could be present.'''

            #2 lists, queries from tweets + queries from retweets, combined and ordered using sorted() for datetime, reverse = True
            
            #Format: (type, date, time, text, tid, writer_id)
            c.execute(f'SELECT tdate, ttime, text, tid, writer_id FROM tweets WHERE LOWER(text) LIKE "%{elem.lower()}%"')
            tl = c.fetchall()
            for tup in tl:
                ctext = tup[2].split() #current text
                cbool = False #check if current data has the elem in proper manner or not
                for word in ctext:
                    if word.lower().isalpha() and word.lower() == elem.lower():
                         cbool = True
                    else:
                        if (elem.lower() in word.lower()):
                            wordl = list(word)
                            for ch in wordl[:]:
                                if (ch.isalpha() != True):
                                    wordl.remove(ch)
                            wordl = ''.join(wordl)
                            if (wordl.lower() == elem.lower()):
                                cbool = True

                if (cbool):
                    tweets.append(['t', tup[0], tup[1], tup[2], tup[3], tup[4]])
                
            c.execute(f'SELECT r1.rdate, t1.text, r1.tid, r1.writer_id FROM tweets t1, retweets r1 WHERE r1.tid = t1.tid AND LOWER(t1.text) LIKE "%{elem.lower()}%"')
            rtl = c.fetchall()
            for tup in rtl:

                ctext = tup[1].split() #current text
                cbool = False #check if current data has the elem in proper manner or not
                for word in ctext:
                    if word.lower().isalpha() and word.lower() == elem.lower():
                         cbool = True
                    else:
                        if (elem.lower() in word.lower()):
                            wordl = list(word)
                            for ch in wordl[:]:
                                if (ch.isalpha() != True):
                                    wordl.remove(ch)
                            wordl = ''.join(wordl)
                            if (wordl == elem.lower()):
                                cbool = True

                if (cbool):
                    #Added retweet date, not original post date
                    #Storing '00:00:00' for time in Retweets since retweets doesnt store time retweeted
                    tweets.append(['rt', tup[0], '00:00:00', tup[1], tup[2], tup[3]])

            tweets = sorted(tweets, key=lambda x: f"{x[1]} {x[2]}", reverse=True)
        
        if (len(tweets) == 0):
            print(f'Keyword "{elem}" does not occur in any tweets.')
            continue

        print(f'Keyword "{elem}" occurs in the following tweets:')
        for i in range(len(tweets)):
            print(f'{i+1}. "{tweets[i][:-2]}"')
            #Splicing till -2th column since tid and writer_id not needed to be printed
            if ((i+1)%5 == 0):
                #Checks with user at the end of every 5th iteration, if present
                cont = input("Would you like to see 5 more? (y/n) ")
                if (cont.strip().lower() == 'y'):
                    if (i+1 == len(tweets)):
                        print("No more results available.")
                    else:
                        continue
                elif (cont.strip().lower() == 'n'):
                    break
                else:
                    print("Invalid input!")
        print()

        #View Statistics
        while True:
            stat = input("Would you like to see statistics of a tweet? (y/n) ")
            if (stat.strip().lower() == 'y'):
                    #using same variable for convenience
                    try:
                        stat = int(input("Which tweet would you like to see stats of? Enter Sno: "))
                        tweets[stat-1]
                        if stat <= 0:
                            0/0
                    except:
                        print("Invalid input!")
                        continue
                    
                    if tweets[stat-1][0] == 'rt':
                        print("ERROR: You have chosen a retweet, statistics cannot be displayed.")
                    else:
                        #tid is at -2 index
                        c.execute(f'SELECT COUNT(*) FROM retweets r WHERE r.tid = {tweets[stat-1][-2]}')
                        rtc = c.fetchall()[0][0] #retweet count

                        c.execute(f'SELECT COUNT(*) FROM tweets t WHERE t.replyto_tid = {tweets[stat-1][-2]}')
                        rpc = c.fetchall()[0][0] #reply count
                        print("Statistics of chosen tweet: (date, time, retweet count, reply count)")
                        print(tweets[stat-1][1], tweets[stat-1][2], rtc, rpc, sep = " | ")

            elif (stat.strip().lower() == 'n'):
                break

            else:
                print("Invalid input!")

        #Compose Tweet using user defined func
        while True:
            comp = input("Would you like to reply to a tweet? (y/n) ")
            if (comp.strip().lower() == 'y'):
                    #using same variable for convenience
                    try:   
                        comp = int(input("Which tweet would you like to reply to? Enter Sno: "))
                        tweets[comp-1]
                        if comp <= 0:
                            0/0
                    except:
                        print("Invalid input!")
                        continue

                    if tweets[comp-1][0] == 'rt':
                        print("ERROR: You have chosen a retweet, cannot reply to retweet.")
                    else:
                        compose_tweet(c, conn, uid, tweets[comp-1][-2]) #tid stored at -2 index

            elif (comp.strip().lower() == 'n'):
                break

            else:
                print("Invalid input!")

        #Retweet Tweet using INSERT
        while True:
            rt = input("Would you like to retweet a tweet? (y/n) ")
            if (rt.strip().lower() == 'y'):
                    #using same variable for convenience
                    try:
                        rt = int(input("Which tweet would you like to retweet? Enter Sno: "))
                        tweets[rt-1]
                        if rt <= 0:
                            0/0
                    except:
                        print("Invalid input!")
                        continue

                    if tweets[rt-1][0] == 'rt':
                           #Assuming Retweets cannot be retweeted
                           print("ERROR: You have chosen a retweet, cannot retweet a retweet.")
                    else:
                        cdate = str(datetime.date.today())
                        
                        c.execute(f'INSERT INTO retweets (tid, retweeter_id, writer_id, spam, rdate) VALUES ({tweets[rt-1][-2]},{uid},{tweets[rt-1][-1]},0,"{cdate}")')
                        #tid stored at -2 and writer_id at -1 indices
                        #Assuming no tweet is spam here
                        conn.commit()
                        print("Tweet retweeted!")
            
            elif (rt.strip().lower() == 'n'):
                break

            else:
                print("Invalid input!")
                

        
