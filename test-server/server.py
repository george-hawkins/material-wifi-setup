from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from re import match

from flask import Flask
from flask import json
from flask import jsonify
from flask import abort
from flask import request
from flask import Response

from werkzeug.exceptions import HTTPException

# The underlying handler still defaults to HTTP/1.0.
BaseHTTPRequestHandler.protocol_version = "HTTP/1.1"

APPLICATION_JSON = "application/json"

app = Flask(__name__)

@app.route('/api/access-points', methods=['GET'])
def access_points():
    return jsonify(_AP_LIST)

_AP_LIST = [["George Hawkins AC", "788a20498c26"], ["UPC Wi-Free", "3a431d3e4ec7"], ["Salt_2GHz_8A9F85", "44fe3b8a9f87"], ["SiCo's", "d8fb5eac6d50"], ["SiCo's Ospiti", "d8fb5eac6d51"], ["Sonja's iPhone", "f249bec2ec94"], ["JB_40", "488d36d5c83a"], ["jonas-guest", "488d36d5c83b"], ["UPC73A7C75", "ac2205767bb4"], ["UPC Wi-Free", "ae2215767bb4"], ["UPC Wi-Free", "925c14cbe5d9"], ["Salt_2GHz_FC5BC1", "44fe3bfc5bc3"], ["UPC7E68DDA", "905c44cbe5d9"], ["Mattinet2", "e0469a684727"], ["jonas-guest", "a0648f3663b1"], ["gurke", "6466b31646e5"], ["uVoPiC", "5467512dbbf6"]]

@app.route('/api/access-point', methods=['POST'])
def access_point():
    bssid = request.form['bssid']
    password = request.form['password']
    print("Received request to connect to {} with password \"{}\"".format(bssid, password))
    # Use the password to specify the response you want:
    # * If it contains "good" the success response NO_CONTENT is returned.
    # * If it contains "invalid" BAD_REQUEST is returned.
    # * If it consists of 3 digits, a space and some text then they're returned as the status code and description.
    # * Otherwise FORBIDDEN is returned.
    if "good" in password:
        # To return a response with JSON you'd do:
        # return Response(json.dumps(...), status=HTTPStatus.OK, mimetype=APPLICATION_JSON)
        return Response(status=HTTPStatus.NO_CONTENT)
    elif "invalid" in password:
        abort(HTTPStatus.BAD_REQUEST)
    else:
        m = match("([0-9]{3}) (.*)", password)
        if m:
            status = int(m.group(1))
            description = m.group(2)
            abort(status, description)
        else:
            abort(HTTPStatus.FORBIDDEN)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    # Return errors as JSON rather than the Flask default of HTML.
    response.content_type = APPLICATION_JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    return response
