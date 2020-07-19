FROM python:3.7-buster

RUN apt-get update

# odbc to ms sql odbc server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update

RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc-dev dos2unix \
    && ln -s /opt/mssql-tools/bin/bcp /usr/bin/bcp

RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev mssql-tools

WORKDIR /usr/lib/app

COPY requirements.txt ./

# system libraries install
RUN apt-get install -y gcc build-essential libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir dumb-init \
    && apt-get purge -y --auto-remove gcc build-essential

ADD app.py ./app.py
ADD /db    ./db
ADD /utils ./utils
ADD config.yml ./config.yml

# simple process supervisor (dumb init)
ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["python", "app.py", "--c", "config.dev.yml"]
