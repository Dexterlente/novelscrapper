from database.db_connection import create_connection
from sqlalchemy import text

def insert_novel(image_url, image_cover_url, title, synopsis, author, genre, tags):
    engine, conn = create_connection()
    if isinstance(synopsis, str):
        synopsis_text = synopsis
    else:
        synopsis_text = synopsis.text if hasattr(synopsis, 'text') else str(synopsis)

    if conn:
        try:
            existing_novel_query = text("SELECT novel_id FROM novels WHERE title = :title;")
            result = conn.execute(existing_novel_query, {"title": title})
            existing_novel = result.fetchone()

            if existing_novel:
                print(f"Novel '{title}' already exists. Skipping insertion.")
                return

            insert_novel_query = text("""
            INSERT INTO novels (image_url, image_cover_url, title, synopsis, author, genre, tags)
            VALUES (:image_url, :image_cover_url, :title, :synopsis, :author , :genre, :tags)
            RETURNING novel_id;
            """)

            result = conn.execute(insert_novel_query, {
                "image_url": image_url,
                "image_cover_url": image_cover_url,
                "title": title,
                "synopsis": synopsis_text,
                "author": author,
                "genre": genre,
                "tags": tags
            })

            novel_id = result.fetchone()[0]
            print(f"Novel inserted successfully with ID: {novel_id}")
            conn.commit()
            return novel_id

        except Exception as e:
            print("Error inserting novel:", e)
        finally:
            # Close the connection after the operation
            conn.close()
    else:
        print("Failed to insert novel due to connection error.")

def insert_chapter(novel_id, title, content, index):
    conn, cursor = create_connection()

    if conn and cursor:
        try:

            insert_chapter_query = """
            INSERT INTO chapters (novel_id, title, content, index)
            VALUES (%s, %s, %s, %s) RETURNING chapter_id;
            """

            cursor.execute(insert_chapter_query, (novel_id, title, content, index))
            chapter_id = cursor.fetchone()[0] 
            conn.commit()
            print(f"Chapter inserted successfully with ID: {chapter_id}")
        except Exception as e:
            print("Error inserting chapter:", e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to insert chapter due to connection error.")


def update_last_chapter(novel_id, last_chapter):
    conn, cursor = create_connection()

    if conn and cursor:
        try:
            # SQL query to update the 'last_chapter' of the specific novel
            update_last_chapter_query = """
            UPDATE novels
            SET last_chapter = %s
            WHERE novel_id = %s;
            """
            
            cursor.execute(update_last_chapter_query, (last_chapter, novel_id))

            conn.commit()
            print(f"last_chapter for novel_id {novel_id} updated to {last_chapter}")

        except Exception as e:
            print("Error updating last_chapter:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to update last_chapter due to connection error.")