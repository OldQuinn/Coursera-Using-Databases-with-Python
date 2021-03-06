import sqlite3   #用于生成database
import re

conn = sqlite3.connect('countEmails.sqlite')   #用于生成database，如果文件名不存在就生成这个文件。
cur = conn.cursor()
#************************************************************
#此处相当于在SQL中执行的语句
cur.execute('''
    DROP TABLE IF EXISTS Counts''')  #如果村子Counts就drop掉

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')   #创建表格
#**************************************************************
fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue
    line = line.rstrip()
    # Find email domain using regular expression
    #x = re.findall('^From.[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,6})', line)
    x = re.findall('[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,6})', line)
    if len(x) > 0:
        domain = x[0]
        cur.execute('SELECT count FROM Counts WHERE org = ? ', (domain, ))
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO Counts (org, count)
                 VALUES ( ?, 1 )''', ( domain, ) )
        else :
            cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', (domain, ))
        conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr) :
    print (str(row[0]), row[1])

cur.close()
