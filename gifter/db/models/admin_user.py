from pony.orm import *
import gifter.db

class AdminUser(gifter.db.Entity):
	id = PrimaryKey(int, auto=True)
	username = Required(str, unique=True)
	actions  = Set('ActionLog')


	def __str__(self):
		return self.username

	def log_login(self):
		self.actions.create(action_type=int(ActionLog.Type.LOGIN), description="logged in")

	###
	### STATIC METHODS
	###


	@staticmethod
	def find_or_create_by_username(username):
		user = AdminUser.get(username = username)
		if user is None:
			user = AdminUser(username = username)
		return user



from gifter.db.models.action_log import ActionLog




	
