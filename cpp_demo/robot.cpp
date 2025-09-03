#include <iostream>
#include <chrono>
#include <thread>
#include "mqtt/async_client.h" // 需要完成readme中的前期准备

const std::string BROKER = "tcp://test.mosquitto.org:1883"; // 公共测试服务器
const std::string CLIENT_ID = "robot001";
const std::string TOPIC_TASK = "dog/001/cmd/task";
const std::string TOPIC_STATUS = "dog/001/status";

class callback : public virtual mqtt::callback {
public:
    void message_arrived(mqtt::const_message_ptr msg) override {
        std::cout << "[机器人] 收到任务: " << msg->to_string()
                  << " (Topic: " << msg->get_topic() << ")" << std::endl;
    }
};

int main() {
    mqtt::async_client client(BROKER, CLIENT_ID);
    callback cb;
    client.set_callback(cb);

    mqtt::connect_options connOpts;
    connOpts.set_keep_alive_interval(60);
    connOpts.set_clean_session(true);

    try {
        std::cout << "[机器人] 连接到 MQTT Broker..." << std::endl;
        client.connect(connOpts)->wait();

        client.start_consuming();
        client.subscribe(TOPIC_TASK, 1)->wait();

        while (true) {
            std::string status = "{\"battery\": 88, \"position\": \"A点\"}";
            client.publish(TOPIC_STATUS, status, 1, false);
            std::cout << "[机器人] 上报状态: " << status << std::endl;
            std::this_thread::sleep_for(std::chrono::seconds(5));
        }

        client.disconnect()->wait();
    } catch (const mqtt::exception& exc) {
        std::cerr << exc.what() << std::endl;
        return 1;
    }

    return 0;
}
