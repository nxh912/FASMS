import sqlite3
import logging
import uuid

from fastapi import FastAPI, Request
from pydantic import BaseModel

from db import create_table, get_dbconn

import inspect
 
def LINE():
   '''Returns the current line number in our program'''
   return inspect.currentframe().f_back.f_lineno

global log
log = logging.getLogger(__name__)

sqlite3_file = "FASMS.db"

from fastapi import FastAPI

app = FastAPI()
create_table( sqlite3_file)
log.info("sample DB created")

def get_uuid(): return uuid.uuid4()


### CREATE NEW applicant
@app.post("/api/applicants")
async def create_applicant(req: Request):
    body_dict = await req.json()
    print("[body_dict]  ==> ", body_dict)
    valid = True

    for field in ['name', 'employment_status', 'sex', 'date_of_birth']:
        if field not in body_dict:
            valid = False
            break
    if not valid:
        return {"result": False, "Message": "Invalid Format"}

    print(f"### [POST] request BODY .. {  ( body_dict )}")
    id = get_uuid()
    sql = f"""
          INSERT INTO applicants( id, name, employment_status, sex, date_of_birth, household_id)
            VALUES('{id}','{body_dict['name']}','{body_dict['employment_status']}','{body_dict['sex']}', '{body_dict["date_of_birth"]}', NULL);
        """
    print(f"### [SQL]  { sql }")
    connection = dbconn = get_dbconn( 'FASMS.db')
    cursor = connection.cursor()
    cursor.execute( sql)
    connection.commit()

    return {'Action':'Added', 'applicant':id, 'line':54}


    id = get_uuid()
    sql = f"""
          INSERT INTO applicants( id, name, employment_status, sex, date_of_birth)
            VALUES('{id}','name','employment_status','sex', 'date_of_birth');
        """
    print(f"SQL : {sql}")
    connection = dbconn = get_dbconn( 'FASMS.db')
    cursor = connection.cursor()
    cursor.execute( sql)

    connection.close()
    return {"create": "applicant", 'Line':68}

### CREAT NEW APPLICATOPM
@app.post("/api/application")
async def create_application(req: Request):
    body_dict = await req.json()
    print("line74 [body_dict]  ==> ", body_dict)


    '''
Application
| **id**        |  UUID        | Primary Key    |
| scheme_id     | UUID         |FD to Scheme    |
| applicant_id  | UUID         |FD to Applicants|
| last_update   | DATETIME     |systime         |
    '''
    valid = True
    for field in ['name', 'employment_status', 'sex', 'date_of_birth']:
        if field not in body_dict:
            valid = False
            break
    if not valid:
        return {"result": False, "Message": "Invalid Format"}

    print(f"### [POST] request BODY .. {  ( body_dict )}")
    id = get_uuid()
    sql = f"""
          INSERT INTO applicants( id, name, employment_status, sex, date_of_birth)
            VALUES('{id}','{body_dict['name']}','{body_dict['employment_status']}','{body_dict['sex']}', '{body_dict['date_of_birth']}');
        """
    print(f"### [SQL]  { sql }")
    dbconn = get_dbconn( 'FASMS.db')
    cursor = dbconn.cursor()
    cursor.execute(sql)
    cursor.close()
    dbconn.close()
    return {"result": "created", "applicant_id":id, "http": "POST"}
    # new applications

### LIST applicants
@app.get("/api/applicants") ######
async def get_applicants():
    dbconn = get_dbconn( 'FASMS.db')
    
    print(f"/api/applicants : DB connection : {dbconn}")

    '''
        table = """CREATE TABLE applicants (
        id UUID PRIMARY KEY,              -- Unique identifier for the applicant
        name VARCHAR(255) NOT NULL,        -- Applicant's name
        employment_status VARCHAR(50),     -- Employment status (e.g., unemployed)
        sex VARCHAR(10),                  -- Gender (e.g., male, female)
        household_id UUID                 -- forign key to household
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
        appts=[]
        for row in rows:
            print( row )
            (uuid, name, emp, sex, bod, address, _) = row
            # ('01913b7a-4493-74b2-93f8-e684c4ca935c', 'James', 'unemployed', 'male', '1990-07-01')
            appts.append( {'uuid':uuid, 'name':name, 'emp':emp, 'sex':sex, 'address':address} )
        print("appts : ", appts)
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
    sql = "SELECT name, marital_status, employment_status, household_number FROM schemes; "
    all_schemes = []
    print("/api/schemes : ")
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Print the table rows
        for row in rows:
            (name, marital, emp_status, household) = row
            scheme_item = {'Scheme_Name':name, 'Marital_Status': marital, 
                           'Employment_Status': emp_status,
                           'Household Size':household}
            all_schemes.append( scheme_item)

        dbconn.close()
        return { 'schemes': all_schemes }
    except sqlite3.Error as error:
        print(f"Error fetching data: {error}")
        print(f"Error fetching sql: {sql}")
        return {"list": [1,2,3,4,5, f"Error fetching data: {error}" ]}

    return {"schemes": "None"}

@app.get("/api/schemes/eligible")
async def get_schemes_eligible ():
    assert( False)

