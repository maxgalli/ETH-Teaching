import argparse
import cv2

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=""
    )

    parser.add_argument("--image", type=str, required=True, help="Path to image")

    parser.add_argument("--real-length", type=float, required=False, default=0.0, help="If passed, it is used to calibrate")
    parser.add_argument("--unit-length", type=float, required=False, default=0.0, help="If passed (in cm), multiply the number of units by this value to get the real length")

    return parser.parse_args()


class DrawLineWidget(object):
    def __init__(self, image, real_length=0.0, unit_length=0.0):
        self.original_image = cv2.imread(image)
        self.clone = self.original_image.copy()
        self.real_length = real_length
        self.unit_length = unit_length

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # List to store start/end points
        self.image_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            print('Starting: {}, Ending: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
            d_coord = self.compute_length()
            if self.real_length != 0.0:
                print('Distance: {}'.format(d_coord))
                print('1 unit = {} cm'.format(self.real_length / d_coord))
            elif self.unit_length != 0.0:
                real_length = d_coord * self.unit_length
                print('Distance: {} cm'.format(real_length))


            # Draw line
            cv2.line(self.clone, self.image_coordinates[0], self.image_coordinates[1], (36,255,12), 2)
            cv2.imshow("image", self.clone)

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def compute_length(self):
        if len(self.image_coordinates) == 2:
            x1, y1 = self.image_coordinates[0]
            x2, y2 = self.image_coordinates[1]

            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        else:
            return 0.0

    def show_image(self):
        return self.clone


def main(args):
    draw_line_widget = DrawLineWidget(args.image, args.real_length, args.unit_length)
    while True:
        cv2.imshow('image', draw_line_widget.show_image())
        key = cv2.waitKey(1)

        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)