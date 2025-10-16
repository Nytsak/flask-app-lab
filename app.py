from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('pages/resume.html')


@app.route("/resume")
def resume():
    return render_template('pages/resume.html')


@app.route("/contact")
def contact():
    return render_template('pages/contact.html')


if __name__ == "__main__":
    app.run(debug=True)
