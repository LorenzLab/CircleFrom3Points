import math

p1x, p1y = input("Point 1 x y (seperated by spaces): ").strip().split()
p2x, p2y = input("Point 2 x y (seperated by spaces): ").strip().split()
p3x, p3y = input("Point 3 x y (seperated by spaces): ").strip().split()

p1x, p1y, p2x, p2y, p3x, p3y = float(p1x), float(p1y), float(p2x), float(p2y), float(p3x), float(p3y)

# calculate circle center
p2x -= p1x
p3x -= p1x
p2y -= p1y
p3y -= p1y

d = 2 * (p2x * p3y - p3x * p2y)
if d == 0:
    raise ValueError("Points are collinear")
z1 = p2x ** 2 + p2y ** 2
z2 = p3x ** 2 + p3y ** 2
cx = (p3y * z1 - p2y * z2) / d + p1x
cy = (p2x * z2 - p3x * z1) / d + p1y

p2x += p1x
p3x += p1x
p2y += p1y
p3y += p1y

# calculate radius
r = ((p1x - cx) ** 2 + (p1y - cy) ** 2) ** 0.5

print(f"Center: ({cx}, {cy}) Radius: {r}")

# calculate p1 tangent slope
m1 = -(p1x - cx) / (p1y - cy)
# calculate line p1 p2 slope
m2 = (p2y - p1y) / (p2x - p1x)

# calculate the angle between the two lines
angle = math.degrees(math.atan((m1 - m2) / (1 + m1 * m2)))

print(f"Angle between line(p1, p2) and the tangent line of p1: {angle}")
