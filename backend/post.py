from flask import Blueprint, render_template

post = Blueprint('post', __name__, template_folder='../frontend')

@post.route('/post', methods=['GET'])
def show():
    return render_template('post.html')