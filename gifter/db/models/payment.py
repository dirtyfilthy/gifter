import enum
from pony.orm import *
from datetime import datetime, date
import gifter.db
from gifter.share import Share


class Payment(gifter.db.Entity):

	class Type(enum.IntEnum):

		BUY_SHARE  = 0

	id = PrimaryKey(int, auto=True)
	user         = Required("PublicUser")
	created_at   = Required(datetime, default=datetime.utcnow)
	updated_at   = Required(datetime, default=datetime.utcnow)
	received_at  = Required(date, default=date.today)
	amount       = Required(int) # amounts are in whole dollars
	share_price  = Optional(int) # share price at time of purchase
	payment_type = Required(int)
	action       = Set("ActionLog")


	def shares_purchased(self):
		if self.payment_type != int(Payment.Type.BUY_SHARE):
			raise TypeError("expecting payment type BUY_SHARE, got {}".format(self.payment_type.name))
		return Share(amount, share_price)


	###
	### STATIC METHODS
	###


	@staticmethod
	@db_session
	def buy_share(user, admin, received_at, amount):
		share_price = Share.price_at(received_at)
		no_purchased = Share.shares_purchased(amount, received_at)
		payment = Payment(user=user, received_at=received_at, amount=amount, share_price=share_price, 
			payment_type=int(Payment.Type.BUY_SHARE))
		desc    = "received payment of ${} on {} for user {} for purchase of {} shares at price ${}".format(amount, received_at, user, no_purchased, share_price)
		log     = ActionLog(action_type=int(ActionLog.Type.BUY_SHARE), user=user, admin=admin, description=desc, amount=amount, payment=payment)


	@staticmethod
	@db_session
	def edit_payment(payment, admin, received_at, amount, payment_type, note):

		if note is None or note.strip() == "":
			raise RuntimeError("you must provide a reason for the adjustment")

		old_amount      = payment.amount
		old_received_at = payment.received_at
		old_type        = payment.payment_type
		changes = []
		if old_type != payment_type:
			changes.push("changed type from {} to {}".format(old_type.name, payment_type.name))
		if old_amount != amount:
			changes.push("changed amount from ${} to ${}".format(old_amount, amount))
		if old_received_at != received_at:
			changes.push("changed date received from {} to {}").format(old_received_at, received_at)
		if len(changes) == 0:
			raise RuntimeError("No changes made!")

		desc = ", ".join(changes)

		payment.amount      = amount
		payment.received_at = received_at
		payment.type        = payment_type
		payment.updated_at  = datetime.utcnow()

		log = ActionLog(action_type=int(ActionLog.Type.ADJUST_SHARE), admin=admin, user=user, description=desc, 
			amount=amount, payment=payment, note=note)

from gifter.db.models.public_user import *
