FROM ubuntu:focal

ARG CARLA_RELEASE=0.9.13

# Install core packages required to install from external repos
# Install CARLA

# Change WORKDIR
WORKDIR /home/carla/

# Install missing CARLA dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
        xdg-user-dirs \
        xdg-utils \
        libsdl2-2.0 \
        xserver-xorg \
        libomp5 \
	    wget \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* 

# Download and extract carla with rss command
RUN sh -c "wget -nc -qO- https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.13_RSS.tar.gz | tar -xzv" 
# -C /home/carla

# Make server ports accessible outside container
EXPOSE 2000-2002

# Add a container user (good practice)
 RUN groupadd work -g 1000 \
    && useradd -ms /bin/bash carla -g 1000 -u 1000 \
    && printf "carla:carla" | chpasswd \
    && printf "carla ALL= NOPASSWD: ALL\\n" >> /etc/sudoers
    
USER carla


# Run the server by default
ENTRYPOINT ["./CarlaUE4.sh"]
