import connexion
from connexion import NoContent
import yaml
from os.path import join, realpath
import mysql.connector as mysql

mysql_db = mysql.connect(
    host="storage",
    user="root",
    password="MyNewPass1!",
    database="events"
)


def statistics():
    """ Add outside temperature reading to the system """
    print("Connected to:", mysql_db.get_server_info())
    return 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(join(realpath("config"), 'openapi.yaml'),
            strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8010)
