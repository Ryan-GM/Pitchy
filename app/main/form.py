from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class PitchyForm(FlaskForm):
    title = StringField('Title',validators=[Required()])
    post = TextAreaField('Pitch it', validators=[Required()])
    category = SelectField('Category',choices=[('Cheesy','Cheesy'),('Life','Life','Funny','Funny')],validators=[Required()])
    submit = SubmitField('Pitchy')

class CommentForm(FlaskForm):
    comment = TextAreaField('Do leave a comment',validators=[Required()])
    submit = SubmitField('Comment')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('A brief one about you',validators=[Required()])
    submit = SubmitField('Save')