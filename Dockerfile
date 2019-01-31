FROM sphere/prod:0.6
WORKDIR /var/www/app

ADD scripts/init_dep.sh /tmp/init_dep.sh
ADD AppWeb/requirements.txt /tmp/requirements.txt
RUN /tmp/init_dep.sh && pip3 install -r /tmp/requirements.txt

ADD . /var/www/app
RUN /var/www/app/scripts/init_projects.sh

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 7000 7001
CMD ["/usr/bin/runsvdir", "/var/www/app/scripts/runit"]