import sqlite3
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create an sqlite database by reading sql commands from the provided .sql file
def create_database(sql_file_path, db_file_path):
    logging.info(f'Creating database using {sql_file_path}')
    # Connect to the new SQLite database file
    # If the file doesn't exist, SQLite will create it
    conn = sqlite3.connect(db_file_path)

    # Read the SQL script
    with open(sql_file_path, 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script
    try:
        conn.executescript(sql_script)
        logging.info("Database created and populated successfully.")
    except sqlite3.Error as e:
        logging.error(f"An error occurred: {e.args[0]}")
    finally:
        conn.close()

# Performs a test query of a hard coded sql statement given the path to an sqlite db
def query_database(db_file_path):
    logging.info(f'Querying database at {db_file_path}')
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)

    # Create a cursor object
    cursor = conn.cursor()

    # Query: Select data from a table (e.g., Album)
    query = "SELECT * FROM students"

    # Execute the sql query
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            logging.info(row)
    except sqlite3.Error as e:
        logging.error(f"An error occurred: {e.args[0]}")
    finally:
        cursor.close()
        conn.close()
        
# Paths
sql_file_path = 'knowledge/schema/starfleet-sqlite.sql'  # Update this to the path of your .sql file
db_file_path = 'starfleet.sqlite'  # The SQLite file to be created

# Create our sample sqlite database and perform a test read
create_database(sql_file_path, db_file_path)
query_database(db_file_path=db_file_path)

