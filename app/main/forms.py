from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import User
from flask_babel import lazy_gettext as _l

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Update')

    def __init__(self, current_username, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.current_username = current_username

    def validate_username(self, username):
        if username.data != self.current_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken')

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
