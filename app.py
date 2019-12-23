from flask import Flask, render_template, request
import requests
from decouple import config
import bs4

app = Flask(__name__)

# Telegram chatbot 기본 url
api_url = 'https://api.telegram.org'

# .env 파일에서 key 가져오기
token = config('TOKEN')
admin_id = config('ADMIN_ID')
secret_url = config('SECRET_URL')
naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')

# commands list
commands = [
    '/번역 <키워드>',
    '/미세먼지',
]

# test 용
@app.route('/')
def index():
    return ':)'

# /chatbot으로 요청이 왔을 때
@app.route('/chatbot', methods=['POST'])
def telegram():
    req = request.get_json()
    user = req['message']['from']['id']  # user의 chat id
    message = req['message']['text']  # user의 입력 메세지
    no_error = '존재하지 않는 명령어입니다.'

    if message[0] == '/':
        if ' ' in message:  # 띄어쓰기 후에 추가 input 있음
            words = message.split(' ')  # '/번역 댕댕이' 문자열이 ['/번역', '댕댕이'] 리스트로 바뀜
            if words[0] == '/번역':
                headers = {
                    'X-Naver-Client-Id': naver_client_id,
                    'X-Naver-Client-Secret': naver_client_secret,
                }

                data = {
                    'source': 'ko',
                    'target': 'en',
                    'text': words[1],
                }

                # URL 에서 Naver에 key를 보내며 API 요청 후 데이터 가져오기
                res = requests.post('https://openapi.naver.com/v1/papago/n2mt', data=data, headers=headers)
                
                # 데이터에서 필요한 정보만 추출
                result = res.json()['message']['result']['translatedText']  # 번역결과
            else:
                result = no_error  # 존재하지 않는 명령어입니다.

        else:  # 띄어쓰기 없음
            if message == '/미세먼지':
                url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80'
                
                # URL에서 크롤링하여 데이터 가져오기
                response = requests.get(url).text

                # Python에서 데이터를 알아볼 수 있게 parser함.
                text = bs4.BeautifulSoup(response, 'html.parser')

                # 데이터에서 필요한 정보만 추출
                result = text.select_one('#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div > div > div.main_box > div.detail_box > div.tb_scroll > table > tbody').text.replace('   ', ', ')

            else:
                result = no_error  # 존재하지 않는 명령어입니다.
    else:
        result = str(commands)

    URL = f'{api_url}/bot{token}/sendMessage?chat_id={user}&text={result} :)'

    # URL에 result 보내겠다.
    requests.get(URL)
    return ('success', 200)

if __name__ == '__main__':
    app.run(debug=True, port=80)
