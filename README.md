## Free Stuff

## Installation

* ```$ virtualenv .env -p python3```
* ```$ source .env/bin/activate```
* ```$ pip3 install virtualenv```
* ```$ pip3 install flask```
* ```$ pip3 install peewee psycopg2```
* ```$ pip3 freeze > requirements.txt```
* ```$ pip3 install flask_login flask-bcrypt```


## Models
```
class Address(Model):
	address_1 = CharField()
	address_2 = CharField()
	city = CharField()
	state = CharField()
	zip_code = CharField()

class User(UserMixin, Model):
	first_name = CharField()
	last_name = CharField()
	picture = CharField()
	latitude = Numeric()
	longitude = Numeric()
	email = CharField(unique=True)
	password = CharField()

class Item(Model):
	name = CharField()
	picture = CharField()
	category = CharField()
	description = CharField()
	latitude = Numeric()
	longitude = Numeric()
	address_1 = CharField()
	address_2 = CharField()
	city = CharField()
	state = CharField()
	zip_code = CharField()
	owner = ForeignKeyField(User, backref='items')
	created_at = DateTimeField(default=datetime.datetime.now)

class Comment(Model):
	comment = CharField()
	author = ForeignKeyField(User, backref='user')
	item = ForeignKeyField(Item, backref='items')
	created_at = DateTimeField(default=datetime.datetime.now)
```

## API routes

--Item

| HTTP method	| URL path			| Description	 |
| ------------- |:-----------------:| --------------:|
| GET 			| `/items` 			| list of items	 |
/// use query string to get items in a certain area /items?lat_lng=60626&distance=10|

| GET 			| `/items/search` 	| list of items by category	 |
| GET 			| `/items/<id>`		| show one item  |
| POST			| `/items`			| create item 	 |
| PUT 			| `/items/<id>` 		| update an item |
| DELETE 		| `/items/<id>` 		| delete an item |


--User

| HTTP method	|	URL path		| Description		  |
| ------------- |:-----------------:| -------------------:|
| GET 			| /users/profile	| user profile		  |
| POST 			| /users/login 		| log user in 		  |
| GET 			| /users/logout 	| log user out 		  |
| POST 			| /users/register 	| register user 	  |
| PUT 			| /users/<id> 		| update user account |
| DELETE 		| /users/<id>		| delete the account  |


--Comment

| HTTP method	|	URL path		| Description		  |
| ------------- |:-----------------:| -------------------:|
| GET 			| `/comments/<item_id>`	| list the comments	for an item |
| POST 			| `/comments/<item_id>` 		| create a comment 	  |
| DELETE 		| `/comments/<id>` 	| delete a comment 	  |


## Developtment process

* Feb 25th-27th, 
	- Auth complete
	- Item complete
	- Comment complete
	



