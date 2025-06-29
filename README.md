# Lakehouse Project

This project implements a modern data lakehouse architecture for processing and analyzing footwear sales data. It leverages a suite of powerful open-source tools to build a robust and scalable data pipeline, from data ingestion to analytics and visualization.

## Dataset

The project uses the [Footwear Sales Dataset](https://www.kaggle.com/datasets/abdullahlahaji/footware-sales-dataset) from Kaggle. This dataset contains wholesale sales data for a footwear company, including information about products, retailers, and sales transactions.

## Architecture

The lakehouse architecture is built using Docker and consists of the following components:

[//]: # (Add your architecture diagram here)

- **Data Lake:** [MinIO](https://min.io/) is used as the data lake for storing raw and processed data in different zones (Bronze, Silver, and Gold).
- **Data Processing:** [Apache Spark](https://spark.apache.org/) is the core processing engine for transforming data between the different lakehouse layers.
- **Data Warehouse:** The project uses a combination of [Apache Hive Metastore](https://cwiki.apache.org/confluence/display/hive/hms) and [Delta Lake](https://delta.io/) to provide data warehousing capabilities on top of the data lake.
- **Query Engine:** [Trino](https://trino.io/) (formerly PrestoSQL) is used as the query engine for fast, interactive SQL queries on the data in the lakehouse.
- **Orchestration:** [Apache Airflow](https://airflow.apache.org/) is used to orchestrate the data pipeline, scheduling and managing the different tasks.
- **Streaming Ingestion:** [Apache Kafka](https://kafka.apache.org/) is used for real-time data ingestion into the lakehouse.
- **BI & Visualization:** [Apache Superset](https://superset.apache.org/) is used for data exploration, visualization, and creating interactive dashboards.

### Medallion Architecture

The data is organized in a multi-layered "medallion" architecture to progressively refine and process the data:

- **Bronze Layer:** This layer holds the raw, ingested data from the Kafka topic. The data is stored in its raw format with no transformations.
- **Silver Layer:** The data from the Bronze layer is cleaned, validated, and deduplicated. This layer provides a more refined and queryable view of the data.
- **Gold Layer:** This layer contains highly refined and aggregated data, ready for analytics and business intelligence. The data is organized in a dimensional model for easy consumption by BI tools.

## Getting Started

To get started with the project, you need to have Docker and Docker Compose installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Lakehouse-project.git
   cd Lakehouse-project
   ```

2. **Build the Docker images:**
   ```bash
   docker-compose -f docker-compose.build.yml build
   ```

3. **Run the services:**
   ```bash
   docker-compose -f docker-compose.run.yml up -d
   ```

## Usage

Once the services are up and running, you can access the different components:

- **MinIO Console:** http://localhost:9001
- **Trino UI:** http://localhost:8081
- **Airflow UI:** http://localhost:8082
- **Spark UI:** http://localhost:4040
- **Superset UI:** http://localhost:8088

### Data Pipeline

The data pipeline is orchestrated by Airflow and consists of the following stages:

1. **Ingestion:** The `lakehouse_ingest_pipeline` DAG in Airflow reads the footwear sales data from the CSV file and produces it to a Kafka topic.
2. **Bronze Layer:** A Spark streaming job consumes the data from Kafka and writes it to the Bronze layer in the data lake in Delta format.
3. **Silver Layer:** Another Spark job reads the data from the Bronze layer, performs data cleaning and transformation, and writes it to the Silver layer.
4. **Gold Layer:** A final Spark job aggregates the data from the Silver layer to create business-level tables in the Gold layer, which are optimized for analytics.

### Analytics

You can use Trino to query the data in the lakehouse and Superset to create dashboards and visualizations.

## Tools Used

- [Docker](https://www.docker.com/)
- [MinIO](https://min.io/)
- [Apache Spark](https://spark.apache.org/)
- [Apache Hive Metastore](https://cwiki.apache.org/confluence/display/hive/hms)
- [Delta Lake](https://delta.io/)
- [Trino](https://trino.io/)
- [Apache Airflow](https://airflow.apache.org/)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache Superset](https://superset.apache.org/)