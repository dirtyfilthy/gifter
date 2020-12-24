from datetime import datetime
from pony.orm import *
from gifter.share import Share
import gifter.db


class PublicUser(gifter.db.Entity):
	id = PrimaryKey(int, auto=True)
	name       = Required(str)
	email      = Required(str)
	landline   = Optional(str)
	mobile     = Optional(str)
	address    = Optional(str)
	created_at = Required(datetime, default=datetime.utcnow)
	updated_at = Required(datetime, default=datetime.utcnow)
	payments   = Set('Payment')
	actions    = Set('ActionLog')


	def __str__(self):
		return "{} ({}}".format(self.name, self.email)


	def share_payments(self):
		''' return all share payments made by this user '''
		return self.payments.select(lambda p: p.payment_type == int(Payment.Type.BUY_SHARE)).order_by(desc(Payment.received_at))


	def shares_owned(self):
		''' return the current number of shares owned by this user '''
		total_shares = Share(0)
		for payment in self.share_payments():
			total_shares += p.shares_purchases()
		return total_shares


	def action_log(self):
		''' return the action log for this user '''
		return self.actions.order_by(desc(ActionLog.created_at))


	###
	### STATIC METHODS
	###

	@staticmethod
	@db_session
	def create(admin, name, email, landline, mobile, address):
		''' create a new user and log it '''
		user = PublicUser(name=name.strip(), email=email.strip(), landline=landline.strip(), mobile=mobile.strip(), address=address.strip())
		desc = "created user {}".format(user)
		log  = ActionLog(action_type=int(ActionLog.Type.CREATE_USER), admin=admin, description=desc, user=user)

	@staticmethod
	@db_session
	def edit(admin, user, name, email, landline, mobile, address, note):
		''' edit an existing user and log it '''
		old_name     = user.name
		old_email    = user.email
		old_landline = user.landline
		old_mobile   = user.mobile
		old_address  = user.address

		changes = []

		if old_name != name:
			changes.push("changed name from '{}' to '{}'".format(old_name, name))
			user.name = name

		if old_email != email:
			changes.push("changed email from '{}' to '{}'".format(old_email, email))
			user.email = email

		if old_landline != landline:
			changes.push("changed landline from '{}' to '{}'".format(old_landline, landline))
			user.landline = landline

		if old_mobile != mobile:
			changes.push("changed mobile from '{}' to '{}'".format(old_mobile, mobile))
			user.mobile = mobile

		if old_address != address:
			changes.push("changed address from '{}' to '{}'".format(old_address, address))
			user.address = address

		if len(changes) == 0:
			raise RuntimeError("no changes made!")

		desc = ", ".join(changes)

		log = ActionLog(action_type=int(ActionLog.Type.UPDATE_USER), admin=admin, user=user, description=desc, note=note)

	@staticmethod
	@db_session
	def search(term, limit=None):
		''' search users for search term 'term', if 'limit' is set it will return a maximum of 'limit' results '''
		query = select(u for u in PublicUser if term in u.name or term in u.email).order_by(PublicUser.name)
		if limit is not None:
			query = query.limit(limit)
		return query

from gifter.db.models.payment import *
from gifter.db.models.action_log import *
