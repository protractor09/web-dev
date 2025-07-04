from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import io
from PIL import Image

app = Flask(__name__)

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_faces():
    try:
        # Get image data from request
        image_data = request.json['image']
        
        # Remove data URL prefix
        image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Convert faces to list for JSON response
        faces_list = []
        for (x, y, w, h) in faces:
            faces_list.append({
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h)
            })
        
        return jsonify({
            'success': True,
            'faces': faces_list,
            'count': len(faces_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)