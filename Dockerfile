# app/Dockerfile

FROM python:3.10.12

WORKDIR /appcampa

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl software-properties-common git libpq-dev

# Clone the app repository
RUN git clone https://github.com/joelr4mire5/appcampa.git .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Remove unnecessary files to reduce image size
RUN rm -rf /var/lib/apt/lists/*


# Expose the port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Entrypoint command
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]