from g4f.client import Client
def chat():
    c = Client()
    m = []
    while True:
        u = input()
        if u.lower() == 'exit': break
        m.append({"role": "user", "content": u})
        try:
            r = c.chat.completions.create(model="gpt-3.5-turbo", messages=m)
            m.append({"role": "assistant", "content": r.choices[0].message.content})
            print(r.choices[0].message.content)
        except: break

chat()
