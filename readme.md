# **Chinese Medicine API** <br>  is a RESTful API for Chinese Medicine practitioners. <br>
Practitioners can use this API to store their patients' Herbal Formula prescriptions. <br> Patients can also use the API to access their own formula history. 
<br><br>
## What problem is this app trying to solve? 
There are a number of web-based practice management apps already available on the web. Such software(s) usually provide a whole gamut of features, including treatment recording and booking systems. They contain many features that aren't relevant or useful to a herbal medicine specialist, and it is often costly to pay for ongoing prescriptions. 

The aim of this app is to provide a solution that is niched towards simple recording of patient data and prescriptions, with a specialised focus on Chinese Medicine herbal formulas. It is a simple and affordable solution for Chinese medicine herbalists. 

## Why this problem needs solving
Chinese medicine practitioners are often sole practitioners, and do not have the resources to invest in expensive software. They are often looking for a simple and affordable solution to record their patient data and prescriptions.

## Why is PostgreSQL the database of choice? And what are the drawbacks compared to others?

PostgreSQL is a powerful, open-source relational database management system. It is a great choice for this project because it is free and open-source, and it is also a very powerful database. It is also a great choice because it is a relational database, which is a great fit for this project. Additionally, it is a very scalable database, which is important for a project that is expected to grow in the future.

(“Advantages of PostgreSQL - CYBERTEC | Data Science & PostgreSQL,” n.d.; PostgreSQL Advantages, n.d.)

In comparison to other databases, some known drawbacks of PostgreSQL include: 

- Slower speeds: while usually not a huge issue, PostgreSQL can be a little slower than other database systems, especially for complex queries and large datasets.

- Less support for non-relational data: PostgreSQL is a relational database, and is not as good at handling non-relational data as other databases.

(What Is PostgreSQL? Introduction, Advantages & Disadvantages, n.d.)

## What are the key functionalities and benefits of an ORM? 

An ORM is an Object Relational Mapper. It is a tool that allows developers to interact with a database using an object-oriented paradigm. It is a great tool for developers because it allows them to interact with a database using an object-oriented paradigm, which is a more intuitive way of interacting with a database. It also allows developers to interact with a database without having to write SQL queries. Additionally, it allows developers to interact with a database without having to worry about the underlying database structure.

(Hoyos, 2019; What Is an ORM – The Meaning of Object Relational Mapping Database Tools, 2022)
<br>

## API endpoints
<br>

### **Authentication**

**/signup** <br>
This creates a new user for navigating the API. An admin account must be created first, for which the admin field should be set to true, and the patient_id and doctor_id fields should be set to null. <br>


```json
{
	"email": "admin@gmail.com",
	"password": "password", 
	"admin": true,
	"patient_id": null,
	"doctor_id": null
    }
```
Once doctors and patients have been created in their respective entities (see doctor and patient endpoints below), the admin can create new user accounts for the doctors and patients. The admin field should be set to false, and the patient_id and doctor_id fields should be set to the id of the patient or doctor that the user is associated with. <br>

Whenever a new user is created, the user will be assigned a JWT token. 

```json
{
	"email": "doctor1@gmail.com",
	"password": "password", 
	"admin": false,
	"patient_id": null,
	"doctor_id": 1
    }
```

**/login** <br>
Existing users can login to the API using this endpoint, after which the user will be assigned a new JWT token.<br>

```json
{
    "email": "patient1@gmail.com",
    "password": "password"
}
```

### **Doctors**

**/doctors** POST <br>
This endpoint allows new doctors to be created, must be logged in as admin. A doctor id will be automatically generated. <br>

```json
    {
	"first_name": "Darren",
	"last_name": "Marksel",
	"email": "darrenmarksel@doctor.com",
	"password": "password",
	"phone_number": "0486680354",
	"AHPRA_number": "LIEN9456484"
}
```

**/doctors** GET <br>
This endpoint allows all doctors to be retrieved, must be logged in as admin. <br>

**/doctors/{doctor_id}** GET <br>
This endpoint allows a specific doctor to be retrieved by doctor_id, must be logged in as admin. <br>

**/doctors/{doctor_id}** PUT <br>
This endpoint allows a specific doctor to be updated by doctor_id, must be logged in as admin. <br>

```json
    {
    "first_name": "Darren",
    "last_name": "Marksel",
    "email": "darrenmarksel@doctor.com",
    "password": "password",
    "phone_number": "0486681111",
    "AHPRA_number": "LIEN9456484"
}
```

**/doctors/{doctor_id}** DELETE <br>
This endpoint allows a specific doctor to be deleted by doctor_id, must be logged in as admin. <br>     

### **Patients**

**/patients** POST <br>
This endpoint allows new patients to be created, must be logged in as a doctor or admin. A patient id will be automatically generated. <br>

```json
    {
    "first_name": "John",
    "last_name": "Smith",
    "email": "johnsmith@patient.com",
    "password": "password",
    "phone_number": "0486680354"
}
```

**/patients** GET <br>
This endpoint allows all patients to be retrieved, must be logged in as admin. <br>

**/patients/{patient_id}** GET <br>
This endpoint allows a specific patient to be retrieved by patient_id, must be logged in as admin. <br>

**/patients/{patient_id}** PUT <br>
This endpoint allows a specific patient to be updated by patient_id, must be logged in as admin. <br>

```json
    {
    "first_name": "Jonathon",
    "last_name": "Smith",
    "email": "johnsmith@patient.com",
    "password": "password",
    "phone_number": "0486681111"
}
```

**/patients/{patient_id}** DELETE <br>
This endpoint allows a specific patient to be deleted by patient_id, must be logged in as admin. <br>

### **Formulas**

**/formulas** POST <br>
This endpoint allows new formulas to be created, must be logged in as a doctor or admin. A formula id will be automatically generated. <br>

***Example 1***
```json
    {
    "name": "Si Ni San",
    "description": "Si Ni San is a traditional Chinese herbal formula used to treat a variety of conditions, including anxiety, depression, insomnia, and menopausal symptoms.",
    "ingredients": "Bai shao, chai hu, zhi shi, zhi gan cao",
    "instructions": "Take 1 tsp of powder in hot water, twice a day"
}
```
***Example 2***
```json
    {
    "name": "Li Zhong Wan",
    "description": "Li zhong wan is a traditional Chinese herbal formula commonly used to treat digestive issues, including indigestion, bloating, and diarrhea.",
    "ingredients": "Bai zhu, Gan jiang, Ren shen, Zhi gan cao",
    "instructions": "Take 3 pills, 3 times a day"
}
```

**/formulas** GET <br>
This endpoint allows all formulas to be retrieved, must be logged in as admin or doctor. <br>

**/formulas/{formula_id}** GET <br>
This endpoint allows a specific formula to be retrieved by formula_id, must be logged in as admin or doctor. <br>

**/formulas/{formula_id}** PUT <br>
This endpoint allows a specific formula to be updated by formula_id, must be logged in as admin or doctor. <br>

```json
    {
    "name": "Li Zhong Wan",
    "description": "Li zhong wan is a traditional Chinese herbal formula commonly used to treat digestive issues, including indigestion, bloating, and diarrhea.",
    "ingredients": "Bai zhu 9, Gan jiang 9, Ren shen 9, Zhi gan cao 9",
    "instructions": "Take 6 pills, twice a day"
}
```

**/formulas/{formula_id}** DELETE <br>
This endpoint allows a specific formula to be deleted by formula_id, must be logged in as admin. <br>

### **Prescriptions**

**/prescriptions** POST <br>
This endpoint allows new prescriptions to be created, must be logged in as a doctor or admin. A prescription id will be automatically generated. <br>

```json
    {
    "formula_id": 1,
    "patient_id": 1,
    "doctor_id": 1
}
```

**/prescriptions** GET <br>
This endpoint allows all prescriptions to be retrieved, must be logged in as admin. <br>

**/prescriptions/{prescription_id}** GET <br>
This endpoint allows a specific prescription to be retrieved by prescription_id, must be logged in as admin, or the original prescribing doctor. <br>

**/prescriptions/{patient_id}** GET <br>
This endpoint allows all prescriptions for a specific patient to be retrieved by patient_id, must be logged in as admin, or the original prescribing doctor. <br>

**/prescriptions/{doctor_id}** GET <br>
This endpoint allows all prescriptions for a specific doctor to be retrieved by doctor_id, must be logged in as admin, or the original prescribing doctor. <br>

**/prescriptions/patient/email/{email}** GET <br>
This endpoint allows all prescriptions for a specific patient to be retrieved by patient email, must be logged in as the patient with the relevant email. This is the main endpoint for patients to view their prescriptions. <br>

**/prescriptions/{prescription_id}** PUT <br>
This endpoint allows a specific prescription to be updated by prescription_id, must be logged in as admin, or the original prescribing doctor. <br>

```json
    {
    "formula_id": 2,
    "patient_id": 1,
    "doctor_id": 1
}
```

**/prescriptions/{prescription_id}** DELETE <br>
This endpoint allows a specific prescription to be deleted by prescription_id, must be logged in as admin. <br>
























## Third party apps
Flask
Sqlalchemy
Jwt
Pyjwt

