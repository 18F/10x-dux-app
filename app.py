from flask import jsonify, make_response, request, Flask
import json
import os
import urllib3

app = Flask(__name__)


@app.route('/stats', methods=["GET", "POST", "PUT"])
def stats():
    try:
        pool_manager = urllib3.PoolManager()
        method = request.method.upper() if request.method else 'GET'
        host = request.args.get('host', default = "10x.gsa.gov", type = str)
        url = f"https://{host}:443"
        info = pool_manager.request(method, url).info()
        return make_response(jsonify(data=dict(info)))
    except Exception as err:
        return make_response(jsonify(error=str(err)), 400)


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
