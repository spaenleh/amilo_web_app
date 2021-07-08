import re

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

import utils

RE_CODE = r'^([a-fA-F0-9]{8})$|^([a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4})$'

app = Flask(__name__)
app.config.from_object('config')

# flask boostrap
Bootstrap(app)


class CodeForm(FlaskForm):
    master_code = StringField('Input master code :', validators=[DataRequired()])
    submit = SubmitField('Get password')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CodeForm()
    message = ''
    if form.validate_on_submit():
        code = form.master_code.data
        if re.findall(RE_CODE, code):
            message = utils.get_password(code)
            return render_template('index.html', form=form, message=message)
        else:
            message = 'Invalide code format, refer to info'
    return render_template('index.html', form=form, message=message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
