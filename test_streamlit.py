import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
import pandas as pd

import json

@st.cache_resource(show_spinner=False)
def load_model():
    return tf.saved_model.load("rock_resnet_model")

@st.cache_data(show_spinner=False)
def load_rock_data():
    with open("rock_data.json", "r") as jsn_f:
        return json.load(jsn_f)

@st.cache_data(show_spinner=False)
def load_store_data():
    with open("store.json", "r") as jsn_f:
        return json.load(jsn_f)

with st.spinner("กำลังเริ่มต้น"):
    model = load_model()
    rock_data = load_rock_data()
    store_data = load_store_data()

st.title("Rock Classification")

cam_mode = st.checkbox("โหมดกล้อง")

if cam_mode:
    img_file = st.camera_input("ถ่ายรูป")
else:
    img_file = st.file_uploader("โปรดใส่รูปภาพ", type=["png", "jpg", "jpeg"])

if img_file is not None:
    img = keras.utils.load_img(img_file, target_size=(384, 384), interpolation="hamming", keep_aspect_ratio=True)
    input_array = keras.utils.img_to_array(img)

    with st.spinner("กำลังประมวณผล"):   
        # some black magic here
        prediction_list = []
        prediction_raw = []
        for _ in range(1):
            prediction, label = model(input_array)
            prediction_list.append(prediction.numpy().argmax())
            prediction_raw.append(prediction.numpy().reshape((9,)))

        max_class = max(prediction_list, key = prediction_list.count)
        prediction = prediction_raw[prediction_list.index(max_class)]

    label = [i.numpy().decode("utf-8") for i in label]

    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption=label[max_class])
    
    with col2:
        for param in ['text.color', 'axes.labelcolor', 'ytick.color', 'xtick.color']:
                plt.rcParams[param] = '0.9'
        fig, ax = plt.subplots()
        ax.set_facecolor('#212946')
        ax.barh(label, prediction)
        ax.grid(color='#2A3459')
        st.pyplot(fig)

    percent = round(prediction[max_class] * 100, 2)

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

    rock_type = label[max_class]

    st.markdown(f'### ผลลัพธ์ {rock_type} ความเป็นไปได้ <span style="color:{color}"> {percent}% </span>', unsafe_allow_html=True)

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

    else:
        st.markdown(f"""
        #### ภาพนี้ไม่ใช่หิน โปรดใส่รูปภาพที่มีหิน
        """)

    if rock_type not in  ["not_rock", "shale", "limestone", "basalt"]:
        st.markdown(f"#### การนำมาผลิตและส่งออกขาย : ")

        for items in store_data[rock_type].keys():
            item = store_data[rock_type][items]

            item_list = []
            for store_no in item.keys():
                for time_price in item[store_no]:
                    item_list.append((time_price["time"], time_price["price"]))

            item_list.sort(key=lambda x: "-".join(list(reversed(x[0].split("-")))))

            # remove the duplicate 
            # TODO: keep the lowest price
            plt.style.use("seaborn-dark") # สไตล์กราฟ
            # สีขอบกราฟ
            for param in ['text.color', 'axes.labelcolor', 'ytick.color']:
                plt.rcParams[param] = '0.9'
            # สีพแกน x
            for param in ['xtick.color', 'legend.facecolor', 'legend.edgecolor']:
                plt.rcParams[param] = '#212946'
            item_list = list(dict.fromkeys(item_list))
            fig_2, ax_2 = plt.subplots()
            prices = [i[1] for i in item_list] # ราคา
            ax_2.plot(prices, marker="o", color="#08F7FE") # ตัวกราฟ
            fig_2.set_facecolor('#212946') # พื้นหลังนอกกราฟ
            ax_2.set_facecolor('#212946') # พื้นหลังในกราฟ
            ax_2.grid(color='#2A3459') # พื้นหลังตาราง

            with st.expander("ตัวอย่างการนำมาผลิตและส่งออกขาย"):
                col3, col4 = st.columns(2)
                with col4:
                    st.pyplot(fig_2)

                with col3:
                    st.markdown(f"""
                    #### {items}
                    <span style="color: #FA3C3C"> ราคาต่ำสุด : {min([i[1] for i in item_list])} บาท </span>

                    <span style="color: #23B613"> ราคาสูงสุด : {max([i[1] for i in item_list])} บาท </span>

                    ราคาปัจจุบัน : {item_list[-1][1]} บาท

                    <span style="color: #00D5FF"> ราคาเฉลี่ย : {round(sum([i[1] for i in item_list]) / len(item_list), 2)} บาท </span>
                    """, unsafe_allow_html=True)
            
