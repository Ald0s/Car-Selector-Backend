import json

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import func, and_, or_, asc, desc, Column, ForeignKey, Integer, String, BigInteger, Numeric, Float
from sqlalchemy.orm import relationship, with_polymorphic

from marshmallow import Schema, fields

from base import db
from base.utility import GetFileContents

class BadgeSchema(Schema):
    id              = fields.Int()
    name            = fields.Str()

    model           = fields.Nested(lambda: ModelSchema( exclude = ( "badges", )), many = False)

class Badge(db.Model):
    __tablename__ = "badge"

    id              = Column(Integer, primary_key = True)
    model_id        = Column(Integer, ForeignKey("model.id"))

    name            = Column(String(50))
    #model          backref to Model

    def Serialize(self, **kwargs):
        schema = BadgeSchema(**kwargs)
        return schema.dump(self)

    def Create(model, badge):
        result = Badge(
            model_id        = model.id,             \
            name            = badge["Badge"])

        db.session.add(result)
        db.session.flush()

        return result

    def __str__(self):
        return "<Badge "+ str(self.id) + ": " + self.name + ">"

class ModelSchema(Schema):
    id              = fields.Int()
    name            = fields.Str()

    make            = fields.Nested(lambda: MakeSchema( exclude = ( "models", )), many = False)
    badges          = fields.Nested(BadgeSchema, many = True)

class Model(db.Model):
    __tablename__ = "model"

    id              = Column(Integer, primary_key = True)
    make_id         = Column(Integer, ForeignKey("make.id"))

    name            = Column(String(50))

    #make           backref to Make
    badges          = relationship("Badge", backref = db.backref("model", uselist = False), uselist = True)

    def Serialize(self, **kwargs):
        schema = ModelSchema(**kwargs)
        return schema.dump(self)

    def Create(make, model):
        result = Model(
            make_id         = make.id,              \
            name            = model["Model"])

        db.session.add(result)
        db.session.flush()

        if "Badges" in model:
            result.LoadBadges( model["Badges"] )

        return result

    def LoadBadges(self, badges):

        for badge in badges:
            result = Badge.Create( self, badge )

            if not result:
                print("Failed to import a badge {0}!".format(badge["Badge"]))
                exit()

    def GetById(modelid):
        return Model.query                      \
            .filter(Model.id == modelid)        \
            .scalar()

    def __str__(self):
        return "<Model "+ str(self.id) + ": " + self.name + ">"

class MakeSchema(Schema):
    id              = fields.Int()
    type_           = fields.Str()
    name            = fields.Str()

    models          = fields.Nested(ModelSchema, many = True)

class Make(db.Model):
    __tablename__ = "make"

    id              = Column(Integer, primary_key = True)
    type_           = Column(String(10))
    name            = Column(String(50))

    models          = relationship("Model", backref = db.backref("make", uselist = False), uselist = True)

    __mapper_args__ = {
        "polymorphic_identity": "make",
        "polymorphic_on": type_
    }

    def Serialize(self, **kwargs):
        schema = MakeSchema(**kwargs)
        return schema.dump(self)

    def LoadModels(self, models):
        for model in models:
            result = Model.Create( self, model )

            if not result:
                print("Failed to import a model {0}!".format(model["Model"]))
                exit()

    # Finds all Make records of type 'type' and returns them, where applicable,
    # as an instance of their derived type.
    def GetByType(type):
        return with_polymorphic(Make, "*").query        \
            .filter(Make.type_ == type)                 \
            .all()

    # Finds the Make record associated with makeid, but returns it with a parent-child relationship
    # between Make and a derived type (if any.)
    # -> Make.GetById( x )
    # <- (Car<x>)
    def GetById(makeid):
        return with_polymorphic(Make, "*").query        \
            .filter(Make.id == makeid)                  \
            .scalar()

    @hybrid_property
    def num_models(self):
        return len(self.models)

    @hybrid_property
    def num_badges(self):
        total = 0

        for x in self.models:
            total += len(x.badges)
        return total

    # Type sensitive hybrid methods.
    # Remember to call on the Class level of a child.

    # Creates a new table based on the derived type for each item in makes.
    # Then generates that makes models, and that models badges (if applicable.)
    # If you define a new type and have custom create logic, you'll need to override this.
    @hybrid_method
    def Create(cls, makes):

        for make in makes:
            if cls.Exists( make["Make"] ):
                continue

            result = cls( 
                name    = make["Make"])

            db.session.add(result)
            db.session.flush()

            result.LoadModels( make["Models"] )

            if not result:
                print("Failed to import type: {0}!".format( cls.__table__.name ))
                exit()

        return True

    # Finds a [ Car/Bike, Model, Badge (if applic.) ] set based on make, model and badge.
    # Can return multiple results. Particularly if you provide no badge.
    # Always returns in the form of a list for consistency. Ensure you do your len() as you may not always get a Badge.
    # ( Toyota, Supra ) would return SZ, RZ, SZ-R etc.
    @hybrid_method
    def Find(cls, make, model, badge = None):
        query = db.session.query(cls, Model, Badge)                                     \
            .join(Model, Model.make_id == cls.id)                                       \
            .outerjoin(Badge, Badge.model_id == Model.id)                               \
                                                                                        \
            .filter(cls.name == make)                                                   \
            .filter(Model.name == model)                                                \
            .filter(or_(Badge.name == badge, or_(badge == None, Badge.name == None)))   \
            .filter(cls.type_ == cls.__table__.name)

        return query.all()

    # Checks whether any make record exists where attached to the type of cls.
    @hybrid_method
    def Exists(cls, name):
        return cls.query                                \
            .filter(cls.name == name)                   \
            .filter(cls.type_ == cls.__table__.name)    \
            .scalar()

class CarSchema(MakeSchema):
    # Car specific content to serialize.
    pass

# Establish a polymorphic relationship here, to distinguish two separate types
# of make with each their own trees of models & badges. One could simply use a 'type'
# column on make, though should you wish to apply bike/car specific functionality or
# add other types of vehicles, this is a great way!
class Car(Make):
    __tablename__ = "car"

    id              = Column(Integer, ForeignKey("make.id"), primary_key = True)

    __mapper_args__ = {
        "polymorphic_identity": "car"
    }

    def Serialize(self, **kwargs):
        schema = CarSchema(**kwargs)
        return schema.dump(self)

    def Import(file):
        if len( Car.query.all() ) > 0:
            print("Car table already has content. Skipping import.")
            return False

        print("Importing cars from {0}".format( file ))

        # Read cars.json and load contents as json.
        makes = json.loads( GetFileContents( file )) ["Cars"]

        if not Car.Create( makes ):
            print("Failed to import cars!")

        total = 0
        cars = Car.query.all()
        for x in cars:
            total += x.num_badges

        print("Imported {0} cars".format( total ))
        return True

    def __str__(self):
        return "<Car "+ str(self.id) + ": " + self.name + ">"

class BikeSchema(MakeSchema):
    # Bike specific content to serialize.
    pass

class Bike(Make):
    __tablename__ = "bike"

    id              = Column(Integer, ForeignKey("make.id"), primary_key = True)

    __mapper_args__ = {
        "polymorphic_identity": "bike"
    }

    def Serialize(self, **kwargs):
        schema = BikeSchema(**kwargs)
        return schema.dump(self)

    def Import(file):
        if len( Bike.query.all() ) > 0:
            print("Bike table already has content. Skipping import.")
            return False
        
        print("Importing bikes from {0}".format( file ))

        # Read bikes.json and load contents as json.
        makes = json.loads( GetFileContents( file )) ["Bikes"]

        if not Bike.Create( makes ):
            print("Failed to import bikes!")
            exit()

        total = 0
        bikes = Bike.query.all()
        for x in bikes:
            total += x.num_models

        print("Imported {0} bikes".format( total ))
        return True

    def __str__(self):
        return "<Bike "+ str(self.id) + ": " + self.name + ">"