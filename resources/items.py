import models
from flask import Blueprint, request, jsonify
# this is so that we can have access to the user that is logged in
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict




items = Blueprint('items', 'items')



# index route
@items.route('/', methods=['GET'])
def item_index():
	# look up all the items
	all_items_query = models.Item.select()

	# conver items to dictionary
	item_dicts = [model_to_dict(item) for item in all_items_query]
	#remove the password from each item's owner
	for idx in range(0, len(item_dicts)):
		item_dicts[idx]['owner'].pop('password')
	print(item_dicts)

	return jsonify(
		data=item_dicts,
		message=f"Succesfully retrieved {len(item_dicts)} items.",
		status=200
		), 200


# item show page
@items.route('/<id>', methods=['GET'])
def get_one_item(id):
	print(id)
	# look up the item that matches this id
	item = models.Item.get_by_id(id)

	# conver item to dict
	item_dict = model_to_dict(item)
	# remove the password
	item_dict['owner'].pop('password')

	return jsonify(
		data=item_dict,
		message=f"Succesfully found item with id {item_dict['id']}",
		status=200
		), 200


# define our create route
@items.route('/', methods=['POST'])
# this is so that only if you are logged in will have access to this route
@login_required
def create_item():
	# get info from body
	payload = request.get_json()
	print(payload)

	# create item
	item = models.Item.create(
		name = payload['name'],
		category = payload['category'],
		description = payload['description'],
		picture = payload['picture'],
		address_1= payload['address_1'],
		address_2= payload['address_2'],
		city= payload['city'],
		state= payload['state'],
		zip_code= payload['zip_code'],
		lat=payload['lat'],
		lng=payload['lng'],
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


# update route
@items.route('/<id>', methods=['PUT'])
# this is so that only if you are logged in will have access to this route
@login_required
def update_item(id):
	# get the information from the request
	payload = request.get_json()

	# look up the item that matches this id
	item = models.Item.get_by_id(id)
	
	# check if user id matches item's owner
	if item.owner.id == current_user.id:
		# if they do, update the item
		print("They match")
	
		# look up the item's address
		item_address = models.Address.get_by_id(item.address.id)

		# update the address
		item_address.address_1 = payload['address_1'] if 'address_1' in payload else None
		item_address.address_2 = payload['address_2'] if 'address_2' in payload else None
		item_address.city = payload['city'] if 'city' in payload else None
		item_address.state = payload['state'] if 'state' in payload else None
		item_address.zip_code = payload['zip_code'] if 'zip_code' in payload else None
		# save the changes
		item_address.save()

		# print(item_address)
		# update the item
		item.name = payload['name'] if 'name' in payload else None
		item.category = payload['category'] if 'category' in payload else None
		item.description = payload['description'] if 'description' in payload else None
		item.picture = payload['picture'] if 'picture' in payload else None
		item.address = item_address
		# save the changes
		item.save()

		# convert item to dictionary
		item_dict = model_to_dict(item)

		# remove owner password
		item_dict['owner'].pop('password')


		return jsonify(
			data=item_dict,
			message=f"Succesfully updated the item named {item_dict['name']}",
			status=200
			), 200
	# if not, their are not allow to do that
	else:
		return jsonify(
			data={},
			message="You are not allow to do that, only the owner can update this item",
			status=403
			), 403



@items.route('/<id>', methods=['Delete'])
# this is so that only if you are logged in will have access to this route
@login_required
def delete_item(id):

	# look up item with this id
	item = models.Item.get_by_id(id)

	# check if user id matches item's owner
	if item.owner.id == current_user.id:
		# if they do, continue

		# look up address of the this item
		item_address = models.Address.get_by_id(item.address.id)
		# delete the address of the item
		item_address.delete_instance()
		print(item)
		print(item_address)
		# delete the item
		item.delete_instance()


		return jsonify(
			data={},
			message="Succesfully deleted item",
			status=200
			), 200
	# if not, their are not allow to do that
	else:
		return jsonify(
			data={},
			message="You are not allow to do that, only the owner can delete this item",
			status=403
		), 403






