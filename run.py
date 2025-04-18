from app import create_app, db

app = create_app()

with app.app_context():
    # Check if tables exist — if not, create them
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()

    if not existing_tables:
        print("No tables found. Creating database tables...")
        db.create_all()
    else:
        print("Tables already exist. Skipping db.create_all().")

if __name__ == '__main__':
    app.run(debug=True)
