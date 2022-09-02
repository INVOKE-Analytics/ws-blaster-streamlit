# Get a python3.10 base image
FROM public.ecr.aws/lambda/python:3.8

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update && \
    apt-get install xvfb xclip -y && \
    apt-get install -y google-chrome-stable

# Copy the requirements for the project
COPY requirements.txt .

# Install the requirements for the project
RUN pip3 install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY ./ws_blaster ${LAMBDA_TASK_ROOT}/ws_blaster
COPY ./app ${LAMBDA_TASK_ROOT}/app

# Run this commend on start up 
CMD [ "app.main.handler" ]