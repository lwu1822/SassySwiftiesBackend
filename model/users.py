""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # Do Swifties virtual currencies
    #_currentTokens = db.Column(db.Integer, unique = False)
    #_allTimeTokens = db.Column(db.Integer, unique = False)
    #_matchingMaxTokens = db.Column(db.Integer, unique = False)
    
    # constructor of a User object, initializes the instance variables within object (self)
    
    #def __init__(self, username, password, currentTokens=0, allTimeTokens=0, matchingMaxTokens=0):
    
    def __init__(self, username, password):
        self._username = username    # variables with self prefix become part of the object, 
        self._password = generate_password_hash(password, method='sha256')
        # Make initial values of Swifties
        #self._currentTokens = currentTokens
        #self._allTimeTokens = allTimeTokens
        #self._matchingMaxTokens = matchingMaxTokens

    # a name getter method, extracts name from object
    @property
    def username(self):
        return self._username
    
    # a setter function, allows name to be updated after initial object creation
    @username.setter
    def username(self, username):
        self._username = username
       
    @property
    def password(self):
        return self._password 

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password, method='sha256')
    
    def passwordCheck(self):
        return self._password

    # Make getters and setters for the Swifties
    
    #@property
    #def currentTokens(self):
        #return self._currentTokens
    
    #@currentTokens.setter
    #def currentTokens(self, currentTokens):
        #self._currentTokens = currentTokens
    
    
    #@property
    #def allTimeTokens(self):
        #return self._allTimeTokens
    
    #@allTimeTokens.setter
    #def allTimeTokens(self, allTimeTokens):
        #self._allTimeTokens = allTimeTokens
        
        
    #@property
    #def matchingMaxTokens(self):
        #return self._matchingMaxTokens
    
    #@matchingMaxTokens.setter
    #def matchingMaxTokens(self, matchingMaxTokens):
        #self._matchingMaxTokens = matchingMaxTokens


    # check password parameter versus stored/encrypted password
    #def is_password(self, password):
     #   """Check against hashed password."""
      #  result = check_password(self._password, password)
      #  return result

    def find_by_username(username):
        with app.app_context():
            user = User.query.filter_by(_username=username).first()
        return user

   # def check_credentials(username, password):
    # query email and return user record
      #  user = find_by_username(username)
      #  if user == None:
      #      return False
     #   if (user.is_password(password)):
      #      return True
      #  return False
    


    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "posts": [post.read() for post in self.posts]
            #Do Swifties
            #"current_swifties": self.currentTokens
            #"all_time_swifties": self.allTimeTokens
            #"matching_max_swifties": self.matchingMaxTokens
        }

    # CRUD update: updates user name, password, phone
    # returns self
    
    
    def update(self, username="", password=""):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if len(password) > 0:
            self.password = password
        db.session.commit()
        return self
    
    # I hope I'm not messing this up. Here's a second update function for the matching game Swifties.
    
    #def update(self, Tokens="")
        # Update nonzero values
        #if Tokens > 0:
            #self.currentTokens = Tokens + self.currentTokens
        #if Tokens > 0:
            #self.allTimeTokens = Tokens + self.allTimeTokens
        #if Tokens > self.matchingMaxTokens:
            #self.matchingMaxTokens = Tokens
        #db.session.commit()
        #return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """

class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }
    
# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(username='jesa06', password='123Ellyna4')
        u2 = User(username='Lwu', password='sassy')
        u3 = User(username='collin07', password='iloveorlando')
        u4 = User(username='orlando23', password='four')
        u5 = User(username='leonard!', password='123code')
        u6 = User(username='yeung', password='twsifty')
        u7 = User(username='mmort', password='codecodecode')
        u8 = User(username='sssachit', password='greenring')
        u9 = User(username='a', password='a')

        users = [u1, u2, u3, u4, u5, u6, u7, u8, u9]



        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.username + " note " + str(num) + ". \n Generated by test data."
                    user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.username}")
            
