# Steps to setup project:

- Install all dependencies using `pip install -r requirements.txt`
- (Optional step) Create all the tables using `python manage.py migrate`.
- Run server `python manage.py runserver`
- Only `signup` and `signin` request can be made without token. For all other requests user will need token which gets generated on signup and login.
- For calling API you can use postman.

# Database Schema
- I have used 3 tables for this project:
## User
- Represents a registered user
- Main fields - 
  - `phone_no` (Foreign key to 'PhoneNumber' table), 
  - `name`,
  - `email` (optional),
  - `password`.

## PhoneNumber
- Represents a phone number.
- Fields - 
  - `number`,
  - `spam_count`.

## Contact
- Represents a contact.
- Fields 
  - `name`,
  - `phone_no` (Foreign key to 'PhoneNumber' table), 
  - `user` (Foreign key to 'User' table)


### Signup
- Url: `http://localhost:8000/signup`
- Sample request: 
```json
{
	"name": "Puneet Garg",
	"email": "puneetgarg@gmail.com",
	"password": "User@123",
	"phone_no": "9999999999"
}
```
`Point to remember, password should be at least 8 characters and contains at least one letter, one number and one special character.`



### Login
- Url: `http://localhost:8000/signin`
- Sample request: 
```json
{
	"phone_no": "9999999999",
	"password": "User@123"
}
```

### Create Contact
- Url: `http://localhost:8000/contact`
- Sample request:
```json
{
	"name": "Rahul",
	"phone_no": "8888888888"
}
```

### Mark a number as spam
- Url: `http://localhost:8000/spam`
- Sample request:
```json
{
	"phone_no": "7777777777"
}
```

### Search using name
- Url: `http://localhost:8000/search`
- Sample request:
```json
{
	"name": "Rahul"
}
```

### Search using phone number
- Url: `http://localhost:8000/search`
- Sample request:
```json
{
	"phone_no": "7777777777"
}
```
`Searching a name returns all the names that start with the search query and all names that contains search query from the contacts database.
Searching a number return the details if the number is registered or if number is not registered then it will return all the users from the contacts databse`