from flask import Flask, request, render_template
from classess.db import DatabaseClient

app = Flask(__name__)


@app.route("/")
def mainRoute():
    db_client = DatabaseClient()

    data = db_client.getAllAppList()
    for result in data:
        print(result['application_url'])
    # applist = get_data.getAllAppList()
    # for result_app_list in applist:
    #     get_result_app_list = result_app_list()
    print(data)
    return render_template("index.html", data=data)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9090, debug=True)