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
	for idx in range(len(item_dicts), 0):
		item_dicts[idx]['owner'].pop('password')
	
	# this is so it shows the last item added first
	item_dicts.reverse()
	return jsonify(
		data=item_dicts,
		message=f"Succesfully retrieved {len(item_dicts)} items.",
		status=200
		), 200


# item show page
@items.route('/<id>', methods=['GET'])
def get_one_item(id):
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

		# update the item info
		item.address_1 = payload['address_1'] if 'address_1' in payload else None
		item.address_2 = payload['address_2'] if 'address_2' in payload else None
		item.city = payload['city'] if 'city' in payload else None
		item.state = payload['state'] if 'state' in payload else None
		item.zip_code = payload['zip_code'] if 'zip_code' in payload else None
		item.lat = payload['lat'] if 'lat' in payload else None
		item.lng = payload['lng'] if 'lng' in payload else None
		item.name = payload['name'] if 'name' in payload else None
		item.category = payload['category'] if 'category' in payload else None
		item.description = payload['description'] if 'description' in payload else None
		item.picture = payload['picture'] if 'picture' in payload else None
		
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
		# delete the item
		item.delete_instance(recursive=True)


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
			status=401
		), 200


# filter by category
@items.route('/<category>/category', methods=['GET'])
def category(category):
	# get the information from our request
	# payload = request.get_json()

	# look up items with that category
	search_items = models.Item.select().where(models.Item.category == category)

	# if we found the items we can continue
	if len(search_items) != 0:
		# convert search_items to dictionary
		search_item_dicts = [model_to_dict(item) for item in search_items]

		# remove owner's password
		for idx in range(0, len(search_item_dicts)):
			search_item_dicts[idx]['owner'].pop('password')

		search_item_dicts.reverse()
		
		return jsonify(
			data=search_item_dicts,
			message=f"Succesfully found {len(search_item_dicts)} items with the category of {category}",
			status=200
			), 200
	# if not, inform the user
	else:
		return jsonify(
			data={},
			message="No items was found on this category",
			status=401
			), 200


# get items by current user
@items.route('/mine', methods=['GET'])
@login_required
def my_items():

	# loop through the items in the current user
	current_user_items = [model_to_dict(item) for item in current_user.items]
	if len(current_user_items) == 0:
		return jsonify(
		data={},
		message=f"This user has no items yet.",
		status=401
		), 200
	else:
		#remove the password
		for item in current_user_items:
			item['owner'].pop('password')

		current_user_items.reverse()
		
		return jsonify(
			data=current_user_items,
			message=f"Successfully retrieved {len(current_user_items)} items.",
			status=200
			), 200



