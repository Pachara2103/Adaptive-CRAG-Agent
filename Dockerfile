FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
#  same COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Docker Cache ของไม่ค่อยเปลี่ยนอยู่บนๆ
COPY ./src ./src

COPY . .

# รัน Server
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# 1. CMD [...] เปิดกล่อง (Container) นี้ขึ้นมา ให้รันคำสั่งนี้เป็นอย่างแรกเลยนะ"
# 2. --server.address=0.0.0.0"
# ตัวสำคัญที่สุด: เหมือนเดิมครับ ต้องตั้งเป็น 0.0.0.0 เพื่อให้คนจากข้างนอก (Browser ในคอมเรา) เจาะเข้าไปดูหน้าเว็บใน Docker ได้ ถ้าไม่ใส่ บรรทัดนี้คุณจะเปิดเว็บไม่ขึ้นครับ





