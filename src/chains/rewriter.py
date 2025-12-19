from langchain_core.prompts import ChatPromptTemplate
from model import llama

def get_rewriter_chain():

    system_prompt = """
    คุณคือระบบ "แก้ไขคำผิด"
    หน้าที่ของคุณคือแก้ไข Input ให้ถูกต้องตามหลักไวยากรณ์และตัวสะกดเท่านั้น
    
    Rules:
    1. หากพบคำภาษาอังกฤษที่สะกดผิด ให้แก้ตัวสะกดให้ถูกต้อง (English Correction)
    2. "ห้ามแปล" คำศัพท์ภาษาอังกฤษเป็นภาษาไทยเด็ดขาด ให้คงคำศัพท์เดิมไว้ (Keep Original English Terms)
    
    ตัวอย่าง (Examples):
    Input: "applw คือ"
    Output: "Apple คือ"
    
    Input: "ทำงานเสดกี่โมง วันไหยหยุดบ้าง"
    Output: "ทำงานเสร็จกี่โมง วันไหนหยุดบ้าง"
    
    Input: "life balanae คือ"
    Output: "Life balance คือ"
    
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Input: {question}\nOutput:"),
        ]
    )

    chain = prompt | llama

    return chain
