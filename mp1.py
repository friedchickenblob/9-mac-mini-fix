import sqlite3
from register import register
from part1 import search_tweet
from part2 import search_users
from part3 import compose_tweet
from part4 import list_followers 

from getpass import getpass #to hide password during login


conn	=	sqlite3.connect(__import__("sys").argv[1])
conn.execute("PRAGMA foreign_keys = ON;") #enables foreign key constraints.

c = conn.cursor()

# c.executescript(''' 
# drop table if exists follows;
# drop table if exists lists;
# drop table if exists include;
# drop table if exists tweets;
# drop table if exists retweets;
# drop table if exists hashtag_mentions;
# drop table if exists users;

# CREATE TABLE users (
#     usr         int,
#     name        text,
#     email       text,
#     phone       int,
#     pwd         text,
#     primary key (usr)
# );

# CREATE TABLE follows (
#     flwer       int,
#     flwee       int,
#     start_date  date,
#     primary key (flwer,flwee),
#     foreign key (flwer) references users(usr) ON DELETE CASCADE,
#     foreign key (flwee) references users(usr) ON DELETE CASCADE
# );

# CREATE TABLE lists (
#     owner_id    int,
#     lname       text,
#     PRIMARY KEY (owner_id, lname),
#     FOREIGN KEY (owner_id) REFERENCES users(usr) ON DELETE CASCADE
# );

# CREATE TABLE include (
#     owner_id    int,
#     lname       text,
#     tid         int,
#     PRIMARY KEY (owner_id, lname, tid),
#     FOREIGN KEY (owner_id, lname) REFERENCES lists(owner_id, lname) ON DELETE CASCADE,
#     FOREIGN KEY (tid) REFERENCES tweets(tid) ON DELETE CASCADE
# );

# CREATE TABLE tweets (
#     tid         int,
#     writer_id   int,
#     text        text,
#     tdate       date, 
#     ttime       time,
#     replyto_tid int,
#     PRIMARY KEY (tid),
#     FOREIGN KEY (writer_id) REFERENCES users(usr) ON DELETE CASCADE,
#     FOREIGN KEY (replyto_tid) REFERENCES tweets(tid) ON DELETE CASCADE
# );

# CREATE TABLE retweets (
#     tid         int,
#     retweeter_id   int, 
#     writer_id      int, 
#     spam        int,
#     rdate       date,
#     PRIMARY KEY (tid, retweeter_id),
#     FOREIGN KEY (tid) REFERENCES tweets(tid) ON DELETE CASCADE,
#     FOREIGN KEY (retweeter_id) REFERENCES users(usr) ON DELETE CASCADE,
#     FOREIGN KEY (writer_id) REFERENCES users(usr) ON DELETE CASCADE
# );

# CREATE TABLE hashtag_mentions (
#     tid         int,
#     term        text,
#     primary key (tid, term),
#     FOREIGN KEY (tid) REFERENCES tweets(tid) ON DELETE CASCADE
# );

# ''')

# c.execute("""insert into users values (1, 'John', 'john@example.com', 1234567891, 'pass1');""")
# c.execute("""insert into users values (2, 'Emma', 'emma@example.com', 9876543212, 'pass2');""")
# c.execute("""insert into users values (3, 'Leo', 'leo@example.com', 5432167893, 'pass3');""");
# c.execute("""insert into users values (4, 'Dion', 'dion@gmail.com', 12345, 'passdion');""");
# c.execute("""insert into users values (5, 'egg', 'egg', 12345, 'egg');""");
# c.execute("""insert into users values (6, 'a', 'a', 12345, 'a');""");
# c.execute("""insert into users values (7, 'b', 'b', 12345, 'b');""");
# c.execute("""insert into users values (8, 'c', 'c', 12345, 'c');""");
# c.execute("""insert into users values (9, 'd', 'd', 12345, 'd');""");
# c.execute("""insert into users values (10, 'Evan', 'evan@gmail.com', 1234355, 'pass4');""");
# c.execute("""insert into users values (11, 'Ema', 'ema@gmail.com', 1234573895, 'passema');""");
# c.execute("""insert into users values (12, 'Emilia', 'emilia@gmail.com', 123243678245, 'passemilia');""");
# c.execute("""insert into follows values (1, 2, '2023-01-20')""")
# c.execute("""insert into follows values (2, 3, '2023-02-14')""")
# c.execute("""insert into follows values (3, 1, '2023-03-01')""")
# c.execute("""insert into follows values (3, 2, '2024-10-22')""")
# c.execute("""insert into follows values (1, 3, '2024-10-22')""")
# c.execute("""insert into follows values (5, 2, '2024-10-22')""")
# c.execute("""insert into follows values (6, 2, '2024-10-22')""")
# c.execute("""insert into follows values (7, 2, '2024-10-22')""")
# c.execute("""insert into follows values (8, 2, '2024-10-22')""")
# c.execute("""insert into follows values (9, 2, '2024-10-22')""")
# c.execute("""insert into tweets values (101, 1, 'John talks about database management #Database', '2024-10-20', '09:00:00', :null)""", {"null": None})
# c.execute("""insert into tweets values (102, 2, "Emma replies to John's thoughts #ReplyToJohn", '2024-10-21', '10:00:00', 101)""")
# c.execute("""insert into tweets values (103, 3, 'Leo comments on the CMPUT291 project #CMPUT291Project', '2024-10-22', '11:00:00', :null)""", {"null": None})
# c.execute("""insert into tweets values (104, 2, 'Emma shares a new project idea #NewProject', '2024-10-23', '12:00:00', :null)""", {"null": None})
# c.execute("""insert into tweets values (105, 2, 'Emma asks for advice on the database project #DatabaseHelp', '2024-10-24', '14:00:00', :null)""", {"null": None})
# c.execute("""insert into tweets values (106, 2, "Emma comments on Leo's post about CMPUT291 #CMPUT291Feedback", '2024-10-25', '15:00:00', 103)""")
# c.execute("""insert into tweets values (107, 3, 'Leo comment 1', '2024-10-23', '11:01:00', :null)""", {"null": None})
# c.execute("""insert into tweets values (108, 4, "Dion comments on Leo's post about CMPUT291 #CMPUT291Feedback", '2024-10-28', '15:00:00', 103)""")
# c.execute("""insert into tweets values (109, 3, 'Leo comment 2', '2024-10-21', '11:01:00', :null)""", {"null": None})
# c.execute("""insert into tweets values (110, 3, 'Leo comment 3', '2024-10-21', '11:02:00', :null)""", {"null": None})
# c.execute("""insert into tweets values (111, 3, 'Leo comment 4', '2024-10-22', '11:03:00', :null)""", {"null": None})
# c.execute("""insert into tweets values (112, 6, 'a comment', '2024-11-15', '00:00:01', :null)""", {"null": None})
# c.execute("""insert into retweets values (101, 2, 1, 0, '2024-10-25')""")
# c.execute("""insert into retweets values (103, 1, 3, 1, '2024-10-25')""")
# c.execute("""insert into retweets values (101, 3, 2, 0, '2024-10-21')""")
# c.execute("""insert into retweets values (102, 4, 2, 0, '2024-10-22')""")
# c.execute("""insert into retweets values (103, 5, 2, 1, '2024-10-23')""")
# c.execute("""insert into retweets values (104, 6, 2, 0, '2024-10-24')""")
# c.execute("""insert into retweets values (105, 7, 2, 0, '2024-10-25')""")
# c.execute("""insert into retweets values (104, 2, 6, 0, '2024-10-24')""")
# c.execute("""insert into retweets values (103, 2, 5, 1, '2024-10-23')""")
# c.execute("""insert into hashtag_mentions values (101, '#Database')""")
# c.execute("""insert into hashtag_mentions values (102, "#ReplyToJohn")""")
# c.execute("""insert into hashtag_mentions values (103, '#CMPUT291Project')""")
# c.execute("""insert into hashtag_mentions values (104, '#NewProject')""")
# c.execute("""insert into hashtag_mentions values (105, '#DatabaseHelp')""")
# c.execute("""insert into hashtag_mentions values (106, "#CMPUT291Feedback")""")
# conn.commit()

uid = None

while True:
    option = input("Enter 1 to register or 2 to login or 3 to exit: ")
    if option == "1": # register
        register(c, conn)

    elif option == "2": # login
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")

        c.execute(
            'SELECT * FROM users WHERE name = :uname AND pwd = :pw;',
            { 'uname': username, 'pw': password },
        )
        result = c.fetchone()
        if result != None:
            print("User signed in!!")

            uid = result[0]
            c.execute(''' SELECT tid, writer_id, text, tdate, ttime FROM tweets
                          WHERE writer_id IN ( SELECT flwee FROM follows WHERE flwer = :uid)
                          UNION ALL
                          SELECT tid, retweeter_id AS writer_id, "retweet" AS text, rdate AS tdate, "00:00:00" AS ttime FROM retweets
                          WHERE retweeter_id IN (SELECT flwee FROM follows WHERE flwer = :uid) ORDER BY tdate DESC, ttime DESC ''',{
                'uid': uid
            })
            followee_tweets=c.fetchall()
            

            page_size = 5
            page_index = 0
            current_page = True # If user clicks anything other than "show more", set this flag to false so tweets are reset
            error = False

            while True:

                if current_page or error:
                    pass
                else:
                    c.execute(''' SELECT tid, writer_id, text, tdate, ttime FROM tweets
                                  WHERE writer_id IN ( SELECT flwee FROM follows WHERE flwer = :uid)
                                  UNION ALL
                                  SELECT tid, retweeter_id AS writer_id, "retweet" AS text, rdate AS tdate, "00:00:00" AS ttime FROM retweets
                                  WHERE retweeter_id IN (SELECT flwee FROM follows WHERE flwer = :uid) ORDER BY tdate DESC, ttime DESC ''',{
                        'uid': uid
                    })
                    followee_tweets=c.fetchall()
                    page_index = 0

                # Show the next 5 posts
                if not error:
                    start_index = page_index * page_size
                    if(start_index >= len(followee_tweets)):
                        print("No more tweets/retweets.")
                    end_index = start_index + page_size
                    posts_to_show = followee_tweets[start_index:end_index]

                    # Print the posts
                    for tweet in posts_to_show:
                        print(f"- {tweet[2]} (Date: {tweet[3]}, Time: {tweet[4]})")

                error = False
                current_page = False

                # Ask if the user wants to see more
                user_input = input("Press m to show more tweets/retweets, 1 to search for tweets, 2 to search for users, 3 to compose a tweet, 4 to check list of followers, 5 to log out: ")
                if user_input == "m":
                    # show more tweets/retweets
                    # Increment page index to show next set of posts
                    page_index += 1
                    current_page = True

                elif user_input == "1":
                    # Search for tweets
                    search_tweet(c, conn, uid, input("Enter keywords separated by commas only: "))

                elif user_input == "2":
                    #search for users.
                    search_users(c, conn, conn, result[0])
                    
                
                elif user_input == "3":
                    # Compose tweet
                    compose_tweet(c, conn, uid, None)
                
                elif user_input == "4":
                    #check list of followers
                    list_followers(c, conn, uid)

                elif user_input == "5":
                    #log out
                    break

                else:
                    #invalid input.
                    error = True
                    print("Invalid input!")
        else:
            print("Error: Invalid username or password.")

    elif option == "3": #exit
        break

    else:
        print("Invalid input!")
