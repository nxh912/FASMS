# FASMS
Financial Assistance Scheme Management System

## Database tables

* table: **schemes**

| Name          | Type          | comment  |
| ------------- |:-------------:| -----:|
| **id**     |  UUID        | Primary Key |
|  name      | VARCHAR(255) |NOT NULL     |
| criteria   | VARCHAR(255) |NOT NULL     |
| last_update| DATETIME     |systime      |


* table: **applicants**

| Name          | Type          | comment  |
| ------------- |:-------------:| -----:|
| **id**     |  UUID        | Primary Key |
|  name      | VARCHAR(255) |NOT NULL     |
| employment_status | VARCHAR(255) |NOT NULL     |
| sex        |VARCHAR(10) | NOT NULL |
| date_of_birth | DATETIME | NOT NULL |
| last_update| DATETIME     |systime  |

* table: **household**

| Name          | Type          | comment  |
| ------------- |:-------------:| -----:|
| **id**        | UUID        | Primary Key |
| applicant_id  | UUID        | NOT NULL |
| name          | VARCHAR(255)| NOT NULL |
| address       | VARCHAR(255)| NOT NULL |
| income        | decimal(9)  | NOT NULL |
| date_of_birth | DATETIME    | NOT NULL |
| last_update   | DATETIME    |systime   |


* table: **benefits**

| Name          | Type          | comment  |
| ------------- |:-------------:| -----:|
| **id**     |  UUID        | Primary Key |
|  scheme_id | UUID         |NOT NULL     |
| name   | VARCHAR(255) |NOT NULL     |
| amount   | decimal(9) |NOT NULL     |
| last_update| DATETIME     |systime      |


* table: **schemes**

| Name          | Type          | comment  |
| ------------- |:-------------:| -----:|
| **id**     |  UUID        | Primary Key |
|  name      | VARCHAR(255) |NOT NULL     |
| criteria   | VARCHAR(255) |NOT NULL     |
| last_update| DATETIME     |systime      |

