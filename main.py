# Scrapping the Chartered Institute of Bankers Website

import pandas as pd
from sqlalchemy import create_engine
from extraction import CIBScrapper

# DEFINE THE DATABASE CREDENTIALS
# change these values to your personal db params
user = 'edu_user'
password = 'edungwo1'
host = '127.0.0.1'
port = 5432
database = 'analysis'


# PYTHON FUNCTION TO CONNECT TO THE POSTGRESQL DATABASE AND
# RETURN THE SQLALCHEMY ENGINE OBJECT
def get_connection():
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )


def main():
    # the db engine would be used to insert data into a postgresdb
    engine = get_connection()

    website = "https://cibng.org/bank-directory?page=1"
    data = CIBScrapper(website, test=False)
    result = data.scrape_cib_data()
    result_df = pd.DataFrame.from_records(result)
    result_df.to_csv("test2.csv", index=False)
    result_df.to_sql(name='ci_bankers', con=engine, if_exists='append', index=False)


# Run the script.
if __name__ == '__main__':
    main()
