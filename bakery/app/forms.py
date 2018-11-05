from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField, TextAreaField, FileField, validators
from wtforms.validators import DataRequired, InputRequired

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class SearchForm(Form):
	searchField = StringField("search")
	category = SelectField('category')
	price = SelectField('price', choices=[("", ""), ("5", "$5"), ("10", "$10"), ("15", "$15"), ("20", "$20"), ("30", "$30"), ("50", "$50")])

class ProductUpdateForm(Form):

	pName = StringField("pName", validators=[InputRequired()])
	price = StringField("price", validators=[DataRequired()])
	title = StringField("title", validators=[DataRequired()])
	text = TextAreaField("text", validators=[DataRequired()])
	productID = StringField("productID", validators=[DataRequired()])
	imageFile = FileField("imageFile")

class QueryForm(Form):
	query = TextAreaField("queryString")

class BulkForm(Form):
	bulk = TextAreaField("BulkString")
