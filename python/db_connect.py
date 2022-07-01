from sqlite3 import connect as _dbc
from sqlite3 import OperationalError
from platform import system as _pl

# Constant variable
DB_NAME = "default.db"
STRUCT = "CREATE TABLE MOVIES( id, name , actor , actress , director , year );"

if(not _pl().lower().startswith("window")):
    R, N, G, I, Y = "\033[31;1m", "\u001b[00m", "\u001b[32;1m", "\u001b[7;1m", "\u001b[33;1m"
else:
    R,N,G,I,Y = ''

TITLE = ["name", "actor", "actress", "director", "year"]

class Class_db():

    def __init__(self, db_name = DB_NAME):
        self.db = _dbc(db_name)
        self.id_ = 1
        try:
            open(DB_NAME, 'rb').close()
            self.getsize()
        except:
            self.db.execute(STRUCT)
            self.commit()

    def getsize(self):
        try:
            for i in self.db.execute("SELECT * FROM MOVIES"):
                self.id_ += 1
        except:
            pass

    def show_title(self):
        [ print('{}{:<10}|{}'.format(I,x,N), end='') for x in ['id'] + TITLE ]
        print()

    def show(self):
        try:
            self.show_title()
            for i in self.db.execute("SELECT * FROM MOVIES"):
                for j in i:
                    print(f"{j:<10}|", end="")
                print()
        except OperationalError:
            print(f"{R}[!]{N} It scheams to be their is no database")

    def delete(self, key):
        key = [ x.strip() for x in key.split(":") ]
        self.db.execute(f"DELETE FROM MOVIES WHERE {key[0]}=\"{key[1]}\";")
        self.commit()
        
    def search(self, key):
        try:
            self.show_title()
            key = [ x.strip() for x in key.split(":") ]
            for i in self.db.execute(f"SELECT * FROM MOVIES WHERE {key[0]}=\"{key[1]}\";"):
                for j in i:
                    print(f"{j:<10}|", end="")
                print()
        except KeyboardInterrupt:
            print(f"{R}[!]{N} It scheams to be their is no database")
        
    def insert(self, name, actor , actress, director, y):
        try:
            self.db.execute(f'INSERT INTO MOVIES VALUES( "{self.id_}","{name}","{actor}", "{actress}","{director}","{y}");')
            self.id_ += 1
            self.commit()
        except OperationalError:
            self.db.execute(STRUCT)
            self.commit()
            self.insert( name, actor , actress, director, y)
    def commit(self):
        self.db.commit()



# Interface:

def main():
    cdb = Class_db()
    f = 1
    name = DB_NAME
    while(1):
        print(f"""
 {G}✓{N}  {name}  {Y}(Active){N}

<1> Set data base  | Default value is default
<2> Insert details | Insert detail.
<3> Show details   | shows all the details.
<4> Search with    | <column>:<search> example: name:kamal
<5> Delete with    | <column>:<value> example: name:kamal
<6> Exit           | exit application.\n\n\n""")
        opt = int(input("Option: "))
        if(opt == 1):
            name = input(f"Enter Name for the database[{name}]:").strip()
            if(name):
                name += ".db"
                cdb = Class_db(name)
        elif(opt == 2):
            data = []
            for i in TITLE:
                t = input(f"Enter data for [{i}]: ").strip()
                if(t):
                    data.append(t)
                else:
                    f = 0
            if(f):
                cdb.insert( data[0], data[1], data[2], data[3], data[4])
        elif(opt == 3):
            cdb.show()
        elif(opt == 4):
            n = input(f"Search <key:value>:").strip()
            if(n):
                cdb.search(n)
        elif(opt == 5):
            n = input(f"Delete <key:value>:").strip()
            if(n):
                cdb.delete(n)
        elif(opt == 6):
            return

main()



