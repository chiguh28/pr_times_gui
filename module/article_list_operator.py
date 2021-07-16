import time
from bs4 import BeautifulSoup
import datetime
from urllib.parse import urljoin


class ArticleListOperator():
    def __init__(self, driver, end_date) -> None:
        self.driver = driver
        self.end_date = end_date

    def more(self):
        """もっとボタンをクリック

        Args:
            page (int): ページ数

        Returns:
            bool: もっとボタンをクリックしたかのフラグ
        """

        try:
            self.driver.find_element_by_xpath(
                "/html/body/main/section/section/div/div/a").click()
            return True
        except BaseException:
            # もっとボタンをクリックできなかった場合の例外処理
            return False

    def can_more(self, articles):
        """もっとボタンをクリックできるか判定

        記事の公開日が検索範囲内か判定する

        Args:
            articles (list): 記事リスト
        """

        for article in articles:
            article_date = self.get_article_date(article)
            # 記事公開日が検索終了日より古い場合はもっとボタンをクリックしない
            if article_date < self.end_date:
                return False

        # forループ処理を正常に終了した場合は公開日が検索範囲内だったためもっとボタンをクリックする
        return True

    def get_articles(self, page, size=40):
        """記事を取得

        Args:
            page (int): 表示されているページ番号
            size (int, optional): 1ページに公開されている記事数. Defaults to 40.

        Returns:
            [list]: [取得した記事]

        Notes:
            表示されている記事を最初から最後まで取得する
            PR Timesはページが下に追加されていく形式のため、ページ開始位置から最後まで取得するという方法を用いる
        """

        # サイトを読み込むための待機時間
        time.sleep(3)
        html = self.driver.execute_script(
            "return document.body.innerHTML")
        soup = BeautifulSoup(html, "html.parser")

        # ページ開始位置から最後まで取得
        articles = soup.select('article.list-article')[page * size:]
        return articles

    def get_article_date(self, article):
        """記事の公開日を取得

        Args:
            article ([type]): 記事アイテム

        Returns:
            date: 公開日
        """
        article_time = article.find(class_='list-article__time')
        # 記事公開日時をdatetime表記に変換
        try:
            str_to_dt = datetime.datetime.strptime(
                article_time.get('datetime'), '%Y-%m-%dT%H:%M:%S%z')
        except BaseException:
            try:
                article_time_cvt = article_time.get(
                    'datetime').replace('+09:00', '+0900')
                str_to_dt = datetime.datetime.strptime(
                    article_time_cvt, '%Y-%m-%dT%H:%M:%S%z')
            except BaseException:
                str_to_dt = datetime.datetime.strptime(
                    article_time.text, '%Y年%m月%d日 %H時%M分')
        article_dt = datetime.datetime(
            str_to_dt.year,
            str_to_dt.month,
            str_to_dt.day,
            str_to_dt.hour,
            str_to_dt.minute)

        return article_dt

    def get_article_urls(self, articles, base_url):
        """記事リンクを取得する

        Args:
            base_url (str): PR TimesのURL
            articles (list): 記事一覧
        Returns:
            article_urls (list): 記事リンク
        """
        article_urls = []

        for article in articles:
            article_link = article.find('a')
            relative_url = article_link["href"]
            # hrefから取得できるURLは相対パスのため絶対パスに変換する
            article_url = urljoin(base_url, relative_url)
            article_urls.append(article_url)

        return article_urls
