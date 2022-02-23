import connexion
from connexion import NoContent
import yaml
from os.path import join, realpath
import mysql.connector as mysql
import pymongo

con = mysql.connect(
    host="storage",
    user="root",
    password="MyNewPass1!",
    database="events"
)


def statistics():
    """ Add outside temperature reading to the system """
    print("Connected to:", con.get_server_info())
    cur = con.cursor(buffered=True)
    count = cur.execute("SELECT COUNT(*) FROM Temperature")
    sum1 = cur.execute("SELECT SUM(temperature) FROM Temperature")
    print(f"\n\n{count}\n\n")
    print(f"\n\n{sum1}\n\n")
    # avg = sum1 / count

    max1 = cur.execute("SELECT MAX(temperature) from Temperature")
    min1 = cur.execute("SELECT MIN(temperature) from Temperature")

    mongo = pymongo.MongoClient("mongodb://root:MyNewPass1!@mongo_storage:27017/")
    mongodb = mongo["calulated_data"]
    mongocol = mongodb["stats"]
    # print(f"avg {avg}\n max {max1}\n min {min1}")
    statList = [
        # {"Average Temp": avg},
        {"Max Temp": max1},
        {"Min Temp": min1}
    ]
    mongocol.insert_many(statList)
    return 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(join(realpath("config"), 'openapi.yaml'),
            strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8010)
