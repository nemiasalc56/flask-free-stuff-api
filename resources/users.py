# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash
from flask_login import login_user



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
	try:
		models.User.get(models.User.email == payload['email'])

		# if it does, inform the user
		return jsonify(
			data={},
			message="A user with this email already exists.",
			status=401
			), 401
	# if it doesn't, then create account
	except models.DoesNotExist:
		# create the address
		user_address = models.Address.create(
			address_1= payload['address_1'],
			address_2= payload['address_2'],
			city= payload['city'],
			state= payload['state'],
			zip_code= payload['zip_code']
			)
		print("user_address")
		print(user_address)

		# create the user with the address
		new_user = models.User.create(
			first_name=payload['first_name'],
			last_name=payload['last_name'],
			picture=payload['picture'],
			address=user_address.id,
			email= payload['email'],
			password= generate_password_hash(payload['password'])
			)

		user_dict = model_to_dict(new_user)
		print(user_dict)
		# remove the password
		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message=f"Succesfully created user with email {user_dict['email']}",
			status=200
			), 200



# login route
@users.route('/login', methods=['POST'])
def login():
	

	return "you hit the login route"





