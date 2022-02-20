import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from temperature import Temperature
from os.path import realpath, join
from datetime import datetime
from uuid import uuid1
import mysql.connector
import pymysql
import yaml

with open(join(realpath("config"), 'app_conf.yml'), 'r') as f:
    app_config = yaml.safe_load(f.read())
    user = app_config['datastore']['user']
    password = app_config['datastore']['password']
    hostname = app_config['datastore']['hostname']
    port = app_config['datastore']['port']
    db = app_config['datastore']['db']


DB_ENGINE = create_engine(
    f"mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


# Storage system Post method_1
def report_outside_temperature(body):
    """ Recieves and saves a new job ad description """
    session = DB_SESSION()
    dt = datetime.now()
    year, month, day = [int(x) for x in str(dt.date()).split('-')]
    hour = dt.hour
    temperature = Temperature(str(uuid1()),
                              float(body['temperature']),
                              year,
                              month,
                              day,
                              hour)

    session.add(temperature)
    session.commit()
    session.close()
    return NoContent, 201

# Storage system GET method_1
# def get_advertisement_description(timestamp):
#     """ Retrieve all the Job Description advertisement that are stored after certain timestamp"""
#     logger.info(f"Hostname: {hostname}, port: {port}")
#     session = DB_SESSION()
#     timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
#     readings = session.query(JobDescription).filter(
#         JobDescription.date_created >= timestamp_datetime)
#     results_list = [reading.to_dict() for reading in readings]
#     session.close()

#     logger.info(
#         f"Query for Job advertisement description after {timestamp} returns {len(results_list)} results.")

#     return results_list, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(join(realpath("config"), 'openapi.yaml'),
            strict_validation=False, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)
