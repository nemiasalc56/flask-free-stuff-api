import models
from flask import Blueprint




items = Blueprint('items', 'items')







# define our create route
@items.route('/', methods=['POST'])
def create_item():
	
	return "You hit the item create route"