import connexion
from connexion import NoContent
import requests
import yaml
from os.path import join, realpath
from json import dumps


def authenticate(body):
    """ Add outside temperature reading to the system """
    headers = {"content-type": "application/json"}
    admin = {
        "Marcus": "MyNewPass1!",
        "Margad": "MyNewPass1!",
        "Adrian": "MyNewPass1!"
    }
    username, password = body['username'], body['password']
    try:
        if admin[username] == password:
            return dumps({"success": True, "statusCode": 201, 'ContentType': 'application/json'})
        else:
            return dumps({"success": False, "statusCode": 400, 'ContentType': 'application/json'})

    except:
        return dumps({"success": False, "statusCode": 400, 'ContentType': 'application/json'})


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(join(realpath("config"), 'openapi.yaml'),
            strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8100)
