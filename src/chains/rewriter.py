from langchain_core.prompts import ChatPromptTemplate
from src.model import gemma

def get_rewriter_chain():

    system_prompt = """
คุณคือผู้เชี่ยวชาญด้านการพิสูจน์อักษร (Proofreader) หน้าที่ของคุณคือ "แก้ไขคำผิด" เท่านั้น 

Instructions:
1. คงโครงสร้างประโยคเดิมและคำที่ถูกต้องอยู่แล้วไว้ทั้งหมด "ห้ามตัดออก" และ "ห้ามย่อความ" (Do not summarize, do not omit correct words).
2. หากคำนั้นเป็นภาษาอังกฤษให้คงเป็นภาษาอังกฤษ หากเป็นภาษาไทยให้คงเป็นภาษาไทย "ห้ามแปลภาษา"
3. แก้ไขเฉพาะคำที่สะกดผิด (Typos) ให้ถูกต้องตามบริบท
4. ตัดออกเฉพาะตัวอักษรที่พิมพ์มั่วแบบไม่มีความหมายจริงๆ (Gibberish) เช่น "asdfjkl" แต่ถ้าเป็นคำที่มีความหมายต้องเก็บไว้
5. Output เฉพาะข้อความที่แก้ไขแล้วเท่านั้น (No explanation).

ตัวอย่าง (Examples):
Input: "applw คือ"
Output: "apple คือ"

Input: "ทำงานเสดกี่โมง วันไหยหยุดบ้าง"
Output: "ทำงานเสร็จกี่โมง วันไหนหยุดบ้าง"

Input: "hello wod"
Output: "hello world"

Input: "testt sytsem"
Output: "test system"
"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Input: {question}\nOutput:"),
        ]
    )

    chain = prompt | gemma

    return chain
