import sqlite3

def get_dbconn(dbfile):
    connection = sqlite3.connect(dbfile)
    return connection

def create_table(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    ### TABLE : applicants
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS  schemes (
            id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            criteria JSONB, 
            last_update DATETIME DEFAULT CURRENT_TIMESTAMP)
        """)
                
        cursor.execute('''CREATE TABLE IF NOT EXISTS  applicants (
                id UUID PRIMARY KEY,
                name VARCHAR(255),
                employment_status VARCHAR(10),
                sex VARCHAR(10),
                date_of_birth DATETIME,
                last_update DATETIME DEFAULT CURRENT_TIMESTAMP
        );''')


        cursor.execute("""CREATE TABLE IF NOT EXISTS  household_person (
            id UUID PRIMARY KEY, 
            applicant_id UUID NOT NULL, 
            name VARCHAR(255) NOT NULL, 
            address VARCHAR(255) NOT NULL,
            income INT NOT NULL,
            last_update DATETIME DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY (applicant_id) REFERENCES applicants(id) ON DELETE CASCADE
        );""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS  benefits (
            id UUID PRIMARY KEY,
            scheme_id UUID NOT NULL, 
            name VARCHAR(255) NOT NULL, 
            amount DECIMAL(10, 2) NOT NULL); 
                       """)

        ## INSERT data into DB
        ## APPLICATION
        insert1="INSERT INTO applicants (id, name, employment_status, sex, date_of_birth)" +\
            " VALUES " +\
            "('01913b7a-4493-74b2-93f8-e684c4ca935c', 'James', 'unemployed', 'male', '1990-07-01'), "+\
            "('01913b80-2c04-7f9d-86a4-497ef68cb3a0', 'Mary', 'unemployed', 'female', '1984-10-06'); "    
        cursor.execute(insert1)



        insert2='''INSERT INTO household (id, applicant_id, name, employment_status, sex, date_of_birth, relation)
        VALUES
        ('01913b88-1d4d-7152-a7ce-75796a2e8ecf', '01913b80-2c04-7f9d-86a4-497ef68cb3a0', 'Gwen', 'unemployed', 'female', '2016-02-01', 'daughter'),
        ('01913b88-65c6-7255-820f-9c4dd1e5ce79', '01913b80-2c04-7f9d-86a4-497ef68cb3a0', 'Jayden', 'unemployed', 'male', '2018-03-15', 'son');
        '''
        cursor.execute(insert2)
        insert3='''
        INSERT INTO schemes (id, name, criteria)
        VALUES
        ('01913b89-9a43-7163-8757-01cc254783f3', 'Retrenchment Assistance Scheme', 
        '{"employment_status": "unemployed"}'),
        ('01913b89-befc-7ae3-bb37-3079aa7f1be0', 'Retrenchment Assistance Scheme (families)', 
        '{"employment_status": "unemployed", "has_children": {"school_level": "primary"}}');
        '''
        cursor.execute(insert3)
        insert4='''
        INSERT INTO benefits (id, scheme_id, name, amount)
        VALUES
        ('01913b8b-9b12-7d2c-a1fa-ea613b802ebc', '01913b89-9a43-7163-8757-01cc254783f3', 'SkillsFuture Credits', 500.00);
        '''
        cursor.execute(insert4)

    except sqlite3.OperationalError as e:
        if "table applicants already exists" in str(e):
            print("Table already exists, skipping creation.")
        else:
            raise e

    # Close the connection
    conn.close()
    return True
