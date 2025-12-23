from langsmith import Client
from dotenv import load_dotenv
load_dotenv()

client = Client()
dataset_name="test-set-1"

dataset = client.create_dataset( dataset_name=dataset_name, description="A sample dataset.")
examples = [
   {
        "inputs": {"question": "CEO ของบริษัทคือใคร"},
        "outputs": {"answer": "นายณัฐพล วิริยะกุล"},
    },
    {
        "inputs": {"question": "บริษัทตั้งอยู่ที่ไหน"},
        "outputs": {"answer": "อาคาร Tech Tower ชั้น 25 ถนนสาทร เขตบางรัก กรุงเทพมหานคร"},
    },

    {
        "inputs": {"question": "ถ้าเข้างาน 10 โมง ต้องเลิกงานกี่โมง"},
        "outputs": {"answer": "ต้องเลิกงาน 19:00 น. (เพื่อนับเวลาทำงานให้ครบ 9 ชั่วโมงรวมพัก ตามนโยบาย Flexible Hours)"},
    },
    {
        "inputs": {"question": "ต้อง check-in เข้างานยังไง"},
        "outputs": {"answer": "ต้อง Check-in ผ่านแอปพลิเคชัน NovaHR เมื่ออยู่ในรัศมี 500 เมตรจากออฟฟิศ หรือเมื่อเริ่มงานจากที่บ้าน"},
    },

    {
        "inputs": {"question": "ทำงานมา 2 ปี ได้วันลาพักร้อนกี่วัน"},
        "outputs": {"answer": "10 วันต่อปี (สำหรับพนักงานอายุงาน 1-3 ปี)"},
    },
    {
        "inputs": {"question": "วันลาพักร้อนสะสมไปปีหน้าได้ไหม"},
        "outputs": {"answer": "ได้ แต่สะสมได้ไม่เกิน 5 วัน"},
    },

    {
        "inputs": {"question": "ตั้งรหัสผ่านต้องยาวกี่ตัวอักษร"},
        "outputs": {"answer": "ความยาวขั้นต่ำ 12 ตัวอักษร"},
    },
    {
        "inputs": {"question": "เอา Flash Drive ส่วนตัวมาใช้ได้ไหม"},
        "outputs": {"answer": "ไม่ได้ (ห้ามเด็ดขาด) หากฝ่าฝืนมีบทลงโทษทางวินัยสูงสุดคือการตักเตือนเป็นลายลักษณ์อักษร"},
    },
    
    {
        "inputs": {"question": "ใส่รองเท้าแตะมาทำงานได้ไหม"},
        "outputs": {"answer": "ไม่ได้ (ในวันจันทร์-พฤหัสบดี ห้ามสวมรองเท้าแตะ ส่วนวันศุกร์ระบุเพียงเสื้อยืดสุภาพ แต่ตามหลัก Business Casual ทั่วไปก็ไม่ควรใส่)"},
    },
    
    # --- คำถามที่ไม่มีคำตอบในเอกสาร ---
    {
        "inputs": {"question": "บริษัทอนุญาตให้เลี้ยงสัตว์ในออฟฟิศไหม"},
        "outputs": {"answer": "ในคู่มือพนักงานไม่ได้ระบุนโยบายเกี่ยวกับสัตว์เลี้ยงไว้"},
    }
]


client.create_examples(dataset_id=dataset.id, examples=examples)