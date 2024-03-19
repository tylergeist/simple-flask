from app import app
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"

    ssn = Column('ssn', Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, first_name, last_name, gender, age):
        self.ssn = ssn
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.first_name} {self.last_name} {self.gender} {self.age}"
    
class Item(Base):
    __tablename__="item"
    
    item_id = Column('item_id', Integer, primary_key=True)
    description = Column('description', String)
    owner = Column(Integer, ForeignKey("people.ssn") )

    def __init__ (self, item_id, description, owner):
        self.item_id = item_id
        self.description = description
        self.owner = owner

    def __repr__(self):
        return f"({self.item_id}) -  {self.description} belongs to -> {self.owner}"
    
engine = create_engine("sqlite:///mydb1.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

person_one = Person(12354, "John", "Doe", "m", 40)
person_two = Person(12531, "Vic", "Denny", "m", 35)
person_three = Person(11454, "Josh", "Neovim", "m", 25)
person_four = Person(11534, "Savage", "Dak", "m", 12)

item_one = Item(1, "Coffee", person_one.ssn)
item_two = Item(2, "Tea", person_two.ssn)
item_three = Item(3, "Energy Drink", person_one.ssn)
item_four = Item(4, "Protein Shake", person_four.ssn)
item_five = Item(5, "Smoothie", person_three.ssn)

session.add(person_one)
session.add(person_two)
session.add(person_three)
session.add(person_four)

session.add(item_one)
session.add(item_two)
session.add(item_three)
session.add(item_four)
session.add(item_five)

session.commit()


results = session.query(Item, Person).filter(Item.owner == Person.ssn).filter(Person.first_name == "John")

for r in results:
    print(r)
