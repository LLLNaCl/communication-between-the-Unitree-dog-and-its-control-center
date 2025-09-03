# 项目内容
搭建简易的传输平台验证 MQTT 双向通信，C++版本
# 项目结构
```plaintext
mqtt_demo_cpp/
├── robot.cpp        # 模拟机器狗
├── control.cpp      # 模拟控制中心
└── CMakeLists.txt
```

# 前期准备
需要先安装 Eclipse Paho MQTT C/C++，Ubuntu 下可以用：
```bash
sudo apt-get install libpaho-mqttpp3-dev libpaho-mqtt3c-dev
```

# 运行
在cpp_demo目录下，使用以下命令编译并运行：
```bash
mkdir build
cd build
cmake ..
make
```
然后分别在两个终端中运行：
```bash
./robot
```
```bash
./control
```