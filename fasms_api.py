import sqlite3, uuid, inspect
import db
from fastapi import FastAPI, Request
from pydantic import BaseModel
from db import create_table, get_dbconn, applicants_table
 
def LINE(): return inspect.currentframe().f_back.f_lineno
# Returns the current line number in our program'''
   
sqlite3_file = "FASMS.db"

app = FastAPI()
create_table( sqlite3_file)

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

    return {'Action':'Added', 'applicant':id, 'debug_line':42}

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
    return {"result": "created", "applicant_id":id, "http": "POST", 'debug_line':82}
    # new applications

### LIST applicants
@app.get("/api/applicants") # all applicates
async def get_all_applicants():
    dbconn = get_dbconn( 'FASMS.db')
    
    print(f"/api/applicants : DB connection : {dbconn}")

    cursor = dbconn.cursor()
    appts = db.applicants_table(cursor)
    
    dbconn.close()
    return { 'action':'get_applicants', 'applicants': appts, 'debug_line':113 }

@app.get("/api/applicants/{name}")
def get_applicants( name) :
    dbconn = get_dbconn( 'FASMS.db')
    
    print(f"LINE 103 ... /api/applicants : Name:{name}, DB connection : {dbconn}")

    cursor = dbconn.cursor()
    appts = db.applicants_table(cursor, name=name)
    
    dbconn.close()

    print(f"get_applicants( '{name}' ) :")
    for appt in appts: print(appt)
    return appts

@app.get("/api/schemes") 
async def get_schemes( ):
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
        return {'action':'get_schemes', 'schemes': all_schemes, 'debug_line':139 }
    except sqlite3.Error as error:
        print(f"Error fetching data: {error}")
        print(f"Error fetching sql: {sql}")
        return {'action':'get_schemes', 'sql':sql, 'error': error, 'debug_line':143 }

    return {"schemes": "None"}


def find_schemes (ts):
    schemes=[]
    print(ts)
    uuid = ts['uuid']
    name = ts['name']
    emp = ts['emp']

    print(f"\n\nFIND SCHEME ( '{uuid}' )")
    dbconn = get_dbconn( 'FASMS.db')
    cursor = dbconn.cursor()

    cursor.execute("SELECT * FROM Schemes")
    rows = cursor.fetchall()
    for row in rows:
        [ _, scheme_name, marrital_status, emp_status, max_household ] = row
        eligible = True    # default
        print(f"\n scheme_name = '{scheme_name}'" )

        # check marrital_status
        marrital_status_list = marrital_status.split("|")
        print(f"[{scheme_name}] -> marrital_status={marrital_status_list}")
        if marrital_status not in marrital_status_list:
            eligible = False
            break

        # check employnent status
        emp_status_list = emp_status.split('|')
        if emp not in emp_status_list:
            eligible = False
            break

        print(f"[{scheme_name}] -> max_household={max_household}" )
        if eligible: schemes.append(scheme_name)
            
    dbconn.close()
    print("ELIGIBLE SCHEM(s) : ", schemes)
    return schemes

@app.get("/api/schemes/eligible")
async def get_schemes_eligible (name):
    print(f"-- get_schemes_eligible( '{name}' )")
    dbconn = get_dbconn( 'FASMS.db')

    cursor = dbconn.cursor()

    print(f"-- applicants_table( cursor, '{name}' )")
    appts = applicants_table( cursor, name)

    print(191)
    if not appts:
        return { 'action':'get_schemes_eligible', 'applicants': [], 'debug_line':158 }
    else:
        print(appts)
        assert(len(appts) > 0)
        name_schemes = dict()

        for ts in appts:
            print(f"\n\n\n LINE 177 >>>>  {ts}")
            uuid = ts['uuid']
            name_schemes[ uuid ] = find_schemes(ts) # update return array
        dbconn.close()
        #appts = db.applicants_table(cursor)
        #        cursor.close()name_scheme
        return {'action':'get_schemes_eligible',
                'eligible_schemes': name_schemes,
                'debug_line':172 }

'''   
{"schemes":[
  {"Scheme_Name":"Single Parent Scheme","Marital_Status":"Widowed|Divorced","Employment_Status":"Employed|Unemployed","Household Size":2},
  {"Scheme_Name":"No Employment Family Scheme","Marital_Status":"Married","Employment_Status":"Unemployed","Household Size":2}
  ]}
'''