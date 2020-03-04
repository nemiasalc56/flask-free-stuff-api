# import everything from peewee
from peewee import *
import datetime
from flask_login import UserMixin



# using sqlite to have a database
# pragmas={'foreign_keys': 1} this will allow us to use cascading delete
DATABASE = SqliteDatabase('items.sqlite', pragmas={'foreign_keys': 1}) 









# defining an address model
class Address(Model):
	address_1 = CharField()
	address_2 = CharField()
	city = CharField()
	state = CharField()
	zip_code = CharField()
	lat = CharField()
	lng = CharField()

	class Meta:
		database = DATABASE



# defining our user model
class User(UserMixin, Model):
	first_name = CharField()
	last_name = CharField()
	picture = CharField()
	email = CharField(unique=True)
	password = CharField()
	address = ForeignKeyField(Address, backref='address')

	# this gives our class instructions on how to connect to a specific database
	class Meta:
		database = DATABASE




# definening our items model
class Item(Model):
	name = CharField()
	picture = CharField()
	category = CharField()
	description = CharField()
	lat = CharField()
	lng = CharField()
	address_1 = CharField() # will come back to this
	address_2 = CharField()
	city = CharField()
	state = CharField()
	zip_code = CharField()
	owner = ForeignKeyField(User, backref='items', on_delete='CASCADE')
	created_at = DateTimeField(default=datetime.datetime.now)

	# connect to a specific database
	class Meta:
		database = DATABASE

# defining our comment model
class Comment(Model):
	comment = CharField()
	author = ForeignKeyField(User, backref='comments')
	item = ForeignKeyField(Item, backref='items', on_delete='CASCADE')
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE


# this method will set up the connection to our database
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Address, Item, Comment], safe=True)

	print("Connected to database and created tables if they weren't already there.")

	DATABASE.close()