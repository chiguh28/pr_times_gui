from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time


class DriverFactory():
    def __init__(self, url) -> None:
        """初期化メソッド

        Args:
            url (str): PR TimesのURL
        """
        # chromedriverの設定
        options = Options()
        options.add_argument('--headless')

        # URLのページを立ち上げる
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
        self.driver.get(url)

    def create(self, keyword):
        """検索ページを作成

        Args:
            keyword (str): PR Timesで検索するキーワード

        Returns:
            driver: 検索検索ページ状態のwebdriver
        """
        time.sleep(3)
        # 検索欄をクリックする
        self.driver.find_element_by_css_selector(
            "input.header-search__input.js-release-search-input").click()
        # 検索バーにキーワードを入れ、クリックする
        search_box = self.driver.find_element_by_css_selector(
            "input.header-search__input.js-release-search-input")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)

        return self.driver
