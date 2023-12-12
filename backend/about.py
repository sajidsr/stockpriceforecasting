from flask import Blueprint, render_template

about = Blueprint('about', __name__, template_folder='../frontend')

@about.route('/about', methods=['GET'])
def show():
    return render_template('about.html')