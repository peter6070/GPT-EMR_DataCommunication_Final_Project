import sqlite3
import openai

# 데이터베이스 연결 생성
conn = sqlite3.connect("patient.db")
cursor = conn.cursor()

# 테이블 생성
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        diagnosis TEXT,
        prescription TEXT
    )
"""
)
# OpenAI API key 설정
openai.api_key = "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"

# GPT-3 모델 설정
gpt_model = "text-davinci-003"


# 환자 정보 입력 및 분류 함수
def process_patient_info(patient_info):
    response = openai.Completion.create(
        engine=gpt_model,
        prompt=patient_info,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )
    classification = response.choices[0].text.strip()
    return classification


isLoop = True
while isLoop:
    menu = input("원하는 기능을 입력하세요(추가/조회/요약/종료(0)): ")
    if menu == "추가":
        patient_info = input("환자 정보를 입력하세요 [이름. 나이. 성별. 증상. 처방](콤마 구분): ")

        # 환자 정보 분류
        patient_info = (
            patient_info
            + " '이름, 나이, 성별, 증상, 처방' 순서로 분류하되 내가 입력했던 정보만 출력하고 분류한대로 줄바꿈해줘. 이름쓰고 줄바꿈, 나이쓰고 줄바꿈 이런식으로 하면 되겠지?"
        )

        # 번역
        trans = input("번역하시겠습니까?(y/n): ")
        if trans == "y" or trans == "ㅛ":
            patient_info = patient_info + " 그리고 모든 한글을 영어로 번역하고 줄바꿈해줘"

        # '이름, 나이, 성별, 증상, 처방' 순서로
        classification = process_patient_info(patient_info)
        print("-----------")
        print(classification)

        # 정보 추출
        info_list = classification.split("\n")
        name = info_list[0].strip()
        age = int(info_list[1].strip())
        gender = info_list[2].strip()
        diagnosis = info_list[3].strip()
        prescription = info_list[4].strip()

        # 환자 정보 데이터베이스에 입력
        cursor.execute(
            """
            INSERT INTO patients (name, age, gender, diagnosis, prescription)
            VALUES (?, ?, ?, ?, ?)
        """,
            (name, age, gender, diagnosis, prescription),
        )
        conn.commit()
    elif menu == "조회":
        # 환자 정보 조회 함수
        def get_patient_info():
            cursor.execute("SELECT * FROM patients")
            rows = cursor.fetchall()
            return rows

        # 환자 정보 가져오기
        patients = get_patient_info()

        # 가져온 환자 정보 출력
        for patient in patients:
            print("환자 정보:")
            print("ID:", patient[0])
            print("이름:", patient[1])
            print("나이:", patient[2])
            print("성별:", patient[3])
            print("증상:", patient[4])
            print("처방:", patient[5])
            print()

    elif menu == "요약":
        # 환자 정보 조회 함수
        def get_patient_info():
            cursor.execute("SELECT * FROM patients")
            rows = cursor.fetchall()
            return rows

        # 환자 정보 가져오기
        patients = get_patient_info()
        findName = input("환자의 이름을 입력하세요: ")
        for patient in patients:
            if patient[1] == findName:
                diagSumm = patient[4] + " 이 증상에 대해 한글로 쉽게 설명해줄래?"
                summary = process_patient_info(diagSumm)
                print("-----\n" + summary + "\n-----")

    elif menu == "0" or menu == "종료":
        isLoop = False

# 연결 종료
conn.close()
