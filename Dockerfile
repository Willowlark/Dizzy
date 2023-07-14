# Use an official Python runtime as a parent image
FROM python:3.11

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE `/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99

COPY . /Lucy
# COPY ./cogs/chromedriver /usr/local/bin/chromedriver
WORKDIR /Lucy

# run pip install cython
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# RUN cd discord.py;python setup.py install;cd /..

# Run app.py when the container launches
CMD ["python", "bot.py"]