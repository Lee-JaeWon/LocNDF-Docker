#!/bin/bash
 
set -e

# echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
# echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc

echo "alias cw='cd ~/workspace'" >> ~/.bashrc
echo "alias cs='cd ~/workspace/src'" >> ~/.bashrc
# echo "alias cm='cd ~/catkin_ws && catkin_make'" >> ~/.bashrc
echo "alias sb='source ~/.bashrc'" >> ~/.bashrc

cd /root/workspace/src

pip install .
pip install -r requirements.txt

git config --global --add safe.directory /root/workspace/src

pip install -U tensorboardX


echo "============== LocNDF Docker Env Ready================"

cd /root/workspace

exec "$@"
