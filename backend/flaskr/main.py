from flask import render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename

import pykakasi
import os

bp = Blueprint('main', __name__)

class Kakash:
    kks = pykakasi.kakasi()
    kks.setMode('H', 'a')
    kks.setMode('K', 'a')
    kks.setMode('J', 'a')
    conv = kks.getConverter()

    @classmethod
    def japanese_to_ascii(cls, text):
      return cls.conv.do(text)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file = request.files['file']
        ascii_filename = Kakash.japanese_to_ascii(file.filename)
        filename = secure_filename(ascii_filename)
        file.save(os.path.join('./static/images', filename))
        return redirect(url_for('uploaded_file', filename=filename))

@bp.route('/uploads/<string:filename>')
def uploaded_file(filename):
    return render_template('uploaded_file.html', filename=filename)

@bp.route('/terms')
def terms():
    return render_template('terms.html')

@bp.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html'), 500

@bp.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404
