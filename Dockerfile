FROM ubuntu:22.04

# Install kubectl and python
RUN apt-get update && apt-get install -y curl python3 python3-pip
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Copy the script
RUN mkdir /opt/app
WORKDIR /opt/app
COPY script.py /opt/app/script.py
COPY requirements.txt /opt/app/requirements.txt

# Install the required python packages
RUN pip install -r requirements.txt

# Run the script
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "script:app"]