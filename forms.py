from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class UserFriendsList(Form):
    steam64id = StringField("steamID64", validators=[DataRequired(), Length(min=1, max=71)])
    submit = SubmitField('Get Friends List')
