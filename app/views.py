from flask import (
    request,
    render_template,
)


def register_routes(app):
    @app.route("/")
    def index():
        return render_template('base.html')

    @app.route("/homepage")
    def home():
        """View for the Home page of your website."""
        agent = request.user_agent
        return render_template('home.html', agent=agent)
