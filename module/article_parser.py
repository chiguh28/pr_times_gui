from bs4 import BeautifulSoup
import requests
import re


MAIL_ADDRESS_PATTERN = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+'
END_INDEX = -1


class ArticleParser():
    def __init__(self) -> None:
        self.mailing_list = []
        self.company_list = []

    def update_soup(self, url):
        """soupをURLが更新されるたびに更新する

        Args:
            url ([type]): 記事URL
        """
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, "html.parser")

    def __get_company(self):
        """会社名取得

        Returns:
            str: 会社名
        """
        soup = self.soup
        company_block = soup.select_one(
            "#main > div.content > article > div > header > div.information-release > div > a")
        if company_block:
            company = company_block.text
        else:
            company = None
        return company

    def __get_mail_address(self):
        """メールアドレスを取得する

        Returns:
            mail_address: str
        Notes:
            メールアドレスを正規表現を用いて取得する
            ① サイトのテキストからメールアドレス表記のテキストを取得(終端のメールアドレス)
            ② 取得したテキストにはメールアドレス表記以外も含まれているのでメールアドレスのみを抽出
        """
        soup = self.soup

        # メールアドレスが書かれているテキストを全て抽出する
        # 必要なアドレスは最後のアドレスだけだが、抽出方法が無いため全て抽出してリストの終端を取得する流れにする
        mail_text_list = soup.find_all(text=re.compile(MAIL_ADDRESS_PATTERN))

        # メールアドレスに該当するテキストが存在した場合は抽出するが、存在しない場合はNoneにする
        if len(mail_text_list) > 0:
            # メールアドレスの終端を取得
            mail_text = str(mail_text_list[END_INDEX])
            mail_address = re.findall(
                MAIL_ADDRESS_PATTERN,
                mail_text)[END_INDEX]
        else:
            mail_address = None

        return mail_address

    def create_mailing_list(self):
        """メーリングリストを作成
            Notes:
                会社名とメールアドレスをリストに追加していく
        """
        company = self.__get_company()
        mail_address = self.__get_mail_address()

        # 会社名とメールアドレスが存在した場合にリストに追加する
        if company is not None and mail_address is not None:

            # リスト内で重複があればリストには追加しない(例外)
            if mail_address in self.mailing_list or company in self.company_list:
                pass
            else:
                self.mailing_list.append(mail_address)
                self.company_list.append(company)

    def getter_company_list(self):
        """会社名リストを渡す

        Returns:
            [list]: 会社名リスト
        """
        return self.company_list

    def getter_mailing_list(self):
        """メーリングリストを渡す

        Returns:
            list: メーリングリスト
        """
        return self.mailing_list
