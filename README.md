# JobPulse
This project is a job board platform built using Django, designed to help companies post job openings and candidates find suitable job opportunities.

## Features
1. User Authentication: Users can sign up, log in, and manage their profiles.
2. Job Listings: Companies can post job listings, including job title, description, salary, location, and seniority level.
3. Search and Filter: Users can search for job listings based on various criteria such as job title, location, and seniority level.
4. User Roles: Different roles such as company recruiters and job seekers are supported, each with their own permissions and capabilities.
5. Email Notifications: Companies receive email notifications when a candidate applies for their job listing, keeping them informed of new applications.
6. Additional Features: In addition to the features mentioned above, this job board project includes many more functionalities to enhance the user experience and meet various business needs.

## Technologies Used
1. Django: Backend framework for building web applications in Python.
2. HTML/CSS/JavaScript: Frontend technologies for building the user interface.
3. PostgreSQL: Database systems used to store application data.
4. Bootstrap: Frontend framework for designing responsive and mobile-first websites.
5. Git and GitHub: Version control system and hosting platform for collaboration and project management.


## Installation
1. Clone the repository:
``` bash
git clone https://github.com/PowerCell12/JobBoardProject
```

Install dependencies:
``` bash
pip install -r requirements.txt
```

Set up the database:
``` python
python manage.py migrate
```

Run the development server:
``` python
python manage.py runserver
```

Access the application at http://localhost:8000 in your web browser.


## License
This project is licensed under the MIT License.

## Acknowledgements
- Special thanks to Django for the powerful web framework.
- Thanks to Bootstrap for the responsive design components.
