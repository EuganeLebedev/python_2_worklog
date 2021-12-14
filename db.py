from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///users.db', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    tg_id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)

    def __init__(self, tg_id, name, username, password):
        self.tg_id = tg_id
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.username, self.password)


def get_user(id: int):
    session = Session()
    query_user = session.query(User).get(id)
    return query_user.username, query_user.password


def get_registred_users_id():
    session = Session()
    query_users_id = session.query(User.tg_id).all()
    usewrs_list = [user.tg_id for user in query_users_id]

    return usewrs_list


def main():
    print(get_registred_users_id())


if __name__ == '__main__':
    main()
