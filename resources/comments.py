# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


comments = Blueprint('comments', 'comments')


# comment index route
@comments.route('/<item_id>')
def get_comments(item_id):
	# look up item
	item = models.Item.get_by_id(item_id)

	# item_id is a string 
	# so we need to convert it to number
	item_id_int = int(item_id)

	# look up the comments that match this item
	all_comments_query = models.Comment.select()
	
	comments_dict = [model_to_dict(c) for c in all_comments_query if c.item.id == item_id_int]

	if len(comments_dict) == 0:
		return jsonify(
		data={},
		message="This item has no comments",
		status=401
		), 200
	else:

		# remove author's password
		for idx in range(0, len(comments_dict)):
			comments_dict[idx]['author'].pop('password')
			comments_dict[idx]['item']['owner'].pop('password')
			
		return jsonify(
			data=comments_dict,
			message=f"Successfully retrieved {len(comments_dict)} comments",
			status=200
			), 200




# comment create route
@comments.route('/<item_id>', methods=['POST'])
# the user must be logged in to use this route
@login_required
def create_comment(item_id):
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

	return jsonify(
		data=comment_dict,
		message="Successfully create commented item",
		status=200
		), 200


# comment delete route
@comments.route('/<id>', methods=['Delete'])
@login_required
def delete_comment(id):
	# look up comment
	comment = models.Comment.get_by_id(id)
	
	# allow author of the comment or owner of the item to delete it
	if comment.author.id == current_user.id or comment.item.owner.id == current_user.id:
		# delete comment
		comment.delete_instance()

		return jsonify(
			data={},
			message="Successfully deleted comment.",
			status=200
			), 200
	else:
		return jsonify(
			data={},
			message="Only the owner of the item or author of the comment can delete this comment.",
			status=401
			), 401

