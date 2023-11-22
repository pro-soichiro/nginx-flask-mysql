from wtforms import Form, StringField, SubmitField, PasswordField, validators

class UserForm(Form):
    name = StringField('名前',[validators.Length(min=4, max=35)], render_kw={"placeholder": "山田 太郎"})
    email = StringField('メールアドレス',[validators.Length(min=6, max=35)], render_kw={"placeholder": "sample@example.com"})
    password = PasswordField('パスワード',[
          validators.DataRequired(),
          validators.EqualTo('password_confirm', message='Passwords must match')
      ])
    password_confirm = PasswordField('パスワードの確認')
    submit = SubmitField('サインアップ')