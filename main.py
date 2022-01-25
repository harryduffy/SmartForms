from Generator.generator import generator_blueprint
from Arterial.arterial import arterial_blueprint
from app import app

app.register_blueprint(arterial_blueprint, url_prefix='')
app.register_blueprint(generator_blueprint, url_prefix='/generator')

if __name__ == '__main__':
    app.run(debug=True)