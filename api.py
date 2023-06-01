from flask import Flask, request
from flask_restful import Resource, Api
import openai
import time
import os
import json

openai.api_key = os.environ.get('OPENAI_KEY')

app = Flask(__name__)
api = Api(app)

MAX_RETRIES = 3
RETRY_DELAY = 2

class Generate(Resource):
    def __init__(self):            
        self.model = request.args.get('model')
        # self.memory = request.args.get('memory')
        self.memory = json.loads(self.memory) if isinstance(self.memory, str) else self.memory
        self.bot_name = request.args.get('bot_name')
        self.input_text = request.args.get('input_text')
        self.streamer_name = request.args.get('streamer_name')
        self.context = request.args.get('context')

    #@ CHAT GPT @#
    def get(self):
        if self.model == 'gpt-3.5-turbo' or self.model == 'gpt-4':
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    # messages=self.memory,
                    messages=self.memory,
                    max_tokens=25,
                    temperature=1,
                    # top_p=top_p,
                )
                generated_text = response.choices[0].message.content
                return generated_text

            except openai.error.AuthenticationError as e:
                return "Error: Invalid API Key"

            except openai.error.RateLimitError:
                return "The rate limit for API requests has been exceeded. The program will wait for some time and retry."
            
            except openai.error.APIError:
                # error_dialog.exec_()
                time.sleep(RETRY_DELAY)
                return "The rate limit for API requests has been exceeded. The program will wait for some time and retry."

        #@ END CHAT GPT @#
        
        #@ DAVINCI @#
        else:
            try:
                response = openai.Completion.create(
                    engine=self.model,
                    prompt=f'{self.context}\n{self.streamer_name}: {self.input_text}\n{self.bot_name}:',
                    temperature=1,
                    max_tokens=25,
                )
                return response.choices[0].text

            except openai.error.AuthenticationError as e:
                return "Error: Invalid API Key"

            except openai.error.RateLimitError:
                return "The rate limit for API requests has been exceeded. The program will wait for some time and retry."
            
            except openai.error.APIError:
                return "The rate limit for API requests has been exceeded. The program will wait for some time and retry."

        #@ DAVINCI @#

api.add_resource(Generate, '/api/v1/generate')

if __name__ == '__main__':
    app.run(debug=True)
