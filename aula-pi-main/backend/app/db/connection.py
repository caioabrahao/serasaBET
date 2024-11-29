from flask import g
import mysql.connector
import os

def get_db():
  if 'db' not in g:
    g.db = mysql.connector.connect(
      host=os.environ.get('DB_HOST'),
      user=os.environ.get('DB_USER'),
      password=os.environ.get('DB_PASSWORD'),
      database=os.environ.get('DB_DATABASE'),
      port=os.environ.get('DB_PORT')
    )

    return g.db

def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()
