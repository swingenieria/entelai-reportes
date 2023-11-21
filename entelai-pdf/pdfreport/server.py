from flask import Flask, render_template
from example_data_faker import fake_volumetria, fake_desmielinizantes
from os import path, makedirs
from shutil import copy2

app = Flask(__name__, template_folder='templates', static_folder="templates")


def load_img(absolute_file_path):
    dirname, filename = path.split(absolute_file_path)
    output_dir = path.join(path.dirname(__file__), 'templates', 'tmp')
    if not path.exists(output_dir):
        makedirs(output_dir)
    copy2(absolute_file_path, output_dir)
    return path.join('tmp', filename)


@app.route('/')
@app.route('/desmielinizantes')
def desmielinizantes():
    return render_template('index.html', report=fake_desmielinizantes(), body_class='debug-server', load_img=load_img)


@app.route('/volumetria')
def volumetria():
    return render_template('index.html', report=fake_volumetria(), body_class='debug-server', load_img=load_img)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
