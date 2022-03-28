import cv2
from matplotlib import pyplot as plt


def get_local_image(path):
	img = cv2.imread(path)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	# plt.imshow(img)
	# plt.show()

	# img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	# plt.imshow(img, cmap='gray')
	# plt.show()
	return img


def get_local_text_file(path):
	with open(path, 'r') as f:
		data = f.read()
		return data


def draw_bounding_box(img, pt1, pt2):
	img = cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
	return img


def getImageWidthHeight(img):
	return img.shape[:2]


def yolo_to_x_y(x_center, y_center, x_width, y_height, width, height):
	x_center *= width
	y_center *= height
	x_width *= width
	y_height *= height
	x_width /= 2.0
	y_height /= 2.0
	return int(x_center - x_width), int(y_center - y_height), int(
		x_center + x_width), int(y_center + y_height)


def change_color_except_point(img, point, color):
	img[point[1], point[0]] = color
	return img


def change_color_to_rgb(color):
	return tuple(map(lambda x: x / 255.0, color))


def change_color_area(x1, y1, x2, y2, img, color):
	img[y1:y2, x1:x2] = color
	return img


def change_color_except_area(x1, y1, x2, y2, img, color):
	img[y1:y2, x1:x2] = color
	return img


origin_image = image = get_local_image('images\\1.jpg')
text = get_local_text_file('labels\\1.txt')
height, width = getImageWidthHeight(image)
points = []
for line in text.split('\n'):
	if not line:
		continue
	split_data = line.split(' ');
	label = split_data[0]
	pos = line[line.find(' ') + 1:]
	x_center, y_center, x_width, y_width = [float(item) for item in
											pos.split(' ')]

	x1, y1, x2, y2 = yolo_to_x_y(x_center, y_center, x_width, y_width, width,
								 height)
	points.append((x1, y1, x2, y2))

for point in points:
	x1, y1, x2, y2 = point[0], point[1], point[2], point[3]
	image = draw_bounding_box(image, (x1, y1), (x2, y2))
	change_color_area(x1, y1, x2, y2, image, change_color_to_rgb((255, 0, 0)))

plt.imshow(image)
plt.show()
