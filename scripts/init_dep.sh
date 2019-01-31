#!/bin/bash

set -e;

# language-pack-en
apt-get update;
apt-get install -y locales gnupg2 nginx default-libmysqlclient-dev software-properties-common;
locale-gen en_US.UTF-8;
update-locale LANG=en_US.UTF-8 LC_CTYPE=en_US.UTF-8;
