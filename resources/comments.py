# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict






comments = Blueprint('comments', 'comments')

# comment create route
@comments.route('/', methods=['GET'])
def test():
	print('hello world')

	return "You hit the comments route"
