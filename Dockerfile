FROM python:3.9-slim

WORKDIR /usr/src/app

# Install required packages from requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . /usr/src/app

# Command to run the main file (change this to your main script if different)
CMD ["python", "classifier.py"]
