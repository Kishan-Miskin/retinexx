import cv2
import numpy as np
import tensorflow as tf

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Load model ONCE at startup, not on every request
print("Loading CNN model...")
_model = tf.saved_model.load("64x3-CNN.model")
_infer = _model.signatures["serving_default"]
print("CNN model loaded successfully.")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_class(path):
    img = cv2.imread(path)
    RGBImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    RGBImg = cv2.resize(RGBImg, (224, 224))
    image = np.array(RGBImg) / 255.0

    predict = _infer(tf.constant([image], dtype=tf.float32))
    probabilities = predict['dense_1'].numpy()[0].tolist()

    diagnosis = (
        "No Diabetic Retinopathy Detected"
        if np.argmax(probabilities) == 1
        else "Diabetic Retinopathy Detected"
    )

    return diagnosis, probabilities