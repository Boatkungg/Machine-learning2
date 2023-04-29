import tensorflow as tf
from tensorflow import keras

reloaded = tf.saved_model.load("rock_resnet")

img_path = "./image/Test/H17868b540438467c8c517f31063c1587S.jpg"
img = keras.utils.load_img(img_path, target_size=(224, 224))
input_array = keras.utils.img_to_array(img)

prediction, label = reloaded(input_array)

label = [i.numpy().decode("utf-8") for i in label]

print(label)
print(label[prediction.numpy().argmax()])