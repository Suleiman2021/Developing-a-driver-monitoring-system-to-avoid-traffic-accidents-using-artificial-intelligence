import cv2
import torch
from ultralytics import YOLO
import random
import requests

# تحميل نموذج YOLOv8
model_path = 'C:/Users/it4infinite/Desktop/Yolo_project/runs/obb/train6/weights/best.pt'
try:
    model = YOLO(model_path)
    print(f"Model loaded successfully from {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# فتح فيديو
video_path = 'C:/Users/it4infinite/Desktop/Yolo_project/YOLO_S1.mp4'
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error opening video file: {video_path}")
    exit()

# الحصول على تفاصيل الفيديو
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f"Video details - Width: {frame_width}, Height: {frame_height}, FPS: {fps}")

# إعداد كاتب الفيديو لحفظ الفيديو الناتج
output_path = 'output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# قائمة من الألوان العشوائية
colors = []

# عنوان سيرفر Flask
flask_url = 'http://127.0.0.1:5000/receive_classes'

# قراءة الإطارات من الفيديو ومعالجتها
frame_counter = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_counter % 10 == 0:
        # تشغيل الكشف على الإطار باستخدام النموذج
        results = model(frame)
        frame_counter += 1

        # تأكد من أن النتائج ليست فارغة
        if not results:
            print(f"No results found for frame {frame_counter}.")
            continue

        print(f"Results for frame {frame_counter}: {results}")

        # قائمة لتخزين أسماء الفئات
        detected_classes = []

        # رسم النتائج على الإطار
        for result in results:
            if result.obb is not None:  # تحقق من أن result.obb ليست None
                for obb in result.obb:
                    # تحويل Tensor إلى numpy array ثم إلى int
                    points = obb.xyxy[0].cpu().numpy().astype(int)
                    conf = obb.conf[0].item()
                    cls = obb.cls[0].item()
                    # تحقق من أن الثقة أكبر من أو تساوي 0.7
                    if conf < 0.7:
                        continue
                    label = f"{model.names[int(cls)]} {conf:.2f}"

                    print(f"Frame {frame_counter}: {label} with confidence {conf:.2f}")

                    # إضافة اسم الفئة إلى القائمة
                    detected_classes.append(model.names[int(cls)])

                    # تحقق من أن قائمة الألوان تحتوي على لون لكل فئة
                    while len(colors) <= int(cls):
                        colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

                    # اختيار اللون المناسب من القائمة
                    color = colors[int(cls)]

                    # رسم المربع المحيط
                    xmin, ymin, xmax, ymax = points
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)

                    # إعداد النص في الزاوية السفلى اليسرى من المربع
                    font_scale = 0.5 + 37 / 100  # تكبير النص بمقدار 18
                    font_thickness = 2
                    text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
                    text_x = xmin
                    text_y = ymax

                    # رسم خلفية للنص
                    cv2.rectangle(frame, (text_x, text_y - text_size[1] - 5), (text_x + text_size[0], text_y + 5), color, -1)

                    # رسم النص
                    cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness)

        # إرسال أسماء الفئات المكتشفة إلى سيرفر Flask
        try:
            response = requests.post(flask_url, json={"classes": detected_classes})
            if response.status_code == 200:
                print(f"Successfully sent classes for frame {frame_counter}: {detected_classes}")
            else:
                print(f"Failed to send classes for frame {frame_counter}: {response.text}")
        except Exception as e:
            print(f"Error sending classes to Flask server: {e}")

        # تغيير حجم الإطار ليتناسب مع نافذة العرض 640x480
        resized_frame = cv2.resize(frame, (640, 480))

        # عرض الإطار الناتج في حجم النافذة المحدد (اختياري)
        cv2.imshow('YOLOv8 Detection', resized_frame)

        # كتابة الإطار الأصلي (غير المعدل بالحجم) إلى ملف الفيديو الناتج
        out.write(frame)

        # اضغط على مفتاح 'q' للخروج من العرض المباشر
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    frame_counter += 1

# تحرير موارد الفيديو
cap.release()
out.release()
cv2.destroyAllWindows()