from kefir import Kefir, Repr


class TestKefirSQLAlchemy:
    def test_sqlalchemy(self):
        from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
        from sqlalchemy.orm import declarative_base, sessionmaker, relationship

        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        session = Session()
        Base = declarative_base()

        class User(Base):
            __tablename__ = "users"
            id = Column(Integer, primary_key=True)
            mail = Column(String)
            password_hash = Column(String)
            orders = relationship("Order", back_populates="user")

        class UserRepr(Repr):
            ignore = ["password_hash"]
            names_map = {"mail": "email"}
            look = ["email"]
            validate = ["email"]

            def look_email(mail_addr):
                return mail_addr[::-1]

            def validate_email(mail_addr):
                assert "@" in mail_addr, "invalid email address!"

        class Order(Base):
            __tablename__ = "orders"
            id = Column(Integer, primary_key=True)
            address = Column(String)
            price = Column(Integer)
            date = Column(String)
            user_mail = Column(String, ForeignKey("users.mail"))
            user = relationship("User", back_populates="orders")

        Base.metadata.create_all(engine)
        user = User(mail="bob@blob.email", password_hash="123")
        order = Order(
            address="la rue", price=42, date="26.01.2021", user_mail="bob@blob.email"
        )
        session.add(user)
        session.add(order)
        session.commit()
        kef = Kefir({User: UserRepr})
        assert kef.dump(order) == {
            "user": {
                "orders": [
                    {
                        "id": 1,
                        "address": "la rue",
                        "price": 42,
                        "date": "26.01.2021",
                        "user_mail": "bob@blob.email",
                    }
                ],
                "id": 1,
                "email": "liame.bolb@bob",
            },
            "id": 1,
            "address": "la rue",
            "price": 42,
            "date": "26.01.2021",
            "user_mail": "bob@blob.email",
        }
        assert kef.dump(user) == {
            "orders": [
                {
                    "id": 1,
                    "address": "la rue",
                    "price": 42,
                    "date": "26.01.2021",
                    "user_mail": "bob@blob.email",
                }
            ],
            "id": 1,
            "email": "liame.bolb@bob",
        }
