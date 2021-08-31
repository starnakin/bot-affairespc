import mysql.connector
    
class Database:
    def __init__(self, ip, port, user, password, database):
        self.mydb = mysql.connector.connect(
            host=ip,
            user=user,
            password=password,
            port=port
        )

        self.cursor = self.mydb.cursor()

        self.cursor.execute("SHOW DATABASES")

        for database_name in self.cursor:
            if database_name[0] == database:
                break
        else:
            print("No database found")
            self.cursor.execute(f"CREATE DATABASE {database}")
            print("database", database, "has been created [OK]")

        self.mydb = mysql.connector.connect(
            host=ip,
            user=user,
            password=password,
            port=port,
            database=database
        )

        self.cursor = self.mydb.cursor()

        self.cursor.execute("SHOW TABLES")

        result = self.cursor.fetchall()

        if not ("users",) in result:
            print("No users table found")
            self.cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(18))") 
            print("table users has been created [OK]")

        if not ("searchs",) in result:
            print("No searchs table found")
            self.cursor.execute("CREATE TABLE searchs (id INT AUTO_INCREMENT PRIMARY KEY, search TEXT)") 
            print("table searchs has been created [OK]")

        if not ("links",) in result:
            print("No links table found")
            self.cursor.execute("CREATE TABLE links (id INT AUTO_INCREMENT PRIMARY KEY, link TEXT)") 
            print("table links has been created [OK]")

        if not ("user_to_searchs",) in result:
            print("No user_to_searchs table found")
            self.cursor.execute("CREATE TABLE user_to_searchs (id INT AUTO_INCREMENT PRIMARY KEY, user INT, search INT)") 
            print("table user_to_searchs has been created [OK]")

        if not ("user_to_links",) in result:
            print("No user_to_links table found")
            self.cursor.execute("CREATE TABLE user_to_links (id INT AUTO_INCREMENT PRIMARY KEY, user INT, link INT)") 
            print("table user_to_links has been created [OK]")

    def add_user_search(self, user: int, search: str) -> list:

        self.cursor = self.mydb.cursor()
        self.cursor.execute(f"SELECT * FROM users WHERE user={user}")

        myresult = self.cursor.fetchall()

        if not len(myresult) > 0:
            self.cursor.execute(f"INSERT INTO users (user) VALUES ({user})")
            self.mydb.commit()

            self.cursor.execute(f"SELECT * FROM users WHERE user ={user}")

            myresult = self.cursor.fetchall()

        user_id = myresult[0][0]


        self.cursor.execute(f"SELECT * FROM searchs WHERE search='{search}'")

        myresult = self.cursor.fetchall()

        if not len(myresult) > 0:
            self.cursor.execute(f"INSERT INTO searchs (search) VALUES ('{search}')")
            self.mydb.commit()

            self.cursor.execute(f"SELECT * FROM searchs WHERE search ='{search}'")

            myresult = self.cursor.fetchall()

        search_id = myresult[0][0]


        self.cursor.execute(f"SELECT * FROM user_to_searchs WHERE user = {user_id} AND search = '{search_id}'")

        myresult = self.cursor.fetchall()

        if len(myresult) == 0:
            
            self.cursor.execute(f"INSERT INTO user_to_searchs (user, search) VALUES ({user_id}, '{search_id}')")
            self.mydb.commit()

    def add_user_link(self, user: int, link: str) -> list:

        self.cursor = self.mydb.cursor()
        self.cursor.execute(f"SELECT * FROM users WHERE user={user}")

        myresult = self.cursor.fetchall()

        if not len(myresult) > 0:
            self.cursor.execute(f"INSERT INTO users (user) VALUES ({user})")
            self.mydb.commit()

            self.cursor.execute(f"SELECT * FROM users WHERE user ={user}")

            myresult = self.cursor.fetchall()

        user_id = myresult[0][0]


        self.cursor.execute(f"SELECT * FROM links WHERE link='{link}'")

        myresult = self.cursor.fetchall()

        if not len(myresult) > 0:
            self.cursor.execute(f"INSERT INTO links (link) VALUES ('{link}')")
            self.mydb.commit()

            self.cursor.execute(f"SELECT * FROM links WHERE link ='{link}'")

            myresult = self.cursor.fetchall()

        link_id = myresult[0][0]


        self.cursor.execute(f"SELECT * FROM user_to_links WHERE user = {user_id} AND link = '{link_id}'")

        myresult = self.cursor.fetchall()

        if len(myresult) == 0:
            
            self.cursor.execute(f"INSERT INTO user_to_links (user, link) VALUES ({user_id}, '{link_id}')")
            self.mydb.commit()

    def get_user_searchs(self, user: int):

        self.cursor = self.mydb.cursor()
        self.cursor.execute(f"SELECT * FROM users WHERE user={user}")

        myresult = self.cursor.fetchall()

        if len(myresult) > 0:

            user_id = myresult[0][0]

            self.cursor.execute(f"SELECT * FROM user_to_searchs WHERE user={user_id}")
            myresult = self.cursor.fetchall()

            searchs=[]
            for i in myresult:
                self.cursor.execute(f"SELECT * FROM searchs WHERE id={i[2]}")
                myresult = self.cursor.fetchall()
                searchs.append(myresult[0][1])
            
            return(searchs)

        else:
            return []

    def get_user_links(self, user: int):

        self.cursor = self.mydb.cursor()
        self.cursor.execute(f"SELECT * FROM users WHERE user={user}")

        myresult = self.cursor.fetchall()

        print(myresult)

        if len(myresult) > 0:

            user_id = myresult[0][0]

            print(user_id)

            print(f"SELECT * FROM user_to_links WHERE user={user_id}")
            self.cursor.execute(f"SELECT * FROM user_to_links WHERE user={user_id}")
            myresult = self.cursor.fetchall()

            print(myresult)

            links=[]
            for i in myresult:
                print(i)
                self.cursor.execute(f"SELECT * FROM links WHERE id={i[2]}")
                myresult = self.cursor.fetchall()
                print(myresult)
                links.append(myresult[0][1])
            
            return(links)

        else:
            return []
    
    def get_all_searchs(self):

        self.cursor = self.mydb.cursor()
        self.cursor.execute(f"SELECT * FROM searchs")

        myresult = self.cursor.fetchall()
        searchs = []
        for i in myresult:
            searchs.append(i[1])
        return searchs
    
    def get_users_by_search(self, search) -> list[int]:
        self.cursor = self.mydb.cursor()
        self.cursor.execute(f"SELECT * FROM searchs WHERE search='{search}'")
        myresult = self.cursor.fetchall()

        search_id = myresult[0][0]

        self.cursor.execute(f"SELECT * FROM user_to_searchs WHERE search={search_id}")
        myresult = self.cursor.fetchall()

        user_ids=[]
        for i in myresult:
            user_ids.append(i[1])
        users=[]
        for user_id in user_ids:
            self.cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
            myresult = self.cursor.fetchall()
            users.append(int(myresult[0][1]))
        
        return users



