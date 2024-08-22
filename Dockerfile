# Base image
FROM tensorflow/tensorflow:2.16.1
#tensorflow/tensorflow:2.16.1

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 8080

#ENV FLASK_APP=server.py
# Set the entry point
CMD ["python", "server.py", "--model", "models/intent_classification1.keras", "--port", "8080"]
#CMD [ "flask", "run" , "--host=0.0.0.0", "--port=8080"]
