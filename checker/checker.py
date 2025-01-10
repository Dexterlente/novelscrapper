from database.db_connection import create_connection
from sqlalchemy import text

def get_last_chapter(novel_id):
    engine, _ = create_connection()

    if engine:
        try:
            with engine.connect() as conn:
                query = text("""
                    SELECT last_chapter FROM novels WHERE novel_id = :novel_id;
                """)

                result = conn.execute(query, {'novel_id': novel_id}).fetchone()

                if result:
                    last_chapter = result[0]
                    return (int(last_chapter) + 1) if last_chapter is not None else None
                else:
                    print(f"No novel found with id {novel_id}")
                    return None
        except Exception as e:
            print("Error retrieving last chapter:", e)

    else:
        print("Failed to retrieve last chapter due to connection error.")
        return None
