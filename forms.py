from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class URLForm(FlaskForm):
    url = StringField(label='Original URL', validators=[DataRequired()])
    submit = SubmitField(label='Submit')