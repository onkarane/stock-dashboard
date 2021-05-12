from flask import Flask, request, jsonify
from pred import Predictions
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

def predict():
    print('Executing')
    Predictions.main()

@app.route('/')
def reply():
    msg = request.args.get('message')
    threading.Thread(target=predict).start()
    
    return jsonify(msg)

if __name__ == '__main__':
    app.run(debug=True)
