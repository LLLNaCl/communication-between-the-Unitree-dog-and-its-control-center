import time
import base64
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import threading

BROKER = "192.168.239.129"   # 测试服务器
PORT = 1883
KEEPALIVE = 60

rtsp_url = None
playing = False

def play_rtsp(rtsp_url):
    """用 OpenCV 播放 RTSP 流"""
    global playing
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print(f"[错误] 无法打开 RTSP 流: {rtsp_url}")
        return

    print(f"[控制中心] 正在播放 RTSP 视频流: {rtsp_url} 按 q 退出")
    playing = True

    while playing:
        ret, frame = cap.read()
        if not ret:
            print("[警告] 读取帧失败，可能是网络抖动")
            break

        cv2.imshow("Robot RTSP Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            playing = False
            break

    cap.release()
    cv2.destroyAllWindows()
    playing = False


def on_message(client, userdata, msg):
    global rtsp_url, playing

    if msg.topic == "dog/001/resp/video":
        rtsp_url = msg.payload.decode()
        print(f"[控制中心] 收到机器人 RTSP 地址: {rtsp_url}")
        if not playing:
            threading.Thread(target=play_rtsp, args=(rtsp_url,), daemon=True).start()

    elif msg.topic == "dog/001/resp/photo":
        print("[控制中心] 收到照片")
        photo_data = base64.b64decode(msg.payload)
        np_arr = np.frombuffer(photo_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        cv2.imshow("Robot Photo", frame)
        cv2.waitKey(3000)  # 显示 3 秒
        cv2.destroyWindow("Robot Photo")


def main():
    client = mqtt.Client(client_id="control001",callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    client.on_message = on_message

    print("[控制中心] 连接到 MQTT Broker...")
    client.connect(BROKER, PORT, KEEPALIVE)

    # 订阅机器人响应
    client.subscribe("dog/001/resp/video")
    client.subscribe("dog/001/resp/photo")

    client.loop_start()

    # 下发测试指令
    time.sleep(2)
    # client.publish("dog/001/cmd", "start_video")   # 让机器人推流

    # time.sleep(10)
    client.publish("dog/001/cmd", "take_photo")   # 抓一张照片

    # 保持运行
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()