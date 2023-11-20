from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
from wtforms import Form, StringField, SubmitField, PasswordField, validators
from models.blog import Blog
from models.user import User
from database import db
from flask_migrate import Migrate

import pykakasi
import os

app = Flask(__name__)
conn = None

app.config['SECRET_KEY'] = b'\xd3\x8e\xf4<8\xdc\xb3\x8fHb\xd7\x1a\xb1\x98\x16\xbe'
app.config.from_object('config.Config')
migrate = Migrate(app, db)
db.init_app(app)

class UserForm(Form):
  name = StringField('名前',[validators.Length(min=4, max=35)], render_kw={"placeholder": "山田 太郎"})
  email = StringField('メールアドレス',[validators.Length(min=6, max=35)], render_kw={"placeholder": "sample@example.com"})
  password = PasswordField('パスワード',[
        validators.DataRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
  password_confirm = PasswordField('パスワードの確認')
  submit = SubmitField('サインアップ')

class Kakash:
  kks = pykakasi.kakasi()
  kks.setMode('H', 'a')
  kks.setMode('K', 'a')
  kks.setMode('J', 'a')
  conv = kks.getConverter()

  @classmethod
  def japanese_to_ascii(cls, text):
    return cls.conv.do(text)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/blogs', methods=['GET'])
def index_blog():
  blogs = Blog.all()
  return render_template('blogs.html', blogs=blogs)

@app.route('/blogs/new')
def new_blog():
  return render_template('new_blog.html')

@app.route('/blogs', methods=['POST'])
def create_blog():
  title = request.form['title']
  body = request.form['body']
  user_id = request.form['user_id']
  blog = Blog(title=title, body=body, user_id=user_id)
  blog.save()
  return redirect(url_for('show_blog', id=blog.id))

@app.route('/blogs/<int:id>', methods=['GET'])
def show_blog(id):
  blog = Blog.find(id)
  return render_template('blog.html', blog=blog)

@app.route('/blogs/<int:id>/edit')
def edit_blog(id):
  blog = Blog.find(id)
  return render_template('edit_blog.html', blog=blog)

@app.route('/blogs/<int:id>', methods=['PATCH'])
def update_blog(id):
  blog = Blog.find(id)
  title = request.json['title']
  body = request.json['body']
  blog.update(title, body)
  return jsonify({ 'status': 'success' })

@app.route('/blogs/<int:id>', methods=['DELETE'])
def delete_blog(id):
  blog = Blog.find(id)
  blog.delete()
  return jsonify({ 'status': 'success' })

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = UserForm(request.form)
  if request.method == 'GET':
    return render_template('signup.html', form=form)
  elif request.method == 'POST':
    if form.validate():
      user = User(name=form.name.data,
                  email=form.email.data,
                  password=form.password.data,
                  password_confirm=form.password_confirm.data)
      user.save()
      return redirect(url_for('thanks'))
    else:
      return render_template('signup.html', form=form)

@app.route('/signup/thanks')
def thanks():
  return render_template('thanks.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'GET':
    return render_template('upload.html')
  elif request.method == 'POST':
    file = request.files['file']
    ascii_filename = Kakash.japanese_to_ascii(file.filename)
    filename = secure_filename(ascii_filename)
    file.save(os.path.join('./static/images', filename))
    return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<string:filename>')
def uploaded_file(filename):
  return render_template('uploaded_file.html', filename=filename)

@app.route('/users')
def users():
  users = User.all()
  return render_template('users.html', users=users)

@app.route('/users/<int:id>')
def user(id):
  user = User.find(id)
  if user is None:
    return render_template('not_found.html'), 404
  return render_template('user.html', user=user)

@app.route('/terms')
def terms():
  return render_template('terms.html')

@app.errorhandler(500)
def internal_server_error(error):
  return render_template('internal_server_error.html'), 500

@app.errorhandler(404)
def not_found(error):
  return render_template('not_found.html'), 404

app.run(port=3000, debug=True)