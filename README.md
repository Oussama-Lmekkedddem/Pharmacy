# Pharmacy System

This project is a **Pharmacy Management System** built using **Odoo** for managing pharmacy processes, **PostgreSQL** for the database, **PGAdmin** for database management, and **Nginx** as a reverse proxy.

The system is designed for three main user roles:
- **Admin**: Manages the overall pharmacy system.
- **Pharmacy Owner**: Manages the pharmacy's daily operations.
- **Client**: Views and orders medications.

---

## Prerequisites

Before starting, make sure you have the following installed:
- **Docker Desktop**: To run the containers.
  - [Download Docker Desktop](https://www.docker.com/products/docker-desktop) based on your OS.
---

## Project Setup

### 1. Clone the Repository

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/Oussama-Lmekkedddem/Pharmacy.git
cd pharmacy
```

### 2. Build and Run with Docker Compose

In the project root directory, you’ll find a `docker-compose.yml` file that sets up all necessary services for the Pharmacy System, including the **Odoo**, **PostgreSQL**, **PGAdmin**, and **Nginx**.

Run the following command to build and start all the services:

```bash
docker-compose up --build
```
This will:

- Build the Docker images (if not already built).
- Start all the services:
  - **Odoo**: ERP system for managing pharmacy operations.
  - **PostgreSQL**: Database for data storage.
  - **PGAdmin**: Database management tool.
  - **Nginx**: Reverse proxy server.

### 3. Application Access Instructions

After running the Docker containers for the application, you can access the different services via the following links:

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
- The services are running on different port (`8069`) and are accessible via their respective URLs.
- If you have set up a reverse proxy with Nginx, the services may be mapped to different paths on the same `localhost`, such as:
  - **admin**: [http://localhost/](http://localhost/)
  - **owner**: [http://localhost/owner/login](http://localhost/owner/login)
  - **client**: [http://localhost/client/login](http://localhost/client/login)

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


## Project Setup and Access Information

### PgAdmin Access
To access PgAdmin, use the following credentials:

- **Email**: `admin@localhost.com`
- **Password**: `admin`

### Connecting to PostgreSQL in PgAdmin
To visualize your Odoo data in PgAdmin, follow these steps to create a new server:

1. **Server Name**: Choose a name, e.g., `ODOO`.
2. **Host**: `postgres-stack`.
3. **Port**: `5432`.
4. **Maintenance Database**: `postgres`.
5. **Username**: `odoo`.
6. **Password**: `odoo`.

### Odoo Database Configuration
The PostgreSQL database for Odoo is pre-configured with the following settings:

- **Database Name**: `odoo`.
- **Username**: `odoo`.
- **Password**: `odoo`.

---

## Additional Information

For any questions or further details, feel free to contact me:

- **Name**: LMEKKEDDEM Oussama  
- **Email**: lmekkeddem.oussama@gmail.com
- **GitHub Profile**: https://github.com/Oussama-Lmekkedddem

