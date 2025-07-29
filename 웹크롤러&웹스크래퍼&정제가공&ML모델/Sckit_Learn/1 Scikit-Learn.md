알고리즘이란?
- 문제를 해결하는 절차나 공식을 말합니다.
- 인공지능에서 말하는 알고리즘은 데이터를 학습하거나 예측하는 수학적 방법입니다.

|분야|알고리즘 예시|
|---|---|
|지도학습|선형 회귀, 로지스틱 회귀, SVM, 결정 트리, 나이브 베이즈|
|비지도학습|K-평균(KMeans), PCA, DBSCAN|
|강화학습|Q-Learning, DQN|
|딥러닝|CNN, RNN, Transformer|

###### 인공지능에서 알로리즘과 모델 프레임워크 / 라이브러리를 구분하여 정리하면 다음과 같습니다.
| 구분               | 정의                        | 예시                                        |
| ---------------- | ------------------------- | ----------------------------------------- |
| 알고리즘 (Algorithm) | 문제 해결을 위한 수학적 방법이나 구조     | Transformer, CNN, RNN, Q-Learning         |
| 모델 (Model)       | 알고리즘을 기반으로 학습된 결과물        | GPT, BERT, LLaMA, YOLO, CLIP              |
| 프레임워크 / 라이브러리    | 알고리즘과 모델을 구현하고 실행하기 위한 도구 | PyTorch, TensorFlow, Hugging Face, OpenCV |

###### 인공지능 주요분야
| 분야                                                                 | 하는 일                   | 쉬운 예시              | 대표 모델              | 핵심 알고리즘           | 사용 도구 / 프레임워크             |
| ------------------------------------------------------------------ | ---------------------- | ------------------ | ------------------ | ----------------- | ------------------------- |
| LLM / NLP                                                          | 텍스트 이해 및 생성            | 번역기, 챗봇, 요약        | GPT, BERT, LLaMA   | Transformer       | Hugging Face, OpenAI      |
| 컴퓨터 비전                                                           . | 이미지/영상 인식              | 얼굴 인식, 자율주행, 사진 분류 | YOLO, ResNet       | CNN               | OpenCV, PyTorch           |
| 음성 AI                                                              | 음성 인식(STT), 음성 생성(TTS) | 음성 자막 생성, 텍스트 읽어주기 | Whisper, Tacotron2 | RNN, Transformer  | Whisper, Mozilla TTS      |
| 멀티모달 AI                                                            | 텍스트 + 이미지 + 음성 복합 처리   | 이미지에 대해 질문하면 설명해줌  | CLIP, BLIP         | Transformer 기반 융합 | Hugging Face, OpenAI CLIP |
###### 인공지능 주요 분야와 대표 기술
| 분야                           | 설명                           | **대표 알고리즘 (구조)**            | **대표 모델 (학습된 결과)**         | **라이브러리 / 프레임워크**                               |
| ---------------------------- | ---------------------------- | --------------------------- | -------------------------- | ----------------------------------------------- |
| LLM / NLP(자연어 처리)            | 텍스트 생성, 번역, 요약, 질의응답 등       | Transformer, Seq2Seq, RNN   | GPT, BERT, LLaMA           | ==**Hugging Face**==, OpenAI API, spaCy         |
| 컴퓨터 비전(이미지/영상)               | 객체 탐지, 이미지 분류, 세분화 등         | CNN, Vision Transformer     | YOLO, ResNet, EfficientNet | ==OpenCV==, PyTorch, Detectron2, ==YOLO==       |
| 음성 AI(STT / TTS)             | 음성 → 텍스트(STT), 텍스트 → 음성(TTS) | CTC, Tacotron2, RNN-T       | Whisper, FastSpeech        | ==Whisper API,== Mozilla TTS, SpeechRecognition |
| 멀티모달                         | 텍스트+이미지+음성 조합                | Transformer + Fusion 구조     | CLIP, BLIP, Flamingo       | ==Hugging Face,== OpenAI CLIP, LAVIS            |
| 강화학습(Reinforcement Learning) | 보상 기반 학습                     | Q-Learning, DQN, PPO        | AlphaGo, OpenAI Five       | Stable-Baselines3, Gymnasium                    |
| 기초 머신러닝                      | 전통적 분류/회귀/클러스터링              | SVM, XGBoost, Decision Tree | (모델마다 데이터에 따라 다름)          | ==Scikit-learn,== XGBoost, LightGBM             |

그중에 Hugging Face는 개발자들이 만든 수많은 모델·라이브러리·데이터셋을 모아놓은 거대한 오픈소스 플랫폼입니다.  
쉽게 말하면 AI 개발자들의 GitHub + 앱스토어 같은 곳이라고 보시면 돼요.

허깅페이스 링크[https://huggingface.co/](https://huggingface.co/)

그래서 개발자는 Hugging Face에 있는 모델이나 라이브러리를 이용해서 웹사이트에 붙이거나 직접 개발할수 있습니다. 

| 이유                  | 설명                                                  |
| ------------------- | --------------------------------------------------- |
| 사전학습 모델 제공          | GPT, BERT, YOLO, Whisper 등 이미 학습된 모델을 바로 사용할 수 있어요. |
| 간단한 코드              | `pip install transformers` 후 3~5줄 코드로 모델 실행 가능.     |
| 웹 데모 도구 제공 (Spaces) | 코딩 없이도 웹앱을 만들 수 있는 **Gradio, Streamlit** 통합         |
| API처럼 호출 가능         | Inference API를 통해 모델을 **REST API로 바로 사용** 가능        |
| 문서와 예제가 풍부          | 초보자용 튜토리얼이 잘 되어 있어 그대로 따라 하기만 해도 OK                 |

허깅페이스의 스트림-릿으로 웹사이트 띄워보기 맛보기
```python
# my_app.py
import streamlit as st
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

st.title("안녕하세요!")
st.write("이건 Streamlit으로 만든 웹앱입니다.")
```

필요한 라이브러리 설치
```bash
pip install streamlit transformers torch
```

터미널에서 다음 명령 실행:
```bash
streamlit run my_app.py
```


Hugging Face의 사전학습 모델 중 하나인 **`skt/kogpt2-base-v2`** 를 기반으로 한 코드

한국어 GPT텍스트 생성기 (KoGPT)
```python
import streamlit as st
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

st.title("📝 한국어 GPT 텍스트 생성기 (KoGPT)")
st.markdown("한국어로 자연스럽게 이어지는 문장을 생성합니다.")

# KoGPT 로딩
@st.cache_resource
def load_model():
    model = GPT2LMHeadModel.from_pretrained("skt/kogpt2-base-v2")
    tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2", bos_token='</s>', eos_token='</s>', unk_token='<unk>', pad_token='<pad>', mask_token='<mask>')
    return model, tokenizer

model, tokenizer = load_model()

# 입력값
text = st.text_area("✍️ 시작 문장을 입력하세요", "나는 오늘 기분이 너무 좋았어")
max_length = st.slider("생성할 길이 (토큰 수)", 20, 100, 50)
temperature = st.slider("창의성 조절 (temperature)", 0.7, 1.5, 1.0)

# 버튼 클릭
if st.button("생성하기"):
    input_ids = tokenizer.encode(text, return_tensors='pt')

    output = model.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        top_p=0.9,
        top_k=50,
        do_sample=True,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id
    )

    result = tokenizer.decode(output[0], skip_special_tokens=True)
    st.markdown("### 🤖 생성된 문장")
    st.success(result)
```

```python
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
```
이 부분이 Hugging Face 라이브러리에서 제공하는 모델 구조 및 토크나이저입니다.  
이 함수들은 Hugging Face Model Hub의 경로를 기반으로 모델을 다음처럼 불러옵니다:
```python
model = GPT2LMHeadModel.from_pretrained("skt/kogpt2-base-v2")
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2")
```
즉, Hugging Face 모델 허브에서 자동으로 다운로드 받아 사용하는 방식입니다.

그러나 우리의 목표는 사전학습된 모델이 아닌 우리가 직접 데이터를 수집하여 직접 학습 또는 파인튜닝을 시키고 결과를 얻어내는 것입니다.

"사전학습(Pretraining)" 과 "파인튜닝(Fine-tuning)"이란?

사전학습 (Pretraining)
- 정의: 모델이 언어의 기본 구조와 규칙을 배우는 첫 번째 학습 단계
- 데이터: 위키백과, 뉴스, 블로그 등 대용량 일반 텍스트
- 목적: 문장 구성, 어휘, 문법 등 언어 자체에 대한 지식 습득
- 예시: GPT, BERT 등은 모두 사전학습된 모델

파인튜닝 (Fine-tuning)
- 정의: 사전학습된 모델을 특정 작업에 맞게 추가 학습시키는 단계
- 데이터: 감정 분석, 뉴스 분류, 챗봇 대화 등 작업별 데이터셋
- 목적: 모델이 특정 문제를 더 잘 해결하도록 조정
- 예시: GPT를 영화 리뷰 감정 분석에 맞게 파인튜닝 → 감정 분석 모델 완성

==간단히 요약하면:==
- ==사전학습 = "세상의 언어를 배우기"==
- ==파인튜닝 = "내가 원하는 일을 잘하도록 맞추기"입니다.==

---
Scikit-Learn이란?
	기계 학습(Machine Learning)을 쉽게 할 수 있도록 도와주는 파이썬 라이브러리입니다. 
쉽게 말해서 데이터를 넣으면:
	➡ 알아서 분석하고  
	➡ 예측도 해주는 똑똑한 도구 모음이에요.
예를 들어:
- "키와 몸무게를 보고 이 사람이 남자인지 여자인지 맞혀볼 수 있을까?"
- "작년 판매 데이터를 보고, 내년 매출을 예측할 수 있을까?"

해결 방법
→ 우리가 이런 문제를 해결할 때 사용하는 게 머신러닝 알고리즘이에요.  
→ 그런데 이걸 직접 코딩하려면 너무 복잡하겠죠?

그래서:
➡ `Scikit-Learn`은 이런 복잡한 알고리즘을 손쉽게 사용할 수 있게 해줘요.  
➡ 마치 "머신러닝 키트"처럼, 필요한 부품(모델, 도구들)을 꺼내 쓰기만 하면 됩니다.

###### Scikit-Learn이 해주는 일:
| 기능                              | 설명                   | 예시               |
| ------------------------------- | -------------------- | ---------------- |
| 분류(Classification)              | 어떤 그룹인지 맞히기          | 이메일이 스팸인지 아닌지    |
| 회귀(Regression)                  | 숫자 예측                | 집값 예측, 온도 예측     |
| 군집화(Clustering)                 | 비슷한 것끼리 묶기           | 고객을 성향별로 나누기     |
| 차원 축소(Dimensionality Reduction) | 복잡한 데이터를 간단하게 만들기    | 이미지에서 중요한 정보만 추출 |
| 모델 선택 / 평가                      | 어떤 모델이 잘 맞는지 비교하고 확인 | 정확도 측정, 교차 검증 등  |

정리하면
- Scikit-Learn은 머신러닝을 위한 파이썬 도구 상자예요.
- 어렵고 복잡한 기계학습 알고리즘을 쉽게 사용하게 해줍니다.
- 데이터 분석, 예측, 분류, 추천 등 다양한 일을 자동으로 할 수 있어요.

설치하기
```bash
pip install --upgrade pip
pip install -U scikit-learn pandas numpy matplotlib
```

실습하기: 우리가 하고 싶은 일 (문제 정의)
Scikit-Learn을 사용해 의사결정트리(Decision Tree) 모델을 학습하고 간단히 예측해보는 데모 코드를 작성합니다.

아이리스(Iris) 데이터를 불러와서 꽃잎의 길이, 너비 같은 데이터를 보고  
이 꽃이 어떤 품종(종류)인지 자동으로 맞히고 싶어요.
"이 꽃은 `setosa`인가요, `versicolor`인가요, `virginica`인가요?"

즉, 우리는:
- 입력값: 꽃잎 길이, 꽃받침 너비 등 수치 데이터
- 정답(타깃값): 꽃의 품종 이름을 가지고, 입력을 보고 정답을 맞히는 모델을 만들고 싶은 겁니다.

라이브러리 불러오기:
```python
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
```
라이브러리 임포트
- `pandas`: 데이터를 표 형태로 다루기 위함
- `load_iris`: Scikit-Learn에서 제공하는 붓꽃 분류용 샘플 데이터셋
- `DecisionTreeClassifier`: 분류용 결정 트리 모델
---
```python
# 데이터 로드
iris = load_iris() # 사이킷런에 내장된 Iris(붓꽃) 데이터셋을 불러옵니다
print(iris.keys()) # 데이터 확인하기
```
출력결과:
```
dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])
```
###### 데이터 로드 및 확인
| 키               | 설명                                 |
| --------------- | ---------------------------------- |
| `data`          | 입력 데이터 (특성)꽃잎 길이, 꽃받침 너비 등 수치형 데이터 |
| `target`        | 정답(레이블) 데이터꽃의 품종 번호 (0, 1, 2)      |
| `frame`         | `pandas.DataFrame` 형식의 전체 데이터      |
| `target_names`  | 클래스 이름 목록0, 1, 2가 어떤 품종인지 이름 제공    |
| `DESCR`         | 데이터셋 설명서 (텍스트)                     |
| `feature_names` | 각 특성(열)의 이름 리스트                    |
| `filename`      | 로컬에 저장된 데이터 파일의 경로                 |
| `data_module`   | 이 데이터셋을 관리하는 내부 모듈                 |

아이리스꽃 데이터셋을 표 형태로 만들고, 그 표에 꽃의 품종(class) 정보를 추가한 다음, 전체 데이터를 출력한 코드:
```python
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['class'] = iris.target
print(df)
```

🔹 `iris.data`
- 꽃의 측정값 (꽃잎/꽃받침의 길이, 너비 등)
- 2차원 배열: 150개 샘플 × 4개 특성 ( 꽃잎 꽃받침의 크기에 따라 다른 품종)
- 예: `[[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], ...]`
    
🔹 `iris.feature_names`
- 각 열의 이름
- 예: `['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']`
    
🔹 `pd.DataFrame(...)`
- 위의 데이터와 열 이름을 활용해 표(`DataFrame`)를 생성함
- 열 이름을 붙인 이유: 보기 좋게 만들기 위해
    
🔹 `df['class'] = iris.target`
- 각 행의 정답(꽃의 품종)을 `class`라는 새 열에 추가
- `iris.target`은 `[0, 0, 0, 1, 1, 2, 2, ...]` 식으로 구성됨
    
🔹 `print(df)`
- 최종적으로 만든 표(입력 데이터 + 품종)를 화면에 출력

데이터 확인:
![[Pasted image 20250727162606.png]]
`sepal length (cm)`	꽃받침 길이
`sepal width (cm)`	꽃받침 너비
`petal length (cm)`	꽃잎 길이
`petal width (cm)`	꽃잎 너비
`class`	품종 (0, 1, 2)으로 구분된 정답 레이블

---
```python
# 모델 생성 및 훈련
model = DecisionTreeClassifier() 
# 의사결정나무 알고리즘 선택해서 빈 모델 객체를 만드는것(학습전)

model.fit(iris.data, iris.target) # .fit()은 모델을 학습시키는 함수
# - iris.data: 입력값 (꽃잎/꽃받침의 길이, 너비 등)
# - iris.target: 정답값 (0=setosa, 1=versicolor, 2=virginica)
```
모델 생성 및 학습
- `DecisionTreeClassifier()`: 결정 트리 분류기 생성
- `fit(...)`: 학습 데이터로 모델 학습

`DecisionTreeClassifier`란?
- 의사결정나무(Decision Tree) 알고리즘을 이용해 데이터를 분류(Classification) 하는 모델입니다.
- 질문을 따라가며 "이건 뭐지?"를 결정하는 나무 구조처럼 동작합니다.

각 파라미터 설명:
![[Pasted image 20250727162751.png]]

| 파라미터 이름                    | 기본값      | 뜻                | 쉽게 설명                                          |
| -------------------------- | -------- | ---------------- | ---------------------------------------------- |
| `criterion`                | `'gini'` | 불순도 계산 방법        | `'gini'` 또는 `'entropy'`. 나무에서 어떤 분할이 좋은지 판단 기준 |
| `splitter`                 | `'best'` | 노드 분할 방식         | `'best'`: 가장 좋은 기준으로 분할. `'random'`: 무작위 선택    |
| `max_depth`                | `None`   | 최대 깊이 제한         | 나무가 너무 깊어지는 것을 막음 (과적합 방지)                     |
| `min_samples_split`        | `2`      | 분할에 필요한 최소 샘플 수  | 이보다 작으면 더 이상 분할하지 않음                           |
| `min_samples_leaf`         | `1`      | 리프 노드 최소 샘플 수    | 끝 노드에 최소 몇 개의 데이터가 있어야 하는지                     |
| `min_weight_fraction_leaf` | `0.0`    | 리프 노드 최소 가중치 비율  | 샘플 가중치 기준 (잘 안 씀)                              |
| `max_features`             | `None`   | 분할할 때 고려할 특성 수   | `'sqrt'`, `'log2'` 등 지정 가능. 랜덤성과 성능 제어         |
| `random_state`             | `None`   | 랜덤 시드 설정         | 결과를 재현 가능하게 하기 위한 숫자                           |
| `max_leaf_nodes`           | `None`   | 리프 노드 최대 개수 제한   | 나무 크기 제한 (복잡도 조절)                              |
| `min_impurity_decrease`    | `0.0`    | 불순도 감소 최소값       | 이 값보다 작으면 분할 안 함                               |
| `class_weight`             | `None`   | 클래스 가중치 조정       | 불균형 데이터에서 소수 클래스 가중치를 높여줌                      |
| `ccp_alpha`                | `0.0`    | 비용-복잡도 가지치기 파라미터 | 복잡한 나무를 잘라 단순하게 만듦 (가지치기)                      |
| `monotonic_cst`            | `None`   | 단조 제약 조건         | 특정 특성이 오를수록 결과도 오르도록 강제 (고급 옵션)                |

---
모델이 잘 학습되었는지 확인하기 위해 데이터의 앞 5개 샘플에 대해 예측값과 실제 정답을 비교하는 코드:
```python
# 예측 테스트
print("예측:", model.predict(iris.data[:5]))
print("실제:", iris.target[:5])
```
- `iris.data[:5]` → 입력 데이터 앞에서 5개만 슬라이싱  
    예: 꽃잎/꽃받침 길이, 너비가 들어 있는 5개 행
- `model.predict(...)` → 학습된 모델에 이 데이터를 넣어서  
    "이건 무슨 품종일까?" 예측
- 예측 결과는 `[0 0 0 0 0]` 이런 식의 배열로 나와요  
    (0: setosa, 1: versicolor, 2: virginica)

결과: 이 출력 결과는 Scikit-Learn의 Decision Tree 모델이 붓꽃(iris) 데이터를 기반으로 학습한 뒤, 첫 5개 샘플을 예측한 결과입니다.
```python
[150 rows x 5 columns] # 총 150개의 샘플 (행)
예측: [0 0 0 0 0]
실제: [0 0 0 0 0]
```
- `predict()`는 학습한 모델이 품종을 어떻게 맞히는지 보여주는 메서드예요.
- 이 코드에서는 학습한 모델에게 입력값 5개를 주고,  
    → 예측값과 실제값이 일치하는지 비교하고 있어요

---
손글씨 숫자 이미지(Digits) 예측
	숫자 손글씨 이미지를 보고, 그 숫자가 몇인지 예측하는 모델을 만들어보겠습니다!

라이브러리 불러오기
```python
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np
```
머신러닝, 데이터 분할, 평가, 시각화를 위한 필수 라이브러리 불러오기

---
데이터 불러오기 및 구성 확인
```python
# 1. 손글씨 숫자 데이터 불러오기
digits = load_digits()
print(digits.keys())
```
손글씨 숫자 데이터셋 로딩 후, 어떤 항목들이 들어있는지 확인 (`data`, `target`, `images`, `DESCR` 등)

```
dict_keys(['data', 'target', 'frame', 'feature_names', 'target_names', 'images', 'DESCR'])
```

| 키 이름            | 설명                                     | 예시                                                |
| --------------- | -------------------------------------- | ------------------------------------------------- |
| `data`          | 입력값: 각 이미지의 픽셀(64개)을 1차원 벡터로 만든 것      | `digits.data[0] → [0.0, 0.0, ..., 5.0, ..., 0.0]` |
| `target`        | 정답값: 해당 숫자(0~9)                        | `digits.target[0] → 0`                            |
| `frame`         | `pandas.DataFrame` 형식 데이터 (대부분 `None`) | 생략 가능                                             |
| `feature_names` | 특성 이름 (보통 없음 또는 0~63 번호)               | `[pixel_0, pixel_1, ...]`                         |
| `target_names`  | 분류 가능한 숫자 리스트                          | `[0, 1, ..., 9]`                                  |
| `images`        | 원본 이미지 데이터 (8x8 배열)                    | `digits.images[0] → 2차원 이미지 배열`                   |
| `DESCR`         | 데이터 설명서 (긴 문자열)                        | `print(digits.DESCR)`                             |

---
입력(X)과 정답(y) 분리
```python
# 2. 입력(X)과 정답(y) 나누기
X = digits.data         # 각 숫자 이미지 (8x8 → 64개 픽셀 값)
y = digits.target       # 해당 숫자 (0~9)

# 이줄이 없으면 모든행이 생략되서 출력됩니다.
np.set_printoptions(threshold=np.inf)

print("X:", X)
print()
print("y:", y)
```
X가 대문자인 이유:
- 수학에서 대문자 X는 행렬(Matrix) 을 나타냅니다.
- 입력값은 여러 개의 특성(feature)을 가지는 2차원 배열이므로 `X`라고 씁니다

y가 소문자인 이유:
- 수학에서 벡터(1차원) 를 나타낼 때 소문자 `y`를 자주 사용합니다.
- 정답값은 보통 하나의 컬럼이니까 1차원 벡터로 표현되며, 그래서 `y`를 씁니다.

`X`는 대문자고 `y`는 소문자인 이유는 수학적 관례와 머신러닝 커뮤니티의 암묵적인 약속입니다. 정해진 법칙은 아니지만, 의미가 있는 표현 방식 입니다.

결과: `np.set_printoptions(threshold=np.inf)` 없이 출력
```
X: [[ 0.  0.  5. ...  0.  0.  0.]
 [ 0.  0.  0. ... 10.  0.  0.]
 [ 0.  0.  0. ... 16.  9.  0.]
 ...
 [ 0.  0.  1. ...  6.  0.  0.]
 [ 0.  0.  2. ... 12.  0.  0.]
 [ 0.  0. 10. ... 12.  1.  0.]]

y:[0 1 2 ... 8 9 8]
```
`X	입력값들 (숫자 이미지의 픽셀 값)`	
- X.shape = (1797, 64) → 1797개의 숫자 이미지
`y	정답값들 (이미지가 나타내는 실제 숫자)`	
- y.shape = (1797,) → 각 이미지의 숫자 라벨
이 데이터는 아직 학습 된게 아니며 그냥 데이터 뭉치 입니다.
학습을 위해 직접 `.fit()`으로 모델에 넣어줘야 합니다.

0.0은 완전 흰색 (밝음 비어있음)  0. == 0.0
8.0은 회색(중간 글자 일부) 8. == 8.0
16.0은 검정색(가장어두운색 글자선이 진함) 16. == 16.0

`np.set_printoptions(threshold=np.inf)` 있게 출력된 결과:
```python
X: [[ 0.  0.  5. 13.  9.  1.  0.  0.  0.  0. 13. 15. 10. 15.  5.  0.  0.  3.
  15.  2.  0. 11.  8.  0.  0.  4. 12.  0.  0.  8.  8.  0.  0.  5.  8.  0.
   16.  9.  8.  0.  0.  4. 11.  0.  1. 12.  7.  0.  0.  2. 14.  5. 10. 12.
   17.  0.  0.  0.  6. 13. 10.  0.  0.  0.]
 [ 0.  0.  0. 12. 13.  5.  0.  0.  0.  0.  0. 11. 16.  9.  0.  0.  0.  0.
   18. 15. 16.  6.  0.  0.  0.  7. 15. 16. 16.  2.  0.  0.  0.  0.  1. 16.
  19.  3.  0.  0.  0.  0.  1. 16. 16.  6.  0.  0.  0.  0.  1. 16. 16.  6.
   20.  0.  0.  0.  0. 11. 16. 10.  0.  0.]
 [ 0.  0.  0.  4. 15. 12.  0.  0.  0.  0.  3. 16. 15. 14.  0.  0.  0.  0.
   21. 13.  8. 16.  0.  0.  0.  0.  1.  6. 15. 11.  0.  0.  0.  1.  8. 13.
  22.  1.  0.  0.  0.  9. 16. 16.  5.  0.  0.  0.  0.  3. 13. 16. 16. 11.
   23.  0.  0.  0.  0.  3. 11. 16.  9.  0.]
       .......]]
       
y: [0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 9 5 5 6 5 0
 9 8 9 8 4 1 7 7 3 5 1 0 0 2 2 7 8 2 0 1 2 6 3 3 7 3 3 4 6 6 6 4 9 1 5 0 9
 5 2 8 2 0 0 1 7 6 3 2 1 7 4 6 3 1 3 9 1 7 6 8 4 3 1 4 0 5 3 6 9 6 1 7 5 4
 4 7 2 8 2 2 5 7 9 5 4 8 8 4 9 0 8 9 8 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7
 8 9 0 1 2 3 4 5 6 7 8 9 0 9 5 5 6 5 0 9 8 9 8 4 1 7 7 3 5 1 0 0 2 2 7 8 2
 0 1 2 6 3 3 7 3 3 4 6 6 6 4 9 1 5 0 9 5 2 8 2 0 0 1 7 6 3 2 1 7 3 1 3 9 1
 7 6 8 4 3 1 4 0 5 3 6 9 6 1 7 5 4 4 7 2 8 2 2 5 5 4 8 8 4 9 0 8 9 8 0 1 2  ......]     
```

---
시각적으로 데이터를 확인해보고 싶다면:
```python
import matplotlib.pyplot as plt

plt.matshow(digits.images[0], cmap='gray') # 첫 번째 숫자 이미지 출력
plt.title(f"Label: {digits.target[0]}")
plt.show()
```

숫자 '0' 그림이 회색 픽셀로 출력
![[Pasted image 20250727175559.png]]

---
전체 데이터를 학습용(train) 과 시험용(test) 으로 나누기 
데이터셋 분할 (train/test split)을 수행하는 코드:
```python
# 3. 학습용/테스트용 데이터 나누기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
- 전체 데이터 중 80%는 학습용, 20%는 테스트용으로 나누기
- `random_state=42`는 결과를 고정하기 위해 사용

| 파라미터              | 의미                           |
| ----------------- | ---------------------------- |
| `test_size=0.2`   | 전체 데이터 중 20%를 시험용(test)으로 사용 |
| `random_state=42` | 데이터 섞을 때 사용하는 시드값 (결과 고정)    |
시드값(seed)이란?
	무작위(random) 작업을 "항상 같은 결과"로 만들기 위한 숫자 값이에요.

왜 시드값이 필요한가요?
`train_test_split()`은 데이터를 "랜덤으로 섞어서" 나눕니다.
- 그래서 매번 실행할 때마다 다른 데이터 조합이 생길 수 있어요.
- 즉, 학습용/시험용 데이터가 계속 바뀝니다 → 예측 결과도 바뀜

그런데 우리가 실험/디버깅/비교할 때는?
- 항상 같은 데이터 조합으로 실험해야 결과 비교가 됩니다.
- 그래서 무작위성을 "고정"하기 위해 `random_state=숫자`를 줍니다.

비유로 이해해볼게요. 예를 들어 시험지를 섞는다고 해볼게요.
- 그냥 `random.shuffle()`로 섞으면 → 매번 다른 시험지 나옴
- `random.seed(42)`를 주고 섞으면 → 항상 같은 순서로 섞임
	→ 이게 `random_state=42`의 의미와 같아요.

`random.seed(정수인 아무 숫자나 줘도 됩니다.)`
42는 전통적으로 프로그래밍에서 유래된 숫자로 개발자들 사이에 매우 유명한 문화적 밈이자 문학적인 유머입니다. 궁금하면 왜 42를 쓰는지 검색해 보세요.

---
모델 만들고 학습시키기
```python
# 4. 모델 만들고 학습하기
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
```
- 결정 트리 모델 생성 후, 학습 데이터를 이용해 모델 훈련(fit)

---
테스트 데이터로 예측하고 정확도 평가
```python
# 5. 예측하고 정확도 평가
y_pred = model.predict(X_test)
print("정확도:", accuracy_score(y_test, y_pred))
```
- 학습된 모델로 테스트 데이터 예측  
- 예측 결과와 실제 정답을 비교해 정확도(accuracy) 계산
- `model.predict(X_test)`는 머신러닝에서 모델이 테스트 데이터를 입력받아 예측 결과를 출력하는 핵심 메소드

`model`	
	학습된 머신러닝 모델 (예: DecisionTreeClassifier, RandomForestClassifier, 등)
`.predict()`	
	입력 데이터를 기반으로 클래스(또는 숫자)를 예측하는 함수
`X_test`	
	예측에 사용할 데이터 (입력 값들)
`y_pred`	
	예측 결과 (예: 클래스 번호, 회귀 값 등)

---
이미지 1장 예측 시각화
```python
# 6. 이미지 1개 예측해보기
plt.gray()
plt.matshow(digits.images[0])  # 첫 번째 이미지 출력
plt.show()
```
- 모델이 예측할 숫자 이미지 1장을 회색조로 출력해서 확인

---
예측 결과 확인
```python
print("실제:", digits.target[0])
print("예측:", model.predict([digits.data[0]]))
```
- 0번째 이미지의 정답(label)과 모델의 예측값을 나란히 출력  
- 잘 맞추면 모델이 해당 숫자를 정확히 예측한 것!