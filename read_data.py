import psycopg2


# read configuration file
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

host = config['Postgres']['host']
port = config['Postgres']['port']
database = config['Postgres']['database']
user = config['Postgres']['user']
password = config['Postgres']['password']
sslmode = config['Postgres']['sslmode']



def main():
    read_data( user, password, host, port, database, sslmode )

def read_data(user_param, pw_param, host_param, port_param, db_param, sslmode_param):

    # try to connect to the database
    try:
        conn = psycopg2.connect(
                                    user = user_param,
                                    password = pw_param,
                                    host = host_param,
                                    port = port_param,
                                    database = db_param,
                                    sslmode = sslmode_param
        )
        cursor = conn.cursor()

    except:
        print ("I am unable to connect to the database.")


    # read table
    try:
        cursor.execute(
            "SELECT * FROM attrition"
        )
        conn.commit

        for record in cursor.fetchall():
            print(record)

    except:
        print ("I am unable to read the table.")
        raise  

# this checks whether our module is the main program
if __name__ == "__main__":
    main()