import sqlite3

class DBMS:
    
    conn = sqlite3.connect('store/DBMS.db')

    def __init__(self):
        try:
            self.__rdc_creations()
        except sqlite3.OperationalError:
            print('Table already created')



    def __rdc_creations(self):
        self.conn.execute("""
                CREATE TABLE RDCDATA
                (
                    ID INT PRIMARY KEY NOT NULL,
                    PH FLOAT NOT NULL,
                    TEMP FLOAT NOT NULL
                );
            """)
        
        print("RDC Tables created")


    def close(self):
        self.conn.close()


if __name__ == "__main__":
    localdbms = DBMS()
    localdbms.close()