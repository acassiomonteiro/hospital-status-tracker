# GEMINI.md - Project Context (Synced with CLAUDE.md)

## Project Overview

This is a **Hospital Status Tracker**, an academic MVP web project for real-time patient status tracking in an emergency room. It aims to solve clinical information fragmentation.

The application allows for:
- Full electronic patient record management.
- Creating and managing patient attendances.
- Tracking patient status through a 7-stage workflow.
- User authentication with three distinct professional profiles (Doctor, Nurse, Admin).

---

## Tech Stack

- **Backend**: Django 5.2.7 + Python 3.11
- **Database**: PostgreSQL (managed via Docker Compose)
- **Frontend**: Django Templates + Tailwind CSS 3.x (via CDN)
- **Containerization & Deployment**: Docker + Docker Compose

---

## Building and Running (Docker First)

The project is **100% dockerized** and designed to be run with Docker Compose. This is the recommended approach.

### Primary Method: Docker Compose

1.  **Build and Run Services**:
    ```bash
    # This single command starts the web app and the database.
    docker-compose up --build
    ```
    **IMPORTANT**: Database migrations are applied **automatically** at startup by the `entrypoint.sh` script. You do not need to run `migrate` manually.

2.  **Common Docker Commands**:
    ```bash
    # Access the Django shell
    docker-compose exec web python manage.py shell

    # Create a superuser
    docker-compose exec web python manage.py createsuperuser

    # View real-time logs for the web service
    docker-compose logs -f web
    ```

### Secondary Method: Local Development

While Docker is preferred, a local setup is also possible.

1.  **Environment**: Create and activate a Python virtual environment.
2.  **Dependencies**: `pip install -r requirements.txt`
3.  **Database**: Ensure a local PostgreSQL instance is running and configured.
4.  **Migrations**: `python manage.py migrate`
5.  **Run**: `python manage.py runserver`

---

## Development Conventions

- **Language**: All code (models, variables, etc.) is written in **Portuguese**.
- **Style**: PEP 8 with a line limit of 100 characters.
- **Models**:
    - Use `verbose_name` in Portuguese for all fields.
    - Use `on_delete=models.PROTECT` for ForeignKeys to prevent accidental data loss.
    - A descriptive `__str__()` method is mandatory.
- **Views**:
    - **Class-Based Views (CBVs)** are preferred (`ListView`, `FormView`, etc.).
    - All views must be protected with the `LoginRequiredMixin`.
    - **Optimize database queries** using `select_related()` for ForeignKey relationships and `prefetch_related()` for many-to-many/reverse ForeignKey.
- **Patient Uniqueness**:
    - To avoid duplicate patient entries, always use `Paciente.objects.get_or_create(cpf=...)`.
- **User Feedback**: Use the `django.contrib.messages` framework to show success or error notifications.

---

## Project Status & Roadmap

- **✅ Phase 1: Authentication (Complete)**: User login/logout and professional profiles are implemented.
- **✅ Phase 2: Patient Data (Complete)**: The `Paciente` model has been expanded into a full electronic record.
- **✅ Phase 3: Clinical Evolution (Complete)**: Staff can now record clinical notes, creating a timeline for each attendance.
- **🎯 NEXT UP - Phase 4: Vital Signs (Critical)**: The next priority is to implement the recording of vital signs for patients.

---

## Context for AI Interaction

- **Preserve Functionality**: Do not remove or break existing code.
- **Follow Patterns**: Adhere strictly to the conventions listed above.
- **Development Order**: When adding features, follow this sequence: **Models -> Forms -> Views -> Templates**.
- **Security**:
    - All views must be protected with `LoginRequiredMixin`.
    - Always validate user input in both the Model and the Form.
    - Never commit secrets or `.env` files.
- **Docker Workflow**: Remember that migrations are automatic. After changing a model, the correct workflow is to rebuild the container: `docker-compose down && docker-compose up --build`.
