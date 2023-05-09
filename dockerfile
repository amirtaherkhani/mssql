#https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver16

# build from the Ubuntu 18.04 image
FROM ubuntu:20.04
 
# create the mssql user
RUN useradd -u 10001 mssql
 
# installing SQL Server
RUN apt-get update && apt-get install -y wget software-properties-common apt-transport-https
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc |  tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/20.04/mssql-server-2022.list)"
RUN apt-get update && apt-get install -y mssql-server
RUN apt-get  autoclean -y 
RUN apt-get clean autoclean
RUN apt-get autoremove --yes
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

# creating directories
RUN mkdir /var/opt/sqlserver
RUN mkdir /var/opt/sqlserver/data
RUN mkdir /var/opt/sqlserver/log
RUN mkdir /var/opt/sqlserver/backup
 
# set permissions on directories
RUN chown -R mssql:mssql /var/opt/sqlserver
RUN chown -R mssql:mssql /var/opt/mssql
EXPOSE 1433
# switching to the mssql user
USER mssql

 
# starting SQL Server
CMD /opt/mssql/bin/sqlservr
