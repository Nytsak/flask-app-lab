import os
from app import create_app, db
from app.posts.models import Post
from app.products.models import Product

app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Post': Post, 'Product': Product}


if __name__ == "__main__":
    app.run(debug=True)
