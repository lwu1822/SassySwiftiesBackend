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
    # _nfts = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False)
    # _profile = db.Column(db.Integer, unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # Do Swifties virtual currencies
    _currentTokens = db.Column(db.Integer, unique=False)
    _allTimeTokens = db.Column(db.Integer, unique=False)
    _matchingMaxTokens = db.Column(db.Integer, unique=False)
    
    # constructor of a User object, initializes the instance variables within object (self)
    
    def __init__(self, username, password, currentTokens=0, allTimeTokens=0, matchingMaxTokens=0):
        self._username = username    # variables with self prefix become part of the object, 
        self._password = generate_password_hash(password, method='sha256')
        # self._nfts = []
        # self._profile = 0
        # Make initial values of Swifties
        self._currentTokens = currentTokens
        self._allTimeTokens = allTimeTokens
        self._matchingMaxTokens = matchingMaxTokens

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
    

    # Nfts
    # @property
    # def nfts(self):
     #    return self._nfts 

    # @nfts.setter
   #  def nfts(self, nfts):
    #     self._nfts = nfts

   # @property
    #def profile(self):
     #   return self._profile 

    #@profile.setter
    #def profile(self, profile):
      #  self._profile = profile

    
    

    # Make getters and setters for the Swifties
    
    @property
    def currentTokens(self):
        return self._currentTokens
    
    @currentTokens.setter
    def currentTokens(self, currentTokens):
        self._currentTokens = currentTokens
    
    
    @property
    def allTimeTokens(self):
        return self._allTimeTokens
    
    @allTimeTokens.setter
    def allTimeTokens(self, allTimeTokens):
        self._allTimeTokens = allTimeTokens
        
        
    @property
    def matchingMaxTokens(self):
        return self._matchingMaxTokens
    
    @matchingMaxTokens.setter
    def matchingMaxTokens(self, matchingMaxTokens):
        self._matchingMaxTokens = matchingMaxTokens


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
            #"nfts": self.nfts,
            #"profile": self.profile,
            "posts": [post.read() for post in self.posts],
            #Do Swifties
            "current_swifties": self.currentTokens,
            "all_time_swifties": self.allTimeTokens,
            "matching_max_swifties": self.matchingMaxTokens
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
    
    def updateToken(self, Username="", Tokens=0, Purchase=0):
        # Update nonzero values
        if Tokens > 0:
            self.currentTokens = Tokens + self.currentTokens
        if Tokens > 0:
            self.allTimeTokens = Tokens + self.allTimeTokens
        if Tokens > self.matchingMaxTokens:
            self.matchingMaxTokens = Tokens
        if Purchase > 0:
            self.currentTokens = self.currentTokens - Purchase
        db.session.commit()
        return self
    
    
    

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """

class Post(db.Model):
    __tablename__ = 'posts11'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String, unique=False)
    _note = db.Column(db.String, unique=False, nullable=False)
    _image = db.Column(db.Integer, unique=False)
    _date = db.Column(db.String, unique=False)
    _username = db.Column(db.String, unique=False)
    _likes = db.Column(db.Integer, unique=False)
    _likedby = db.Column(db.String, unique=False)

    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, title, note, image, date, username):
        self._title = title
        self._note = note
        self._image = image
        self._date = date
        self._username = username
        self._likes = 0
        self._likedby = ""

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        self._note = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def likes(self):
        return self._likes

    @likes.setter
    def likes(self, value):
        self._likes = value

    @property
    def likedby(self):
        return self._likedby

    @likedby.setter
    def likedby(self, value):
        self._likedby = value

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID)  + "," + str(self.userID) + ")"

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
        # path = app.config['UPLOAD_FOLDER']
        # file = os.path.join(path, self.image)
        # file_text = open(file, 'rb')
        # file_read = file_text.read()
        
        return {
            "id": self.id,
            "userID": self.userID,
            "title": self._title,
            "note": self._note,
            "image": self._image,
            "date": self._date,
            "username": self._username,
            "likes": self._likes,
            "likedby": self._likedby
        }
    def update(self, likes = 0, add_like = "", remove_like = ""):
        """Only updates values with length"""
        self.likes = self.likes + likes

        if(len(add_like) > 0 or len(remove_like) > 0):
            likedby_list = string_to_list(self.likedby)
            if(len(add_like) > 0):
                likedby_list.append(add_like)
            if(len(remove_like) > 0):
                likedby_list.remove(remove_like)

            self.likedby = list_to_string(likedby_list)

        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
class Nfts(db.Model):
    __tablename__ = 'nfts3'
    id = db.Column(db.Integer, primary_key=True)
    _userID = db.Column(db.Integer, unique=True)
    _profile = db.Column(db.Integer, unique=False)
    _nft0 = db.Column(db.Boolean, unique=False)
    _nft1 = db.Column(db.Boolean, unique=False)
    _nft2 = db.Column(db.Boolean, unique=False)
    _nft3 = db.Column(db.Boolean, unique=False)
    _nft4 = db.Column(db.Boolean, unique=False)
    _nft5 = db.Column(db.Boolean, unique=False)

    def __init__(self, userID, nfts, profile):
        self._userID = userID
        self._nft0 = nfts[0]
        self._nft1 = nfts[1]
        self._nft2 = nfts[2]
        self._nft3 = nfts[3]
        self._nft4 = nfts[4]
        self._nft5 = nfts[5]
        self._profile = profile

    @property
    def userID(self):
        return self._userID

    @userID.setter
    def userID(self, value):
        self._userID = value

    @property
    def nfts(self):
        return [self._nft0, self._nft1, self._nft2, self._nft3, self._nft4, self._nft5]

    @nfts.setter
    def nfts(self, value):
        self._nft0 = value[0]
        self._nft1 = value[1]
        self._nft2 = value[2]
        self._nft3 = value[3]
        self._nft4 = value[4]
        self._nft5 = value[5]

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, value):
        self._profile = value

    def __repr__(self):
        return "Nfts(" + str(self.id) + "," + str(self.userID) + "," + str(self.nfts) + "," + str(self.profile) + ")"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "userID": self.userID,
            "nfts": self.nfts,
            "profile": self.profile
        }

    def update(self, nfts=None, profile=None):
        if nfts is not None:
            self.nfts = nfts
        if profile is not None:
            self.profile = profile
        db.session.commit()
        return self

class Scoreboard(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String, unique=False)
    _score = db.Column(db.Integer, unique=False, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, username, score):
        self._username = username
        self._score = score

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    def __repr__(self):
        return f"Scoreboard({self.id}, {self._username}, {self._score}, {self.userID})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "userID": self.userID,
            "username": self._username,
            "score": self._score
        }





def string_to_list(string):
    return [x for x in string.split(', ')]

def list_to_string(lst):
    return ', '.join(map(str, lst))



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
                    # user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png', title="Temp title", date="1/2/3", username="Temp name"))
                '''add user/post data to table'''
                user.create()
                #Nfts(userID = user.id, profile = 0, nft0 = True, nft1 = False, nft2 = False, nft3 = False, nft4 = False, nft5 = False, ).create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.username}")
            
