# Ninjabot GUI

## setup
```bash
#clone repo change dir to project dir
npm install
```
add ninjabot stack
add ros-bridge-suit package of branch ros distro
add tf2-web-republisher package
to catkin_ws

### Run
should run roscore service manually, for physical robot not neccesarry it has already roscore running
Terminal1:
``` bash
#set network config
source ./set_env.sh
enter robot IP:xxx.xxx.xxx.xxx #localhost for current machine/simulation

roscore
```
Terminal2:
``` bash
#set network config
source ./set_env.sh
enter robot IP:xxx.xxx.xxx.xxx #localhost for current machine/simulation

#launch GUI
./launch_gui.sh
```