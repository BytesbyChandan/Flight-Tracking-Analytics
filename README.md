# Flight Tracking Analytics

An end-to-end data engineering and analytics project that extracts aircraft data from the **OpenSky Network API**, processes it using Python, stores it in **Amazon S3**, loads it into **Snowflake**, and visualizes analytical insights through an interactive web dashboard.

## Project Overview

The objective of this project is to build a practical data pipeline that demonstrates how flight tracking data can be collected, cleaned, stored, analyzed, and presented through a web-based dashboard.

The project combines cloud storage, data warehousing, SQL analytics, Python development, and data visualization.

## Project Architecture

```text
OpenSky Network API
        |
        v
Python Requests
        |
        v
Pandas (Data Cleaning & Transformation)
        |
        v
AWS S3 (Cloud Storage)
        |
        v
Snowflake External Stage
        |
        v
Snowflake Table
        |
        v
SQL Analytics
        |
        v
Flask Backend API
        |
        v
HTML + CSS + JavaScript + Chart.js
        |
        v
Interactive Dashboard
```

## Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| API | OpenSky Network API |
| Data Processing | Pandas, NumPy |
| Cloud Storage | AWS S3 |
| Cloud Access | AWS IAM |
| AWS SDK | Boto3 |
| Data Warehouse | Snowflake |
| Query Language | SQL |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Visualization | Chart.js |
| Environment Management | python-dotenv |

## Project Workflow

### 1. Data Extraction
- Connected to the OpenSky Network API.
- Retrieved aircraft state information.
- Used Python Requests for API communication.

### 2. Data Cleaning and Transformation
- Processed API data using Pandas.
- Identified and handled missing values.
- Removed columns containing only null values.
- Converted Unix epoch timestamps into UTC datetime format.
- Exported the cleaned dataset to CSV.

### 3. AWS S3 Integration
- Created an AWS S3 bucket.
- Configured access through AWS IAM.
- Uploaded the cleaned flight dataset using Boto3.

### 4. Snowflake Data Loading
- Created a Snowflake database and schema.
- Configured an external stage connected to AWS S3.
- Created the `FLIGHT_TRACKING` table.
- Loaded data using Snowflake's `COPY INTO` command.

### 5. SQL Analytics

Performed analytical queries to generate insights such as:

1. Total aircraft records.
2. Airborne versus grounded aircraft.
3. Top 10 countries by aircraft count.
4. Top 10 fastest aircraft.
5. Average aircraft velocity by country.
6. Average barometric altitude by country.
7. Country-wise grounded and airborne aircraft.
8. Top countries by grounded aircraft count.
9. Missing callsign records by country.
10. Ground percentage by country.

### 6. Flask API and Dashboard
- Developed a Flask application to connect Python with Snowflake.
- Created API endpoints to retrieve analytical results.
- Built an interactive dashboard using HTML, CSS, JavaScript, and Chart.js.
- Displayed key performance indicators and analytical charts.
- Added a dashboard refresh feature.

## Dashboard

The dashboard presents flight tracking insights through KPI cards and interactive charts.

**Dashboard Screenshot:**

Screenshots are added as a 1,2,3.png

## Installation and Setup

### Prerequisites

- Python 3.x
- AWS account
- Snowflake account
- OpenSky Network API access
- Git (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/BytesbyChandan/Flight-Tracking-Analytics.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Flight-Tracking-Analytics
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a local `.env` file using `.env.example` as a template.

Add your Snowflake connection details:

```env
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
```

### Step 5: Run the Application

```bash
python app.py
```

### Step 6: Open the Dashboard

Visit:

```text
http://127.0.0.1:5000/dashboard
```

**Note:** The dashboard runs locally and requires the Flask application and Snowflake connection to be active.

## Security

- Never upload `.env` files to GitHub.
- Never expose AWS access keys, secret keys, or Snowflake passwords.
- Use `.env.example` with placeholder values only.
- Keep credentials protected through appropriate environment and IAM configurations.

## Learning Outcomes

Through this project, I gained practical experience in:

- REST API data extraction.
- Data cleaning and transformation using Python.
- AWS S3 and IAM integration.
- Snowflake external stages and data loading.
- Analytical SQL queries.
- Python-Snowflake connectivity.
- Flask API development.
- Interactive dashboard development.

## Author

**Chandan Nama**

- **LinkedIn:** [in/chandan-nama-b1b05a2b8](https://www.linkedin.com/in/chandan-nama-b1b05a2b8)

## Disclaimer

This project is developed for educational and portfolio purposes. The dashboard analyzes collected aircraft data and is not a continuously streaming air traffic control system. It should not be used for operational aviation decisions.
