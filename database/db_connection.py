from sqlalchemy import create_engine

def create_connection():
    dbname = "novelserver"
    user = "dexter"
    password = "dexter"
    host = "localhost"
    port = 5432
    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
        conn = engine.connect()

        print("Connection to PostgreSQL successful!")
        return engine, conn 
    except Exception as e:
        print("Error connecting to PostgreSQL:", e)
        return None, None