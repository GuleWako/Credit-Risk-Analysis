from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Load the trained model
rf_cs = joblib.load('credit_scoring_random_forest_model.pkl')
rf_model = rf_cs
gb_cs = joblib.load('credit_scoring_gradientBoosting_model.pkl')
gb_model = gb_cs
@app.route('/')
def home():
    return """
Welcome to the Credit score API. Use the https://credit-score-model.onrender.com/predict/random_forest
endpoint to send request and get prediction for random forest and 
https://credit-score-model.onrender.com/predict/gradient_boosting endpoint for gradient boosting."""

@app.route('/predict/random_forest', methods=['POST'])
def predict_using_rf():
    data = request.get_json()
    features = list(data.values())
    features_array = np.array([features])
    prediction = rf_model.predict(features_array)
    return jsonify({'prediction': int(prediction[0])})
@app.route('/predict/gradient_boosting', methods=['POST'])
def predict_using_gradient():
    data = request.get_json()
    features = list(data.values())
    features_array = np.array([features])
    prediction = gb_model.predict(features_array)
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
