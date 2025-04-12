from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from pdf2image import convert_from_path

app = Flask(__name__)

# 업로드 및 변환 이미지 저장 경로
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# 폴더 없으면 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 파일 확장자 확인
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf_to_images():
    if 'pdfFile' not in request.files:
        return jsonify({'error': '파일이 없습니다.'}), 400

    file = request.files['pdfFile']

    if file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # 기존 변환 이미지 제거
        for f in os.listdir(OUTPUT_FOLDER):
            os.remove(os.path.join(OUTPUT_FOLDER, f))

        # PDF → 이미지 변환
        try:
            images = convert_from_path(filepath, dpi=200)
            image_urls = []

            for i, image in enumerate(images):
                output_filename = f'page_{i + 1}.jpg'
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                image.save(output_path, 'JPEG')
                image_urls.append(f'/static/output/{output_filename}')

            return jsonify({'images': image_urls})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'PDF 파일만 업로드 가능합니다.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
