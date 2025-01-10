from database.db_connection import create_connection

def insert_novel(image_url, image_cover_url, title, genre, synopsis, author, tags):
    conn, cursor = create_connection()

    if conn and cursor:
        try:
            insert_novel_query = """
            INSERT INTO novels (image_url, image_cover_url, title, genre, synopsis, author, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING novel_id;
            """
            cursor.execute(insert_novel_query, (image_url, image_cover_url, title, genre, synopsis, author, tags))
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