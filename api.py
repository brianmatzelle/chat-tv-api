from flask import Flask, request
from flask_restful import Resource, Api
import openai
import time
import os

openai.api_key = os.environ.get('OPENAI_KEY')

app = Flask(__name__)
api = Api(app)

MAX_RETRIES = 3
RETRY_DELAY = 2

# class Generate(Resource):
#     def get(self):
#         prompt = request.args.get('prompt')
#         response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100)
#         return {'text': response.choices[0].text.strip()}

# def Generate(self, input_text, streamer_name, debug_signal, max_tokens=25, temperature=1, top_p=1)
class Generate(Resource):
    def __init__(self):            
        self.model = request.args.get('model')
        self.memory = request.args.get('memory')
        self.bot_name = request.args.get('bot_name')
        self.input_text = request.args.get('input_text')
        self.streamer_name = request.args.get('streamer_name')
        self.context = request.args.get('context')

    #@ CHAT GPT @#
    def get(self):
        if self.model == 'gpt-3.5-turbo' or self.model == 'gpt-4':
            for _ in range(MAX_RETRIES):  # You need to define MAX_RETRIES
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
                    # error_dialog = QMessageBox()
                    # error_dialog.setIcon(QMessageBox.Critical)
                    # error_dialog.setWindowTitle("Error")
                    # error_dialog.setText("Error: Invalid API Key")
                    # error_dialog.setInformativeText("Your API key is incorrect, or you didn't provide one. You can obtain an API key from https://platform.openai.com/account/api-keys.")
                    # error_dialog.setStandardButtons(QMessageBox.Ok)
                    # error_dialog.exec_()
                    # QApplication.instance().quit()
                    return "Error: Invalid API Key"

                except openai.error.RateLimitError:
                    # debug_signal.emit("The rate limit for API requests has been exceeded. The program will wait for some time and retry.")
                    time.sleep(RETRY_DELAY)  # You need to define RETRY_DELAY
                
                except openai.error.APIError:
                    # error_dialog.exec_()
                    # debug_signal.emit("The rate limit for API requests has been exceeded. The program will wait for some time and retry.")
                    time.sleep(RETRY_DELAY)

            # If the code reaches this point, it means all retries failed.
            # error_dialog = QMessageBox()
            # error_dialog.setIcon(QMessageBox.Critical)
            # error_dialog.setWindowTitle("Error")
            # error_dialog.setText("Error: All retries failed")
            # error_dialog.setInformativeText("All retries to connect to the OpenAI API failed due to rate limit exceeding. Please try again later.")
            # error_dialog.setStandardButtons(QMessageBox.Ok)
            # error_dialog.exec_()
            # QApplication.instance().quit()
            return "Error: All API retries failed"

        #@ END CHAT GPT @#
        
        #@ DAVINCI @#
        else:
            for _ in range(MAX_RETRIES):
                try:
                    response = openai.Completion.create(
                    engine=self.model,
                    prompt=f'{self.context}\n{self.streamer_name}: {self.input_text}\n{self.bot_name}:',
                    temperature=1,
                    max_tokens=25,
                    )
                    return response.choices[0].text

                except openai.error.AuthenticationError as e:
                    # error_dialog = QMessageBox()
                    # error_dialog.setIcon(QMessageBox.Critical)
                    # error_dialog.setWindowTitle("Error")
                    # error_dialog.setText("Error: Invalid API Key")
                    # error_dialog.setInformativeText("Your API key is incorrect, or you didn't provide one. You can obtain an API key from https://platform.openai.com/account/api-keys.")
                    # error_dialog.setStandardButtons(QMessageBox.Ok)
                    # error_dialog.exec_()
                    # QApplication.instance().quit()
                    return "Error: Invalid API Key"

                except openai.error.RateLimitError:
                    # debug_signal.emit("The rate limit for API requests has been exceeded. The program will wait for some time and retry.")
                    time.sleep(RETRY_DELAY)  # You need to define RETRY_DELAY
                
                except openai.error.APIError:
                    # error_dialog.exec_()
                    # debug_signal.emit("The rate limit for API requests has been exceeded. The program will wait for some time and retry.")
                    time.sleep(RETRY_DELAY)

            return "Error: All API retries failed"
        #@ DAVINCI @#

api.add_resource(Generate, '/api/v1/generate')

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request
# from flask_restful import Resource, Api
# import openai
# import os

# openai.api_key = os.environ.get('OPENAI_KEY')

# app = Flask(__name__)
# api = Api(app)

# class Generate(Resource):
#     def get(self):
#         prompt = request.args.get('prompt')
#         response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=25)
#         return {'text': response.choices[0].text.strip()}

# api.add_resource(Generate, '/api/v1/generate')

# if __name__ == '__main__':
#     app.run(debug=True)
