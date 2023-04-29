import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras

model = tf.saved_model.load("rock_resnet")

st.title("Rock Classification")

img_file = st.file_uploader("รูปภาพ", type=["png", "jpg", "jpeg"])
if img_file is not None:
    img = keras.utils.load_img(img_file, target_size=(224, 224))
    input_array = keras.utils.img_to_array(img)

    prediction, label = model(input_array)

    label = [i.numpy().decode("utf-8") for i in label]

    st.image(img_file, caption=label[prediction.numpy().argmax()])
    
    fig, ax = plt.subplots()
    ax.barh(label, prediction.numpy().reshape((4,)))
    st.pyplot(fig)
    