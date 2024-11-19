import sqlite3

def search_users(c, conn, db_name, logged_in_user):
    keyword = input("Enter a keyword to search for users: ").strip()
    sql_query = """
        SELECT usr, name
        FROM users
        WHERE LOWER(name) LIKE ?
        ORDER BY LENGTH(name) ASC
        LIMIT 5 OFFSET ?;
    """

    offset = 0
    params = (f"%{keyword.lower()}%",)

    while True:
        c.execute(sql_query, (*params, offset))
        results = c.fetchall()

        if not results:
            print("No more results.")
            break

        print("\nUser Search Results:")
        for index, row in enumerate(results, start=1):
            print(f"{index}. User ID: {row[0]}, Name: {row[1]}")
        
        choice = input("\nSelect a user number to view details or press 'n' to see more results: ").strip()

        if choice.isdigit():
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(results):
                selected_user_id = results[selected_index][0]
                view_user_details(c, conn, db_name, selected_user_id, logged_in_user)
            else:
                print("Invalid selection. Please try again.")
        elif choice.lower() == 'n':
            offset += 5
        else:
            break

def view_user_details(c, conn, db_name, user_id, logged_in_user):
    # Get user tweet count, following count, and follower count
    c.execute("SELECT COUNT(*) FROM tweets WHERE writer_id = ?", (user_id,))
    tweet_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM follows WHERE flwer = ?", (user_id,))
    following_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM follows WHERE flwee = ?", (user_id,))
    follower_count = c.fetchone()[0]
    
    print(f"\nUser ID: {user_id}")
    print(f"Number of tweets: {tweet_count}")
    print(f"Following: {following_count}")
    print(f"Followers: {follower_count}")
    
    # Retrieve and display up to three recent tweets
    c.execute("""
        SELECT text, tdate, ttime
        FROM tweets
        WHERE writer_id = ?
        ORDER BY tdate DESC, ttime DESC
        LIMIT 3;
    """, (user_id,))
    recent_tweets = c.fetchall()
    
    if recent_tweets:
        print("\nRecent Tweets:")
        for tweet in recent_tweets:
            print(f"- {tweet[0]} (Date: {tweet[1]}, Time: {tweet[2]})")
    else:
        print("\nNo recent tweets available.")
    
    # Option to follow the user
    follow_choice = input("Would you like to follow this user? (y/n): ").strip().lower()
    if follow_choice == 'y':
        follow_user(c, conn, logged_in_user, user_id)

def follow_user(c, conn, logged_in_user, user_id):
    # Verify both logged_in_user and selected user exist
    c.execute("SELECT 1 FROM users WHERE usr = ?", (logged_in_user,))
    if c.fetchone() is None:
        print("Error: Logged-in user does not exist.")
        return
    
    c.execute("SELECT 1 FROM users WHERE usr = ?", (user_id,))
    if c.fetchone() is None:
        print("Error: Selected user does not exist.")
        return
    
    # Check if the follow relationship already exists
    c.execute("SELECT 1 FROM follows WHERE flwer = ? AND flwee = ?", (logged_in_user, user_id))
    if c.fetchone():
        print("You are already following this user.")
        return

    # Check if they are trying to follow themselves
    c.execute("SELECT 1 FROM follows WHERE ? = ?", (logged_in_user, user_id))
    if c.fetchone():
        print("You cannot follow yourself")
        return
    
    # Insert the follow relationship
    try:
        c.execute("""
            INSERT INTO follows (flwer, flwee, start_date)
            VALUES (?, ?, date('now'))
        """, (logged_in_user, user_id))
        conn.commit()
        print("You are now following the user.")
    except sqlite3.IntegrityError as e:
        print(f"Failed to follow user due to integrity error: {e}")
