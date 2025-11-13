from flask import Blueprint

posts_bp = Blueprint(
    'posts_bp',
    __name__,
    url_prefix='/post',
    template_folder='templates/posts',
    static_folder='static'
)

from . import views
