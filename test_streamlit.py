import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras

@st.cache_resource
def load_model():
    return tf.saved_model.load("rock_resnet_model")

with st.spinner("กำลังเริ่มต้น"):
    model = load_model()

st.title("Rock Classification")

img_file = st.file_uploader("รูปภาพ", type=["png", "jpg", "jpeg"])
if img_file is not None:
    img = keras.utils.load_img(img_file, target_size=(224, 224))
    input_array = keras.utils.img_to_array(img)

    with st.spinner("กำลังประมวณผล"):
        prediction, label = model(input_array)

    label = [i.numpy().decode("utf-8") for i in label]

    max_class = prediction.numpy().argmax()

    col1, col2 = st.columns(2)
    with col1:
        st.image(img_file, caption=label[max_class])
    
    with col2:
        fig, ax = plt.subplots()
        ax.barh(label, prediction.numpy().reshape((4,)))
        st.pyplot(fig)

    percent = round(prediction.numpy().reshape((4,))[max_class] * 100, 2)

    color = "purple"
    if percent >= 80:
        color = "lime"
    elif percent >= 60:
        color = "green"
    elif percent >= 40:
        color = "orange"
    elif percent >= 20:
        color = "red"
    else:
        color = "purple"

    st.markdown(f'### {label[max_class]} การประเมินผล <span style="color:{color}"> {percent}% </span>', unsafe_allow_html=True)


    