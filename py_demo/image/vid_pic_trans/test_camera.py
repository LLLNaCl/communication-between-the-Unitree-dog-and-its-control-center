import cv2

def test_camera():
    # 打开默认摄像头（通常是0，也可能是1等，取决于系统配置）
    cap = cv2.VideoCapture(0)
    
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    # 循环读取摄像头帧并显示
    while True:
        # 读取一帧画面
        ret, frame = cap.read()
        
        # 如果读取失败，退出循环
        if not ret:
            print("无法接收帧 (可能摄像头已断开)。退出中...")
            break
        
        # 显示画面
        cv2.imshow('摄像头测试 (按q退出)', frame)
        
        # 等待1毫秒，如果按下'q'键则退出循环
        if cv2.waitKey(1) == ord('q'):
            break
    
    # 释放摄像头资源
    cap.release()
    # 关闭所有OpenCV窗口
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()
    