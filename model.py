from asyncio.base_futures import _FINISHED
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, delete, or_


engine = sqlalchemy.create_engine('sqlite:///timetable.db', echo=True)

Base = declarative_base()


class Programs(Base):
    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True)

    title = Column(String)

    type = Column(String)

    modules = relationship(
        "Modules", back_populates="programs",
        cascade="all, delete",
        passive_deletes=True,
        lazy='subquery'
    )

    def __repr__(self):
        return f'{self.id} - {self.title} - {self.type}'

    def __str__(self):
        return f'{self.id} - {self.title} - {self.type}'

    @staticmethod
    def insert(program):
        session = sessionmaker(bind=engine)()
        session.add(program)
        session.commit()
        session.close()

    @staticmethod
    def update(program):
        session = sessionmaker(bind=engine, autocommit=True)()
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

    program_id = Column(Integer, ForeignKey('programs.id', ondelete="CASCADE"))

    programs = relationship("Programs", back_populates="modules", cascade="all, delete",
                            passive_deletes=True,
                            lazy='subquery')

    year = Column(Integer)

    term = Column(Integer)

    optional = Column(Boolean)

    activities = relationship(
        "Activities", back_populates="modules",
        cascade="all, delete",
        passive_deletes=True,
        lazy='subquery'
    )

    def __repr__(self):
        return f'{self.id} - {self.title} [year:{self.year} term:{self.term} {"Optional" if self.optional else "Mandatory"}]'

    def __str__(self):
        return f'{self.id} - {self.title} [year:{self.year} term:{self.term} {"Optional" if self.optional else "Mandatory"}]'

    @staticmethod
    def insert(module):
        session = sessionmaker(bind=engine)()
        session.add(module)
        session.commit()
        session.close()

    @staticmethod
    def update(module):
        session = sessionmaker(bind=engine, autocommit=True)()
        session.query(Modules).filter(Modules.id == module.id).\
            update({
                Modules.title: module.title,
                Modules.program_id: module.program_id,
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

    @staticmethod
    def get_by_program_id(id):
        session = sessionmaker(bind=engine)()
        return session.query(Modules).filter(Modules.program_id == id).all()


class Activities(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)

    module_id = Column(Integer, ForeignKey('modules.id', ondelete="CASCADE"))

    modules = relationship("Modules", back_populates="activities")

    day_of_week = Column(String)

    start = Column(String)

    finish = Column(String)

    def __repr__(self):
        return f'{self.modules} - {self.day_of_week} - {self.start} - {self.finish}'

    def __str__(self):
        return f'{self.modules} - {self.day_of_week} - {self.start} - {self.finish}'

    @staticmethod
    def insert(activity):
        session = sessionmaker(bind=engine)()
        session.add(activity)
        session.commit()
        session.close()

    @staticmethod
    def update(activity):
        session = sessionmaker(bind=engine, autocommit=True)()
        session.query(Activities).filter(Activities.id == activity.id).\
            update({
                Activities.module_id: activity.module_id,
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

    @staticmethod
    def count(activity):
        session = sessionmaker(bind=engine)()
        return session.query(Activities).filter(
            Activities.module_id == activity.module_id,
            Activities.day_of_week == activity.day_of_week,
            Activities.start == activity.start,
            Activities.finish == activity.finish
        ).count()

    @staticmethod
    def get_by_program_year_term(program, year, term, hour):
        session = sessionmaker(bind=engine)()

        result = session.query(Activities).filter(
            Activities.module_id == Modules.id,
            or_(Activities.start == hour, Activities.finish > hour),
            Modules.program_id == program.id,
            Modules.year == year,
            Modules.term == term
        ).all()

        return result


Base.metadata.create_all(engine)
