from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
import base64
import io
import os
from datetime import datetime

app = Flask(__name__)
client = OpenAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        prompt = request.json.get('prompt', '')
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            moderation="low"
        )
        
        image_base64 = result.data[0].b64_json
        
        return jsonify({
            'success': True,
            'image_data': image_base64
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_image():
    try:
        image_data = request.json.get('image_data', '')
        filename = request.json.get('filename', '')
        
        if not image_data or not filename:
            return jsonify({'error': 'Image data and filename are required'}), 400
        
        image_bytes = base64.b64decode(image_data)
        filepath = os.path.join('/home/benau/ImageAPI2/generated_image', filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        return jsonify({'success': True, 'message': f'Image saved as {filename}'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)