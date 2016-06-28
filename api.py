from flask import Flask, jsonify
from flask import request
from sqldata import get_data
app = Flask(__name__)


@app.route('/projects/<city>', methods=['GET'])
def get_tasks(city):
	return jsonify(get_data(city))

@app.route('/projects/<city>', methods=['PUT'])
	return jsonify(set_data(name,roofpikID))
if __name__ == "__main__":
	app.run(debug = True, host='192.168.2.53')