from fastapi import FastAPI
from db import create_db, get_dbconn
import sqlite3
import logging
global log
log = logging.getLogger(__name__)

sqlite3_file = "FASMS.db"

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()
create_db( sqlite3_file)
log.info("sample DB created")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/items/")
async def create_item(item: Item):
    print("create_item : ", Item)
    return item



@app.post("/api/applicants")
##async def create_person( applicant_id:int, name:str, employment_status:str, sex:str, date_of_birth: str, relation:str):
async def create_person( applicant_id:int,  date_of_birth: str):
    print("### ... create_person")
    from UUID import uuid5

    uuid = uuid5()
    #    id UUID PRIMARY KEY,              -- Unique identifier for the household member
    #    applicant_id UUID NOT NULL,       -- Foreign key to the applicants table
    #    name VARCHAR(255) NOT NULL,       -- Household member's name
    #    employment_status VARCHAR(50),    -- Employment status of household member
    #    sex VARCHAR(10),                 -- Gender of household member
    #    date_of_birth DATE,              -- Date of birth of the household member
    #    relation VARCHAR(50),            -- Relation to th

    return {"uuid": uuid}
    assert(0)
    sql = f"""
          INSERT INTO applicants( id, applicant_id, name, employment_status, sex, date_of_birth, relation)
            VALUES(uuid,'{name}','{employment_status}','{sex}, '{date_of_birth}','{relation}');
        """
    print(f"SQL : {sql}")
    connection = dbconn = get_dbconn( 'FASMS.db')
    cursor = connection.cursor()
    cursor.execute( sql)

    connection.close()
    return {"create": "applicant"}

@app.post("/api/application")
def create_application():
    return {"create": "application /api/application POST"}
    # new applications

@app.get("/api/applicants")
def get_applicants():
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

@app.get("/api/schemes")
def get_schemes():
    return {"list": "schemes"}

@app.get("/api/schemes/eligible")
def get_schemes_eligible ():
    assert( False)

