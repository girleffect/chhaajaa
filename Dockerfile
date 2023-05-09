# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.10.11-slim-buster

# Create the user and group first as they shouldn't change often.
# Specify the UID/GIDs so that they do not change somehow and mess with the
# ownership of external volumes.
RUN addgroup --system --gid 107 wagtail \
    && adduser --system --uid 104 --ingroup wagtail wagtail
    # && mkdir /etc/gunicorn

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    nginx \
    gosu \
    # Below required for RapidPro cronjobs
    unixodbc unixodbc-dev \
 && rm -rf /var/lib/apt/lists/*


# Add nginx user to wagtail group so that Nginx can read/write to gunicorn socket
RUN adduser --system nginx --ingroup wagtail
COPY nginx/ /etc/nginx/
RUN sed -i 's/www-data;/nginx wagtail;/' /etc/nginx/nginx.conf

# Install gunicorn
RUN pip install "gunicorn==20.0.4"
COPY gunicorn/ /etc/gunicorn/
RUN mkdir /run/gunicorn && chown wagtail:wagtail /run/gunicorn

EXPOSE 8000
WORKDIR /app

RUN chown wagtail:wagtail /app
# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Install the project requirements.
COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt 

ENV DJANGO_SETTINGS_MODULE=chajaa.settings.production 
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
CMD [ "./entrypoint.sh" ]