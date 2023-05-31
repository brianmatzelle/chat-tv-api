import requests

def main():
    prompt = "hey how are you?"
    response = generate(prompt)
    if response:
        print(response)
    else:
        print("An error occurred")


def generate(prompt):
    response = requests.get(f'https://git.heroku.com/chat-tv-api/v1/generate?prompt={prompt}')
    if response.status_code == 200:
        return response.json()['text']
    else:
        return None


if __name__ == '__main__':
    main()
