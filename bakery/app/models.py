class User():

	def __init__(self, id, name, password, active, employee):
		self.id = id
		self.name = name
		self.password = password
		self.active = active
		self.isEmployee = employee

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	@property
	def is_employee(self):
		return self.isEmployee

	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3
