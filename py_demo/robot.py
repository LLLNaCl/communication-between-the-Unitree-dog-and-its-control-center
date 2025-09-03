import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"  # 公共测试服务器
PORT = 1883
KEEPALIVE = 60

# 收到任务时的回调
def on_message(client, userdata, msg):
    print(f"[机器人] 收到任务: {msg.payload.decode()} (Topic: {msg.topic})")
    task = msg.payload.decode()
    
    # if task == "巡检A路线":
        
    #     # 这里可以调用实际的动作函数
    # elif task == "返回充电":
        
    #     # 这里可以调用实际的动作函数
    # else:
    #     print("[机器人] 未知任务，等待指令")

client = mqtt.Client()
client.on_message = on_message

print("[机器人] 连接到 MQTT Broker...")
client.connect(BROKER, PORT, KEEPALIVE)

# 订阅任务 Topic
client.subscribe("dog/001/cmd/task")

# 启动循环
client.loop_start()

# 模拟定时发送状态
while True:
    status_msg = '{"battery": 88, "position": "A点"}'
    client.publish("dog/001/status", status_msg)
    print(f"[机器人] 上报状态: {status_msg}")
    time.sleep(5)
