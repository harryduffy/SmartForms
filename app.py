from flask import Flask, render_template

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('web_error_templates/404.html')

@app.errorhandler(403)
def resource_forbidden(e):
    return render_template('web_error_templates/403.html')