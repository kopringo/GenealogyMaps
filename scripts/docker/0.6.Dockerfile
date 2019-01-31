FROM ubuntu:bionic

# Use baseimage-docker's init system.
CMD ["/bin/run_empty"]

ADD . /bd_build
RUN bash /bd_build/image/prepare6.sh

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*