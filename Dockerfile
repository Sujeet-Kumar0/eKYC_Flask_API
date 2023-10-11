# Use an official Python runtime as the base image
FROM python:3.10-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Passing the aws credentials
COPY ./.aws/ /root/.aws/ 

# Copy the current directory contents into the container at /app
COPY . /app

# # Install the tesseract and its required packages
# # This is method to install the tesseract5
# RUN apt-get update && apt-get install -y apt-utils && \
#    apt-get install -y software-properties-common && \
#    apt-get install -y gnupg \
#    wget && \
#    apt-get install apt-transport-https && \
#    apt-get clean

# RUN echo "deb https://notesalexp.org/tesseract-ocr5/bullseye/ bullseye main" \
#    | tee /etc/apt/sources.list.d/notesalexp.list > /dev/null

# RUN wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add -

RUN apt-get update -y&& apt-get upgrade -y &&\
   apt-get install -y --fix-missing --no-install-recommends\
   build-essential \
   gcc mono-mcs \
   g++\
   autoconf automake libtool \
   cmake \
   gfortran \
   libopenblas-dev \
   libavcodec-dev \
   libavformat-dev \
   libswscale-dev \
   libavdevice-dev  \
   libavfilter-dev  \
   libswresample-dev \
   libavutil-dev \
   libleptonica-dev \
   ffmpeg libsm6 libxext6  \ 
   pkg-config \
   libpng-dev \
   libjpeg62-turbo-dev \
   libtiff5-dev \
   zlib1g-dev \
   libwebpdemux2 libwebp-dev \
   libopenjp2-7-dev\
   libgif-dev\
   libarchive-dev libcurl4-openssl-dev && \
   apt upgrade -y && \
   apt-get clean && rm -rf /tmp/* /var/tmp/*

# ca-certificates\
# cabextract\
# debconf\
# wget\ 
# xfonts-utils\
# fonts-liberation\
# RUN wget http://ftp.tw.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.8_all.deb

# RUN dpkg -i ttf-mscorefonts-installer_3.8_all.deb

# Install Git and Git LFS
RUN apt-get update && \
   apt-get install -y git-lfs && \
   git lfs install

# Set the username and password for authentication
ARG USERNAME=your_username
ARG PASSWORD=your_password

# Create the weights folder
RUN mkdir weights

# Create the .netrc file with Git credentials
RUN echo "machine huggingface.co login $USERNAME password $PASSWORD" > ~/.netrc && \
   chmod 600 ~/.netrc

# Clone the private repository
RUN git clone https://huggingface.co/SujeetKumar/kyc_docs_classification /app/weights

# Clean up unnecessary files
RUN rm -rf /app/weights/.git

# RUN cd ~ && \
#    mkdir -p dlib && \
#    git clone https://github.com/davisking/dlib.git dlib/ && \
#    cd  dlib/ && \
#    python3 setup.py install

# RUN cd /app

# Install all dependencies for python
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV=production

# Expose port 5000 for the Flask API to listen on
EXPOSE 5000

RUN python setup.py

# Run the command to start the Flask API
# CMD ["flask", "run", "--host=0.0.0.0"]

# Run the command to start as the Gunicorn API
CMD ["gunicorn", "--workers=2","--threads=6", "--timeout=60","--graceful-timeout=300", "--bind=0.0.0.0:5000", "app:app"]