from flask import Flask, render_template, request, jsonify
from flask_mongoengine import MongoEngine
from mongoengine import *
import json

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db = MongoEngine(app)

class Record(db.DynamicDocument):
   pass

# listing records
@app.route('/records')
@app.route('/records/json')
def index():
        record_key_list = []

        records = Record.objects.map_reduce('function() { for (var key in this) { emit(key, null); } }','function(key, stuff) { return null; }', 'inline')
        for record in records:
            record_key_list.append(record.key)
        record_key_list = [key for key in record_key_list if key not in ('_id')]

        record = Record.objects.all()
        record_value_list = json.loads(record.to_json())

        if request.path == '/records/json':
               return jsonify(record)
        return render_template('index1.html', records = record_key_list, records_value = record_value_list)
    
# Show one record
@app.route('/records/<_id>')
def show(_id):
    record = Record.objects(pk=_id)
    return jsonify(record)

# Create new record
@app.route('/records', methods=['POST'])
def create():
  record = Record(**request.json).save()
  return jsonify(record)
    
# Update record
@app.route('/records/<_id>', methods=['PUT'])
def update(_id):
    record = Record.objects(pk=_id)
    if record:
        record.update(**request.json)
        return jsonify(record)
    else:
        return jsonify({'response': 'user is not present'})

# Delete record
@app.route('/records/<_id>', methods=['DELETE'])
def destory(_id):
    record = Record.objects(pk=_id)
    if record:
        record.delete()
        return jsonify({'response': 'Success'})
    else:
        return jsonify({'response': 'Failed'})

if __name__ == "__main__":
    app.run()
