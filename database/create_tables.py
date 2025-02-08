from db_connection import create_connection
from sqlalchemy import text

def create_tables():
    engine, conn = create_connection()

    if engine and conn:
        try:
            create_novels_table = text("""
            CREATE TABLE IF NOT EXISTS novels (
                novel_id SERIAL PRIMARY KEY,
                image_url VARCHAR(255),
                title VARCHAR(255),
                genre TEXT[],
                synopsis TEXT,
                tags TEXT[],
                author VARCHAR(255),
                last_chapter INTEGER
            );
            """)

            create_chapters_table = text("""
            CREATE TABLE IF NOT EXISTS chapters (
                chapter_id SERIAL PRIMARY KEY,
                novel_id INTEGER NOT NULL,
                title TEXT,
                content TEXT,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                index INTEGER,
                FOREIGN KEY (novel_id) REFERENCES novels(novel_id)
            );
            """)

            conn.execute(create_novels_table)
            conn.execute(create_chapters_table)
            conn.commit()

            print("Tables created successfully!")

        except Exception as e:
            print(f"Error creating tables: {e}")

        finally:
            # Close the connection when done
            conn.close()

if __name__ == '__main__':
    create_tables()
