import models
from flask import Blueprint, request, jsonify
# this is so that we can have access to the user that is logged in
from flask_login import current_user
from playhouse.shortcuts import model_to_dict




items = Blueprint('items', 'items')



# index route
@items.route('/', methods=['GET'])
def item_index():

	return "You hit the index route"



# define our create route
@items.route('/', methods=['POST'])
def create_item():
	# get info from body
	payload = request.get_json()
	print(payload)

	# create address first
	item_address = models.Address.create(
		address_1= payload['address_1'],
		address_2= payload['address_2'],
		city= payload['city'],
		state= payload['state'],
		zip_code= payload['zip_code']
		)

	# create item
	item = models.Item.create(
		name = payload['name'],
		description = payload['description'],
		picture = payload['picture'],
		address = item_address.id,
		owner = current_user.id
		)
	item_dict = model_to_dict(item)

	# remove password
	item_dict['owner'].pop('password')

	return jsonify(
		data=item_dict,
		message="Succesfully create an item",
		status=200
		), 200