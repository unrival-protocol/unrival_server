from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from unrival_py import *
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

@app.route('/context/<address>')
def load_context(address):
  """
  Map context parts associating interpretation addresses with values
  to parts associating addresses with strings
  """
  return resolve_context(address)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def parse_path(path, context):
  """
  Determine whether a valid interpretation has been entered in a url,
  or if a valid object address has been entered,
  and return the object address if so.

  Args:
    path (str): part of a url representing a possible interpretation and/or object address
    context (str): address of context in which interpretation is meaningful
  Returns:
    str: interpretation
  """

  value = interpret_object(context, None, [path])
  print(value)
  if value:
    return value
  return None

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



