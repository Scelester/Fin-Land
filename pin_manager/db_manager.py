import sqlite3

class DBMS:
    
    conn = sqlite3.connect('store/DBMS.db')


    # ----------------------------------------------------------------
    # initialize table creation
    def __init__(self):
        try:
            self.__rdc_creations()
        except sqlite3.OperationalError:
            print('Table already created')


    # ----------------------------------------------------------------
    # rdc table creation
    def __rdc_creations(self):
        self.conn.execute("""CREATE TABLE RDCDATA
                (
                    ID INT PRIMARY KEY NOT NULL,
                    PH FLOAT NOT NULL,
                    TEMP FLOAT NOT NULL,
                    TIMER INT NOT NULL
                );""")

        print("RDC Tables created")

    # update into rdc table
    def update_rdc(self,col,newid,previd):
        self.conn.execute(f"""UPDATE RDCDATA set {col} = {newid} where {col}={previd}""")
        self.conn.commit()
        print(f"{col} column updated successfully")
    
    def get_rdc(self,col):
        data = self.conn.execute(f"select {col} from RDCDATA;")
        self.conn.commit()
        return data.fetchall()[0][0]
        
    def exec(self,sqlscript):
        ret_data = self.conn.execute(sqlscript)
        self.conn.commit()
        return ret_data


       

    # ----------------------------------------------------------------
    def close(self):
        self.conn.close()






if __name__ == "__main__":
    localdbms = DBMS()
    localdbms.close()