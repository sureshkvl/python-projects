from flask import Flask, request
from flask import jsonify
import sys
import uuid
import json
import jsonschema
from jsonschema import validate

# Key Value Store / In Memory DB
in_memory_db = {}


def create_kv(key, value):
    global in_memory_db
    in_memory_db[key] = value
    return in_memory_db[key]

def update_kv(key, value):
    global in_memory_db
    if in_memory_db.has_key(key):
        in_memory_db[key] = value
        return in_memory_db[key]
    else:
        return {"error": "key not found"}


def get_kv(key):
    global in_memory_db
    if in_memory_db.has_key(key):
        return in_memory_db[key]
    else:
        return {"error": "key not found"}


def list_kv():
    return in_memory_db


# UUID Generation
def generate_uuid():
    return uuid.uuid4()

# 
stud_id = 0
def generate_id():
    global stud_id
    stud_id += 1
    return stud_id


student_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#", 
    "definitions": {}, 
    "id": "http://example.com/example.json", 
    "properties": {
      "age": {
        "default": 17, 
        "description": "An explanation about the purpose of this instance.", 
        "id": "/properties/age", 
       "title": "The age schema", 
       "type": "integer"
     }, 
     "course": {
       "default": "Computer Science", 
       "description": "An explanation about the purpose of this instance.", 
       "id": "/properties/course", 
       "title": "The course schema", 
       "type": "string"
     }, 
     "dept": {
       "default": "Computer", 
       "description": "An explanation about the purpose of this instance.", 
       "id": "/properties/dept", 
       "title": "The dept schema", 
       "type": "string"
     }, 
     "name": {
       "default": "Anitha Das", 
       "description": "An explanation about the purpose of this instance.", 
       "id": "/properties/name", 
       "title": "The name schema", 
       "type": "string"
     }
   }, 
   "type": "object"
 }



# Rest Server
app = Flask(__name__)


@app.route('/students', methods=['POST'])
def addstudents():
    if request.method == 'POST':
        content = request.get_json()
        #print json.dumps(content)
        try:
            validate(content, student_schema)
        except jsonschema.ValidationError as e:
            return e.message
        except jsonschema.SchemaError as e:
            return e
        content["id"] = generate_id()
        return jsonify(create_kv(content["id"], content))

@app.route('/students', methods=['GET'])
def getstudents():
    if request.method == 'GET':
        return jsonify(list_kv())

@app.route('/students/<int:id>', methods=['GET'])
def getstudent(id):
    if request.method == 'GET':
        return jsonify(get_kv(id))


@app.route('/students/<int:id>', methods=['PUT'])
def putstudent(id):
    if request.method == 'PUT':
        content = request.get_json()
        return jsonify(update_kv(id, content))


def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    main()
