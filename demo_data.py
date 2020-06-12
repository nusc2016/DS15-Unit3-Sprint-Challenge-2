import sqlite3

conn = sqlite3.connect('demo.sqlite3')

def make_db():
    """Creating the table"""
    c = conn.cursor()
    c.execute("""Create table if it does not exist demo
                 (a, b, c)""")
    c.close()
    conn.commit()

def addentries():
    """I am adding entries to the table"""
    c = conn.cursor()
    c.execute("""INSERT INTO demo (a, b, c)
                 VALUES
                 ('d', 3, 6),
                 ('x', 4, 7),
                 ('g', 7, 7);""")
    c.close()
    conn.commit()

## I will run queries next
def run_queries():
    """ I will check the data """
    c = conn.cursor()
    print(c.execute('SELECT * from demo;').fetchall())

def more_queries():
    """ If you count the rows, there should be 3 of them.
    -- How many rows are there where both 'x' and 'y' are at least 5?
    -- How many unique values of 'y' are there(hint - 'COUNT()' can accept a keyword
    --'Distinct')?"""
    c = conn.cursor()
    print(c.execute("""SELECT COUNT(*) FROM demo""").fetchall())
    print(c.execute("""SELECT * FROM demo WHERE x > 5 AND y >5""").fetchall())
    print(c.execute("""SELECT COUNT(DISTINCT y) FROM demo""").fectchall())

if __name__ == "__main__":
   make_db()
   addentries()
   run_queries()
   more_queries()
