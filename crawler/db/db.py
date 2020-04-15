import sqlite3
import os

db_path = '../db.sqlite'
conn = sqlite3.connect(db_path)

def tuple_to_ptr_object(ptr_tuple):
  return {
    'id': ptr_tuple[0],
    'senator_id': ptr_tuple[1],
    'url': ptr_tuple[2],
    'date': ptr_tuple[3]
  }

def tuple_to_senator_object(senator_tuple):
  return {
    'id': senator_tuple[0],
    'first_name': senator_tuple[1],
    'middle_initial': senator_tuple[2],
    'last_name': senator_tuple[3],
    'office': senator_tuple[4],
    'status': senator_tuple[5]
  }

def tuple_to_transaction_object(transaction_tuple):
  return {
    'id': transaction_tuple[0],
    'senator_id': transaction_tuple[1],
    'ptr_id': transaction_tuple[2],
    'owner': transaction_tuple[3],
    'ticker': transaction_tuple[4],
    'asset_name': transaction_tuple[5],
    'asset_type': transaction_tuple[6],
    'transaction_type': transaction_tuple[7],
    'transaction_lower': transaction_tuple[8], 
    'transaction_upper': transaction_tuple[9],
    'comment': transaction_tuple[10],
    'date': transaction_tuple[11]
  }

def create_table_if_not_exists(table_query):
  c = conn.cursor()

  #run the table creation script
  c.execute(table_query)
  conn.commit()
  c.close()

def insert(query, values):
  c = conn.cursor()
  c.execute(query, values)
  conn.commit()
  c.close()


# def get_unliked_posts(hashtag):
#   c = conn.cursor()

#   # get the hashtags from db
#   c.execute("""SELECT * FROM posts WHERE hashtag=? AND liked = 0""", (hashtag, ))

#   posts = [tuple_to_post_obj(row)for row in c]
#   print('unliked posts:', posts)

#   c.close()
#   return posts

# def get_liked_posts(hashtag):
#   c = conn.cursor()

#   c.execute("""SELECT * FROM posts WHERE hashtag=? AND liked = 1""", (hashtag,))
#   posts = [tuple_to_post_obj(row) for row in c]
#   print('liked posts:', posts)

#   c.close()
#   return posts

def get_senator(first_name, middle_initial, last_name, status):
  c = conn.cursor()
  c.execute("""SELECT * FROM senators WHERE first_name=? AND (middle_initial=? OR middle_initial IS NULL) AND last_name=? AND status=?""", (first_name, middle_initial, last_name, status))
  senators = [tuple_to_senator_object(row) for row in c]
  c.close()
  
  if not senators:
    return None
  
  return senators[0]

def get_ptr(ptr_url):
  c = conn.cursor()
  c.execute("""SELECT * FROM ptrs WHERE url=?""", (ptr_url,))
  ptrs = [tuple_to_ptr_object(row) for row in c]
  c.close()
  
  if not ptrs:
    return None

  return ptrs[0]

def set_ptr_to_collected(ptr_id):
  c = conn.cursor()
  c.execute("""UPDATE ptrs SET collected = 1 WHERE id=?""", (ptr_id,))
  c.close()
  return

def get_all_active_ptrs():
  c = conn.cursor()
  c.execute("""SELECT * FROM ptrs WHERE collected=0""")
  ptrs = [tuple_to_ptr_object(row) for row in c]
  c.close()

  if not ptrs:
    ptrs = None
  
  return ptrs

# def count_posts_for_hashtag(hashtag):
#   c = conn.cursor()

#   c.execute("""SELECT * FROM posts WHERE hashtag=?;""", (hashtag,))
#   posts = [tuple_to_post_obj(row) for row in c]
#   total_posts = len(posts)
#   print('found {} hashtags for hashtag #{}'.format(total_posts, hashtag))

#   c.close()
#   return total_posts

# def set_post_liked(post_url):
#   c = conn.cursor()

#   c.execute("""UPDATE posts SET liked=? WHERE url=?;""", (True, post_url,))
#   conn.commit()
#   c.close()
#   return

# def delete_post(post_url):
#   c = conn.cursor()

#   c.execute("""DELETE FROM posts WHERE url=?;""", (post_url,))
#   conn.commit()
#   c.close()
#   return

def insert_ptr(ptr_obj):
  c = conn.cursor()

  c.execute("""INSERT INTO ptrs (senator_id, url, submitted_date) VALUES(?,?,?)""", ptr_obj)
  conn.commit()
  c.close()
  return c.lastrowid

def insert_senator(senator_obj):
  c = conn.cursor()

  c.execute("""INSERT INTO senators (first_name, middle_initial, last_name, office, status) VALUES(?,?,?,?,?)""", senator_obj)
  conn.commit()
  c.close()
  return c.lastrowid

def insert_transaction(transaction_obj):
  c = conn.cursor()

  c.execute("""INSERT INTO transactions (senator_id, ptr_id, owner, ticker, asset_name, asset_type, transaction_type, transaction_lower, transaction_upper, comment, date) VALUES(?,?,?,?,?,?,?,?,?,?,?)""", transaction_obj)
  conn.commit()
  c.close()
  return c.lastrowid

# on startup, create the ptrs table if it doesn't exist
create_table_if_not_exists(""" CREATE TABLE IF NOT EXISTS senators (id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, middle_initial TEXT, last_name TEXT NOT NULL, office TEXT, status TEXT);""")
create_table_if_not_exists(""" CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, senator_id INTEGER NOT NULL, ptr_id INTEGER NOT NULL, owner TEXT, ticker TEXT, asset_name TEXT, asset_type TEXT, transaction_type TEXT, transaction_lower INTEGER NOT NULL, transaction_upper INTEGER NULL, comment TEXT, date TEXT);""")
create_table_if_not_exists(""" CREATE TABLE IF NOT EXISTS ptrs (id INTEGER PRIMARY KEY, senator_id INTEGER NOT NULL, url TEXT NOT NULL, submitted_date TEXT);""")