# 💳 Subscription Management & Automated Billing Platform

BillPro is a subscription management platform designed to simplify and automate billing, payments, invoices, and subscription workflows. It provides dedicated customer and admin dashboards for managing subscriptions, payments, invoices, profiles, and notifications through a secure and scalable architecture.

## 🚀 Features

* 🔐 Secure JWT-based authentication & protected routes
* 👤 Customer registration, login & profile management
* 📦 Subscription management & tracking
* 💳 Payment & automated billing management
* 🧾 Invoice generation & management
* 📊 Customer & Admin dashboards
* 🔔 Notification & email integration
* 🗄️ PostgreSQL database with SQLAlchemy
* ⚡ Redis & Celery background processing
* 🔗 RESTful API integration


## 🛠️ Tech Stack

### 🎨 Frontend

* React.js
* Vite
* Tailwind CSS

### ⚙️ Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic

### 🗄️ Database & Services

* PostgreSQL
* Redis
* Celery
* JWT Authentication
* SMTP Email

### 🧰 Development Tools

* Git
* GitHub
* Visual Studio Code

## 🏗️ Project Architecture

BillPro follows a layered application architecture that separates the frontend, API, business logic, data access, and database responsibilities. This structure improves maintainability, scalability, security, and future development.

```text
Customer / Admin
       ↓
React Frontend
       ↓
REST APIs
       ↓
FastAPI Backend
       ↓
Service Layer
       ↓
Repository Layer
       ↓
PostgreSQL
```

### ⚡ Background Processing Architecture

Redis and Celery are used to support background processing and asynchronous workflows such as email notifications, invoice processing, scheduled billing tasks, and subscription renewal notifications.

```text
FastAPI
   ↓
Redis
   ↓
Celery Background Tasks
   ↓
Email / Scheduled Billing / Notifications
```

## 📁 Project Structure

The project is organized into separate frontend and backend components with a layered backend architecture.

```text
BillPro/
│
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   ├── auth/
│   └── tasks/
│
├── alembic/
│   └── versions/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── images/
│
├── requirements.txt
├── .env
└── README.md
```

## 👤 Customer Module

The Customer Module provides customers with a centralized interface to manage their subscriptions and billing information. Customers can register and log in securely, access their dashboard, view subscriptions, track payments, manage invoices, update profile information, manage phone numbers and addresses, receive notifications, and manage their subscription details.

### Customer Capabilities

* 📝 Register and login
* 📊 View customer dashboard
* 📦 View and manage subscriptions
* 💳 Track payments
* 🧾 View invoices
* 👤 Update profile
* 📱 Manage phone number and address
* 🔔 Receive notifications
* ⚙️ Manage subscription details

## 👨‍💼 Admin Module

The Admin Module provides administrators with centralized control over customers, subscriptions, payments, invoices, notifications, and billing activities. The admin dashboard allows administrators to monitor platform activities and manage important subscription and billing operations.

### Admin Capabilities

* 📊 View dashboard statistics
* 👥 Manage customers
* 📋 Manage subscription plans
* 📦 Manage subscriptions
* 💳 View payments
* 🧾 Manage invoices
* 📈 Monitor billing activities
* 🔔 Manage notifications

## 🔐 Authentication

BillPro uses JWT-based authentication to securely protect user accounts and application resources. User credentials are validated during login, after which a JWT token is generated and used to access protected routes.

```text
User Login
    ↓
Validate Credentials
    ↓
Generate JWT Token
    ↓
Store Token
    ↓
Access Protected Routes
```

### 👥 Role-Based Access

```text
Customer → Customer Dashboard
Admin    → Admin Dashboard
```

Protected routes ensure that users can only access the resources and dashboards permitted for their assigned role.

## 📧 Email Notifications

BillPro integrates SMTP-based email delivery to provide customers with important subscription and billing notifications.

The platform supports notifications for:

* 👋 Welcome email after registration
* ✅ Successful payment
* ❌ Failed payment
* 🧾 Invoice generation
* 🔄 Subscription renewal
* 🚫 Subscription cancellation

SMTP is used for email delivery, while Redis and Celery can be used to process email-related tasks in the background without blocking the main application.

## 🗄️ Database

BillPro uses PostgreSQL as its primary relational database. SQLAlchemy is used for database interaction and ORM functionality, while Alembic manages database schema migrations.

### Main Entities

* 👤 Users
* 📋 Subscription Plans
* 📦 Subscriptions
* 💳 Payments
* 🧾 Invoices
* 🔔 Notifications

Alembic allows database schema changes to be tracked and applied consistently across development and deployment environments.

## ⚡ Redis & Background Processing

Redis provides temporary data storage and communication support for background processing workflows. Celery is used to execute background tasks independently from the main FastAPI application.

Potential background processing workflows include:

* 📧 Email processing
* 🔄 Subscription renewal notifications
* 🧾 Invoice processing
* ⏰ Scheduled billing tasks
* 💾 Redis-based caching and temporary task communication

This architecture helps keep the application responsive while allowing resource-intensive or scheduled operations to run asynchronously.

## 🚀 How to Run

### ⚙️ Backend Setup

Create and activate a Python virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
alembic upgrade head
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

### 🌐 Backend

```text
http://127.0.0.1:8000
```

### 📚 Swagger API Documentation

```text
http://127.0.0.1:8000/docs
```

### 🎨 Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

### 🌐 Frontend

```text
http://localhost:5173
```

## ⚙️ Environment Variables

Create a `.env` file in the backend project and configure the required environment variables:

```env
DATABASE_URL=your_database_url

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=BillPro
SMTP_USE_TLS=true
```

### 🔒 Security Notice

**Never commit your `.env` file, passwords, API keys, or other secrets to GitHub.**

Add `.env` to your `.gitignore` file:

```text
.env
venv/
__pycache__/
node_modules/
```
## 🎯 Project Goal

BillPro aims to simplify subscription and billing management through a centralized platform where customers and administrators can efficiently manage subscriptions, payments, invoices, profiles, and notifications. The project focuses on providing a secure, organized, and scalable architecture for automated billing workflows.


## 👨‍💻 Developer

**Hariharan**

💻 **Full-Stack Developer | Python | React | FastAPI**

Passionate about developing scalable web applications and backend services using modern technologies such as Python, FastAPI, React, PostgreSQL, and REST APIs.

---

⭐ If you find this project useful, consider giving the repository a star!
