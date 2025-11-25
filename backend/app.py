from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import io
import re

# Set path to tesseract if needed (only for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Flask backend is running. POST to /api/check-label', 200

@app.route('/api/check-label', methods=['POST'])
def check_label():
    # Get form data
    brand = request.form.get('brand', '')
    product_type = request.form.get('type', '')
    abv_input = request.form.get('abv', '')
    volume_input = request.form.get('volume', '')

    # Get uploaded image
    image = request.files.get('label')
    if not image:
        return jsonify({'success': False, 'details': [{
            'field': 'image', 'message': 'No image uploaded', 'match': False
        }]}), 400

    try:
        img = Image.open(io.BytesIO(image.read()))
        ocr_text = pytesseract.image_to_string(img)
    except Exception as e:
        return jsonify({'success': False, 'details': [{
            'field': 'image', 'message': f'OCR error: {str(e)}', 'match': False
        }]}), 500

    ocr_text_lower = ocr_text.lower()
    results = []

    # 1. Brand Name (case-sensitive exact match)
    brand_match = brand in ocr_text
    results.append({
        'field': 'Brand Name',
        'message': f"{'✅' if brand_match else '❌'} " +
                   (f"Exact Brand Name found: '{brand}'" if brand_match else f"Brand name '{brand}' not found (case-sensitive)"),
        'match': brand_match
    })

    # 2. Product Type (fuzzy contains)
    type_match = product_type.lower() in ocr_text_lower
    results.append({
        'field': 'Product Type',
        'message': f"{'✅' if type_match else '❌'} " +
                   (f"Product Type found: '{product_type}'" if type_match else f"Product type '{product_type}' not found"),
        'match': type_match
    })

    # 3. Alcohol Content
    abv_numeric = re.sub(r'[^\d.]', '', abv_input.strip())
    abv_pattern = rf'\b{abv_numeric}\s*%?(?:\s*(?:abv|alc|alc\.?/vol\.?|alcohol by volume))?\b'
    abv_match = re.search(abv_pattern, ocr_text_lower)
    results.append({
        'field': 'Alcohol Content',
        'message': f"{'✅' if abv_match else '❌'} " +
                   (f"Alcohol Content found: '{abv_numeric}%'" if abv_match else f"Alcohol content '{abv_input}' not found"),
        'match': bool(abv_match)
    })

    # 4. Volume (optional)
    if volume_input:
        volume_pattern = re.escape(volume_input.lower()).replace('ml', r'\s?ml').replace('oz', r'\s?oz')
        volume_match = re.search(volume_pattern, ocr_text_lower)
        results.append({
            'field': 'Volume',
            'message': f"{'✅' if volume_match else '❌'} " +
                       (f"Volume found: '{volume_input}'" if volume_match else f"Volume '{volume_input}' not found"),
            'match': bool(volume_match)
        })

    # 5. Government Warning
    gov_warn_match = 'government warning' in ocr_text_lower
    results.append({
        'field': 'Government Warning',
        'message': f"{'✅' if gov_warn_match else '❌'} " +
                   ('Found "GOVERNMENT WARNING"' if gov_warn_match else '"GOVERNMENT WARNING" not found'),
        'match': gov_warn_match
    })

    success = all(r['match'] for r in results)

    return jsonify({'success': success, 'details': results})

if __name__ == '__main__':
    print("Flask backend running at http://localhost:5000")
    app.run(debug=True)