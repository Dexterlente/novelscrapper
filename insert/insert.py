from database.db_connection import create_connection
from sqlalchemy import text

def insert_novel(image_url, image_cover_url, title, synopsis, author, genre, tags):
    engine, conn = create_connection()
    
    synopsis_text = str(synopsis) if not isinstance(synopsis, str) else synopsis

    if conn:
        try:
            existing_novel_query = text("SELECT novel_id FROM novels WHERE title = :title;")
            result = conn.execute(existing_novel_query, {"title": title})
            existing_novel = result.fetchone()

            if existing_novel:
                print(f"Novel '{title}' already exists. Skipping insertion.")
                novel_id = existing_novel[0]
                return novel_id

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
            conn.close()
    else:
        print("Failed to insert novel due to connection error.")

def insert_chapter(novel_id, title, content, index):
    engine, conn = create_connection()

    content_text = str(content) if not isinstance(content, str) else content

    if not title or not content_text.strip():
        print("Title or content is empty, skipping chapter insertion.")
        return None

    if conn:
        try:
            existing_chapter_query = text("SELECT novel_id FROM chapters WHERE title = :title;")
            result = conn.execute(existing_chapter_query, {"novel_id": novel_id, "title": title})
            existing_chapter = result.fetchone()

            if existing_chapter:
                print(f"Chapter '{title}' already exists in chapters table.")
                return None
                
            insert_chapter_query = text("""
            INSERT INTO chapters (novel_id, title, content, index)
            VALUES (:novel_id, :title, :content, :index) 
            RETURNING chapter_id;
            """)

            result = conn.execute(insert_chapter_query, {
                "novel_id": novel_id,
                "title": title, 
                "content": content_text, 
                "index": index
                })

            chapter_id = result.fetchone()[0] 
            conn.commit()
            print(f"Chapter inserted successfully with ID: {chapter_id}")
            return chapter_id
        except Exception as e:
            print("Error inserting chapter:", e)
            return None
        finally:
            conn.close()
    else:
        print("Failed to insert chapter due to connection error.")
        return None

def update_last_chapter(novel_id, last_chapter):
    engine, conn = create_connection()

    if conn:
        try:
            update_last_chapter_query = text("""
            UPDATE novels
            SET last_chapter = :last_chapter
            WHERE novel_id = :novel_id;
            """)
            
            conn.execute(update_last_chapter_query, {
                "last_chapter": last_chapter,
                "novel_id": novel_id
                 })

            conn.commit()
            print(f"last_chapter for novel_id {novel_id} updated to {last_chapter}")

        except Exception as e:
            print("Error updating last_chapter:", e)
        finally:
            conn.close()
    else:
        print("Failed to update last_chapter due to connection error.")