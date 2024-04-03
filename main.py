import math


def calculate_answer(p1x, p1y, p2x, p2y, p3x, p3y):
    # calculate circle center
    p2x -= p1x
    p3x -= p1x
    p2y -= p1y
    p3y -= p1y

    d = 2 * (p2x * p3y - p3x * p2y)
    if d == 0:
        raise ValueError("Points are collinear")
    z1 = p2x**2 + p2y**2
    z2 = p3x**2 + p3y**2
    cx = (p3y * z1 - p2y * z2) / d + p1x
    cy = (p2x * z2 - p3x * z1) / d + p1y

    p2x += p1x
    p3x += p1x
    p2y += p1y
    p3y += p1y

    # calculate radius
    r = ((p1x - cx) ** 2 + (p1y - cy) ** 2) ** 0.5

    # calculate p1 tangent slope
    m1 = -(p1x - cx) / (p1y - cy)
    # calculate line p1 p2 slope
    m2 = (p2y - p1y) / (p2x - p1x)

    # calculate the angle between the two lines
    angle = math.degrees(math.atan((m1 - m2) / (1 + m1 * m2)))
    return cx, cy, r, angle


def main_terminal_input_mode():
    p1x, p1y = input("Point 1 x y (seperated by spaces): ").strip().split()
    p2x, p2y = input("Point 2 x y (seperated by spaces): ").strip().split()
    p3x, p3y = input("Point 3 x y (seperated by spaces): ").strip().split()

    p1x, p1y, p2x, p2y, p3x, p3y = (
        float(p1x),
        float(p1y),
        float(p2x),
        float(p2y),
        float(p3x),
        float(p3y),
    )

    cx, cy, r, angle = calculate_answer(p1x, p1y, p2x, p2y, p3x, p3y)

    print(f"Center: ({cx}, {cy}) Radius: {r} Angle: {angle}")


def annotate_image(image_path):
    import cv2

    LINE_MULTIPLIER = 10
    
    points = []
    good = False
    
    def draw_circle(event, x, y, flags, param):
        global cx, cy, r, angle
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
            mouseX, mouseY = x, y
            points.append((mouseX, mouseY))
            if len(points) == 2:
                cv2.line(image, points[0], points[1], (0, 0, 255), 2)
            if len(points) == 3:
                cx, cy, r, angle = calculate_answer(points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1])
                
                normal_vector = (cy - points[0][1]) * LINE_MULTIPLIER, -(cx - points[0][0]) * LINE_MULTIPLIER
                cv2.line(image, (points[0][0], points[0][1]), (int(points[0][0] + normal_vector[0]), int(points[0][1] + normal_vector[1])), (0, 255, 0), 2)
                cv2.line(image, (points[0][0], points[0][1]), (int(points[0][0] - normal_vector[0]), int(points[0][1] - normal_vector[1])), (0, 255, 0), 2)

                cx, cy, r = int(cx), int(cy), int(r)
                cv2.circle(image, (cx, cy), r, (0, 255, 255), 2)
                cv2.putText(image, f"Angle: {angle:.2f}", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", draw_circle)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)


    while True:
        cv2.imshow("image", image)
        k = cv2.waitKey(20) & 0xFF
        if k == ord('a'):
            # good
            good = True
            break
        elif k == ord('r'):
            # reset
            break
        
    return cx, cy, r, angle, good

def main_looping_image_mode(image_folder_path):
    import os
    import csv

    for image_path in os.listdir(image_folder_path):
        if not image_path.endswith((".png", ".jpg", ".jpeg")):
            continue
        while True:
            cx, cy, r, angle, good = annotate_image(os.path.join(image_folder_path, image_path))
            if good:
                print(f"Center: ({cx}, {cy}) Radius: {r} Angle: {angle} Image: {image_path}")
                with open(f"output_{image_folder_path}.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([image_path, cx, cy, r, angle])
                    break
            else:
                print(f"Image {image_path} was reset")
    pass


if __name__ == "__main__":
    main_looping_image_mode("test_imgs")
