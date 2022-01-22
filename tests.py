import unittest
from dataclasses import dataclass
from kefir import Kefir, Repr

class TestKefirBase(unittest.TestCase):
    
    def setUp(self):
        self.kef = Kefir()
    
    def test_basic(self):
        
        class A:
          def __init__(self, some_attr):
            self.attr = some_attr
        
        class B:
          def __init__(self, some_attr, some_a_object):
            self.attr = some_attr
            self.a_object = some_a_object

        class BRepr(Repr):
            loads = {'a_object': A}

        self.kef.represents = {B:BRepr}  # bad monkey patching
        a_object = A('kefir')
        b_object = B(42, a_object)
        raw_data = {'attr' :'some text', 'a_object': {'attr': 'just attr'}}
        new_obj = self.kef.load(raw_data, B)
        
        self.assertEqual(self.kef.dump(a_object), {'attr': 'kefir'})
        self.assertEqual(self.kef.dump(b_object), {'attr': 42, 'a_object': {'attr': 'kefir'}})
        self.assertEqual(type(new_obj), B)
        self.assertEqual(type(new_obj.a_object), A)
    
    def test_dataclass(self):
        
        @dataclass
        class ADataClass:
            attr: str
        
        @dataclass
        class BDataClass:
            attr: int
            a_object: ADataClass

        a_object = ADataClass('kefir')
        b_object = BDataClass(42, a_object)
        
        self.assertEqual(self.kef.dump(a_object), {'attr': 'kefir'})
        self.assertEqual(self.kef.dump(b_object), {'attr': 42, 'a_object': {'attr': 'kefir'}})

    def test_class_with_slots(self):

        class AWithSlots:
            __slots__ = ['attr']
            def __init__(self, some_attr):
                self.attr = some_attr

        class BWithSlots:
            __slots__ = ['attr', 'a_object']
            def __init__(self, some_attr, some_a_object):
                self.attr = some_attr
                self.a_object = some_a_object

        a_object = AWithSlots('kefir')
        b_object = BWithSlots(42, a_object)
        
        self.assertEqual(self.kef.dump(a_object), {'attr': 'kefir'})
        self.assertEqual(self.kef.dump(b_object), {'attr': 42, 'a_object': {'attr': 'kefir'}})

class TestKefirRepr(unittest.TestCase):
    def test_repr(self):
        
        class A:
          def __init__(self, some_attr):
            self.attr = some_attr
        
        class B:
          def __init__(self, some_id, some_attr, some_a_object, unused=None):
            self.id = some_id
            self.attr = some_attr
            self.a_object = some_a_object
            self.unused = unused

        class BRepr(Repr):
            ignore = ['unused']
            names_map = {
                'a_object': 'a_obj'
            }
            extra = {
                'url': 'path/to/b_object/<id>'
            }
            look = ['a_obj']
            validate = ['attr']
            def look_a_obj(a_obj):
                return {'first': a_obj['attr'].partition(' ')[0], 'second': a_obj['attr'].partition(' ')[2]}
            def validate_attr(attr):
                assert 'kef' in attr, 'kef not in attr! WHY?'
        
        a_object = A('kefir project')
        b_object = B(42, 'ke', a_object)   
        kef = Kefir(represents={B:BRepr})
        self.assertEqual(kef.dump(b_object), {'id': 42, 'attr': 'kef not in attr! WHY?', 'a_obj': {'first': 'kefir', 'second': 'project'}, 'url': 'path/to/b_object/42'})

class TestKefirSQLAlchemy(unittest.TestCase):
    def test_alchemy(self):
        from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text, select
        from sqlalchemy.orm import declarative_base, sessionmaker, relationship

        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        session = Session()
        Base = declarative_base()
    
        class User(Base):
            __tablename__ = 'users'
            id = Column(Integer, primary_key=True)
            mail = Column(String)
            password_hash = Column(String)
            orders = relationship('Order', back_populates='user')

            def __repr__(self):
                return f"Hello!\nMy mail is {self.mail}"

        class UserRepr(Repr):
            ignore = ['password_hash']
            names_map = {
                'mail': 'email'
            }
            extra = {
                'url': 'api/users/<id>'
            }
            look = ['email']
            validate = ['email']

            def look_email(mail_addr):
                return mail_addr[::-1]

            def validate_email(mail_addr):
                assert '@' in mail_addr, "invalid email address!"

        
        class Order(Base):
            __tablename__ = 'orders'
            id = Column(Integer, primary_key=True)
            address = Column(String)
            price = Column(Integer)
            date = Column(String)
            user_mail = Column(String, ForeignKey('users.mail'))
            user = relationship('User', back_populates='orders')

            def __repr__(self):
                return f"Order\n#{self.id}\nPrice:{self.price}"
        
        Base.metadata.create_all(engine)
        user = User(mail='bob@blob.email', password_hash='123')
        order = Order(address='la rue', price=42, date='26.01.2021', user_mail='bob@blob.email')    
        session.add(user)
        session.add(order)
        session.commit()
        kef = Kefir({User:UserRepr})
        self.assertEqual(kef.dump(order), {'user': {'orders': [{'id': 1, 'address': 'la rue', 'price': 42, 'date': '26.01.2021', 'user_mail': 'bob@blob.email'}], 'id': 1, 'email': 'liame.bolb@bob', 'url': 'api/users/1'}, 'id': 1, 'address': 'la rue', 'price': 42, 'date': '26.01.2021', 'user_mail': 'bob@blob.email'})
        self.assertEqual(kef.dump(user), {'orders': [{'id': 1, 'address': 'la rue', 'price': 42, 'date': '26.01.2021', 'user_mail': 'bob@blob.email'}], 'id': 1, 'email': 'liame.bolb@bob', 'url': 'api/users/1'})
