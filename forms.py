# --Citation for 13-digit ISBN Regex:
# Date: 05/20/2022
# Copied From: O'Reilly Regular Expressions Cookbook
# Source URL: https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s13.html -->

#  Citation for HTML dropdown menu:
# Date: 05/17/2022
# Based on: Free Code Camp HTML Select Tag tutorial
# Source URL: https://www.freecodecamp.org/news/html-select-tag-how-to-make-a-dropdown-menu-or-combo-list/

#  Citation for Year Regex:
# Date: 05/20/2022
# Copied from: Regex Pattern Year
# Source URL: https://regexpattern.com/year/


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Regexp


class AuthorsFilter(FlaskForm):
    author_dropdown = SelectField(
        "Filter by Author", coerce=int, validators=[InputRequired()]
    )
    submit = SubmitField()


class AddBook(FlaskForm):
    isbn = StringField(
        "13-Digit ISBN",
        validators=[
            InputRequired(),
            Regexp(
                "^97[89][-]?[0-9]{1,5}[-][0-9]+[-]?[0-9]+[-]?[0-9]$",
                message="Must be a valid ISBN",
            ),
        ],
    )
    title = StringField("Book Title", validators=[InputRequired()])
    author_dropdown = SelectField("Author", coerce=int, validators=[InputRequired()])
    publisher_dropdown = SelectField(
        "Publisher", coerce=int, validators=[InputRequired()]
    )
    year = StringField(
        "Year Published",
        validators=[
            InputRequired(),
            Regexp("^[12][0-9]{3}$", message="Must be valid year."),
        ],
    )
    submit = SubmitField()
