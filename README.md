# FASMS
Financial Assistance Scheme Management System

## User Stories

1. view all available financial assistance schemes.

```
```

2. add new scheme applicants.

3. view the schemes that an applicant is eligible to apply for.


## Database tables

* table: **Administrators**

| Name          | Type          | comment  |
| ------------- |:-------------:| -----:|
| **id**     |  UUID        | Primary Key |
|  name      | VARCHAR(255) |NOT NULL     |
| employment_status | VARCHAR(255) |NOT NULL     |
| sex        |VARCHAR(10) | NOT NULL |
| date_of_birth | DATETIME | NOT NULL |
| last_update| DATETIME     |systime  |


* table: **Applicants**

| Name          | Type          | comment  |
| ------------- |:-------------:| -----:|
| **id**     |  UUID        | Primary Key |
|  name      | VARCHAR(255) |NOT NULL     |
| employment_status | VARCHAR(255) |NOT NULL     |
| sex        |VARCHAR(10) | NOT NULL |
| date_of_birth | DATETIME | NOT NULL |
| last_update| DATETIME     |systime  |

* table: **Schemes**

| Name          | Type          | comment  |
| ------------- |:-------------:| -----:|
| **id**     |  UUID        | Primary Key |
|  name      | VARCHAR(255) |NOT NULL     |
| criteria   | VARCHAR(255) |NOT NULL     |
| last_update| DATETIME     |systime      |

* table: **Applications**

| Name          | Type          | comment       |
| ------------- |:-------------:| -------------:|
| **id**        |  UUID        | Primary Key    |
| scheme_id     | UUID         |FD to Scheme    |
| applicant_id  | UUID         |FD to Applicants|
| last_update   | DATETIME     |systime         |



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


## Setup

  1. ```sudu apt-get install curl```
  1. ```pip3 install fastapi```
  1. ```fastapi run fasms_api.py```
     
