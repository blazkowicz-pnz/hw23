import os
from flask_restx import Api, abort, Resource
from flask import Flask,request


app = Flask(__name__)
api = Api(app)
my_ns = api.namespace("perform_query")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def create_query(it, cmd, value):
    res = map(lambda x: x.strip(), it)
    if cmd == "filter":
        res = filter(lambda x: value in x, res)
    if cmd =="sort":
        value = bool(value)
        res = sorted(res, reverse=value)
    if cmd == "unique":
        res = set(res)
    if cmd == "limit":
        value = int(value)
        res = list(res)[: value]
    if cmd == "map":
        value = int(value)
        res = map(lambda x: x.split(" ")[value], res)
    return res


@my_ns.route("/")
class QueryView(Resource):
    def get(self):
        try:
            cmd_1 = request.args["cmd_1"]
            cmd_2 = request.args["cmd_2"]
            val_1 = request.args["val_1"]
            val_2 = request.args["val_2"]
            file_name = request.args["file_name"]
        except Exception:
            abort(400, message="invalid query")
        path_file = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(path_file):
            abort(400, message="file not found")

        with open(path_file) as f:
            result = create_query(f, cmd_1, val_1)
            result = create_query(result, cmd_2, val_2)
            result = "\n".join(result)

        return app.response_class(result, content_type="text/plain")


if __name__ == "__main__":
    app.run(debug=False)
