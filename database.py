import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

HighScore = []
bruker = []

def make_database():
    db = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        port=os.getenv("PORT"),
        charset=os.getenv("CHARSET"),
        collation=os.getenv("COLLATION")
    )
    cursor = db.cursor()
    cursor.execute(''' create database if not exists portfoolje; ''')
    db.commit()
    db.close()
    
make_database()

def connect_to_db():
    mydb = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        port=os.getenv("PORT"),
        charset=os.getenv("CHARSET"),
        collation=os.getenv("COLLATION")
    )
    return mydb

def create_database_tables():
    db = connect_to_db()
    cursor = db.cursor()
    
    
    
    cursor.execute('''
        CREATE TABLE if not exists brukere(
        bruker_id INT AUTO_INCREMENT PRIMARY KEY,
        navn VARCHAR(255) NOT NULL,
        etternavn VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        passord VARCHAR(255) NOT NULL, 
        role text NOT NULL default 'user',
        opprettet_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        ''')
    
    cursor.execute('''
            CREATE TABLE if not exists poeng_liste (
            poeng_id INT AUTO_INCREMENT PRIMARY KEY,
            bruker_id INT NOT NULL,
            poeng INT NOT NULL,
            oppnådd_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bruker_id) REFERENCES brukere(bruker_id) ON DELETE CASCADE);
            ''')
    
    cursor.execute('''CREATE TABLE if not exists bokbestillinger (
            bok_id INT AUTO_INCREMENT PRIMARY KEY,
            bruker_id INT NOT NULL,
            Boknavn VARCHAR(255) NOT NULL,
            Sider VARCHAR(255) NOT NULL,
            Ord VARCHAR(255) NOT NULL ,
            Beskrivelse VARCHAR(255) NOT NULL, 
            is_active VARCHAR(255) NOT NULL DEFAULT 'yes',
            opprettet_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bruker_id) REFERENCES brukere(bruker_id) ON DELETE CASCADE);
            ''')
    
    db.commit()
    db.close()

create_database_tables()

def hash_passord(passord):
    passord = passord.encode("utf-8" )
    passord_hashed = bcrypt.hashpw(passord, bcrypt.gensalt())
    return passord_hashed



def opprett_bruker(navn, etternavn, email, passord, role="user"):
    db = connect_to_db()
    cursor = db.cursor()

    passord_hash = hash_passord(passord)
    try:
        sql = "INSERT INTO brukere (navn, etternavn, email, passord, role) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (navn, etternavn, email, passord_hash, role))
        db.commit()
        db.close()
        return "Bruker opprettet!"
    except mysql.connector.IntegrityError:
        return "Email er allerede i bruk."
    
opprett_bruker("Anders", "Christenen", "andersmschristensen@icloud.com", "1234", "admin")

def logg_inn(email, passord):
    db = connect_to_db()
    cursor = db.cursor()

    global bruker, id_bruker
    try:
        sql = "SELECT bruker_id, passord, role, navn FROM brukere WHERE email = %s"
        cursor.execute(sql, (email,))
        bruker = cursor.fetchone()
        db.close()
        id_bruker = bruker
        if bcrypt.checkpw(passord.encode('utf-8'), bruker[1].encode('utf-8')):
            return bruker 
        else:
            return "Feil email eller passord."
    except TypeError:
        return "Feil email eller passord."

def lagre_poeng(bruker, score):
        db = connect_to_db()
        cursor = db.cursor()

        sql = "INSERT INTO poeng_liste (bruker_id, poeng) VALUES (%s, %s)"
        cursor.execute(sql, (bruker[0], score))
        db.commit()
        db.close()

def hent_poeng(bruker):
    db = connect_to_db()
    cursor = db.cursor()

    sql = "SELECT poeng FROM poeng_liste WHERE bruker_id = " + str(bruker[0])
    cursor.execute(sql)
    
    poeng_liste = cursor.fetchall()
    for values in poeng_liste:
        HighScore.append(values[0])
    db.close()

def spiller_poeng():
    poengliste = []
    db = connect_to_db()
    cursor = db.cursor()
    try:
        
        sql = "SELECT poeng, oppnådd_tidspunkt FROM poeng_liste WHERE bruker_id = " + str(id_bruker[0]) + " order by poeng DESC limit 10"
        cursor.execute(sql)
        poengliste.append(cursor.fetchall())


        db.close()
        
        return poengliste

    except NameError:
        return "Logg inn for å se poengliste"
    except TypeError:
        return "Logg inn for å se poengliste"
    except IndexError:
        return "Ingen poeng registrert."


def highscore():
    fullpoengliste = []
    fakstisk_fullpoengliste = []
    
    db = connect_to_db()
    cursor = db.cursor()
    try:
        
        sql = "SELECT poeng, oppnådd_tidspunkt, bruker_id FROM poeng_liste order by poeng DESC limit 20"
        cursor.execute(sql)
        fullpoengliste.append(cursor.fetchall())
        
        for i in range (len(fullpoengliste[0])):
            liste = []
            for j in range (len(fullpoengliste[0][i])):
                liste.append(fullpoengliste[0][i][j])
            fakstisk_fullpoengliste.append(liste)

        for i in range(len(fakstisk_fullpoengliste)):
            sql = "SELECT navn FROM brukere WHERE bruker_id = " + str(fakstisk_fullpoengliste[i][2]) 
            cursor.execute(sql)
            navn = cursor.fetchone()
            fakstisk_fullpoengliste[i].append(navn[0])
       

        db.close()
        
        return fakstisk_fullpoengliste

    except mysql.connector.IntegrityError:
        return "Email er allerede i bruk."
    
def admin_info():
    db = connect_to_db()
    cursor = db.cursor()
    sql = "SELECT * FROM brukere"
    cursor.execute(sql)
    bruker_info = cursor.fetchall()
    db.close()
    
    return bruker_info


def bokbestillinger(bruker_id, Boknavn, Sider, Ord, Beskrivelse):
    db = connect_to_db()
    cursor = db.cursor()
    if bruker_id is not None:
        try:
            sql = "INSERT INTO bokbestillinger  (bruker_id, Boknavn, Sider, Ord, Beskrivelse) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (int(bruker_id), Boknavn, Sider, Ord, Beskrivelse))
            db.commit()
            db.close()
            return "Bokbestilling registrert!"
        except mysql.connector.Error as error:
            return str(error)
    else:
        return "Vennligst logg inn for å bestille bøker."
    

def sebokbestillinger():
    bok_id_liste = []
    db = connect_to_db()
    cursor = db.cursor()
    try:
        bestilling = {"boknavn": [], "sider": [], "ord": [], "beskrivelse": []}
        sql = "SELECT Boknavn FROM bokbestillinger WHERE bruker_id = " + str(id_bruker[0]) + " AND is_active = 'yes'"
        cursor.execute(sql)
        bestilling["boknavn"].append(cursor.fetchall())

        sql = "SELECT Sider FROM bokbestillinger WHERE bruker_id = " + str(id_bruker[0]) + " AND is_active = 'yes'"
        cursor.execute(sql)
        bestilling["sider"].append(cursor.fetchall())

        sql = "SELECT Ord FROM bokbestillinger WHERE bruker_id = " + str(id_bruker[0]) + " AND is_active = 'yes'"
        cursor.execute(sql)
        bestilling["ord"].append(cursor.fetchall())

        sql = "SELECT Beskrivelse FROM bokbestillinger WHERE bruker_id = " + str(id_bruker[0]) + " AND is_active = 'yes'" 
        cursor.execute(sql)
        bestilling["beskrivelse"].append(cursor.fetchall())

    
        sql = "SELECT bok_id FROM bokbestillinger WHERE bruker_id = " + str(id_bruker[0]) + " AND is_active = 'yes'"
        cursor.execute(sql)
        bok_id_liste.append(cursor.fetchall())
        
        db.close()
        liste = [bestilling, bok_id_liste]
        return liste

    except NameError:
        return "Logg inn for å se bestillinger"
    except TypeError:
        return "Logg inn for å se bestillinger"
    except IndexError:

        return "Ingen bokbestilling registrert."

def delete_bestillinger(bokid):
    print(bokid)
    db = connect_to_db()
    cursor = db.cursor()
    print(bokid)
    sql = "update bokbestillinger set is_active = 'no' where bok_id = " + bokid 
    print(sql)
    cursor.execute(sql)
    db.commit()
    db.close()