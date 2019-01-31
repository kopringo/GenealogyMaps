FROM sphere/prod:0.6
WORKDIR /var/www/app

# ADD scripts/init_dep.sh /tmp/init_dep.sh
ADD requirements.txt /tmp/requirements.txt
ADD scripts/init_dep.sh /tmp/init_dep.sh
RUN bash /tmp/init_dep.sh && pip3 install -r /tmp/requirements.txt

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# porty + domysle polecenie
EXPOSE 7000 7001
CMD ["/usr/bin/runsvdir", "/var/www/app/scripts/runit"]