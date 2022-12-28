# import json


# x = json.load(open('pin_manager/state.json','r'))
# print(x.get('RDC_ID'))





import sqlite3


conn = sqlite3.connect('test/test.db')



# conn.execute("CREATE ")


conn.close()