# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from module.commander import Commander

SEARCH_LIMIT_LIST = ['1日', '1週間', '1か月', '1年', '2年', '3年', '4年', '5年']


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui_dialog = self.load_ui()

        # 検索期間の選択項目の作成
        self.ui_dialog.search_span_box.addItems(SEARCH_LIMIT_LIST)

        # イベントハンドラ
        self.ui_dialog.browse_button.clicked.connect(self.browse_dir)
        self.ui_dialog.run_button.clicked.connect(self.run)

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

    def browse_dir(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, 'ファイル保存先を選択')
        self.ui_dialog.path_display.setText(self.dir_path)

    def run(self):
        cd = Commander()
        cd.get_params(
            self.dir_path,
            self.ui_dialog.search_span_box.currentText())
        cd.run()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
