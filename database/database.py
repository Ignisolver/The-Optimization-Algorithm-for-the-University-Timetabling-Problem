from database_model import engine, Base, Session
Base.metadata.create_all(engine)
session = Session()