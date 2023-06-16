from flask import Flask, request, jsonify
from flask_cors import CORS
import models.model as model
import models.ngram as ngram

app = Flask(__name__)
CORS(app)

######################################################
@app.route('/')
def index():
    return "Test."

@app.route('/predict', methods=['POST'])
def postInput():
    req = request.get_json()
    result = ngram.predict(req['name'], int(req['length']),int(req['gram']), req['textSeed'], int(req['seeding']))
    return jsonify({'return': str(result)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4004, debug=True)