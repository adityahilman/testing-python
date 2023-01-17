from flask import Flask
import json

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def getHome():
	response = {
		"Status": "OK"
	}
	return json.dumps(response)

@app.route("/2s", methods = ['GET'])
def getlocal2():
	response = {
		"Status": "OK"
	}
	return json.dumps(response)

@app.route("/3", methods = ['GET'])
def getlocal3():
	response = {
		"Status": "OK"
	}
	return json.dumps(response)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)