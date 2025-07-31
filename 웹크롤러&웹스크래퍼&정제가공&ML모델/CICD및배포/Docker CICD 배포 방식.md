Docker란?
- 내 앱을 컨테이너로 감싸는 기술
- 쉽게 말해, Django + Python + 설정 파일들을 하나의 상자로 포장
---
도커 다운받기 및 Download Docker Desktop 후 install
https://www.docker.com/products/docker-desktop/

![[Pasted image 20250731151922.png]]
- Docker Desktop 실행하기
    - 시작 메뉴에서 `Docker Desktop` 검색 후 실행
- 오른쪽 위 ⚙️ **[Settings] (설정)** 클릭
- 왼쪽 메뉴에서 **[Resources]** 클릭 → 하위 메뉴 중 **[WSL Integration]** 클릭
- 여기서 Ubuntu (또는 사용 중인 WSL 배포판) 찾아서 체크!

WSL2 터미널(Ubuntu)에서 Docker 명령어가 잘 작동하는지 테스트:
```bash
docker --version
```

VScode에서 도커를 설치합니다.
![[Pasted image 20250731192015.png]]
- Dockerfile 작성, 이미지 빌드, 컨테이너 목록 확인, 컨테이너 시작/중지 UI 제공
- VSCode에서 Docker와 관련된 대부분의 기능을 시각적으로 관리 가능

---
Django 프로젝트 & Dockerfile 작성
```bash
mkdir docker_project2
cd docker_project2

python -m venv .venv
source .venv/bin/activate
pip install django djangorestframework gunicorn python-dotenv

django-admin startproject proj .
python manage.py startapp myapp

# 패키지 기록
pip freeze > requirements.txt
```
`gunicorn`은 Docker 컨테이너 내부에서 Django 앱을 실행할 때 사용합니다.

```python
INSTALLED_APPS = [
    "myapp",
    "rest_framework"
]
```

`Dockerfile` 작성
```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "proj.wsgi:application", "--bind", "0.0.0.0:8000"]
```

보조 파일 구성
.dockerignore
```dockerfile
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
.env
.venv
venv
db.sqlite3
```
Docker 빌드 시, 이미지에 포함하지 않을 파일을 정의  
`docker build .` 할 때, 컨텍스트에서 제외됨

.env
```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=*
```
이후 Docker에서 `.env`도 읽게 하려면 환경 변수 연동 작업이 추가로 필요합니다.

로컬에서 Docker 빌드 및 실행
```bash
docker build -t django-docker-app .
```

실행
```bash
docker run -d -p 8000:8000 django-docker-app

# 브라우저에서 실행
http://localhost:8000/
```

도커중지(필요시) 포트 8000 사용 중인 컨테이너 확인
```bash
docker ps
docker stop <컨테이너_ID> 
docker rm -f 4a1bcdef5678
```

.pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black", "--filter-files"]

  # - repo: https://github.com/pycqa/flake8
  #   rev: 7.0.0
  #   hooks:
  #     - id: flake8
  #       args: [--max-line-length=92]
```

.pre-commit-config.yaml사용을 위한 명령어 실행
```bash
pip install pre-commit
pre-commit install
```

.gitignore만들기
```python
# Python 기본 캐시 및 가상환경 파일 제외
venv/
env/
__pycache__/
*.pyc
*.pyo
*.pyd
.gitignore

# 환경 변수 파일 (보안 중요)
.env

# 가상환경
.venv/

# 데이터베이스 파일 제외 (SQLite 등)
db.sqlite3
*.sqlite3

# Django 마이그레이션 캐시 제외
**/migrations/*.pyc
**/migrations/*.py
!**/migrations/__init__.py

# 로그 파일 제외
*.log
*.out
*.err

# 미디어 및 정적 파일 (수동 업로드 방지)
media/
staticfiles/
static/
node_modules/

# VS Code 및 IDE 설정 파일 제외
.vscode/
.idea/
*.sublime-workspace

# Docker 관련 파일 제외 (사용할 경우)
docker-compose.override.yml
```

---
CICD연결하기

깃허브에서 레파지토리 생성
![[Pasted image 20250730133823.png]]

![[Pasted image 20250730140730.png]]

Docker CI만들기 ( docker-ci.yml)
```yml
name: Django CI with Docker

on:
  push:
    branches: [ "main", "dev" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout source code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Build Docker image
      run: |
        docker build -t django-test-image .

    - name: Run tests inside Docker container
      run: |
        docker run --rm django-test-image python manage.py test
```


```bash
# 원격 저장소 내용을 먼저 가져와 병합하고 푸시하기 (권장)
git pull origin main --allow-unrelated-histories

git init
git remote add origin https://github.com/handgonpo/docker_project2.git
git add .
git commit -m "init dockerized django project"
git branch -M main
git push -u origin main
```


---
AWS EC2 기반 배포 설정

전체 순서 (EC2 기반 Docker 배포)
1.  EC2 인스턴스 생성 및 설정
2.  보안 그룹(포트 열기) 설정
3.  SSH 접속 및 Docker 설치
4.  GitHub에서 코드 받아오기
5.  `.env` 파일 생성
6.  Docker 빌드 및 실행
7.  EC2 퍼블릭 IP로 접속 확인
---
EC2 인스턴스 생성
![[Pasted image 20250731150751.png]]
![[Pasted image 20250731152318.png]]
![[Pasted image 20250731152546.png]]
키는 다운로드에 잘 저장되어 있습니다. 잘 보관해야 합니다.

“인스턴스 시작” 클릭
![[Pasted image 20250731153047.png]]

.pem 파일의 저장경로를 확인합니다.
![[Pasted image 20250731162343.png]]

터미널에서:
```bash
# 1. 키 저장 폴더 생성 (최초 1회)
mkdir -p ~/aws_keys

# 2. Windows 경로에서 WSL 홈 디렉토리로 키 파일 복사
cp /mnt/c/Users/MS/Downloads/my-ec2-key.pem ~/aws_keys/

# 3. 권한 설정 (중요!)
chmod 400 ~/aws_keys/my-ec2-key.pem
```

EC2 인스턴스에 접속
```bash
ssh -i ~/aws_keys/my-ec2-key.pem ubuntu@54.180.115.79
```
이때 `yes`가 뜨면 반드시 `yes` 전부 입력해야 합니다

성공 시 화면 예시
```bash
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

ubuntu@ip-172-31-45-109:~$ 
```

Docker 설치 및 환경 구성
1단계: Docker 설치
Docker 설치 (VSCode 터미널에서 EC2에 SSH 접속한 상태에서 실행)
```bash
# 패키지 업데이트
sudo apt update

# Docker 설치
sudo apt install -y docker.io

# Docker 데몬 실행 및 부팅 시 자동 시작 설정
sudo systemctl start docker
sudo systemctl enable docker
```
도커 설치 및 자동 실행 설정 완료


EC2에서 Ubuntu로 접속하려면:
![[Pasted image 20250731164224.png]]
![[Pasted image 20250731164310.png]]

2단계: Docker 동작 확인
현재 사용자(`ubuntu`)를 `docker` 그룹에 추가 (EC2 내부에서 실행)
```bash
# 도커 명령어를 sudo 없이 실행할 수 있도록 권한 부여
sudo usermod -aG docker ubuntu

# 그룹 변경사항 적용을 위한 세션 재접속
exit  # SSH 세션 종료

# 다시 SSH 접속
ssh -i ~/aws_keys/my-ec2-key.pem ubuntu@54.180.115.79  

# 그룹확인
groups

#결과 정상적으로 docker 그룹에 포함
ubuntu docker

# Docker 정상 작동 테스트
docker run hello-world

# 출력결과
Hello from Docker!
```
도커 완벽 설치 및 작동 확인 완료

---
다음 단계: GitHub Actions 기반 CI/CD 구성

목표: `main` 브랜치에 push 할 때마다  
GitHub Actions가 EC2에 자동으로 접속 → 코드 pull → Docker 재빌드 및 재시작


EC2에서 GitHub 접속용 SSH 키 생성
```bash
# EC2에서 실행
ssh-keygen -t rsa -b 4096 -C "ec2-cicd" -f ~/.ssh/deploy_key
```

프롬프트가 뜨면 그냥 Enter → 패스프레이즈 없이 생성
![[Pasted image 20250731164524.png]]
엔터를 두번 누르면 다음과 같은 화면이 나옵니다.
![[Pasted image 20250731164634.png]]

공개 키를 GitHub 저장소에 등록: 공개 키 확인
```bash
cat ~/.ssh/deploy_key.pub
```
출력된 내용 전체를 복사하세요 (예: `ssh-rsa AAAA...` 로 시작)
![[Pasted image 20250731165323.png]]


GitHub 저장소에 Deploy Key 등록: 위에서 복사한 키를 자신의 깃허브 레포에 저장합니다.
![[Pasted image 20250731165103.png]]
등록을 완료합니다.

---
EC2에서 `.ssh/config` 설정
EC2에 SSH로 접속한 상태에서 아래 명령 실행:
```bash
nano ~/.ssh/config
```

EC2 서버에서 GitHub에 SSH 접속할 때 어떤 키 파일을 사용할지 알려주는 설정
```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/deploy_key
```
- 입력 후 `Ctrl + O` → 엔터 (저장)
- `Ctrl + X` (종료)

다음 단계: Git 연결 테스트
이제 실제로 GitHub 저장소에 연결 가능한지 테스트합니다:
```bash
# EC2에서 저장할 디렉토리 이동
cd ~
mkdir -p deploy_test && cd deploy_test

# SSH 방식으로 클론 (URL 중요!)
git clone git@github.com:handgonpo/docker_project2.git

# 이렇게 질문하면 yes라고 입력합니다.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```
 GitHub 서버에 처음 SSH로 접속할 때 나오는 정상적인 보안 확인 메시지입니다.  
 한 번만 `yes`를 입력하면 Git이 GitHub 서버를 신뢰하고 접속을 계속하게 됩니다.

이런 메시지가 보이면 EC2와 GitHub 간 SSH 연결이 완벽히 구성된 상태입니다.
```bash
Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.
remote: Enumerating objects: ...
...
Cloning into 'docker_project2'...
```

---
GitHub Secrets에 EC2 비공개 키 등록
이 작업은 Deploy Key의 비공개 키(`~/.ssh/deploy_key`) 내용을 GitHub에 등록해서  GitHub Actions가 EC2에 SSH 접속할 수 있도록 하는 과정입니다.

EC2에서 비공개 키 내용 확인
```bash
cat ~/.ssh/deploy_key
```
![[Pasted image 20250731171119.png]]

이부분을 모두 복사합니다. 
```
-----BEGIN OPENSSH PRIVATE KEY-----
abdksxldkaldkfsadlkfjsadlfk.....
-----END OPENSSH PRIVATE KEY-----
```
정확히 확인하려면 다운로드에 내려받은 `my-ec2-key.pem`를 vscode로 열어서 모두 복사후 깃허브 Actions에 생성하여 붙여넣습니다.

다시 깃허브로 가서 settings에서 Actions를 클릭합니다.
![[Pasted image 20250731171429.png]]

그다음 복사한 키를 아래와 같이 붙여넣습니다.
![[Pasted image 20250731171004.png]]
Add secret클릭하여 저장합니다.

이후 EC2_HOST와 EC2_USER도 등록합니다.
![[Pasted image 20250731175147.png]]
 EC2_HOST확인하는 방법: EC2 우분투에서 퍼블릭 IP 확인 명령어
```bash
curl http://checkip.amazonaws.com
```

출력예시:
```
54.180.115.79
```

EC2_USER는 ubuntu입니다. 이렇게 3개를 위의 이미지와 같이 등록해 주세요.
이제 GitHub Actions가 `EC2_SSH_KEY`를 사용해서 EC2에 접속할 수 있게 되었어요!

---
EC2 자동 배포용 워크플로 파일 추가
새로운 파일 생성
`docker-deploy.yml` 같은 이름으로 아래 디렉토리에 새로 만드세요:
```bash
.github/workflows/docker-deploy.yml
```

```yml
name: Deploy to EC2

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up SSH
      run: |
        mkdir -p ~/.ssh
        echo "${{ secrets.EC2_SSH_KEY }}" > ~/.ssh/id_rsa
        chmod 600 ~/.ssh/id_rsa
        ssh-keyscan -H ${{ secrets.EC2_HOST }} >> ~/.ssh/known_hosts

    - name: Deploy to EC2
      run: |
        ssh -o StrictHostKeyChecking=no ${{ secrets.EC2_USER }}@${{ secrets.EC2_HOST }} << 'EOF'
        cd ~/deploy_test/docker_project2
        git pull origin main
        docker build -t django-docker-app .
        docker stop django-app || true
        docker rm django-app || true
        docker run -d -p 8000:8000 --name django-app django-docker-app
        EOF
```
배포 조건
- `main` 브랜치에 `push` 될 때 자동 배포됩니다.
- Secrets:
    - `EC2_HOST` → 예: `ubuntu@54.180.115.79`
    - `EC2_KEY` → `.pem` 파일 내용 (비공개)

이제 배포가 성공되는지 READMD.md와 새로 생성한 배포파일을 커밋 푸시 해봅니다
Git 커밋 & 푸시 명령어
```bash
# 1. 모든 변경사항을 Git stage에 추가
git add .

# 2. 커밋 메시지 작성
git commit -m "chore: add deploy workflow and update README"

# 3. main 브랜치로 푸시
git push origin main
```

푸시 후 확인
- GitHub → Actions 탭에서 워크플로 실행 확인
- EC2에서 `docker ps` 로 컨테이너 확인
- 웹 브라우저에서 `http://<EC2_PUBLIC_IP>:8000` 확인

다운로드에서 받은 .pem파일을 현재 작업하고 있는 프로젝트에 복사해서 붙여 넣습니다.
![[Pasted image 20250731181506.png]]

권한 설정
```bash
chmod 400 my-ec2-key.pem
```
`.pem` 파일은 보안상 권한이 꼭 `400`이어야 합니다.

터미널에서 다음과 같이 접속합니다.
```
ssh -i my-ec2-key.pem ubuntu@54.180.115.79
```

마지막으로 Docker 컨테이너 실행 확인하기: EC2 utuntu
```bash
docker ps
```

이렇게 출력되면 연결 성공입니다:
![[Pasted image 20250731185843.png]]

---
아래는 자주 겪는 변경 시나리오별로 Dockerfile, GitHub Actions(YAML), 기타 설정을 수정해야 하는지 여부를 정리한 것입니다.

| 시나리오                                         | Dockerfile 수정              | GitHub Actions 수정         | 기타                                                    |
| -------------------------------------------- | -------------------------- | ------------------------- | ----------------------------------------------------- |
| 모델 생성/변경 후 마이그레이션                            | ❌ 필요 없음                    | ❌ 필요 없음                   | EC2 접속 → `docker exec`로 `manage.py migrate` 실행        |
| 새로운 Python 패키지 설치                            | ✅ `requirements.txt` 갱신 필요 | ❌ 보통 필요 없음                | `Dockerfile`에서 `pip install -r requirements.txt` 재반영됨 |
| 새로운 앱(app) 생성                                | ❌                          | ❌                         | 코드 커밋만 하면 됨                                           |
| settings.py 수정 (디버그/DB/API 변경 등)             | ❌                          | ❌ 또는 🔶 `.env`/Secrets 수정 | 변경된 설정을 반영한 커밋만 필요                                    |
| 정적 파일 수집 필요 (collectstatic)                  | ❌ 또는 ✅ (설정 추가 시)           | ❌ 또는 ✅ (명령어 추가 시)         | production 배포 시 필요 (예: whitenoise 사용)                 |
| SQL 데이터베이스 종류 변경 (SQLite → MySQL/PostgreSQL) | ✅ (DB 드라이버 추가)             | ✅ (환경변수 추가)               | `.env`, `settings.py`, DB 설정 전환                       |
| Gunicorn 명령어 옵션 변경                           | ✅                          | ❌                         | `CMD` 또는 `ENTRYPOINT` 수정 필요                           |
| API 키 / 시크릿 키 등 환경 변수 변경                     | ❌                          | ✅ (GitHub Secrets에서 수정)   | Django에서는 `os.environ.get()`으로 관리                     |

---
EC2 인바운드 보안그룹
![[Pasted image 20250731190237.png]]
![[Pasted image 20250731190359.png]]
포트 8000은 운영 시 제거하거나 Nginx 뒤에 둘 예정입니다.


추후 마이그레이트 명령어: vscode 터미널에서
컨테이너 이름을 검색합니다. 예시:
```bash
CONTAINER ID   IMAGE               COMMAND                  CREATED             STATUS             PORTS                                       NAMES
5e1e9d73534f   django-docker-app   "gunicorn proj.wsgi:…"   About an hour ago   Up About an hour   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   **django-app**

```
컨테이너 이름은 django-app입니다.

확인후 다음과같이 마이그레이트를 합니다.
```bash
docker exec -it django-app python manage.py migrate
```

`.env` 또는 환경변수
```env
DJANGO_SECRET_KEY=your-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=54.180.115.79,localhost
```

proj/settings.py
```python
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")


INSTALLED_APPS = [
    "myapp",
    "rest_framework"
]
```