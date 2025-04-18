class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/crowdcheck'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
