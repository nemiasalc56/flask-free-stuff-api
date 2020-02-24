# import everything from peewee
from peewee import *
import datetime



# using sqlite to have a database
DATABASE = SqliteDatabase('items.sqlite')
















# defining our item model
class Item(Model):
	name = CharField()
	picture = CharField()
	address = CharField()
	owner = CharField() # we will add this ForeignKeyField(User, backref='items') late here
	created_at = DateTimeField(default=datetime.datetime.now)

	# this gives our class instructions on how to connect to a specific databse
	class Meta:
		database = DATABASE

# this method will set up the connection to our database
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Item], safe=True)

	print("Connected to database and created tables if they weren't already there.")

	DATABASE.close()