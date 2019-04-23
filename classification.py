import pandas   # for dataframes
import psycopg2 # to connect to Postgres
from sklearn.model_selection import train_test_split    # to split test and train data
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier   # forest classifiers
from pandas.api.types import is_string_dtype    # to check which labels to recode
from sklearn.preprocessing import LabelEncoder  # to recode labels
from sklearn.metrics import precision_score, recall_score # for other metrics than accuracy


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

    # from csv
    # dataframe = pandas.read_csv('employee_attrition_full_data.csv')

    # from Postgres
    dataframe = read_data( user, password, host, port, database, sslmode )


    X = dataframe.copy().drop(columns='attrition')
    y = dataframe['attrition'].copy()

    # split data to train and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # class recoding multiple columns
    # https://medium.com/hugo-ferreiras-blog/dealing-with-categorical-features-in-machine-learning-1bb70f07262d
    class MultiColumnLabelEncoder:
        
        def __init__(self, columns = None):
            self.columns = columns # list of column to encode
        def fit(self, X, y=None):
            return self
        def transform(self, X):
            '''
            Transforms columns of X specified in self.columns using
            LabelEncoder(). If no columns specified, transforms all
            STRING type columns in X.
            '''
            
            output = X.copy()
            
            # if no column is specified...
            if self.columns is not None:
                for col in self.columns:
                    output[col] = LabelEncoder().fit_transform(output[col])
            else:
                for colname, col in output.iteritems():
                    # only string columns, except keep the original values
                    if is_string_dtype(col) == True:
                        output[colname] = LabelEncoder().fit_transform(col)
                    else:
                        output[colname] = col
            
            return output
        def fit_transform(self, X, y=None):
            return self.fit(X, y).transform(X)

    # create an instance of the class
    le = MultiColumnLabelEncoder()

    # apply transformation
    X_train_le = le.fit_transform(X_train)
    X_test_le = le.fit_transform(X_test)

    # call modeling function with our transformed data
    modeling(X_train_le, X_test_le, y_train, y_test)

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
        sql = "SELECT * FROM attrition"

        # read data directly to dataframe
        dataframe = pandas.read_sql_query(sql, conn)
        print("data read:\n", dataframe)
        return dataframe


    except:
        print ("I am unable to get data from the database.")


def modeling(xtrain, xtest, ytrain, ytest):
    # feature importance
    model = ExtraTreesClassifier()
    model.fit(xtrain, ytrain)
    print(model.feature_importances_)

    # train and test the model
    extc = ExtraTreesClassifier(max_depth = 10, n_estimators = 25)
    extc.fit(xtrain, ytrain)
    print("accuracy:", extc.score(xtest, ytest))
    y_predicted = extc.predict(xtest)

    # Accuracy = TP+TN/TP+FP+FN+TN
    # Ratio of correctly predicted labels in all observations.
    # Not good in asymmetric datasets as 
    # a model can be highly accurate even if it completely fails in the underrepresented label.

    # checking out other metrics as well
    
    print("precision:", precision_score(ytest, y_predicted, average = 'macro'))
    # Precision = TP/TP+FP
    # Among the ones predicted to leave, how many left actually?

    print("recall:", recall_score(ytest, y_predicted, average = 'macro'))
    # Recall = TP/TP+FN
    # Among the employees truly left, how many are labeled correctly.

if __name__ == "__main__":
    main()