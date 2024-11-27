from flask import g
import mysql.connector

def get_db():
  if 'db' not in g:
    g.db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="docker",
      database="serasa-bet",
      port="3306"
    )

    return g.db

def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()
