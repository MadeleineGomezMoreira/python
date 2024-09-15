import os
from flask import Flask

#here I will create and configure the app
def create_app(test_config=None):
    #instance relative config tells the app that configurration files are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        #secret key should be overridden by a random value when deploying
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite') 
    )
    
    #here I will load the instance config if it does exist whenever I am not testing
    if test_config is None:
        #this will override the current configuration with values from config.py file (where we can set a real secret key)
        app.config.from_pyfile('config.py', silent=True)
    
    #if I am testing then I will load the test config
    else:
        app.congif.from_mapping(test_config)
        
    #I will ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #a route to a simple test page
    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app
        
    