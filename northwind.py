import sqlite3

conn = sqlite3.connect('northwind_small.sqlite3')

def run_queries():
    """Run the following queries:
       - What are the ten most expensive items (per unit price) in the database?
            1. Côte de Blaye
            2. Thüringer Rostbratwurst
            3. Mishi Kobe Niku
            4. "Sir Rodney's Marmalade"
            5. Carnarvon Tigers
            6. Raclette Courdavault
            7. Manjimup Dried Apples
            8. Tarte au sucre
            9. Ipoh Coffee
            10. Rössle Sauerkraut
       - What is the average age of an employee at the time of their hiring? (Hint: a
         lot of arithmetic works with dates.)
            - Answer - 37.22
       - (*STRETCH*) How does the average age of an employee at hire vary by city?
        """
    c = conn.cursor()
    print(c.execute('SELECT (UnitPrice) FROM Product ORDER BY UnitPrice desc limit 10;').fetchall())
    print(c.execute('SELECT AVG(HireDate - BirthDate) FROM Employee;').fetchall())


def run_queries2():
    """- What are the ten most expensive items (per unit price) in the database *and*
         their suppliers?
            1. Côte de Blaye - Aux joyeux ecclésiastiques
            2. Thüringer Rostbratwurst - Plutzer Lebensmittelgroßmärkte AG
            3. Mishi Kobe Niku - Tokyo Traders
            4. "Sir Rodney's Marmalade" - Specialty Biscuits, Ltd.
            5. Carnarvon Tigers	- Pavlova, Ltd.
            6. Raclette Courdavault - Gai pâturage
            7. Manjimup Dried Apples - "G'day, Mate"
            8. Tarte au sucre - "Forêts d'érables"
            9. Ipoh Coffee - Leka Trading
            10. Rössle Sauerkraut - Plutzer Lebensmittelgroßmärkte AG
       - What is the largest category (by number of uniqe products in it)?
            - Confections which is Category #3
       - (*STRETCH*) Who is the employee with the most territories? Use 'TerritoryId'
         (not name, region, or other fields) as the unique identifier for territories.
    """
    c = conn.cursor
    print(c.execute("""SELECT Product Name, CompanyName, FROM
                         (SELECT * FROM Product
                         INNER JOIN Supplier
                         ON Supplier.Id = Product.Supplier
                         ORDER BY UnitPrice desc limit 10)""").fetchall())
    print(c.execute("""SELECT CategoryName, COUNT(CategoryName) AS cnt FROM
                          (SELECT * FROM Product
                          INNER JOIN Category
                          ON Categor.Id = Product.Category.Id)
                          GROUP BY CategoryName
                          ORDER BY cnt desc
                          LIMIT 1;""").fetchall())



if __name__ == "__main__":
    run_queries()
    run_queries2()