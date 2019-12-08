from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from application import gtfs_feed

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['zip'])


def allowed_file(filename):
    return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/import', methods=['POST'])
def insert():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        gtfs_feed.parse(file)
        resp = jsonify({'message': 'File successfully uploaded' + filename})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file type is zip'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
