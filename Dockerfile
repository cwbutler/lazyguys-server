# Pull base image from Python 3
FROM python:3
ENV PYTHONUNBUFFERED 1

# Create group and user for running service
RUN groupadd -r app && useradd --no-log-init -r -g app app

# Set base directory for code
ENV BASE_APP_DIR /code
RUN mkdir -p ${BASE_APP_DIR}
RUN chown app ${BASE_APP_DIR}

# Set work directory
WORKDIR ${BASE_APP_DIR}

# Install dependencies
COPY requirements.txt ${BASE_APP_DIR}
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run app as non root user
USER app

# Set entrypoint script
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD [ "start" ]

# Copy project to working directory
COPY . ${BASE_APP_DIR}
