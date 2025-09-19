import time
lines = []
while True:
    line = input()
    if not line: 
        break
    lines.append(line)
user_input = ""
actual_output = ""
for i in range(len(lines)):
    if "say" in lines[i]:
        actual_output = lines[i].replace("say ", "print(")
        actual_output = actual_output.replace("please", ")")
    user_input +=  actual_output + "\n"
    if "jork it" in lines[i] and "please" in lines[i]:
        jorking_it = ["for w in range(12):","    time.sleep(2)","    print('im jorking it')", "print('i jorked it')" ]
        for line in jorking_it:
            user_input += line + "\n"
    if "<-" in lines[i]:
        actual_output = lines[i].replace("<-", "=")
        user_input += actual_output + "\n"
    try:
        exec(user_input)
    except Exception as e:
        print("syntax error twin")