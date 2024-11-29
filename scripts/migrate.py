import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def apply_migration(cursor, migration_file):
  with open(migration_file, 'r') as f:
    sql = f.read()
    
  for statement in sql.split(';'):
    if statement.strip():
      cursor.execute(statement)

def main():
  db = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_DATABASE'),
    port=os.environ.get('DB_PORT'),
  )

  cursor = db.cursor()

  migrations_dir = 'migrations'
  migrations = sorted(f for f in os.listdir(migrations_dir) if f.endswith('.sql'))

  for migration in migrations:
    migration_file = os.path.join(migrations_dir, migration)
    print(f"applying {migration_file}...")
    apply_migration(cursor, migration_file)
    db.commit()

    cursor.close()
    db.close()

if __name__ == '__main__':
    main()
