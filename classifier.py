from flask import Flask, request, jsonify
import os
from feature_extraction import feature_extraction  # Your custom function
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the upload folder path
UPLOAD_FOLDER = 'uploads'

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load your trained model (ensure the model is saved using pickle)
with open('malware_detection_model.pkl', 'rb') as model_file:
    clf = pickle.load(model_file)

# Define allowed file types for security
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['pdf']

    if file and allowed_file(file.filename):
        try:
            # Securely handle the file name and save the file
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Perform feature extraction
            features = feature_extraction(file_path)
            features = [features]  # Reshape for prediction

            # Predict using your trained model
            result = clf.predict(features)

            # Clean up the file after processing
            os.remove(file_path)

            return jsonify({'result': int(result[0])})

        except Exception as e:
            return jsonify({'error': f"An error occurred: {str(e)}"})

    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)
