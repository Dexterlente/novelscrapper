from database.db_connection import create_connection

def get_last_chapter(novel_id):
    conn, cursor = create_connection()

    if conn and cursor:
        try:
            # Define the SQL query to get the last chapter for a given novel_id
            query = """
                SELECT last_chapter FROM novels WHERE novel_id = :novel_id;
            """
            cursor.execute(query, {'novel_id': novel_id})
            result = cursor.fetchone()
            
            if result:
                return (int(result[0]) + 1) if result[0] is not None else None
            else:
                print(f"No novel found with id {novel_id}")
                return None
        except Exception as e:
            print("Error retrieving last chapter:", e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to retrieve last chapter due to connection error.")
        return None
