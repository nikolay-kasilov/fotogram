from database import Base, engine, session_factory

with session_factory() as session:
    Base.metadata.create_all(bind=engine)
    session.commit()
