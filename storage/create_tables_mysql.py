import mysql.connector
import yaml
from os.path import join, realpath

with open(join(realpath("config"), 'app_conf.yml'), 'r') as f:
    app_config = yaml.safe_load(f.read())
    user = app_config['datastore']['user']
    hostname = app_config['datastore']['hostname']
    password = app_config['datastore']['password']
    database = app_config['datastore']['db']
    port = app_config['datastore']['port']

db_conn = mysql.connector.connect(
    host=hostname, user=user, password=password, database=database)

db_cursor = db_conn.cursor()

db_cursor.execute('''
        CREATE TABLE temperature
        (id INT NOT NULL AUTO_INCREMENT,
         temperature_id VARCHAR(250) NOT NULL,
         temperature FLOAT NOT NULL,
         year INTEGER NOT NULL,
         month INTEGER NOT NULL,
         day INTEGER NOT NULL,
         hour INTEGER NOT NULL,
         CONSTRAINT temperature_pk PRIMARY KEY(id))
        ''')

db_conn.commit()
db_conn.close()
