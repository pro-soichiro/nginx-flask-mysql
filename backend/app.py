from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
from wtforms import Form, StringField, SubmitField, PasswordField, validators
import mysql.connector

import pykakasi
import os

app = Flask(__name__)
conn = None

app.config['SECRET_KEY'] = b'\xd3\x8e\xf4<8\xdc\xb3\x8fHb\xd7\x1a\xb1\x98\x16\xbe'

class DBManager:
    def __init__(self, database='example', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user,
            password=pf.read(),
            host=host, # name of the mysql service as set in the docker compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()

    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,5)])
        self.connection.commit()

    def query_titles(self):
        self.cursor.execute('SELECT title FROM blog')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec


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

class User:
  def __init__(self, id, name, age, icon, is_logged_in):
    self.id = id
    self.name = name
    self.age = age
    self.icon = icon
    self.is_logged_in = is_logged_in

  def is_adult(self):
    return self.age >= 20

  def __str__(self):
    return '<User id:{}, name:{}, email:{}, password:{}, password_confirm:{}, age:{}, icon:{}, is_logged_in:{}>'.format(
      self.id,
      self.name,
      self.email,
      self.password,
      self.password_confirm,
      self.age,
      self.icon,
      self.is_logged_in
    )

  @staticmethod
  def all():
    return [
      User(1, '太郎', 20, 'icon1.png', True),
      User(2, '次郎', 25, 'icon2.png', False),
      User(3, '花子', 30, 'icon3.png', True),
      User(4, '一郎', 35, 'icon4.png', False),
      User(5, '幸子', 40, 'icon5.png', True)
    ]

  @staticmethod
  def find(id):
    for user in User.all():
      if user.id == id:
        return user
    return None



@app.template_filter('birth_year')
def birth_year(age):
  current_year = datetime.now().year
  return current_year - age

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/blogs')
def listBlog():
  global conn
  if not conn:
    conn = DBManager(password_file='/run/secrets/db-password')
    conn.populate_db()
  blogs = conn.query_titles()

  return render_template('blogs.html', blogs=blogs)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = UserForm(request.form)
  if request.method == 'GET':
    return render_template('signup.html', form=form)
  elif request.method == 'POST':
    if form.validate():
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