import enum
from datetime import datetime
from pony.orm import *
import gifter.db


# the action log is an append only log of all actions taken for transparency. 

class ActionLog(gifter.db.Entity):

	class Type(enum.IntEnum):

		CREATE_USER  = 0
		UPDATE_USER  = 1
		BUY_SHARE    = 2
		ADJUST_SHARE = 3
		LOGIN        = 4


	id = PrimaryKey(int, auto=True)
	description = Required(str)
	action_type = Required(int)
	note        = Optional(str)
	admin       = Required("AdminUser")
	user        = Optional("PublicUser")
	amount      = Optional(int)
	payment     = Optional("Payment")
	created_at  = Required(datetime, default=datetime.utcnow)


	@staticmethod
	@db_session
	def last_100_actions():
		return select(a for a in ActionLog).order_by(desc(ActionLog.created_at)).limit(100)



from gifter.db.models.admin_user import *
from gifter.db.models.public_user import *
from gifter.db.models.payment import *

