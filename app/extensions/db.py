'''
Main Database connection is done here
'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search
from flask_mail import Mail

SECRET_KEY = os.urandom(32)

print("===============================")
app = Flask(
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
    static_url_path="/",
)



# name = os.environ.get('MYSQL_HOST','localhost')

db_host = os.environ.get('MYSQL_HOST','localhost')
db_port = os.environ.get('MYSQL_PORT',3306)
db_user = os.environ.get('MYSQL_USER','root')
db_password = os.environ.get('MYSQL_PASSWORD','root')
db_name = os.environ.get('MYSQL_DB','flaskDB')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
print(
    '============================================================='
)
print(app.config['SQLALCHEMY_DATABASE_URI'])
print(
    '============================================================='
)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"

app.config['SECRET_KEY'] = SECRET_KEY


# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'manthan0404soni@gmail.com'
app.config['MAIL_PASSWORD'] = 'ydbvvkqkcmmbajlm'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

print("===============================")


print("===============end================")


db = SQLAlchemy(app)

search = Search(db=db)
search.init_app(app)



# db.init_app(app)


def create_db():
    ''' it will create model table if not exist.'''
    from app.model.auth import Profile, Course, Enrollments

    with app.app_context():
        # db.init_app(app1)
        db.create_all()
        
