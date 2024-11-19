from datetime import datetime

def list_followers(c, conn, uid):
    c.execute("select * from follows where :flwee = flwee", {"flwee": uid})
    follower_list = c.fetchall()

    # Check if the user has no followers
    if len(follower_list) == 0:
        print("You have no followers")
        return

    # Print followers in chunks of 5
    follower_dict = {}
    user_input = None

    print("Followers:")
    for i in range(0, len(follower_list) // 5 + 1):
        for x in follower_list[i * 5: i * 5 + 5]:
            follower = x[0]
            c.execute("select * from users where :usr = usr", {"usr": follower})
            follower_info = c.fetchone()
            follower_name = follower_info[1]
            follower_dict[follower_name] = follower_info
            print(follower_name)

        user_input = input("Select a follower or press m for next 5: ")
        if user_input != "m":
            break
    else:
        print("Listed all followers")
        
    follower_select = user_input

    # Loop until valid follower selected
    while follower_select not in follower_dict:
        follower_select = input("Select a follower: ")
    follower_id = follower_dict[follower_select][0]
    
    # Print info of follower selected
    print(f"{follower_select} Info:")

    c.execute("select * from tweets where :writer_id = writer_id", {"writer_id": follower_id})
    print(f"Has made {len(c.fetchall())} tweets")
    
    c.execute("select * from follows where :flwer = flwer", {"flwer": follower_id})
    print(f"Follows {len(c.fetchall())} people")

    c.execute("select * from follows where :flwee = flwee", {"flwee": follower_id})
    print(f"Has {len(c.fetchall())} followers")

    # Sort according to date and time descending
    c.execute(''' SELECT * FROM tweets WHERE writer_id = :writer_id ORDER BY tdate DESC, ttime DESC''', {'writer_id':follower_id})
    follower_select_tweets = c.fetchall()

    print("Most Recent Tweets:")
    for tweet in follower_select_tweets[:3]:
        print(f"- {tweet[2]} (Date: {tweet[3]}, Time: {tweet[4]})")

    user_input = None
    curr_slice = 1

    # Display more tweets and ability to follow
    while user_input != "2":
        if user_input == "m":
            if len(follower_select_tweets[curr_slice * 3 : curr_slice * 3 + 3]) == 0:
                print("No more tweets")
            else:
                for tweet in follower_select_tweets[:3]:
                    print(f"- {tweet[0]} (Date: {tweet[1]}, Time: {tweet[2]})")
                
                curr_slice += 1

        elif user_input == "1":
            c.execute("""select * from follows where :flwee = flwee and :flwer = flwer;""", {"flwer": uid, "flwee": follower_id})
            if len(c.fetchall()) != 0:
                print("Already following this user")
            else:
                c.execute("""insert into follows values (:flwer, :flwee, :start_date);""", {"flwer": uid, "flwee": follower_id, "start_date": datetime.today().strftime("%Y-%m-%d")})
                conn.commit()
                print("You are now following this user")

        user_input = input("Press m to see more tweets, 1 to follow this person, 2 to go back to main menu: ")
