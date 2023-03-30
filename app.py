from flask import Flask, request, jsonify
from flask_cors import CORS
import model

app = Flask(__name__)
CORS(app)

######################################################
@app.route('/')
def index():
    a = model.general('jolin2', 40, 5)
    return a

@app.route('/predict', methods=['POST'])
def postInput():
    # 取得前端傳過來的數值
    req = request.get_json()
    print(req)
    result = model.general(req['name'], int(req['length']), int(req['seeding']))
    return jsonify({'return': str(result)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4004, debug=True)