import connexion
from connexion import NoContent
import requests
import yaml
from os.path import join, realpath


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
        return (NoContent, 201) if admin[username] == password else (NoContent, 400)
    except KeyError:
        return NoContent, 400

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(join(realpath("config"), 'openapi.yaml'),
            strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8100)
