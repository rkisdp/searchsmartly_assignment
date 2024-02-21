# searchsmartly assignment - Points of Interest (PoI) Data Loader
Assignment repository for searchsmartly: 

This Django management command script loads Points of Interest (PoI) data from various file formats into the database.

## Description

The script provides functionality to import PoI data from CSV, JSON, and XML file or files into the database using Django's management command system.

### Supported File Formats
CSV, JSON, XML

## Usage with Docker

To use the script with Docker, follow these steps:

1. Ensure you have Docker installed on your machine.
2. Clone this repository to your local machine.
3. Navigate to the project directory.

### Build Docker Image

```bash
docker-compose up --build
```

### Load data
To load data, you need to get into docker container, follow these steps:

1. Execute command to list all the running container using
```bash
docker ps
```
2. Copy the id of container and then run:
```bash
docker exec -it <container id> bash
```
3. then you can test load data using this command:
```bash
python manage.py load_data <path of file or files>
```

### Run Test Functionality of project
To run the test cases you can run the following command
```bash
python manage.py test
```


