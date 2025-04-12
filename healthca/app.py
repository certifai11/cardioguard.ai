from flask import Flask, render_template, request, jsonify
import pickle
import json
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

# Load the trained model
model_path = os.path.join('model', 'model.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Load feature information
feature_info_path = os.path.join('model', 'feature_info.json')
with open(feature_info_path, 'r') as file:
    feature_info = json.load(file)

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')
@app.route('/assessment')
def assessment():
    """Render the assessment page."""
    return render_template('assessment.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for risk prediction."""
    try:
        # Get form data
        data = request.json
        
        # Extract features in the correct order
        features = [
            float(data.get('age')),
            float(data.get('sex')),
            float(data.get('cp')),
            float(data.get('trestbps')),
            float(data.get('chol')),
            float(data.get('fbs')),
            float(data.get('restecg')),
            float(data.get('thalach')),
            float(data.get('exang')),
            float(data.get('oldpeak')),
            float(data.get('slope')),
            float(data.get('ca')),
            float(data.get('thal'))
        ]
        
        # Convert to numpy array and reshape for prediction
        features_array = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction_proba = model.predict_proba(features_array)[0][1]
        threshold = float(request.args.get('threshold', 0.5))
        
        # Determine risk level based on probability
        if prediction_proba >= 0.7:
            risk_level = "high"
            risk_percentage = round(prediction_proba * 100)
            message = "High Risk of Heart Disease"
        elif prediction_proba >= threshold:
            risk_level = "moderate"
            risk_percentage = round(prediction_proba * 100)
            message = "Moderate Risk of Heart Disease"
        else:
            risk_level = "low"
            risk_percentage = round(prediction_proba * 100)
            message = "Low Risk of Heart Disease"
        
        # Determine key risk factors (simplified version)
        risk_factors = []
        
        if float(data.get('age')) > 60:
            risk_factors.append("Advanced age (>60 years)")
        
        if float(data.get('chol')) > 240:
            risk_factors.append("High cholesterol (>240 mg/dl)")
        
        if float(data.get('trestbps')) > 140:
            risk_factors.append("High blood pressure (>140 mm Hg)")
        
        if float(data.get('thalach')) < 150:
            risk_factors.append("Low maximum heart rate (<150 bpm)")
        
        if float(data.get('oldpeak')) > 2:
            risk_factors.append("Significant ST depression (>2)")
        
        if float(data.get('ca')) >= 2:
            risk_factors.append("Multiple vessels colored by fluoroscopy")
        
        # If no specific factors were identified, add a general note
        if not risk_factors and risk_level != "low":
            risk_factors.append("Multiple factors contributing to overall risk")
        elif risk_level == "low" and not risk_factors:
            risk_factors.append("No significant risk factors identified")
        
        # Create response
        response = {
            'success': True,
            'risk_level': risk_level,
            'risk_percentage': risk_percentage,
            'message': message,
            'risk_factors': risk_factors,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/feature-info', methods=['GET'])
def get_feature_info():
    """API endpoint to get feature information."""
    return jsonify(feature_info)

@app.route('/api/stats', methods=['POST'])
def update_stats():
    """API endpoint to update dashboard statistics."""
    try:
        data = request.json
        assessment_count = data.get('assessment_count', 0)
        high_risk_count = data.get('high_risk_count', 0)
        moderate_risk_count = data.get('moderate_risk_count', 0)
        low_risk_count = data.get('low_risk_count', 0)
        
        # In a real application, you would store these in a database
        # For this example, we'll just return the values back
        
        return jsonify({
            'success': True,
            'assessment_count': assessment_count,
            'high_risk_count': high_risk_count,
            'moderate_risk_count': moderate_risk_count,
            'low_risk_count': low_risk_count
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)