import sqlite3
import sqlite3, uuid, inspect

def get_uuid(): return uuid.uuid4()

def get_dbconn(dbfile):
    connection = sqlite3.connect(dbfile)
    return connection

def create_table(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        ### TABLE : household
        bishan_id = get_uuid()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS 
                        household ( id UUID PRIMARY KEY,
                                    address VARCHAR(255) NOT NULL,
                                    income INT NOT NULL,
                                    last_update DATETIME DEFAULT CURRENT_TIMESTAMP);
                       ''')
        cursor.execute(f'''
                       INSERT INTO household ( id,
                                               address,
                                               income)
                       VALUES ( "{bishan_id}", "#08-09 Bishan St 64", 5000)  
                       ''')

        cursor.execute("CREATE TABLE IF NOT EXISTS \
                        schemes ( id UUID           PRIMARY KEY,\
                                  Scheme_Name       VARCHAR(255), \
                                  Marital_Status    VARCHAR(255), \
                                  Employment_Status VARCHAR(255), \
                                  Household_Size Int,             \
                                  last_update DATETIME DEFAULT CURRENT_TIMESTAMP); ")
        print("TABLE : schemes CREATED")

        # family scheme
        cursor.execute("""INSERT INTO schemes( name, marital_status, employment_status, household_number) 
            VALUES
               ('Single Parent Scheme',       'Widowed|Divorced', 'Employed|Unemployed' , 2),
               ('No Employment Family Scheme','Married',          'Unemployed',           2);
        """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS  household (
            applicant_id UUID PRIMARY KEY, 
            name VARCHAR(255) NOT NULL, 
            address VARCHAR(255) NOT NULL,
            income INT NOT NULL,
            last_update DATETIME DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY (applicant_id) REFERENCES applicants(id) ON DELETE CASCADE
        );""")
        print("TABLE : household_person CREATED")





        cursor.execute("""CREATE TABLE IF NOT EXISTS  benefits (
            id UUID PRIMARY KEY,
            scheme_id UUID PRIMARY KEY, 
            name VARCHAR(255) NOT NULL, 
            amount DECIMAL(10, 2) NOT NULL); 
                       """)
        print("TABLE : benefits CREATED")

        cursor.execute('''CREATE TABLE IF NOT EXISTS  applicants (
                id UUID PRIMARY KEY,
                name VARCHAR(255) PRIMARY KEY,
                employment_status VARCHAR(10),
                sex VARCHAR(10),
                date_of_birth DATETIME PRIMARY KEY,
                household_id UUID DEFAULT NULL,
                last_update DATETIME DEFAULT CURRENT_TIMESTAMP
        );''')
        print("TABLE : applicants CREATED")

        cursor.execute("""CREATE TABLE IF NOT EXISTS  applications (
            id UUID PRIMARY KEY,
            scheme_id UUID    PRIMARY KEY, 
            applicant_id UUID PRIMARY KEY, 
            last_update DATETIME DEFAULT CURRENT_TIMESTAMP
                       )""")
        print("# TABLE : applications CREATED")

    except sqlite3.OperationalError as e:
        if "table applicants already exists" in str(e):
            print("Table already exists, skipping creation.")
        else:
            raise e

    # Close the connection
    conn.close()
    return True

def applicants_table( cursor, name=None):
    sql = "SELECT id, name, employment_status, sex, date_of_birth FROM applicants "
    if name: sql = sql + f" WHERE name LIKE '%{name}%' "
    appts = []
    print("db.py -> 103")

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        # Print the table header
        print(f"------------------------------")
        appts=[]
        for row in rows:
            print( row )
            (uuid, name, emp, sex, bod) = row
            # ('01913b7a-4493-74b2-93f8-e684c4ca935c', 'James', 'unemployed', 'male', '1990-07-01')
            appts.append( {'uuid':uuid, 'name':name, 'emp':emp, 'sex':sex} )

    except sqlite3.Error as error:
        print(f"Error fetching data: {error}")
        print(f"Error fetching sql: {sql}")
        return {"list": [1,2,3,4,5, f"Error fetching data: {error}" ]}
    return appts
