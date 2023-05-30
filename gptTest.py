import openai

# OpenAI API key 설정
openai.api_key = "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"

# GPT-3 모델 설정
gpt_model = "text-davinci-003"


# 환자 정보 입력 및 분류 함수
def process_patient_info(patient_info):
    response = openai.Completion.create(
        engine=gpt_model,
        prompt=patient_info,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    classification = response.choices[0].text.strip()
    return classification


diagnosis = ""
isLoop = True
while isLoop:
    menu = input("원하는 기능을 입력하세요(추가/조회/0=종료): ")
    if menu == "추가":
        patient_info = input("환자 정보를 입력하세요 [이름. 나이. 성별. 증상. 처방](콤마 구분): ")

        # 환자 정보 분류
        patient_info = (
            patient_info
            + " '이름, 나이, 성별, 증상, 처방' 순서로 분류하되 내가 입력했던 정보만 출력하고 분류한대로 줄바꿈해줘. 이름쓰고 줄바꿈, 나이쓰고 줄바꿈 이런식으로 하면 되겠지?"
        )
        # 번역
        trans = input("번역하시겠습니까?(y/n): ")
        if trans == "y":
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
    if menu == "요약":
        diagnosis = diagnosis + " 해당 증상에 대해 한글로 쉽게 설명해줄래?"
        summary = process_patient_info(diagnosis)
        print(summary)

    elif menu == "0":
        isLoop = False
