import cv2
import torch
import torchvision
from torchvision import transforms as T
import numpy as np

model = torchvision.models.detection.ssd300_vgg16(weights="SSD300_VGG16_Weights.DEFAULT")
model.eval()


transform = T.ToTensor()


coco_names = [
    "__background__", "Person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", 
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "cat", "horse", 
    "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", 
    "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", 
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", 
    "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", 
    "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "TV", "laptop", "mouse", 
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", 
    "clock", "vase", "scissors", "mobile", "teddy bear", "hair drier", "toothbrush"
]

video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Error: Could not open webcam.")
    exit()

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = video.read()   
    if not ret:
        print("Failed to grab frame")
        break

    img = transform(frame)
    img = img.unsqueeze(0)
    
    with torch.no_grad():
        pred = model(img)
    
    bboxes, scores, labels = pred[0]["boxes"], pred[0]["scores"], pred[0]["labels"]
    indices = torch.where(scores > 0.5)[0]
  
    for i in indices:
        x1, y1, x2, y2 = bboxes[i].numpy().astype("int")
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        
        if labels[i] < len(coco_names):
            class_name = coco_names[labels[i]]
            frame = cv2.putText(frame, class_name, (x1, y1 - 10), font, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
    

    cv2.imshow('Khela hobe!', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
