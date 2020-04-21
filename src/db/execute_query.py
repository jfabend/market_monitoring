import psycopg2

class QueryExecution():

    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def execute_query(self, query_string):
        #try:
        #    conn = psycopg2.connect(database = "projetofinal", user = "postgres", password = "admin", host = "localhost", port = "5432")
        #except:
        #    print("I am unable to connect to the database") 

        #cur = conn.cursor()
        try:
            self.cur.execute(query_string)
        except:
            print("I can't drop our test database!")

        self.conn.commit() # <--- makes sure the change is shown in the database
