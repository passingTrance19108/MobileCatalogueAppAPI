# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Optional: Add a non-root user for security
RUN adduser --disabled-password myuser
USER myuser

# Set additional environment variables
ENV FLASK_APP=MainInterface.py
ENV FLASK_ENV=production

# Optional: Add a healthcheck to monitor container health
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s CMD curl -f http://localhost:5000/ || exit 1

# CMD ["flask", "run", "--host=0.0.0.0"]
# Run the application using Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "MainInterface:app"]