from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, RadioField


class SampleForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    id = IntegerField("ID")
    date = DateField("Date", format='%m/%d/%Y')
    radio = RadioField("Name", choices=[('code1', 'Name1'),
                                         ('code2', 'Name2')
                                         ])

    campus = SelectField("Name/Type", choices=[('code1', "Name1"),
                                            ('code2', 'Name2'),
                                            ('code3', 'Name3')
                                            ])