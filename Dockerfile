# Use a specific Python version
FROM python:3.11.2

# Set the working directory
WORKDIR /app

# Copy everything to the working directory
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Execute the ETL
CMD ["python", "src/main.py"]

# Start the Dash app
CMD ["python", "src/app.py"]
