import csv
import openai
import requests
import base64
from dotenv import load_dotenv
import os
from datetime import datetime


class Article:
    """
    A class responsible for Article creation using OpenAI and WordPress.
    """

    def __init__(self):
        """
        Initializes an instance of the Article class.
        Sets up environment variables, keywords, and default title.
        """
        load_dotenv()
        self.keywords = []
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.wp_api_password = os.environ.get("WP_API_PASSWORD")
        self.wp_api_username = os.environ.get("WP_API_USERNAME")
        self.title = 'Best Indonesian Gold Coins'
        self.post = {}

    def read_keywords(self):
        """
        Reads keywords from a CSV file and appends them to the keywords attribute.
        """
        with open('data/keywords.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                keyword = row[0]
                script = row[1]
                self.keywords.append({'keyword': keyword, 'script': script})

    def get_chatgpt_response(self, prompt):
        """
        Fetches a response from ChatGPT based on the provided prompt.

        Args:
            prompt (str): The input string to get a response for.

        Returns:
            str: The response content from ChatGPT.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user",
                 "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']

    def create_image(self):
        """
        Creates an image using OpenAI based on a given prompt.

        Returns:
            str: The URL of the generated image.
        """
        response = openai.Image.create(
            prompt="a white siamese cat",
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url

    def create_post(self):
        """
        Constructs the post with default configurations and calls methods to set the title and content.
        """
        self.post = {
            'status': 'draft',
            'date': str(datetime.now())
        }
        self.set_title()
        self.set_content()

    def set_title(self):
        """
        Sets the post's title attribute.
        """
        self.post['title'] = self.title

    def set_content(self):
        """
        Sets the post's content attribute by fetching a response from ChatGPT.
        """
        self.post['content'] = self.get_chatgpt_response(self.title)

    def create_article(self):
        """
        Constructs the article post and sends it to WordPress.

        Returns:
            dict: The JSON response from the blog post creation.
        """
        self.create_post()
        username = os.environ.get("WP_API_USERNAME")
        password = os.environ.get("WP_API_PASSWORD")
        url = os.environ.get("BLOG_POST_URL")
        creds = username + ':' + password
        cred_token = base64.b64encode(creds.encode())

        header = {'Authorization': 'Basic ' + cred_token.decode('utf-8')}

        response = requests.post(url, headers=header, json=self.post)
        return response.json()
