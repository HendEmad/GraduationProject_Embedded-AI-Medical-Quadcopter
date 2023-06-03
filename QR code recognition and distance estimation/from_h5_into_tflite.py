import tensorflow as tf
from keras.models import load_model
model = load_model('my_model.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
with open('my_model.tflite', 'wb') as f:
    f.write(tflite_model)