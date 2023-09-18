# Use a specific Python version
FROM python:3.11.2-slim-buster

# Set the working directory
WORKDIR /app

# Copy the SQLite database and the rest of the files to the working directory
COPY data/fast_rent_a_car.db /app/data/fast_rent_a_car.db
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Execute the ETL
# CMD ["python", "src/main.py"]

# Start the Dash app
CMD ["python", "src/app.py"]
