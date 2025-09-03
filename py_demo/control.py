import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
KEEPALIVE = 60

# 收到机器人状态时的回调
def on_message(client, userdata, msg):
    print(f"[控制中心] 收到状态: {msg.payload.decode()} (Topic: {msg.topic})")

client = mqtt.Client()
client.on_message = on_message

print("[控制中心] 连接到 MQTT Broker...")
client.connect(BROKER, PORT, KEEPALIVE)

# 订阅机器人状态
client.subscribe("dog/001/status")

# 启动循环
client.loop_start()

# 模拟下发任务
while True:
    task_msg = "巡检A路线"
    client.publish("dog/001/cmd/task", task_msg)
    print(f"[控制中心] 下发任务: {task_msg}")
    time.sleep(5)
