import json

# 중첩된 딕셔너리를 평평하게(1단계 구조로) 만드는 함수
def flatten(data, parent_key='', sep='.'):
    # 결과를 담을 빈 리스트를 만든다
    result_list = []

    # 주어진 딕셔너리 안의 모든 키와 값을 하나씩 꺼낸다
    for key, value in data.items():

        # 새로운 키를 만든다: 상위 키가 있으면 "상위.현재" 형태로 붙이고, 
        # 없으면 그냥 현재 키
        if parent_key == '':
            new_key = key
        else:
            new_key = parent_key + sep + key

        # 만약 값이 또 다른 딕셔너리라면
        if isinstance(value, dict):
            # 그 안의 키-값들도 평탄화하기 위해 다시 이 함수를 호출한다 (재귀)
            inner_flattened = flatten(value, new_key, sep)
            # 결과 리스트에 합쳐준다
            result_list.extend(inner_flattened.items())
        else:
            # 값이 딕셔너리가 아니면, 지금 만든 키와 값을 리스트에 추가한다
            result_list.append((new_key, value))

    # 리스트를 딕셔너리로 바꿔서 반환한다
    return dict(result_list)

# 예시로 사용할 중첩된 데이터
nested_data = {
    "user": {
        "name": "Alice",
        "age": 30
    },
    "location": {
        "city": "Seoul",
        "country": "Korea"
    }
}

# 위 데이터를 평탄화한다
flattened_data = flatten(nested_data)

# 결과를 JSON 파일로 저장하기
with open("data/flatten.json", "w", encoding="utf-8") as file:
    # ensure_ascii=False → 한글이 깨지지 않게 저장
    # indent=2 → 보기 좋게 들여쓰기해서 저장
    json.dump(flattened_data, file, ensure_ascii=False, indent=2)

# 완료 메시지 출력
print("데이터가 'flattened.json'에 저장되었습니다.")
