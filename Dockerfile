# Use an official Python runtime as a parent image
FROM python:3.11-slim

# RUN git clone https://github.com/Willowlark/Dizzy.git
# COPY auth.py /Dizzy/auth.py
COPY . /Lucy

# Set the working directory to /app
WORKDIR /Lucy


# RUN apt-get update
# RUN apt-get install -y wget curl apt-transport-https gcc
# RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
# RUN chmod +x mariadb_repo_setup
# RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.4"
# RUN apt-get update
# RUN apt-get install -y libmariadb3 libmariadb-dev

# run pip install cython
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# RUN cd discord.py;python setup.py install;cd /..

# Run app.py when the container launches
CMD ["python", "bot.py"]