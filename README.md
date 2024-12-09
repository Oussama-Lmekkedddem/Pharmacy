# Pharmacy System

This project is a **Pharmacy Management System** built using **Angular** for the frontend, **Odoo** for managing pharmacy processes, **PostgreSQL** for the database, **PGAdmin** for database management, and **Nginx** as a reverse proxy.

The system is designed for three main user roles:
- **Admin**: Manages the overall pharmacy system.
- **Pharmacy Owner**: Manages the pharmacy's daily operations.
- **Client**: Views and orders medications.

---

## Prerequisites

Before starting, make sure you have the following installed:
- **Docker Desktop**: To run the containers.
  - [Download Docker Desktop](https://www.docker.com/products/docker-desktop) based on your OS.
- **Git**: To pull or push the project code.
  - [Download Git](https://git-scm.com/downloads)

---

## Project Setup

### 1. Clone the Repository

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/Oussama-Lmekkedddem/Pharmacy.git
cd pharmacy
```

### 2. Create a New Environment

If needed, create a new environment for the project:
```bash
# (Optional) Create a new environment for the project
python -m venv pharmacy-venv
source pharmacy-venv/bin/activate  # For Linux/MacOS
pharmacy-venv\Scripts\activate     # For Windows
```

### 3. Build and Run with Docker Compose

In the project root directory, you’ll find a `docker-compose.yml` file that sets up all necessary services for the Pharmacy System, including the **Angular app**, **Odoo**, **PostgreSQL**, **PGAdmin**, and **Nginx**.

Run the following command to build and start all the services:

```bash
docker-compose up --build
```
This will:

- Build the Docker images (if not already built).
- Start all the services:
  - **Angular**: Frontend application.
  - **Odoo**: ERP system for managing pharmacy operations.
  - **PostgreSQL**: Database for data storage.
  - **PGAdmin**: Database management tool.
  - **Nginx**: Reverse proxy server.

### 4. Application Access Instructions

After running the Docker containers for the application, you can access the different services via the following links:

#### Angular Application
- Access the Angular application at:  
  [http://localhost:4200/](http://localhost:4200/)  
  This will serve the frontend application.

#### PGAdmin
- Access PGAdmin at:  
  [http://localhost:8080/](http://localhost:8080/)  
  This will allow you to manage the PostgreSQL database used by the system.

#### Odoo Application
- Access the Odoo application at:  
  [http://localhost:8069/](http://localhost:8069/)  
  This will allow you to interact with the Odoo ERP system.

---

#### Notes:
- The services are running on different ports (`4200`, `8080`, and `8069`) and are accessible via their respective URLs.
- If you have set up a reverse proxy with Nginx, the services may be mapped to different paths on the same `localhost`, such as:
  - **Angular**: [http://localhost/](http://localhost/)
  - **PGAdmin**: [http://localhost/data](http://localhost/data)
  - **Odoo**: [http://localhost/owner](http://localhost/owner)

---

## How to Run the Application
1. Ensure that Docker and Docker Compose are installed.
2. Build and start the containers using Docker Compose:
   ```bash
   docker-compose up --build

## Features

- **Admin Dashboard**: Manage users, permissions, and overall pharmacy system settings.
- **Pharmacy Owner Dashboard**: Manage inventory, sales, and pharmacy operations.
- **Client Dashboard**: Browse medications, place orders, and view order history.

## Troubleshooting
- **If you encounter any issues** with running the containers, make sure Docker Desktop is running and try restarting the containers with:
```bash
docker-compose down
docker-compose up --build
```


Credentials:

- **Username**: odoo
- **Password**: odoo

## Additional Information

For any questions or further details, feel free to contact me:

- **Name**: LMEKKEDDEM Oussama  
- **Email**: lmekkeddem.oussama@gmail.com
- **GitHub Profile**: https://github.com/Oussama-Lmekkedddem

