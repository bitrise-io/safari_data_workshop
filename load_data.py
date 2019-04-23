import psycopg2
import pandas

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
    # run 
    load_data( user, password, host, port, database, sslmode )


def load_data(user_param, pw_param, host_param, port_param, db_param, sslmode_param):

    # read csv
    dataframe = pandas.read_csv('employee_attrition_full_data.csv')

    #dataframe to array
    array = dataframe.values

    # initial sql
    init_sql = '''
        DROP TABLE IF EXISTS attrition;
        
        CREATE TABLE attrition (
            Age                      int,
            Attrition                varchar(3),
            BusinessTravel           varchar(50),
            DailyRate                int,
            Department               varchar(50),
            DistanceFromHome         int,
            Education                int,
            EducationField           varchar(50),
            EmployeeCount            int,
            EmployeeNumber           int,
            EnvironmentSatisfaction  int,
            Gender                   varchar(50),
            HourlyRate               int,
            JobInvolvement           int,
            JobLevel                 int,
            JobRole                  varchar(50),
            JobSatisfaction          int,
            MaritalStatus            varchar(50),
            MonthlyIncome            int,
            MonthlyRate              int,
            NumCompaniesWorked       int,
            Over18                   varchar(1),
            OverTime                 varchar(3),
            PercentSalaryHike        int,
            PerformanceRating        int,
            RelationshipSatisfaction int,
            StandardHours            int,
            StockOptionLevel         int,
            TotalWorkingYears        int,
            TrainingTimesLastYear    int,
            WorkLifeBalance          int,
            YearsAtCompany           int,
            YearsInCurrentRole       int,
            YearsSinceLastPromotion  int,
            YearsWithCurrManager     int
        );
    '''

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

    # create table
    try:
        cursor.execute(
            init_sql
        )
        conn.commit

    except:
        print ("I am unable to create the table.")    

    # load initial data
    for i in array[0:100]:
        try:
            cursor.execute(
                "INSERT INTO attrition VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                i
            )
            print("Record loaded.")

        except:
            print ("I am unable to load record into the database.")
            raise

        
if __name__ == "__main__":
    main()