from wtforms import (
    Form,
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    HiddenField,
    DateField,
    FileField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError
)
from flaskr.models.user import User
from flaskr.models.user_connect import UserConnect
from flask_login import current_user

class CreateForm(Form):
    name = StringField('名前',
                       [Length(min=4, max=35)],
                       render_kw={"placeholder": "山田 太郎"})
    email = StringField('メールアドレス', [Email()],
                        render_kw={"placeholder": "sample@example.com"})
    submit = SubmitField('サインアップ')

    def validate_email(self, field):
        if User.find_by_email(field.data):
            raise ValidationError('このメールアドレスは既に登録されています')

class ResetPasswordForm(Form):
    password = PasswordField('パスワード',[
                        DataRequired(),
                        EqualTo('password_confirm',
                                           message='パスワードが一致しません')
                        ])
    password_confirm = PasswordField('パスワードの確認', [DataRequired()])
    submit = SubmitField('パスワードの設定')

class ForgotPasswordForm(Form):
    email = StringField('メールアドレス', [
        Length(min=6, max=35),
        DataRequired(),
        Email()
    ])
    submit = SubmitField('パスワードをリセットする')

    def validate_email(self, field):
        if not User.find_by_email(field.data):
            raise ValidationError('このメールアドレスは登録されていません')

class ChangePasswordForm(Form):
    current_password = PasswordField('現在のパスワード', [DataRequired()])
    new_password = PasswordField('新しいパスワード', [
        DataRequired(),
        EqualTo('new_password_confirm',
                           message='パスワードが一致しません')
    ])
    new_password_confirm = PasswordField('新しいパスワードの確認', [DataRequired()])
    submit = SubmitField('パスワードの変更')

    def validate_current_password(self, field):
        user = User.find(current_user.id)
        if not user.validate_password(field.data):
            raise ValidationError('現在のパスワードが間違っています')

class LoginForm(Form):
    email = StringField('メールアドレス', [
        Email(),
        DataRequired()
    ])
    password = PasswordField('パスワード', [DataRequired()])
    submit = SubmitField('ログイン')

class UpdateForm(Form):
    name = StringField('名前', [Length(min=4, max=35)])
    email = StringField('メールアドレス', [Email(), DataRequired()])
    icon = FileField('アイコン')
    birthday = DateField('生年月日')
    submit = SubmitField('更新')

class BlogForm(Form):
    title = StringField('タイトル', [Length(min=1, max=100)])
    body = TextAreaField('内容', [Length(min=1, max=1000)])
    submit = SubmitField('投稿')

class UserSearchForm(Form):
    name = StringField('名前', [DataRequired()])
    submit = SubmitField('検索')

class ConnectForm(Form):
    connect_condition = HiddenField()
    to_user_id = HiddenField()
    submit = SubmitField()

class MessageForm(Form):
    to_user_id = HiddenField()
    room = HiddenField()
    message = TextAreaField('メッセージ', [Length(min=1, max=1000)])
    submit = SubmitField('送信')

    def validate(self):
        if not super(Form, self).validate():
            return False
        if not UserConnect.is_friend(self.to_user_id.data, current_user.id):
            return False
        return True