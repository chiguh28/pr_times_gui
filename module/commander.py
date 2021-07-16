import datetime
from .driver_factory import DriverFactory
from .article_parser import ArticleParser
from .article_list_operator import ArticleListOperator
from .writer import ExcelWriter

URL = 'https://prtimes.jp/'
KEYWORDS = [
    'Mail',
    'mail',
    'メール',
    'メールアドレス',
    'E-mail',
    'e-mail',
    'Email',
    'email']


class Commander():
    def __init__(self) -> None:
        self.path = None
        self.end_time = None
        self.LAST_ONE_DAY = datetime.timedelta(days=1)
        self.LAST_ONE_WEEK = datetime.timedelta(weeks=1)
        self.LAST_ONE_MONTH = datetime.timedelta(weeks=4)
        self.LAST_ONE_YEAR = datetime.timedelta(weeks=12)
        self.LAST_TWO_YEAR = datetime.timedelta(weeks=24)
        self.LAST_THREE_YEAR = datetime.timedelta(days=36)
        self.LAST_FOUR_YEAR = datetime.timedelta(days=48)
        self.LAST_FIVE_YEAR = datetime.timedelta(days=60)

    def run(self):
        # 記事を解析するクラス
        parser = ArticleParser()

        # 記事リンク一覧
        article_url_list = []

        for keyword in KEYWORDS:
            page = 0
            is_next_page = True

            ######################################
            # ① PR Timesを開きキーワード検索
            ######################################
            factory = DriverFactory(URL)
            driver = factory.create(keyword)

            # キーワード検索結果ページを受け取る
            operator = ArticleListOperator(
                driver, self.end_time)

            ######################################
            # 記事リスト作成
            ######################################
            while is_next_page:
                ######################################
                # ②検索結果ページから記事リンクを取得
                ######################################
                articles = operator.get_articles(page)
                article_url_list.append(
                    operator.get_article_urls(
                        articles, URL))

                ######################################
                # ③もっとボタンをクリックできる場合はクリック
                ######################################
                if operator.can_more(articles):
                    is_next_page = operator.more()

                    # もっとボタンをクリックした場合はページをめくる
                    page += 1
                else:
                    is_next_page = False
                ######################################
                # ④もっとボタンがクリックできなくなるまでリンクを取得し続ける
                ######################################
            # 1キーワードが終わり次第、生成したドライバーを閉じる
            driver.close()
        ##################################
        # メーリングリスト作成
        ##################################
        for article_urls in article_url_list:
            for article_url in article_urls:
                parser.update_soup(article_url)
                parser.create_mailing_list()

        company_list = parser.getter_company_list()
        mailing_list = parser.getter_mailing_list()
        ##################################
        # メーリングリストファイル作成
        ##################################
        writer = ExcelWriter(self.path)
        writer.write(company_list, mailing_list)


    def get_params(self, path, end_time):
        """パラメータ取得

        Args:
            path (str): excelファイル保存先
            end_time (str): 検索範囲の期間
        Notes:
            必要なパラメータを取得するためのメソッド
            runメソッドを実行させる前に実行しておく
        """
        self.path = path
        self.end_time = self.calc_end_time(end_time)

    def calc_end_time(self, end_time):
        """期間を計算する

        Args:
            end_time (str): 検索期間

        Returns:
            datetime: 検索期間を時間に変換した値

        Notes:
            メソッドを実行した時間から検索期間を引くことで上限時間を算出する
        """
        dt_now = datetime.datetime.now()

        if '1日' in end_time:
            dt_delta = self.LAST_ONE_DAY
        elif '1週間' in end_time:
            dt_delta = self.LAST_ONE_WEEK
        elif '1か月' in end_time:
            dt_delta = self.LAST_ONE_MONTH
        elif '1年' in end_time:
            dt_delta = self.LAST_ONE_YEAR
        elif '2年' in end_time:
            dt_delta = self.LAST_TWO_YEAR
        elif '3年' in end_time:
            dt_delta = self.LAST_THREE_YEAR
        elif '4年' in end_time:
            dt_delta = self.LAST_FOUR_YEAR
        elif '5年' in end_time:
            dt_delta = self.LAST_FIVE_YEAR
        else:
            # デフォルトは1年とする
            dt_delta = self.LAST_ONE_YEAR

        limit_time = dt_now - dt_delta

        return limit_time
