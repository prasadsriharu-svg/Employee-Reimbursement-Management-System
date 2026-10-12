# Employee Reimbursement Management System

A web-based Employee Reimbursement Management System built using Python, Streamlit, FastAPI, and SQLite.

The application helps organizations manage employee expense claims, review approvals, and reimbursement payments.

## Features

- **Employee:** Submit reimbursement claims, select expense categories, and upload receipts.
- **Manager:** Review and approve or reject submitted claims.
- **Finance:** Manage reimbursement payment processing.
- **Admin:** View the administration dashboard.
- **Authentication:** User authentication using JWT and password hashing.
- **Database:** Store reimbursement claims and related information using SQLite.

## Technologies Used

- Python
- Streamlit — Frontend user interface
- FastAPI — Backend API
- SQLite — Database
- JWT — Authentication
- Argon2 — Password hashing
- Git and GitHub — Version control

## Project Structure

```text
ReimbursementManagementSystem/
├── app.py
├── api_client.py
├── auth_service.py
├── security.py
├── database.py
├── create_admin.py
├── backend/
│   └── main.py
├── Learnings/
├── .streamlit/
│   └── config.toml
├── .gitignore
└── README.md
```

## Project Status

This project is under active development.

Implemented functionality includes employee reimbursement submission, manager review, finance processing, authentication, and the admin dashboard.

Additional admin management and reporting features are planned.

## Getting Started

1. Clone the GitHub repository.
2. Create a Python virtual environment.
3. Install the project's required Python dependencies.
4. Configure the necessary environment variables.
5. Initialize the database and required user accounts.
6. Start the FastAPI backend.
7. Start the Streamlit frontend.

Detailed installation and configuration commands will be added as the project setup is finalized.

## Learning Objectives

This project was created to gain practical experience in:

- Python programming
- Building web applications using Streamlit
- Developing REST APIs using FastAPI
- Working with SQLite databases
- Implementing user authentication and role-based workflows
- Using Git and GitHub for version control

## Author

GitHub: [prasadsriharu-svg](https://github.com/prasadsriharu-svg)