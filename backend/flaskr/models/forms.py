from wtforms import (
    Form,
    StringField,
    SubmitField,
    PasswordField,
    validators,
    HiddenField,
    DateField
)
from flaskr.models.user import User

class CreateForm(Form):
    name = StringField('名前',
                       [validators.Length(min=4, max=35)],
                       render_kw={"placeholder": "山田 太郎"}
                       )
    email = StringField('メールアドレス',
                        [validators.Length(min=6, max=35)],
                        render_kw={"placeholder": "sample@example.com"}
                        )
    submit = SubmitField('サインアップ')

    def validate_email(self, field):
        if User.find_by_email(field.data):
            raise validators.ValidationError('このメールアドレスは既に登録されています')

class ResetPasswordForm(Form):
    password = PasswordField('パスワード',[
                        validators.DataRequired(),
                        validators.EqualTo('password_confirm',
                                           message='パスワードが一致しません')
                        ])
    password_confirm = PasswordField('パスワードの確認', [validators.DataRequired()])
    submit = SubmitField('パスワードの設定')

class LoginForm(Form):
    email = StringField('メールアドレス', [validators.Length(min=6, max=35)])
    password = PasswordField('パスワード', [validators.DataRequired()])
    submit = SubmitField('ログイン')

class UpdateForm(Form):
    id = HiddenField()
    name = StringField('名前', [validators.Length(min=4, max=35)])
    email = StringField('メールアドレス', [validators.Length(min=6, max=35)])
    birthday = DateField('生年月日')
    submit = SubmitField('更新')
