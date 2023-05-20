import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras

import json

@st.cache_resource(show_spinner=False)
def load_model():
    return tf.saved_model.load("rock_resnet_model")

@st.cache_resource(show_spinner=False)
def load_rock_data():
    with open("rock_data.json", "r") as jsn_f:
        return json.load(jsn_f)

with st.spinner("กำลังเริ่มต้น"):
    model = load_model()
    rock_data = load_rock_data()

st.title("Rock Classification")

cam_mode = st.checkbox("โหมดกล้อง")

if cam_mode:
    img_file = st.camera_input("ถ่ายรูป")
else:
    img_file = st.file_uploader("โปรดใส่รูปภาพ", type=["png", "jpg", "jpeg"])

if img_file is not None:
    img = keras.utils.load_img(img_file, target_size=(384, 384))
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
        ax.barh(label, prediction.numpy().reshape((9,)))
        st.pyplot(fig)

    percent = round(prediction.numpy().reshape((9,))[max_class] * 100, 2)

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

    st.markdown(f'### ผลลัพธ์ {label[max_class]} ความเป็นไปได้ <span style="color:{color}"> {percent}% </span>', unsafe_allow_html=True)
    
    rock_type = label[max_class]

    # หิน
    if rock_type != "not_rock":
        try:
            st.markdown(f"""
            #### ข้อมูล :

            * ชื่อ : {rock_data[rock_type]["name"]}

            * ประเภท : {rock_data[rock_type]["type"]}

            * แหล่งที่มา : {rock_data[rock_type]["source"]}

            * แหล่งที่พบในประเทศไทย : {rock_data[rock_type]["location"]}

            * ประโยชน์ : {rock_data[rock_type]["usage"]}
            """)
        except KeyError:
            pass