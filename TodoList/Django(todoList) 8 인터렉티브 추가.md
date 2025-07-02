수정한 파일명
- list.html 
- create.html -> completed_at을 완료버튼과 동시에 자동으로 설정하기
- todo/serializers.py
- todo/api_views.py

추가할 앱
- interaction

| 필드                | 관계 유형      | 설명                                              | 주요 옵션                                                |
| ----------------- | ---------- | ----------------------------------------------- | ---------------------------------------------------- |
| `ForeignKey`      | 다대일<br>M2O | 한 모델 인스턴스(`보통 1`)가 다른 모델 인스턴스(`여러 개`)에 연결될 때 사용 | `on_delete`(삭제 시 동작), `related_name`, `null` 등       |
| `ManyToManyField` | 다대다<br>M2M | 두 모델 인스턴스가 서로 여러 개씩 연결될 때 사용                    | `through`(중개 모델 지정), `related_name`, `symmetrical` 등 |
| `OneToOneField`   | 일대일<br>1:1 | 한 모델 인스턴스가 다른 모델 인스턴스와 1:1로만 연결될 때 사용           | `on_delete`, `related_name`, `primary_key` 등         |
`ForeignKey (다대일):` 한 게시글(`Post`)에 여러 댓글(`Comment`)이 달릴 때
`ManyToManyField (다대다):` 학생(`Student`)과 강의(`Course`)가 서로 다대다로 연결될 때
`OneToOneField (일대일):` 사용자(`User`)와 프로필(`Profile`)이 1:1로 연결될 때

데이터와 표현의 역할 분리
모델은 "데이터 저장"이 목적이고, 시리얼라이저는 "응답 표현"이 목적입니다. 
좋아요 수를 DB에 저장하면 `좋아요/취소` 때마다 수동으로 +1/-1 처리해야 함 → 오류 가능성 증가하며 `count()`로 계산하면 항상 최신 값이 보장됨 (실시간 반영)하므로 좋아요 카운트는 시리얼 라이저에만 넣습니다.

✔️ "좋아요는 누르는 버튼이니까 → 모델에 저장"  
✔️ "좋아요 수는 보여주는 숫자니까 → 시리얼라이저에서 계산해서 제공"

