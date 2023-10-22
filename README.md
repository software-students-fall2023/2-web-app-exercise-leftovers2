# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our app is an online address book where the user can store imformation on their contact's addresses and make notes specific to each contact.

## User stories

[Issues Page](https://github.com/software-students-fall2023/2-web-app-exercise-leftovers2/issues)

## Task boards

- [Sprint 1 Board](https://github.com/orgs/software-students-fall2023/projects/17)
- [Sprint 2 Board](https://github.com/orgs/software-students-fall2023/projects/43)


## Install Instructions
To install and run our application locally, follow these instructions below:
1. Download the source code from the repository.
2. Using your preferred Python editor of choice, open the project and create a new virtual environment using your preferred method.
3. Activate your virtual environment.
4. Run `pip install -r requirements.txt` from the command line.
5. Create a file named `.env` at the head of the project directory.
6. Inside, the file should contain the following lines:  
    `MONGODB_URI = "mongodb+srv://<username>:<password>@cluster0.bgoigar.mongodb.net/?retryWrites=true&w=majority"`   
   `MONGODB_DATABASE = "ContactData"`   
`MONGODB_COLLECTION = "people"`
7. To get a username and password, message one of repository contributors to generate one or alternatively create your own MongoDB Atlus database following the same naming conventions.
8. If you ask an admin, you should also give the ip address you are using to run the program so that it can be whitelisted. If you are creating your own database, make sure to create a database name `ContactData` with a collection named `people`.
9. Replace `<username>` and `<password>` with your own respectively. If you are creating your own database, replace the string in `MONGODB_URI` entirely with own to your own.
10. Lastly, run `app.py` with a command such as `python app.py` to launch the program.