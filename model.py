from asyncio.base_futures import _FINISHED
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, delete


engine = sqlalchemy.create_engine('sqlite:///timetable.db', echo=True)

Base = declarative_base()


class Programs(Base):
    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True)

    title = Column(String)

    type = Column(String)

    def __repr__(self):
        return f'{self.title} - {self.type}'

    def __str__(self):
        return f'{self.title} - {self.type}'

    @staticmethod
    def insert(program):
        session = sessionmaker(bind=engine)()
        session.add(program)
        session.commit()
        session.close()

    @staticmethod
    def update(program):
        session = sessionmaker(bind=engine)()
        session.query(Programs).filter(Programs.id == program.id).\
            update({Programs.title: program.title,
                   Programs.type: program.type}, synchronize_session=False)

    @staticmethod
    def delete(id):
        session = sessionmaker(bind=engine)()
        session.query(Programs).filter(Programs.id == id).\
            delete(synchronize_session=False)
        session.commit()
        session.close()

    @staticmethod
    def get_all():
        session = sessionmaker(bind=engine)()
        return session.query(Programs).all()

    @staticmethod
    def get_by_id(id):
        session = sessionmaker(bind=engine)()
        return session.query(Programs).filter_by(id=id).first()


class Modules(Base):
    __tablename__ = 'modules'

    id = Column(Integer, primary_key=True)

    title = Column(String)

    program = Column(Integer, ForeignKey('programs.id'))

    year = Column(Integer)

    term = Column(Integer)

    optional = Column(Boolean)

    def __repr__(self):
        return f'{self.title} - {self.program} - {self.year} - {self.term} - {self.optional}'

    def __str__(self):
        return f'{self.title} - {self.program} - {self.year} - {self.term} - {self.optional}'

    @staticmethod
    def insert(module):
        session = sessionmaker(bind=engine)()
        session.add(module)
        session.commit()
        session.close()

    @staticmethod
    def update(module):
        session = sessionmaker(bind=engine)()
        session.query(Modules).filter(Modules.id == module.id).\
            update({
                Modules.title: module.title,
                Modules.program: module.program,
                Modules.year: module.year,
                Modules.term: module.term,
                Modules.optional: module.optional
            }, synchronize_session=False)

    @staticmethod
    def delete(id):
        session = sessionmaker(bind=engine)()
        session.query(Modules).filter(Modules.id == id).\
            delete(synchronize_session=False)
        session.commit()
        session.close()

    @staticmethod
    def get_all():
        session = sessionmaker(bind=engine)()
        return session.query(Modules).all()

    @staticmethod
    def get_by_id(id):
        session = sessionmaker(bind=engine)()
        return session.query(Modules).filter_by(id=id).first()


class Activities(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)

    module = Column(Integer, ForeignKey('modules.id'))

    day_of_week = Column(String)

    start = Column(String)

    finish = Column(String)

    def __repr__(self):
        return f'{self.module} - {self.day_of_week} - {self.start} - {self.finish}'

    def __str__(self):
        return f'{self.module} - {self.day_of_week} - {self.start} - {self.finish}'

    @staticmethod
    def insert(activity):
        session = sessionmaker(bind=engine)()
        session.add(activity)
        session.commit()
        session.close()

    @staticmethod
    def update(activity):
        session = sessionmaker(bind=engine)()
        session.query(Activities).filter(Activities.id == activity.id).\
            update({
                Activities.module: activity.module,
                Activities.day_of_week: activity.day_of_week,
                Activities.start: activity.start,
                Activities.finish: activity.finish
            }, synchronize_session=False)

    @staticmethod
    def delete(id):
        session = sessionmaker(bind=engine)()
        session.query(Activities).filter(Activities.id == id).\
            delete(synchronize_session=False)
        session.commit()
        session.close()

    @staticmethod
    def get_all():
        session = sessionmaker(bind=engine)()
        return session.query(Activities).all()

    @staticmethod
    def get_by_id(id):
        session = sessionmaker(bind=engine)()
        return session.query(Activities).filter_by(id=id).first()


Base.metadata.create_all(engine)
