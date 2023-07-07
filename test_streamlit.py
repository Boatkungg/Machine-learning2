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
        fig.set_facecolor('#212946')
        ax.set_facecolor("#212946")
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
        for items in store_data[rock_type]:
            store_list = list(store_data[rock_type][items].keys())

            if "shop" in store_list:
                show_type = "shop"
            elif "map" in store_list:
                show_type = "map"
            else:
                show_type = None

            if show_type is not None:
                store_list.remove(show_type)
    
            link_and_price = [(store_data[rock_type][items][store]["link"], store_data[rock_type][items][store]["price"]) for store in store_list]
            link_and_price = sorted(link_and_price, key=lambda x: x[1])

            lowest_price = link_and_price[0][1]
            lowest_price_link = link_and_price[0][0]

            highest_price = link_and_price[-1][1]
            highest_price_link = link_and_price[-1][0]
            
            average_price = round(sum([i[1] for i in link_and_price]) / len(link_and_price), 2)
            
            with st.expander("ตัวอย่างการนำมาผลิตและส่งออกขาย"):
                col3, col4 = st.columns(2)
                with col4:
                    if show_type == "shop":
                        st.markdown(f"""
                                    * {store_data[rock_type][items]["shop"][0]}
                                    * {store_data[rock_type][items]["shop"][1]}
                                    * {store_data[rock_type][items]["shop"][2]}
                                    """)
                    elif show_type == "map":
                        st.markdown(f"""
                        <iframe src="{store_data[rock_type][items]["map"]}"></iframe>
                        """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    #### {items}
                    <a style="color: #23B613" href="{highest_price_link}"> ราคาสูงสุด : {highest_price} บาท </a>

                    <a style="color: #ff0000" href="{lowest_price_link}"> ราคาต่ำสุด : {lowest_price} บาท </a>

                    <span style="color: #008eff"> ราคาเฉลี่ย : {average_price} บาท </span>
                    """, unsafe_allow_html=True)
            
