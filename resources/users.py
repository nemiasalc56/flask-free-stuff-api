# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user



# the first users is the blueprint name
# the second argument is its import_name
users = Blueprint('users', 'users')


# register create route
@users.route('/register', methods=['POST'])
def register():

	# get the information from the request
	payload = request.get_json()
	
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
			zip_code= payload['zip_code'],
			lat=payload['lat'],
			lng=payload['lng']
			)

		# create the user with the address
		new_user = models.User.create(
			first_name=payload['first_name'],
			last_name=payload['last_name'],
			picture=payload['picture'],
			address=user_address.id,
			email= payload['email'],
			password= generate_password_hash(payload['password'])
			)
		# this logs the user and starts a session
		login_user(new_user)

		user_dict = model_to_dict(new_user)
		
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
	# get the info from the request
	payload = request.get_json()
	
	# make the email lower case
	payload['email'] = payload['email'].lower()

	try:
		# look use up by email
		user = models.User.get(models.User.email == payload['email']) 
		# this will cause an error if the user doesn't exist

		user_dict = model_to_dict(user)

		# check the password
		password_is_good = check_password_hash(user_dict['password'], payload['password'])

		# if the password is good, log user in
		if password_is_good:
			# this logs the user and starts a session
			login_user(user)
			# remove the password before we send the information to the user
			user_dict.pop('password')

			return jsonify(
				data=user_dict,
				message=f"Succesfully logged in with the email {user_dict['email']}",
				status=200
				), 200
		# if not, inform the user that the email or password is incorrect
		else:
			return jsonify(
				data={},
				message="The email or password is incorrect.",
				status=401
			), 200
	# if we don't find the user
	except models.DoesNotExist:
		# inform user that email or password is incorrect.
		return jsonify(
				data={},
				message="The email or password is incorrect.",
				status=401
		), 201


# user show route
@users.route('/profile', methods=['GET'])
def user_profile():
	
	# look up user with current_user id
	user = models.User.get_by_id(current_user.id)

	# convert to dictionary
	user_dict = model_to_dict(user)
	# remove password
	user_dict.pop('password')
	
	return jsonify(
		data=user_dict,
		message=f"Succesfully found user with id {current_user.id}",
		status=200
		), 200


# logout route
@users.route('/logout', methods=['GET'])
def logout():
	# this is to log user out
	logout_user()
	return jsonify(
		data={},
		message="The user was successfully logged out.",
		status=201
	), 201

# update route
@users.route('/<id>', methods=['PUT'])
def update_user(id):
	# get the info from the body
	payload = request.get_json()
	
	# look up user with the same id
	user = models.User.get_by_id(id)
	

	# update address info
	address = models.Address.get_by_id(user.address.id)
	address.address_1 = payload['address_1'] if 'address_1' in payload else None
	address.address_2 = payload['address_2'] if 'address_2' in payload else None
	address.city = payload['city'] if 'city' in payload else None
	address.state = payload['state'] if 'state' in payload else None
	address.zip_code = payload['zip_code'] if 'zip_code' in payload else None
	address.lat = payload['lat'] if 'lat' in payload else None
	address.lng = payload['lng'] if 'lng' in payload else None
	address.save()


	# update user info
	user.first_name = payload['first_name'] if 'first_name' in payload else None
	user.last_name = payload['last_name'] if 'last_name' in payload else None
	user.picture = payload['picture'] if 'picture' in payload else None
	user.email = payload['email'] if 'email' in payload else None
	user.password = generate_password_hash(payload['password']) if 'password' in payload else None
	user.address = address
	user.save()

	# convert model to a dictionary
	user_dict = model_to_dict(user)

	# remove the password
	user_dict.pop('password')

	return jsonify(
		data=user_dict,
		message="Succesfully update the user information",
		status=200
		),200


# destroy route
@users.route('/<id>', methods=['Delete'])
def delete_user(id):

	# look up user
	user = models.User.get_by_id(id)

	# look up user address
	user_address = models.Address.get_by_id(user.address.id)

	# delete address
	user_address.delete_instance(recursive=True)
	# delete user
	user.delete_instance(recursive=True)

	return jsonify(
		data={},
		message="Succesfully deleted user account.",
		status=200
		), 200


# check who is logged in
@users.route('/logged_in', methods=['GET'])
def logged_in():

	if not current_user.is_authenticated:
		return jsonify(
		data={},
		message="No user is currently logged in.",
		status=401
		), 200
	else:
		user_dict = model_to_dict(current_user)
		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message="Found logged in user",
			status=200
		), 200


