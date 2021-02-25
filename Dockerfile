# Use an official Python runtime as a parent image
FROM python:3.7-slim

# RUN git clone https://github.com/Willowlark/Dizzy.git
# COPY auth.py /Dizzy/auth.py
COPY . /Dizzy

# Set the working directory to /app
WORKDIR /Dizzy


RUN apt-get update
RUN apt-get install -y wget curl apt-transport-https gcc
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN echo "6528c910e9b5a6ecd3b54b50f419504ee382e4bdc87fa333a0b0fcd46ca77338 mariadb_repo_setup" | sha256sum -c -
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.4"
RUN apt-get update
RUN apt-get install -y libmariadb3 libmariadb-dev

# run pip install cython
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# RUN cd discord.py;python setup.py install;cd /..

# Run app.py when the container launches
CMD ["python", "dizzy.py"]