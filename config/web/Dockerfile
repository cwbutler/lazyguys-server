# Pull base image from Python 3
FROM python:3
ENV PYTHONUNBUFFERED 1

# Set working directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD [ "start" ]

# Copy project to working directory
COPY /app/ /code/
