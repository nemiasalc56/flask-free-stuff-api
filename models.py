# import everything from peewee
from peewee import *
import datetime




















# defining our item model
class Item(Model):
	name = CharField()
	picture = CharField()
	address = CharField()
	owner = ForeignKeyField(User, backref='items')
	created_at = DateTimeField(default=datetime.datetime.now)

