"""Diem khoi dong ung dung desktop."""
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import sys
import tempfile
from app.knowledge import ROOT, load_knowledge


def configure_logging():
    candidates = [
        ROOT / 'logs',
        Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'MekongExpert' / 'logs',
        Path(tempfile.gettempdir()) / 'MekongExpert' / 'logs',
    ]
    failures = []
    for directory in candidates:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            path = directory / 'app.log'
            handler = RotatingFileHandler(path, maxBytes=2_000_000, backupCount=3, encoding='utf-8')
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(levelname)s %(name)s: %(message)s',
                handlers=[handler, logging.StreamHandler()],
                force=True,
            )
            for failure in failures:
                logging.warning(failure)
            logging.info('Nhật ký: %s', path)
            return path
        except OSError as exc:
            failures.append(f'Không ghi được log tại {directory}: {exc}')
    logging.basicConfig(level=logging.INFO, force=True)
    raise OSError('Không tạo được tệp log.\n' + '\n'.join(failures))


def main():
    try:
        log_path = configure_logging()
    except OSError as exc:
        print(exc, file=sys.stderr)
        return 1
    try:
        from PyQt6.QtWidgets import QApplication, QMessageBox
        from app.main_window import MainWindow
    except ImportError:
        logging.exception('Thiếu PyQt6 hoặc thư viện Qt. Hãy cài requirements.txt.')
        print(f'Không nạp được Qt. Xem {log_path}', file=sys.stderr)
        return 1
    application = QApplication(sys.argv)

    def report_unhandled(exc_type, exc_value, traceback):
        logging.critical('Lỗi chưa xử lý', exc_info=(exc_type, exc_value, traceback))
        QMessageBox.critical(None, 'Lỗi ứng dụng', f'Có lỗi trong ứng dụng. Chi tiết: {log_path}')
    sys.excepthook = report_unhandled
    try:
        events, destinations, rules, warnings = load_knowledge()
        for warning in warnings:
            logging.warning(warning)
        window = MainWindow(events, destinations, rules)
        window.setToolTip(f'Tệp log: {log_path}')
        window.show()
    except Exception:
        logging.exception('Khởi động thất bại')
        QMessageBox.critical(
            None,
            'Không thể khởi động',
            f'Không đọc được dữ liệu hoặc giao diện.\nChi tiết: {log_path}',
        )
        return 1
    return application.exec()


if __name__ == '__main__':
    sys.exit(main())
