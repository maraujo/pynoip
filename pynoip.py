from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
from datetime import datetime
from flask_restful import reqparse

db_connect = create_engine('sqlite:///requests.db')
conn = db_connect.connect()
IP_COL = "IP"
TIME_COL = "TIME"
LABEL_COL = "LABEL"
query = conn.execute("CREATE TABLE IF NOT EXISTS requests (ID INTEGER PRIMARY KEY AUTOINCREMENT, " +
                     "IP TEXT," +
                     "TIME TEXT," +
                     "LABEL TEXT)")
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('label', type=str, help='Identification', required=True)

def deleted_all_requests():
    conn = db_connect.connect()
    query = conn.execute("DELETE FROM requests")
    conn.close()

def insert_new_data_in_requests(data):
    conn = db_connect.connect()
    query = conn.execute("INSERT INTO requests (IP, TIME, LABEL) VALUES (?,?,?)", data["ip"], data["now"], data["label"])
    conn.close()

def select_rows_from_request(number=1):
    conn = db_connect.connect()
    query = conn.execute('SELECT * FROM requests ORDER BY ID DESC LIMIT ?', number)
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    conn.close()
    return jsonify(result)

class NoIpRequests(Resource):
    def post(self):
        args = parser.parse_args()
        data = {}
        data["ip"] = request.remote_addr
        data["now"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["label"] = args["label"]
        insert_new_data_in_requests(data)
        return {'message': "Request Saved"}

    def get(self):
        return {"status":"online"}

class NoIpRequestsDeleteAll(Resource):
    def get(self):
        deleted_all_requests()
        return {'message': "All Instances Deleted"}

class NoIpRequestsList(Resource):
    def get(self, number_results):
        result = select_rows_from_request(number_results)
        return result


api.add_resource(NoIpRequests, '/')
api.add_resource(NoIpRequestsList, '/<number_results>')
api.add_resource(NoIpRequestsDeleteAll, '/delete')

if __name__ == '__main__':
    app.run(port=5002)
