# YouTube API - ELT Pipeline

## Overview

An automated ELT (Extract, Load, Transform) data pipeline that extracts YouTube channel statistics using the YouTube Data API, orchestrates the data workflow with Apache Airflow, and stores processed data in PostgreSQL databases. The project implements data engineering best practices including containerization, automated testing, and CI/CD workflows.

## Architecture

<p align="center">
  <img width="500" height="400" src="project_architecture.png" alt="Project Architecture Diagram">
</p>

## Motivation

This project demonstrates modern data engineering practices by building a production-ready ELT pipeline. Key learning objectives include:

- Orchestrating data workflows with Apache Airflow
- Containerizing applications using Docker and Docker Compose
- Implementing data quality checks and unit testing
- Setting up CI/CD pipelines for automated deployment
- Working with external APIs and managing data transformations

## Dataset

The pipeline extracts data from YouTube channels using the YouTube Data API v3. The default configuration pulls data from the 'MrBeast' channel, but can be easily adapted to any YouTube channel by updating the Channel ID or Handle in the configuration.

### Extracted Variables

The pipeline extracts the following metrics for each video:

- **Video ID** - Unique identifier for each video
- **Video Title** - Title of the video
- **Upload Date** - Date when the video was published
- **Duration** - Length of the video
- **View Count** - Total number of views
- **Likes Count** - Number of likes received
- **Comments Count** - Total number of comments

## Project Workflow

The ELT pipeline follows these steps:

1. **Extract**: Data is extracted from the YouTube API using Python scripts
2. **Load (Staging)**: Raw data is loaded into a `staging schema` in PostgreSQL
3. **Transform & Load (Core)**: Data undergoes transformations and is loaded into the `core schema`
4. **Quality Checks**: Automated tests validate data integrity and quality

### Data Loading Strategy

- **Initial Load**: Full historical data extraction on first run
- **Incremental Updates**: Subsequent runs perform upserts to update changed metrics (views, likes, comments)

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Orchestration** | Apache Airflow |
| **Containerization** | Docker, Docker Compose |
| **Data Storage** | PostgreSQL |
| **Programming Languages** | Python, SQL |
| **Testing** | pytest (unit tests), SODA Core (data quality) |
| **CI/CD** | GitHub Actions |
| **API** | YouTube Data API v3 |

## Setup & Configuration

### Prerequisites

- Docker and Docker Compose installed
- YouTube Data API key
- GitHub account (for CI/CD)

### Containerization Details

The project uses a customized Apache Airflow deployment based on the official [docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) with the following modifications:

1. **Custom Docker Image**: Extended Airflow image built with project-specific dependencies, managed through GitHub Actions and stored in Docker Hub

2. **Environment Variables**: 
   - Database connections: `AIRFLOW_CONN_{CONN_ID}` (URI format)
   - Airflow variables: `AIRFLOW_VAR_{VARIABLE_NAME}`

3. **Security**: Fernet key encryption for sensitive connection details and passwords

### Airflow DAGs

The pipeline consists of three sequential DAGs accessible via the Airflow UI at `http://localhost:8080`:

1. **produce_json**: Extracts raw data from YouTube API and generates JSON files
2. **update_db**: Processes JSON data and loads it into staging and core database schemas
3. **data_quality**: Executes data quality checks across both database layers

## Data Access

Access the processed data through either:

- **psql**: Connect directly to the PostgreSQL container
- **Database Management Tools**: Use tools like DBeaver, pgAdmin, or DataGrip to query the database

```bash
# Example: Access PostgreSQL container
docker exec -it <postgres_container_name> psql -U <username> -d <database>
```

## Testing

### Unit Testing
- Framework: pytest
- Coverage: Python functions and data processing logic

### Data Quality Testing
- Framework: SODA Core
- Validation: Schema compliance, data freshness, null checks, and business rules

Run tests locally:
```bash
# Unit tests
pytest tests/

# Data quality tests
soda scan -d postgres -c configuration.yml checks.yml
```

## CI/CD Pipeline

GitHub Actions automates the following workflows:

- **Build**: Creates and pushes Docker images to Docker Hub
- **Test**: Runs unit and integration tests
- **Deploy**: Starts Airflow containers with updated code
- **Validate**: Ensures DAGs parse correctly and run without errors

The CI/CD pipeline triggers on:
- Push to main branch
- Pull request creation
- Manual workflow dispatch

## Environment Variables

The project requires the following environment variables. Create a `.env` file in the root directory with these configurations:

### Docker & Image Configuration
```bash
DOCKERHUB_USERNAME=your_dockerhub_username
DOCKERHUB_PASSWORD=your_dockerhub_password
DOCKERHUB_NAMESPACE=your_dockerhub_namespace
DOCKERHUB_REPOSITORY=yt_api_elt
IMAGE_TAG=1.0.1
```

### Airflow Configuration
```bash
AIRFLOW_UID=50000
AIRFLOW_WWW_USER_USERNAME=admin
AIRFLOW_WWW_USER_PASSWORD=your_secure_password
FERNET_KEY=your_fernet_key  # Generate using: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### PostgreSQL - Metadata Database (Airflow)
```bash
METADATA_DATABASE_NAME=airflow
METADATA_DATABASE_USERNAME=airflow
METADATA_DATABASE_PASSWORD=your_secure_password
```

### PostgreSQL - ELT Database (Staging & Core Schemas)
```bash
ELT_DATABASE_NAME=youtube_elt
ELT_DATABASE_USERNAME=elt_user
ELT_DATABASE_PASSWORD=your_secure_password
```

### PostgreSQL Connection
```bash
POSTGRES_CONN_HOST=postgres
POSTGRES_CONN_PORT=5432
POSTGRES_CONN_USERNAME=postgres
POSTGRES_CONN_PASSWORD=your_secure_password
```

### Celery Backend (Redis)
```bash
CELERY_BACKEND_NAME=redis
CELERY_BACKEND_USERNAME=default
CELERY_BACKEND_PASSWORD=your_secure_password
```

### YouTube API Configuration
```bash
CHANNEL_HANDLE=MrBeast  # Change to any YouTube channel handle
YOUTUBE_API_KEY=your_youtube_api_key  # Get from Google Cloud Console
```

### Generating Required Keys

**Fernet Key** (for encrypting Airflow connections):
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**YouTube API Key**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Copy the API key to your `.env` file



## Project Structure

```
.
├── dags/                   # Airflow DAG definitions
├── plugins/               # Custom Airflow plugins
├── scripts/               # Data extraction and transformation scripts
├── tests/                 # Unit and integration tests
├── docker-compose.yml     # Docker orchestration configuration
├── Dockerfile            # Custom Airflow image definition
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Future Enhancements

- Add data visualization dashboard
- Implement data versioning with DVC
- Expand to multiple YouTube channels
- Add alerting for pipeline failures
- Implement data lineage tracking


## Acknowledgments

- YouTube Data API v3 documentation
- Apache Airflow community
- Docker and containerization best practices
