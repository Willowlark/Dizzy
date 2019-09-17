# Use an official Python runtime as a parent image
FROM python:3.7-alpine
RUN apk add --no-cache git

# RUN git clone https://github.com/Willowlark/Dizzy.git
# COPY auth.py /Dizzy/auth.py
COPY . /Dizzy

# Set the working directory to /app
WORKDIR /Dizzy


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["python", "dizzy.py"]