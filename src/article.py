import csv
import openai
import requests
import base64
from dotenv import load_dotenv
import os


class Article:
    """
    A class responsible for Article creation.
    """

    def __init__(self):
        load_dotenv()
        self.keywords = []
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.wp_api_password = os.environ.get("WP_API_PASSWORD")
        self.wp_api_username = os.environ.get("WP_API_USERNAME")
        self.script_best = {
            'introduction': 'Write an introduction for a blog article about [keyword], 250 words, do not name anything',
            'section_1': '[keyword]. Write a blog section about the first item of your list, h2 tags for the title, 250 words',
            'section_2': '[keyword]. Write a blog section about the second item of your list, h2 tags for the title, 250 words, '
                         'use a different structure from your previous answer',
            'section_3': '[keyword]. Write a blog section about the third item of your list, h2 tags for the title, 250 words, '
                         'use a different structure from your previous answer',
            'conclusion': 'conclusion of the blog article on [keyword]. '
                          'Use a comparison table to compare the 3 answers above. '
                          'conclude with an opening philosophical question.' }

    def read_keywords(self):
        """
        Read the keywords.
        """
        with open('data/keywords.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                keyword = row[0]
                script = row[1]
        self.keywords.append({'keyword': keyword, 'script': script})


    def create_content(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user",
                 "content": "What is France? 200 words"}
            ]
        )
        return response['choices'][0]['message']['content']


    def create_image(self):
        response = openai.Image.create(
            prompt="a white siamese cat",
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url


    def create_article(self):
        url = "https://altcoinoracle.com/wp-json/wp/v2/posts"
        user = self.wp_api_username
        password = self.wp_api_password
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        post = {'title': 'Hello World',
                'status': 'draft',
                'content': 'This is my first post created using rest API',
                'categories': 5,
                'date': '2020-01-05T10:00:00'}
        return requests.post(url, headers=header, json=post)
