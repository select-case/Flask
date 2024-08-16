from flask import Flask, request, jsonify
import pandas as pd



app = Flask(__name__)

stored_data = {}
summary_data = {}

# Define the API key
API_KEY = 'abcd'

# Helper function to validate API key
def require_api_key():
    api_key = request.headers.get('api_key')
    print(api_key)
    if api_key != API_KEY:
        return False
    return True

@app.route('/upload', methods=['POST'])
def upload():
    print(request.files)
    if not require_api_key():
        return jsonify({'error': 'Invalid API Key'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file.filename.split('.')[-1] != 'csv':
        return jsonify({'error': 'Invalid file type'}), 400
    
    df = pd.read_csv(file)
    idx = len(stored_data)

    stored_data[idx] = df
    summary_data[idx] = df.describe().to_dict()

    return jsonify({'message': 'File uploaded successfully', 'index': idx}), 200

@app.route('/summary/<int:idx>', methods=['GET'])
def summary(idx):
    if not require_api_key():
        return jsonify({'error': 'Invalid API Key'}), 401

    if idx not in summary_data:
        return jsonify({'error': 'Invalid index'}), 400

    return jsonify(summary_data[idx]), 200

@app.route('/query/<int:idx>', methods=['GET'])
def query(idx):
    if not require_api_key():
        return jsonify({'error': 'Invalid API Key'}), 401

    if idx not in stored_data:
        return jsonify({'error': 'Invalid index'}), 400

    query1 = request.args.get('column')
    query2 = request.args.get('value')

    if query1 is None:
        return jsonify({'error': 'Query column is required'}), 400
    
    if query2 is None:
        return jsonify({'error': 'Query value is required'}), 400

    df = stored_data[idx]

    if query1 not in df.columns:
        return jsonify({'error': 'Invalid query column'}), 400
    
    column_type = df[query1].dtype
    try:
        if column_type == 'int64':
            query2 = int(query2)
        elif column_type == 'float64':
            query2 = float(query2)
        elif column_type == 'object':
            query2 = str(query2)
        else:
            return jsonify({"error": "Unsupported column type"}), 400
        
        result = df[df[query1] == query2]
        return result.to_json(), 200
        
    except:
        return jsonify({"error": "Invalid query value"}), 400

if __name__ == '__main__': 
    app.run(debug=True)
