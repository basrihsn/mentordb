import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE users ( 
            user_id serial NOT NULL PRIMARY KEY,
            f_name VARCHAR(30) NOT NULL,
            s_name VARCHAR(30),
            surname VARCHAR(30) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password TEXT NOT NULL )        
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        #for command in commands:
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


#if __name__ == '__main__':
#    create_tables()