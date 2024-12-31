# Start with Python 3.9.
FROM python:3.9

# Set working directory to container.
WORKDIR /api

# Copy directory over.
COPY . .

# Install packages from requirements.
RUN pip install \
    --no-cache-dir \
    --upgrade \
    -r requirements.txt

# Expose 8081, which is where Gunicorn is configured to spawn
# our app.
EXPOSE 8081

# Set permissions on the start app script.
RUN chmod +x ./start-app.sh

# Set command to run the start app script.
CMD [ "./start-app.sh" ]