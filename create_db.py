import sqlite3

def create_db(dbfile):
    # Connect to the SQLite database
    connection = sqlite3.connect('FASMS.db')

    # Create a cursor object
    cursor = connection.cursor()

    # Create table applicants
    table = """CREATE TABLE applicants (
        id UUID PRIMARY KEY,              -- Unique identifier for the applicant
        name VARCHAR(255) NOT NULL,        -- Applicant's name
        employment_status VARCHAR(50),     -- Employment status (e.g., unemployed)
        marital_status VARCHAR(20),       -- 
        sex VARCHAR(10),                  -- Gender (e.g., male, female)
        date_of_birth DATE
    );
    """
    cursor.execute(table)

    # Create table household
    table = """CREATE TABLE household (
        id UUID PRIMARY KEY,              -- Unique identifier for the household member
        applicant_id UUID NOT NULL,       -- Foreign key to the applicants table
        name VARCHAR(255) NOT NULL,       -- Household member's name
        employment_status VARCHAR(50),    -- Employment status of household member
        sex VARCHAR(10),                 -- Gender of household member
        marrital_status VARCHAR(10),     -- Single /Married /Divorced
        date_of_birth DATE,              -- Date of birth of the household member
        relation VARCHAR(50),            -- Relation to the applicant (e.g., daughter, son)
        FOREIGN KEY (applicant_id) REFERENCES applicants(id) ON DELETE CASCADE  -- Ensures referential integrity
    );"""
    cursor.execute(table)

    # Create table applicants
    table = """CREATE TABLE schemes (
        id UUID PRIMARY KEY,              -- Unique identifier for the scheme
        name VARCHAR(255) NOT NULL,       -- Scheme name (e.g., Retrenchment Assistance Scheme)
        criteria JSONB                   -- JSON data for the eligibility criteria 
    );"""
    cursor.execute(table)

    # Create table benefits
    table = """CREATE TABLE benefits (
        id UUID PRIMARY KEY,              -- Unique identifier for the benefit
        scheme_id UUID NOT NULL,          -- Foreign key linking to the schemes table
        name VARCHAR(255) NOT NULL,       -- Name of the benefit (e.g., SkillsFuture Credits)
        amount DECIMAL(10, 2) NOT NULL,   -- Amount for the benefit (e.g., 500.00)
        FOREIGN KEY (scheme_id) REFERENCES schemes(id) ON DELETE CASCADE  -- Ensures referential integrity
    );
    """
    cursor.execute(table)

    ## INSERT data into DB
    insert1='''
    INSERT INTO applicants (id, name, employment_status, sex, date_of_birth) VALUES
    ('01913b7a-4493-74b2-93f8-e684c4ca935c', 'James', 'unemployed', 'male', '1990-07-01'), ('01913b80-2c04-7f9d-86a4-497ef68cb3a0', 'Mary', 'unemployed', 'female', '1984-10-06');
    '''
    cursor.execute(insert1)
    insert2='''
    INSERT INTO household (id, applicant_id, name, employment_status, sex, date_of_birth, relation)
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

    # Close the connection

    return connection
