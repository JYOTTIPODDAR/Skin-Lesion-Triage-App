from database.database import engine, Base
from database.models import User

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")