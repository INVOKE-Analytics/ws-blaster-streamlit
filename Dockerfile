# Get a python3.10 base image
FROM public.ecr.aws/lambda/python:3.8

RUN yum -y install wget

# # install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | yum-config-manager --add-repo - && \
#     sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    yum install ./google-chrome-stable_current_*.rpm -y


RUN yum -y update && \
    yum install xorg-x11-server-Xvfb -y && \
    yum install -y google-chrome-stable

# Copy the requirements for the project
COPY requirements.txt .

# Install the requirements for the project
RUN pip3 install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY ./ws_blaster ${LAMBDA_TASK_ROOT}/ws_blaster
COPY ./app ${LAMBDA_TASK_ROOT}/app

# Run this commend on start up 
CMD [ "app.main.handler" ]