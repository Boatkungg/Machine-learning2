// More API functions here:
// https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/image

// the link to your model provided by Teachable Machine export panel
const URL = 'https://teachablemachine.withgoogle.com/models/WZxSXu8P9/';

let model, labelContainer, maxPredictions;

// Load the image model 
async function init() {
    const modelURL = URL + 'model.json';
    const metadataURL = URL + 'metadata.json';

    // load the model and metadata
    model = await tmImage.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();

    labelContainer = document.getElementById('label-container');
    for (let i = 0; i < maxPredictions; i++) {
        // and class labels
        labelContainer.appendChild(document.createElement('div'));
    }
}

// Drop File


// หน้าโหลด
let title = document.getElementById('title')
let openload = document.querySelector(".openload")
const input = document.getElementById("imageUpload")
let screenOutput = document.getElementById("screen")

function Eventload() {
    openload.style.display = "block"
    screenOutput.style.display = "none"
    title.innerHTML = "กำลังประมวลผล"

    setTimeout(() => {
        openload.style.display = 'none'
        screenOutput.style.display = "block"
        title.innerHTML = "Machine Learning"
    }, 8000)
}

input.addEventListener("input", Eventload)

// Output
async function predict() {
    // predict can take in an image, video or canvas html element
    var image = document.getElementById('imagePreview');
    const prediction = await model.predict(image, false);
    let percent = document.getElementById("percent")

    for (let i = 0; i < maxPredictions; i++) {
        // หินแต่ละชนิด
        const shale = prediction[0].probability.toFixed(2); // หินดินดาน
        const sandstone = prediction[1].probability.toFixed(2); // หินทราย
        const marble = prediction[2].probability.toFixed(2); // หินอ่อน
        const none = prediction[3].probability.toFixed(2); // ไม่ใช่หิน

        let max = Math.max(shale, sandstone, marble, none)
        let rockpercent = max * 100

        // แสดงสีตาม เปอร์เซนต์
        if (rockpercent > 80 && rockpercent <= 100) {
            percent.style.color = "green"
        }

        else if (rockpercent <= 80 && rockpercent > 60) {
            percent.style.color = "#3eb13e"
        }
        else if (rockpercent <= 60 && rockpercent > 40) {
            percent.style.color = "orange"
        }
        else if (rockpercent <= 40 && rockpercent > 20) {
            percent.style.color = "red"
        }
        else if (rockpercent <= 20 && rockpercent > 0) {
            percent.style.color = "#bc0011"
        }

        // หินดินดาน
        if (max == shale) {
            var classPrediction = "ชื่อ : หินดินดาน<br><br>" + "แหล่งที่มา : โดยทั่วไปแหล่งผลิตหินดินดานส่วนใหญ่จะอยู่ใกล้กับโรงงาน ปูนซีเมนต์ แหล่งผลิตหินดินดานแหล่งใหญ่ คือ จังหวัดสระบุรี รองลงมา คือ จังหวัดนครศรีธรรมราช และลำปาง<br><br>" + "ประโยชน์ : ใช้เป็นวัตถุดิบในอุตสาหกรรมปูนซีเมนต์"
            // ความถูกต้อง
            percent.innerHTML = "ความแม่นยำ : " + shale * 100 + "%"
        }
        // หินทราย
        else if (max == sandstone) {
            var classPrediction = "ชื่อ : หินทราย<br><br>" + "แหล่งที่มา : เกิดจากการสะสมตัวของเศษหินดินทราย ที่แตกหลุด และการพังทลายของหินอื่นหรือถูกละลายชะ ล้างมาจากดินหรือหินอื่นๆ แล้วถูกกระแสน้ำหรือกระแสลมทับถมอยู่เป็นชั้นๆ<br><br>" + "ประโยชน์ : ตกแต่งบ้านและสวน"
            // ความถูกต้อง
            percent.innerHTML = "ความแม่นยำ : " + sandstone * 100 + "%"
        }
        // หินอ่อน
        else if (max == marble) {
            var classPrediction = "ชื่อ : หินอ่อน<br><br>" + "แหล่งที่มา : เริ่มต้นมาจากหินปูนหรือแคลเซียมคาร์บอเน็ต ที่มีผลึกแร่คัลไซต์เป็นส่วนประกอบหลัก เกิดการทับถมกันเป็นชั้น ประกอบกับความร้อนและแรงดันที่เกิดจากแมกมาของภูเขาไฟใต้ทะเล และปัจจัยสภาพแวดล้อมทางธรณีวิทยาอันหลากหลาย จนเกิดการประสานกันของผลึกภายในตัวหิน ทำให้หินมีลวดลายที่สวยงาม ประกอบด้วยเส้นสีสันต่างๆ อันเป็นเอกลักษณ์เฉพาะตัว<br><br>" + "ประโยชน์ : ใช้เป็นวัสดุก่อสร้างและหินประดับ เช่น ปูพื้นอาคาร, ปูผนัง, ทำขั้นบันได, โต๊ะ, และรูปสลักต่างๆ"
            // ความถูกต้อง
            percent.innerHTML = "ความแม่นยำ : " + marble * 100 + "%"
        }
        // ไม่ใช่หิน
        else if (max == none) {
            var classPrediction = "ภาพนี้ไม่ใช่หิน<br>โปรดใส่รูปภาพที่มีหิน"
            // ไม่แสดงความถูก
            percent.innerHTML = ""
        }

        labelContainer.childNodes[1].innerHTML = classPrediction;
    }
}