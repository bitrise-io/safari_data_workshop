import psycopg2
import pandas
import threading


# read configuration file
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

host = config['Postgres']['host']
port = config['Postgres']['port']
database = config['Postgres']['database']
user = config['Postgres']['user']
password = config['Postgres']['password']
table = config['Postgres']['table']
sslmode = config['Postgres']['sslmode']



def main():

    # read csv
    dataframe = pd.read_csv(io.StringIO(uploaded['employee_attrition_data.csv'].decode('utf-8')))

    #dataframe to array
    array = dataframe.values

    # initial sql
    init_sql = '''
        DROP TABLE IF EXISTS attrition;
        
        CREATE TABLE attrition (
            Attrition varchar(3),
            Age int,
            DailyRate int,
            DistanceFromHome int,
            Education int,
            EmployeeCount int,
            EmployeeNumber int,
            EnvironmentSatisfaction int,
            HourlyRate int,
            JobInvolvement int,
            JobLevel int,
            JobSatisfaction int,
            MonthlyIncome int,
            MonthlyRate int,
            NumCompaniesWorked int,
            PercentSalaryHike int,
            PerformanceRating int,
            RelationshipSatisfaction int,
            StandardHours int,
            StockOptionLevel int,
            TotalWorkingYears int,
            TrainingTimesLastYear int,
            WorkLifeBalance int,
            YearsAtCompany int,
            YearsInCurrentRole int,
            YearsSinceLastPromotion int,
            YearsWithCurrManager int
        );
    '''

    # connect to database
    try:
        conn = psycopg2.connect(
                                    user = user,
                                    password = password,
                                    host = host,
                                    port = port,
                                    database = database,
                                    sslmode = sslmode
        )
        cursor = conn.cursor()

    except:
        print ("I am unable to connect to the database.")

    # load initial data
    try:
        for i in array:
        cur.execute(
            "INSERT INTO attrition VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            tuple(i)
        )
        conn.commit

    except:
        print ("I am unable to load data into the database.")


    # wait 5 minutes
    threading.Timer(300.0, main).start()
        
if __name__ == "__main__":
    main()

def prediction():
    pass