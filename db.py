import sqlite3

def get_dbconn(dbfile):
    connection = sqlite3.connect(dbfile)
    return connection

def create_table(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    ### TABLE : applicants
    try:
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

        cursor.execute("""CREATE TABLE IF NOT EXISTS  household_person (
            id UUID PRIMARY KEY, 
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
