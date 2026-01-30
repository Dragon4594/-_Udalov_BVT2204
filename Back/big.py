import os
from ultralytics import YOLO
from PIL import Image
import cv2
import datetime
import json
def print_box(box):
    class_id, cords, conf = box
    print("Object type:", class_id)
    print("Coordinates:", cords)
    print("Probability:", conf)
    print("---")
    return class_id


def result(b,img):
    '''count_class = []
    for box in b.boxes:
        (print_box([
            b.names[box.cls[0].item()],
            [round(x) for x in box.xyxy[0].tolist()],
            round(box.conf[0].item(), 2)
        ]))'''
    i=0
    path = r"report_requests\serv_data"
    file = f"report_requests\serv_data\i{i}.json"
    if not os.path.exists(path):
        os.makedirs(path)
    while os.path.exists(file):
        i += 1
        file = f"report_requests\serv_data\i{i}.json"

    count_class = []
    for box in b.boxes:
        count_class.append(b.names[box.cls[0].item()])

    countClass = [["car", 0], ["threewheel", 0], ["bus", 0], ["truck", 0], ["motorbike", 0], ["van", 0]]

    for img_class in count_class:
        if img_class == "car":
            countClass[0][1] += 1
        elif img_class == "threewheel":
            countClass[1][1] += 1
        elif img_class == "bus":
            countClass[2][1] += 1
        elif img_class == "truck":
            countClass[3][1] += 1
        elif img_class == "motorbike":
            countClass[4][1] += 1
        elif img_class == "van":
            countClass[5][1] += 1
    data = [[f"time: {datetime.datetime.now()}"]]
    for box in b.boxes:
        data.append(
            [f"Object type: {b.names[box.cls[0].item()]}", f"Coordinates: {[round(x) for x in box.xyxy[0].tolist()]}",
             f"Probability: {round(box.conf[0].item(), 2)}", "==============="])
    data.append([countClass,f"cars_detected: {len(countClass)}"])
    data.append([f"original_img_directory: {img}", f"normalized_img_directory: {img[:-4] + "_norm.jpg"}", f"augmented_img_directory: {img[:-4] + "_aug.jpg"}"])
    with open(file, "w") as f:
        json.dump(data, f, indent=2)
    return countClass


def neuro_proceed(img: str):
    #print("neuro called and saw img: ", img)
    image = cv2.imread(img)
    size = image.shape
    if (1<(size[1]/size[0])<2) and (size[1]<1000):
        x=940
        y=600
    elif (size[1]/size[0]>=2) :
        x = 1060
        y = 600
    elif (1<=(size[1]/size[0])<2):
        x=1060
        y=600

    normalized_image = cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
    normalized_image = cv2.resize(normalized_image, (x, y), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f".{img.partition('.')[2].partition('.')[0]}_norm.jpg", normalized_image)
    model = YOLO(f"{os.path.abspath('')}/Back/best.pt")
    a = model.predict(f".{img.partition('.')[2].partition('.')[0]}_norm.jpg")
    b = a[0]
    res = result(b, img)
    #print(res, " / Общее число автосредств:", res[0][1] + res[1][1] + res[2][1] + res[3][1] + res[4][1] + res[5][1])

    for i, r in enumerate(a):
        print(f".{img.partition('.')[2].partition('.')[0]}_aug.jpg")
        r.save(filename=f".{img.partition('.')[2].partition('.')[0]}_aug.jpg")
    return (str(res) + " / cars are overloaded: " +
            str( res[0][1] + res[1][1] + res[2][1] + res[3][1] + res[4][1] + res[5][1]) + "\n"
            + "size norm: "+ str(normalized_image.shape[1]) +"x"+str(normalized_image.shape[0]) +
            " original: " + str(size[1]) +"x"+str(size[0]))
