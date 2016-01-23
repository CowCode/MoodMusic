from wtforms import Form, TextAreaField

class MoodForm(Form):
    entry = TextAreaField("Describe your day...")