import base64
import cv2
import numpy as np
import paho.mqtt.client as mqtt

BROKER = "your-cloud-server-ip"
PORT = 1883
KEEPALIVE = 60

def on_message(client, userdata, msg):
    if msg.topic == "dog/001/resp/video":
        rtsp_url = msg.payload.decode()
        print(f"[控制中心] 机器人视频流地址: {rtsp_url}")
        print("用 VLC/ffplay 播放，例如:")
        print(f"ffplay {rtsp_url}")

    elif msg.topic == "dog/001/resp/photo":
        photo_data = base64.b64decode(msg.payload)
        np_arr = np.frombuffer(photo_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        cv2.imshow("Robot Photo", frame)
        cv2.waitKey(3000)  # 显示3秒

def main():
    client = mqtt.Client("control001")
    client.on_message = on_message

    print("[控制中心] 连接到 MQTT Broker...")
    client.connect(BROKER, PORT, KEEPALIVE)

    # 订阅机器人响应
    client.subscribe("dog/001/resp/video")
    client.subscribe("dog/001/resp/photo")

    client.loop_start()

    # 下发测试指令
    time.sleep(2)
    client.publish("dog/001/cmd", "start_video")
    time.sleep(5)
    client.publish("dog/001/cmd", "take_photo")

    while True:
        pass

if __name__ == "__main__":
    main()