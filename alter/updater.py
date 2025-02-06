from database.db_connection import create_connection
from sqlalchemy import text


def update_subchapters():
    engine, conn = create_connection()

    if conn:
        try:
            query = text("""
            WITH RankedChapters AS (
                SELECT c.chapter_id,
                    ROW_NUMBER() OVER (PARTITION BY c.novel_id, c.index ORDER BY c.timestamp) AS subchapter
                FROM chapters c
                WHERE EXISTS (
                    SELECT 1
                    FROM chapters c2
                    WHERE c2.novel_id = c.novel_id AND c2.index = c.index
                    HAVING COUNT(*) > 1
                )
            )
            UPDATE chapters c
            SET subchapter = rc.subchapter
            FROM RankedChapters rc
            WHERE c.chapter_id = rc.chapter_id
            AND c.subchapter IS NULL;
            """
            )
            conn.execute(query)
            conn.commit()
            print("Subchapters updated successfully!")

        except Exception as e:
            print("Error updating subchapters:", e)
        finally:
            conn.close()
    else:
        print("Failed to update subchapters due to connection error.")