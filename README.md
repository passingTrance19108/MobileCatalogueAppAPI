# Phone API

A RESTful API for managing mobile phone data using Flask and SQLAlchemy. The API supports CRUD operations and flexible search functionality based on various phone fields (e.g., serial number, IMEI, brand, etc.). It features custom validation, robust error handling, and is prepared for future migration to a MySQL Docker environment.

## Features

- **CRUD Operations:**  
  Add, update, delete, and retrieve mobile phone records.
- **Flexible Search:**  
  Search by any field, including partial matching for network technologies.
- **Input Validation:**  
  Uses custom validation functions to ensure data integrity.
- **Database Abstraction:**  
  Uses Flask-SQLAlchemy, making the code database-agnostic.
- **Testing:**  
  Comprehensive automated tests with an in-memory SQLite database.
- **Docker Ready:**  
  Configurable via environment variables for easy migration to MySQL using Docker.

## Setup

### Prerequisites

- Python 3.6+
- pip (Python package installer)
