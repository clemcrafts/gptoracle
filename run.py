from src.article import Article


def run():
    """
    Run the article creation.
    """
    article = Article()
    print(article.create_article())


if __name__ == '__main__':
    run()
