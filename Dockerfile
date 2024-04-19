# 파이썬 공식 이미지 사용
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /code

# 의존성 파일 복사 후 설치
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

# 애플리케이션 코드 복사
COPY ./app /code/app

# 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
