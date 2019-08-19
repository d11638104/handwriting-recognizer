import argparse

from sklearn.externals import joblib
from sklearn.svm import LinearSVC

import dataset
from hog import HOG

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-d', '--dataset', required=True, help='Path to the dataset file.')
argument_parser.add_argument('-m', '--model', required=True, help='Path to where the model will be stored.')
arguments = vars(argument_parser.parse_args())

(digits, target) = dataset.load_digits(arguments['dataset'])
data = []

hog = HOG(orientations=18, pixels_per_cell=(10, 10), cells_per_block=(1, 1), transform=True)

for image in digits:
    image = dataset.deskew(image, 20)
    image = dataset.center_extent(image, (20, 20))

    histogram = hog.describe(image)
    data.append(histogram)

model = LinearSVC(random_state=42)
model.fit(data, target)

joblib.dump(model, arguments['model'])
