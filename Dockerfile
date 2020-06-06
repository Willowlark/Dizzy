# Use an official Python runtime as a parent image
FROM python:3.7-slim

# RUN git clone https://github.com/Willowlark/Dizzy.git
# COPY auth.py /Dizzy/auth.py
COPY . /Dizzy

# Set the working directory to /app
WORKDIR /Dizzy


# Install any needed packages specified in requirements.txt
# RUN apk update
# RUN apk add make automake gcc g++ subversion python3-dev
# run pip install cython
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# RUN cd discord.py;python setup.py install;cd /..

# Run app.py when the container launches
CMD ["python", "dizzy.py"]