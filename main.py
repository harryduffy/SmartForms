from Generator.generator import generator_blueprint
from Arterial.arterial import arterial_blueprint
from Generator.packs import packs_blueprint
from app import app

app.register_blueprint(arterial_blueprint, url_prefix='')
app.register_blueprint(generator_blueprint, url_prefix='/generator')
app.register_blueprint(packs_blueprint, url_prefix='/packs')

if __name__ == '__main__':
    app.run(debug=True)