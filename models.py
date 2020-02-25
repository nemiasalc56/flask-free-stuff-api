# import everything from peewee
from peewee import *
import datetime
from flask_login import UserMixin



# using sqlite to have a database
DATABASE = SqliteDatabase('items.sqlite')










# defining an address model
class Address(Model):
	address_1 = CharField()
	address_2 = CharField()
	city = CharField()
	state = CharField()
	zip_code = CharField()

	class Meta:
		database = DATABASE


# defining our user model
class User(UserMixin, Model):
	first_name = CharField()
	last_name = CharField()
	picture = CharField()
	address = ForeignKeyField(Address, backref='address')
	email = CharField(unique=True)
	password = CharField()

	# this gives our class instructions on how to connect to a specific database
	class Meta:
		database = DATABASE



# definening our items model
class Item(Model):
	name = CharField()
	picture = CharField()
	category = CharField()
	description = CharField()
	address = ForeignKeyField(Address, backref='address')
	owner = ForeignKeyField(User, backref='items')
	created_at = DateTimeField(default=datetime.datetime.now)

	# connect to a specific database
	class Meta:
		database = DATABASE

# this method will set up the connection to our database
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Address, Item], safe=True)

	print("Connected to database and created tables if they weren't already there.")

	DATABASE.close()