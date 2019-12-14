commands = [
    '/번역 댕댕이',
    '/주식 aapl',
    '/미세먼지',
    'hi'
]
command = commands[0]

if commands[0] == '/':
    if ' ' in command:  # 띄어쓰기 후에 추가 input 있음 
        words = command.split(' ')  # '/번역 댕댕이' 문자열이 ['/번역', '댕댕이'] 리스트로 바뀜
        if words[0] == '/번역':
            pass  # 번역작업 with words[1]
    else:  # 띄어쓰기 없음
        if command == '/미세먼지':
            pass
        
else:
    print(commands)
