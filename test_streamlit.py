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

cam_mode = st.checkbox("")

cam = st.camera_input("Take a picture")
img_file = st.file_uploader("โปรดใส่รูปภาพ", type=["png", "jpg", "jpeg"])
if img_file is not None or cam is not None:
    if cam is not None:
        img_file = cam
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

    # หินดินดาน
    if rock_type == "shale":
        st.markdown("""
        #### ข้อมูล :
        
        * ชื่อ : หินดินดาน (Shale)

        * แหล่งที่มา : โดยทั่วไปแหล่งผลิตหินดินดานส่วนใหญ่จะอยู่ใกล้กับโรงงาน ปูนซีเมนต์

        * แหล่งผลิตหินดินดานแหล่งใหญ่ คือ จังหวัดสระบุรี รองลงมา คือ จังหวัดนครศรีธรรมราช และลำปาง

        * ประโยชน์ : ใช้เป็นวัตถุดิบในอุตสาหกรรมปูนซีเมนต์
        """)
        