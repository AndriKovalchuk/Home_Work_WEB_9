from mongoengine import *

connect(
    db="Home_Work_WEB_9",
    host="mongodb+srv://andrii:sSMTQV52H7RbLUbm@cluster0.irqsim5.mongodb.net/?retryWrites=true&w=majority",
)


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)
    meta = {"collection": "authors"}


class Quote(Document):
    quote = StringField(required=True, unique=True)
    tags = ListField(max_length=50)
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    meta = {"collection": "quotes"}
