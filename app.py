from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

app.config['CORS_HEADERS'] = 'Content-Type'
from unrival_py import *

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def parse_path(path):
  queue = path.split('/')
  possible_interpretation = ''

  while len(queue):
    head = queue[0]
    would_be_interpretation = possible_interpretation + head
    # is the would be interpretation a real interpretation?
    if is_interpretation(would_be_interpretation):
      pass

  return path

@app.route('/object/<path>/<address>')
def parse_object(path, address):
    # address = address_string.split('/')[-1]
    print(address)
    try:
        object_string = read(address)
        object_parts = parse(object_string)
        return jsonify(object_parts)
    except Exception:
      raise Exception

"""
Create action
"""

@app.route('/object/<path>/create', methods=['PUT', 'OPTIONS'])
@cross_origin()
def create_object(path):
    try:
        object_parts = request.json
        address = create(object_parts, 'ipfs')
        return address
    except Exception:
      raise Exception

"""
Prove action
"""

@app.route('/object/<path>/prove')
@cross_origin()
def prove_object(path):
    address = path.split('/')[-1]
    try:
        prove(address)
        return { 'success' : True }
    except Exception:
      raise Exception

@app.route('/object/context/<address>')
def load_context(address):
    interpretations = {}
    try:
        object_string = read(address)
        return jsonify(object_string)
    except Exception:
        raise Exception

@app.route('/utility/read_object/<address>')
def get_object(address):
    try:
        object_string = read(address)
        return jsonify(object_string)
    except Exception:
        raise Exception



