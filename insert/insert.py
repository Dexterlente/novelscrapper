from db_connection import create_connection

def insert_novel(image_url, title, genre, synopsis, author, last_chapter):
    conn, cursor = create_connection()

    if conn and cursor:
        try:
            insert_novel_query = """
            INSERT INTO novels (image_url, title, genre, synopsis, author, last_chapter)
            VALUES (%s, %s, %s, %s, %s) RETURNING novel_id;
            """
            cursor.execute(insert_novel_query, (image_url, title, genre, synopsis, author, last_chapter))
            novel_id = cursor.fetchone()[0] 
            conn.commit()
            print(f"Novel inserted successfully with ID: {novel_id}")
            return novel_id
        except Exception as e:
            print("Error inserting novel:", e)
            conn.rollback()
        finally:
            cursor.close()
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
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to insert chapter due to connection error.")
