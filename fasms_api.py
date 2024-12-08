import sqlite3
import logging
import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from db import create_table, get_dbconn

global log
log = logging.getLogger(__name__)

sqlite3_file = "FASMS.db"

from fastapi import FastAPI

app = FastAPI()
create_table( sqlite3_file)
log.info("sample DB created")

### CREAT NEW
@app.post("/api/applicants/{applicant_id}")
async def create_applicant():
    print("### ... create_applicant : {applicant_id}")

    id = uuid.uuid4()
    sql = f"""
          INSERT INTO applicants( id, name, employment_status, sex, date_of_birth)
            VALUES('{id}','name','employment_status','sex', 'date_of_birth');
        """
    print(f"SQL : {sql}")
    connection = dbconn = get_dbconn( 'FASMS.db')
    cursor = connection.cursor()
    cursor.execute( sql)

    connection.close()
    return {"create": "applicant"}

### CREAT NEW APPLICATOPM
@app.post("/api/application/{applicant_id}")
async def create_application(applicant_id):
    
    return {"create": "application", "applicant_id":applicant_id, "http": "POST"}
    # new applications

@app.get("/api/applicants") ######
async def get_applicants():
    dbconn = get_dbconn( 'FASMS.db')

    log.info("DB connection : %s", str(dbconn))
    log.debug("DB : %s", dbconn)
    '''
        table = """CREATE TABLE applicants (
        id UUID PRIMARY KEY,              -- Unique identifier for the applicant
        name VARCHAR(255) NOT NULL,        -- Applicant's name
        employment_status VARCHAR(50),     -- Employment status (e.g., unemployed)
        sex VARCHAR(10),                  -- Gender (e.g., male, female)
        date_of_birth DATE
    );
    '''
    cursor = dbconn.cursor()
    sql = "SELECT * FROM applicants "
    appts = []

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        # Print the table header
        print(f"------------------------------")
        #print(f"Content of table 'applicants':")
        #print(*[column[0] for column in cursor.description], sep='\t')

        # Print the table rows
        for row in rows:
            (uuid, name, emp, sex, address) = row
            # ('01913b7a-4493-74b2-93f8-e684c4ca935c', 'James', 'unemployed', 'male', '1990-07-01')
            appts.append( {'uuid':uuid, 'name':name, 'emp':emp, 'sex':sex, 'address':address} )

        #{"applicants": [1,2,3,4,5]}
        dbconn.close()
        return { 'applicants': appts }
    except sqlite3.Error as error:
        print(f"Error fetching data: {error}")
        print(f"Error fetching sql: {sql}")
        return {"list": [1,2,3,4,5, f"Error fetching data: {error}" ]}

@app.get("/api/schemes") ######
async def get_schemes():
    dbconn = get_dbconn( 'FASMS.db')
    cursor = dbconn.cursor()
    sql = "SELECT * FROM schemes; "
    appts = []

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Print the table rows
        for row in rows:
            (id, name, criteria) = row
            appts.append( {'uuid':id, 'name':name, 'criteria':criteria} )
        print( "schemes : \n", appts )
        dbconn.close()
        return { 'schemes': appts }
    except sqlite3.Error as error:
        print(f"Error fetching data: {error}")
        print(f"Error fetching sql: {sql}")
        return {"list": [1,2,3,4,5, f"Error fetching data: {error}" ]}

    return {"schemes": "None"}

@app.get("/api/schemes/eligible")
async def get_schemes_eligible ():
    assert( False)

