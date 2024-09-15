import sqlite3

import click
#g is a special object that is unique for each request, used to store data that can be accessed by multiple functions during the request.
from flask import current_app, g

def get_db():
    if 'db' not in g:
        #sqlite3.connect establishes a connection to the file pointed at by the DATABASE configuration key
        g.db = sqlite3.connect(
            #current_app points to the flask application handling the request 
            #(using an application factory there is no application object in the rest of the code)
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #this will allow accessing the columns by name
        g.db.row_factory = sqlite3.Row
        
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()
        
def init_db():
    db = get_db()
    
    #open resource is a file relative to the flaskr package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#click command defines a command called 'init_db' that calls the init_db function
@click.command('init.db')
def init_db_command():
    #clear existing data and create new tables
    init_db()
    click.echo('Initialized the database!')
    
#the close_db and init_db_command functions need to be registered with the application instance to be used by the application
#but the instance is not available due to using a factory function

def init_app(app):
    #this tells Flask to call that function when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    #adds a new command that can be called with the Flask command
    app.cli.add_command(init_db_command)