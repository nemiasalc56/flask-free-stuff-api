# import our models and blueprint
import models
from flask import Blueprint, request



# the first users is the blueprint name
# the second argument is its import_name
users = Blueprint('users', 'users')


# register create route
@users.route('/register', methods=['POST'])
def register():
	# get the information from the request
	payload = request.get_json()
	print(payload)
	# make email lower case
	payload['email'] = payload['email'].lower()
	# check if the email already exists
	# if it does, inform the user

	# if it doesn't, then create account

	return "You hit the register route"