# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict






comments = Blueprint('comments', 'comments')

# comment create route
@comments.route('/<item_id>', methods=['POST'])
# the user must be logged in to use this route
@login_required
def test(item_id):
	# get the information from the body
	payload = request.get_json()

	# look up item
	item = models.Item.get_by_id(item_id)

	# create the comment
	comment = models.Comment.create(
		comment=payload['comment'],
		author=current_user.id,
		item=item.id
		)
	comment_dict = model_to_dict(comment)

	# remove password
	comment_dict['author'].pop('password')
	comment_dict['item']['owner'].pop('password')

	print(comment_dict)

	return jsonify(
		data=comment_dict,
		message="Successfully create commented item",
		status=200
		), 200
