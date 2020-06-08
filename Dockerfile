#
# Dockerfile for pfurl repository.
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pfurl .
#
# In the case of a proxy (located at say 10.41.13.4:3128), do:
#
#    export PROXY="http://10.41.13.4:3128"
#    docker build --build-arg http_proxy=${PROXY} --build-arg UID=$UID -t local/pfurl .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pfurl
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pfurl
#

FROM fnndsc/ubuntu-python3:latest
MAINTAINER fnndsc "dev@babymri.org"

# Pass a UID on build command line (see above) to set internal UID
ARG UID=1001
ENV UID=$UID

COPY . /src/pfurl
RUN apt-get update &&                                    \
    apt-get install -qq libssl-dev libcurl4-openssl-dev  \
    && pip install /src/pfurl                            \
    && rm -rf /src                                       \
    && useradd -M -u $UID pfurl

# Start as user $UID
USER $UID

ENTRYPOINT ["/usr/local/bin/pfurl"]
