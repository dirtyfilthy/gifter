from pony.orm import *
from pony.orm.dbapiprovider import IntConverter, StrConverter, Converter
from enum import Enum
from typing import Type
import gifter.config as config

_db = None # local pony db variabe
Entity = None
initialized = False

def initialize():
	global _db
	global Entity
	global initialized
	
	if initialized:
		return


	_db = Database()

	# if in local development mode, create a local sqlite database, otherwise connect to mysql

	if not config.is_production():
		_db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
	else:
		_db.bind(provider='mysql', host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASS, db=config.DB_NAME)

	# export relevant Pony classes

	Entity = _db.Entity

	# register Enum converter, it should really come standard 

	##_db.provider.converter_classes.append((Enum, StrConverter))

	initialized = True


def map():
	global _db
	initialize()
	_db.generate_mapping(create_tables=True)


initialize()

# import the models to generate the tables










