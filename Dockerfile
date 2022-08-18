# Get a python3.10 base image
FROM python:3.10

# Set the main working directory
WORKDIR /ws-blaster-prod

# Copy the requirements for the project
COPY ./requirements.txt /ws-blaster-prod/requirements.txt

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Install the requirements for the project
RUN apt-get install xvfb xclip -y && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# set display port to avoid crash
# ENV DISPLAY=:99

# Copy the main files into the container
COPY ./ws_blaster /ws-blaster-prod/ws_blaster
COPY ./images /ws-blaster-prod/images
COPY ./Screenshot /ws-blaster-prod/Screenshot

# Run this commend on start up 
CMD ["python", "-m", "streamlit", "run", "ws_blaster/launch.py"]