import sqlite3
try:
    conn=sqlite3.connect('C:\\Users\\HP\\Documents\\PythonWorks\\sqlite-tools-win32-x86-3330000\\test.db')
    print("succeeded")
except Exception as e:
    print("error: "+str(e))
results=conn.execute("select * from maintain")
for row in results:
    print (row)
conn.close()