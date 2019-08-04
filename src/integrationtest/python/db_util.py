
class DBUtil:

    def create_table(self, db_conn,create_table_sql):
        cursor = db_conn.cursor()
        cursor.execute((create_table_sql))
        cursor.close()

    def insert_into_table(self, db_conn,insert_query):
        cursor = db_conn.cursor()
        cursor.execute(insert_query)
        db_conn.commit()
        cursor.close()

    def drop_table(self, db_conn,drop_table_query):
        cursor = db_conn.cursor()
        cursor.execute((drop_table_query))
        cursor.close()

    def get_row_count(self,db_conn,select_query):
        cursor = db_conn.cursor()
        cursor.execute((select_query))
        final_result = [list(i) for i in cursor]
        return final_result