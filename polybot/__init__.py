from datetime import datetime
import platform
import os
import csv 
import implementML
import json
from flask import Flask, render_template, send_file, flash, request, redirect, url_for, send_from_directory
from polybot.version import __version__  # noqa: F401
from flask_cors import CORS

def create_app(test_config: dict = None) -> Flask:
    """Create the polybot server application"""
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    SECRET_KEY = 'super_secret_key'
    app.config['SECRET_KEY'] = SECRET_KEY
    # Load in the configuration
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'config.py'), silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Make the initial status page
    start_time = datetime.now().isoformat()

    @app.route('/')
    def home():
        return render_template('home.html',
                               message=f'Running on {platform.node()} since {start_time}')
    
    # @app.route("/chooseExperiment")
    # def getExperiment():
        #get react app the data from the form 
        # return implementML.implementML()
    @app.route('/upload', methods = ["POST"])
    def handleUpload():
        # json_data = request.get_json()
        # print(json_data)
        # check that file exists through filename
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        json_data = request.get_json()
        print("FIRST PRINT", json_data)
        # `file` -> actual file type; can send this through buffer

        file = request.files['file'] 
        
        print(file.filename)
        print(os.getcwd())
        join_to_static_dir = lambda x: os.path.join("polybot/static/csv", x)

        download_filename = join_to_static_dir("in.csv")
        with open(download_filename, 'w', newline="") as f:
            f.write(file.read().decode("utf-8"))
            
        output_filepath = join_to_static_dir("out.csv")
        
        json_data = json.loads(request.files["parameters"].read())
        num_to_select = int(json_data['numExperiments'])
        acquisition = json_data['acquisition']
        print("JSON DATA", json_data)
        print("num to select", num_to_select)
        print("acquisition", acquisition)
        # num_to_select = json_data[""] 
        # acquisition = json_data[""] 

        """
        app.py -> current dir
        send_from_directory("out.csv") -> look for "out.csv" in current dir

        """
        # p = "C:/Users/alanx/OneDrive/Desktop/ieeepolybort/polybot/static/csv"
        pathAbstracted = os.path.abspath("polybot/static/csv")
        implementML.active_learning(download_filename, num_to_select = num_to_select ,acquisition = acquisition, target_file_name=output_filepath)
        print("currentPath:", pathAbstracted)
        return send_from_directory(pathAbstracted, filename="out.csv", as_attachment = True)

    @app.route('/test')
    def test_file():
        return render_template('test.html')

    @app.route('/download')
    def download_file():
        path = "C:/Users/alanx/OneDrive/Desktop/polybot/polybot/static/csv/netflix_titles.csv"
        return send_file(path, as_attachment=True, cache_timeout=0)

    # Load the blueprints
    from .views import ingest
    app.register_blueprint(ingest.bp)

    return app
    
    app.config["CLIENT"] = "C:/Users/alanx/OneDrive/Desktop/polybot/polybot/static"
    @app.route("/directory/<path:path>")
    def get_all(path):
        print(type(path))
        try:
            return send_from_directory(app.config["CLIENT"], filename=path, as_attachment = True)
        except FileNotFoundError:
            abort(404)
    
    app.config["DOWNLOAD_CSV_PATH"] = "C:/Users/alanx/OneDrive/Desktop/ieeepolybort/polybot/static/csv"     #REMMEBER ENDPOINT TO BE /DOWNLOAD/CSVNAME    
    @app.route("/download/<csv_id>")
    def get_csv(csv_id):
        print('THIS IS A GET REQUEST')
        filename = f"{csv_id}.csv"
        print(filename)
        try:
            return send_from_directory(app.config["DOWNLOAD_CSV_PATH"], filename=filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)