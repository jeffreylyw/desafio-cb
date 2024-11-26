FROM apache/airflow:2.9.2-python3.11
USER airflow
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt