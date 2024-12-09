import sqlite3, uuid, inspect
def get_uuid(): return uuid.uuid4()

#  "('01913b7a-4493-74b2-93f8-e684c4ca935c', 'James', 'unemployed', 'male', '1990-07-01'), 
#  "('01913b80-2c04-7f9d-86a4-497ef68cb3a0', 'Mary', 'unemployed', 'female', '1984-10-06'); "    


########### applicants / POST
printf "#####\n# POST applicants \n\n"

ENDPOINT='http://localhost:8000/api/applicants'  
printf "ENDPOINT : %s\n" $( echo $ENDPOINT | sed s/'.*api'/''/g )
 
#curl --header "Content-Type: application/json" --request POST --data '{"date_of_birth":"1990-07-01", "sex":"Male",   "name":"James", "employment_status":"unemployed"}'  'http://localhost:8000/api/applicants'  
#curl --header "Content-Type: application/json" --request POST --data '{"date_of_birth":"1990-07-01", "sex":"Female", "name":"Mary",  "employment_status":"unemployed"}'  'http://localhost:8000/api/applicants'  

JAMES_ID=` \
curl --data '{"date_of_birth":"1990-07-01", "sex":"Male",   "name":"James", "employment_status":"unemployed"}' --header "Content-Type: application/json" --request POST "$ENDPOINT" \
 | tr '\n' ' ' | sed s/'.*applicant'/''/g | cut -f3 -d\" `

echo "  ----> JAMES_UUID : ${JAMES_ID}"

MARY_CHILD1=` \
curl --data '{"date_of_birth":"2006-10-06", "sex":"Female", "name":"Nancy",  "employment_status":"unemployed"}' --header "Content-Type: application/json" --request POST "$ENDPOINT" \
 | tr '\n' ' ' | sed s/'.*applicant'/''/g | cut -f3 -d\" `

MARY_CHILD2=` \
curl --data '{"date_of_birth":"2008-10-06", "sex":"Male", "name":"Oliver",  "employment_status":"unemployed"}' --header "Content-Type: application/json" --request POST "$ENDPOINT" \
 | tr '\n' ' ' | sed s/'.*applicant'/''/g | cut -f3 -d\" `

## Nancy {"Action":"Added","applicant":"e3b9f1b2-9bf4-4234-bf87-6692394e2d70","line":54}
## Oliver {"Action":"Added","applicant":"0ace2660-9871-4f7e-bd25-dbdc7f24ceeb","line":54}



MARY_ID=` \
curl --data '{"date_of_birth":"1984-10-06", "sex":"Female", "name":"Mary",  "employment_status":"unemployed"}' --header "Content-Type: application/json" --request POST "$ENDPOINT" \
 | tr '\n' ' ' | sed s/'.*applicant'/''/g | cut -f3 -d\" `

curl --data '{"date_of_birth":"1984-10-06", "sex":"Female", "name":"Mary",  "employment_status":"unemployed"}' --header "Content-Type: application/json" --request POST "$ENDPOINT"





