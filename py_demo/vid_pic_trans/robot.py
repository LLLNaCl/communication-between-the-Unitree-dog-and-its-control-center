import time
import base64
import cv2
import paho.mqtt.client as mqtt
import subprocess
import signal
import os

BROKER = "192.168.239.129"   # 测试服务器，后续换成云端 IP
PORT = 1883
KEEPALIVE = 60

# 推流目标地址（假设你的 RTSP 服务器在本地或云端 8554 端口）
RTSP_URL = "rtsp://192.168.239.129:8554/dog001"

ffmpeg_process = None  # 保存 ffmpeg 子进程句柄


def start_ffmpeg_stream():
    """启动 ffmpeg，将本机摄像头推送到 RTSP 服务器"""
    global ffmpeg_process

    if ffmpeg_process is not None:
        print("[机器人] 推流已经在进行中")
        return

    # Linux 摄像头: v4l2
    # Windows 摄像头: dshow -i video="你的摄像头名称"
    cmd = [
        "ffmpeg",
        "-f", "v4l2",
        "-i", "/dev/video0",
        "-s", "640x360",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-f", "rtsp",
        RTSP_URL
    ]

    try:
        ffmpeg_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[机器人] ffmpeg 推流进程已启动，推送到 {RTSP_URL}")
    except Exception as e:
        print(f"[机器人] 启动 ffmpeg 失败: {e}")


def stop_ffmpeg_stream():
    """停止 ffmpeg 推流"""
    global ffmpeg_process
    if ffmpeg_process is not None:
        os.kill(ffmpeg_process.pid, signal.SIGTERM)
        ffmpeg_process = None
        print("[机器人] 已停止 ffmpeg 推流")


def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"[机器人] 收到指令: {command}")

    if command == "start_video":
        start_ffmpeg_stream()
        # 回复 RTSP 地址
        client.publish("dog/001/resp/video", RTSP_URL)

    elif command == "stop_video":
        stop_ffmpeg_stream()

    elif command == "take_photo":
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            _, buffer = cv2.imencode(".jpg", frame)
            photo_b64 = base64.b64encode(buffer).decode("utf-8")
            client.publish("dog/001/resp/photo", photo_b64)
            print("[机器人] 上传当前照片")
        else:
            print("[机器人] 拍照失败")


def main():
    client = mqtt.Client(client_id="robot001",callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    client.on_message = on_message

    print("[机器人] 连接到 MQTT Broker...")
    client.connect(BROKER, PORT, KEEPALIVE)

    # 订阅控制指令
    client.subscribe("dog/001/cmd")

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        stop_ffmpeg_stream()
        print("[机器人] 退出")


if __name__ == "__main__":
    main()
