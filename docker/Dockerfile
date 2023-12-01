# Author: Jaewon Lee
# email: jawwoni@naver.com

FROM ubuntu:20.04

RUN apt-get -y update
RUN apt-get -y install python3.9
RUN apt-get -y install python3-pip

RUN apt-get -y update
RUN apt-get install -y git

# Python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
RUN python -m pip install --upgrade pip

# Dependency
RUN apt-get install -y python3.9-dev
RUN apt-get install -y python3-tk
RUN apt-get install -y libgl1-mesa-glx libx11-dev
RUN ldconfig

RUN apt-get install -y libfreetype6-dev libfontconfig1-dev

WORKDIR /root/workspace/src

WORKDIR /root/workspace

# Load ROS environment at each run
COPY ./entrypoint.sh /
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["bash"]

# Issues
# https://stackoverflow.com/questions/62352767/cant-install-open3d-libraries-errorcould-not-find-a-version-that-satisfies-th
# https://daebaq27.tistory.com/90