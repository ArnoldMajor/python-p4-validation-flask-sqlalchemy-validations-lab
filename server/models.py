from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def name_exists_and_is_unique(self, key, name):
        if not name or name.strip() == "":
             raise ValueError("Name cannot be empty")
        elif Author.query.filter(Author.name == name).first():
            raise ValueError('Name must be unique') 
        return name
    
    @validates('phone_number')
    def phone_number_has_ten_digits(self, key, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title')
    def title_exists(self, key, title):
        clickbaits = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title or title.strip() == "":
            raise ValueError("Post must have a title")
        elif not any(word.lower() in title.lower() for word in clickbaits):
            raise ValueError("Title must contain clickbaity words")
        return title 
      
    @validates('content')
    def content_250_or_more(self, key, content):
        if not len(content.strip()) >= 250:
            raise ValueError("Post content should be atleast 250 characters long")
        return content
    
    @validates('summary')
    def content_250_or_less(self, key, summary):
        if summary is None or len(summary.strip()) > 250:
            raise ValueError("Post summary should be maximum 250 characters long")
        return summary
    
    @validates('category')
    def category_types(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category has to be either Fiction or Non-Fiction")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
