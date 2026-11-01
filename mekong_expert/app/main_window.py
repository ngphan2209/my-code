"""Nap UI Designer, lay lua chon va hien thi ket qua."""
import logging
from PyQt6 import uic
from PyQt6.QtCore import QEvent, QSize, Qt, QUrl
from PyQt6.QtGui import QBrush, QPalette, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QListWidgetItem,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
try:
    from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
    from PyQt6.QtMultimediaWidgets import QVideoWidget
except ImportError:
    QMediaPlayer = None
from app.knowledge import ROOT, GROUPS, GROUP_LABELS
from app.inference import infer, NO_RESULT

logger = logging.getLogger(__name__)


class LandscapeVideoFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.setMinimumSize(200, 112)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return round(width * 9 / 16)

    def sizeHint(self):
        return QSize(640, 360)


class MainWindow(QMainWindow):
    def __init__(self, events, destinations, rules):
        super().__init__()
        uic.loadUi(str(ROOT / 'ui/main.ui'), self)
        self.events = events
        self.event_map = {event['code']: event for event in events}
        self.destinations = {place['code']: place for place in destinations}
        self.rules = rules
        self.rule_map = {rule['id']: rule for rule in rules}
        self.results = {}
        self.photo = QPixmap()
        self.player = None
        self.backgrounds = {}
        self.combos = dict(zip(
            GROUPS,
            [
                self.tinhthanh_cb,
                self.khoangcach_cb,
                self.ngansach_cb,
                self.trainghiem_cb,
                self.loaihinh_cb,
                self.nhomdi_cb,
                self.thoigian_cb,
            ],
        ))
        for group, combo in self.combos.items():
            combo.addItem('— Chọn ' + GROUP_LABELS[group].lower() + ' —', None)
            for event in events:
                if event['group'] == group:
                    combo.addItem(event['label'], event['code'])
                    combo.setItemData(combo.count() - 1, event['label'], Qt.ItemDataRole.ToolTipRole)
            combo.currentIndexChanged.connect(self.selection_changed)
        self.start_btt.clicked.connect(lambda: self.pages.setCurrentWidget(self.consult_page))
        self.quaylai_btt.clicked.connect(lambda: self.pages.setCurrentWidget(self.home_page))
        self.guide_btt.clicked.connect(self.show_guide)
        self.exit_btt.clicked.connect(self.close)
        self.tuvan_btt.clicked.connect(self.consult)
        self.xoa_btt.clicked.connect(self.reset)
        self.ketqua_list.currentItemChanged.connect(self.show_destination)
        self.hinhanh_lb.installEventFilter(self)
        for page, filename in [(self.home_page, 'home.png'), (self.consult_page, 'consult.png')]:
            pixmap = QPixmap(str(ROOT / 'assets/backgrounds' / filename))
            if pixmap.isNull():
                logger.warning('Thiếu hoặc không đọc được nền %s; dùng nền màu.', filename)
            self.backgrounds[page] = pixmap
            page.setAutoFillBackground(True)
            page.installEventFilter(self)
            self.update_background(page)
        self.setup_video()
        self.mainSplitter.setSizes([350, 800])
        self.resultSplitter.setSizes([280, 420])
        self.clear_results()

    def show_guide(self):
        QMessageBox.information(self, 'Hướng dẫn',
            '1. Bấm Bắt đầu tư vấn.\n2. Chọn đủ bảy tiêu chí.\n'
            '3. Bấm Tư vấn để xem tất cả địa điểm khớp hoàn toàn.\n'
            '4. Chọn địa điểm để xem ảnh, mô tả và thẻ Lý do đề xuất & luật.\n'
            '5. Bấm Xóa lựa chọn để bắt đầu lại.\n\n'
            'Không có kết quả nghĩa là tập luật chưa có tổ hợp bạn chọn. '
            'Ứng dụng không suy luận gần đúng. Dữ liệu chưa được xác minh thực tế.')

    def clear_results(self):
        self.results = {}
        self.ketqua_list.clear()
        self.photo = QPixmap()
        self.hinhanh_lb.clear()
        self.hinhanh_lb.setText('Chưa có ảnh địa điểm')
        self.mota_text.clear()
        self.giaithich_text.clear()
        self.clear_video()

    def selection_changed(self):
        self.clear_results()
        self.status_lb.setText('Lựa chọn đã thay đổi. Chọn đủ bảy tiêu chí và bấm Tư vấn.')

    def reset(self):
        for combo in self.combos.values():
            combo.setCurrentIndex(0)
        self.clear_results()
        self.status_lb.setText('Đã xóa. Chọn đủ bảy tiêu chí để tư vấn lại.')

    def consult(self):
        self.clear_results()
        facts = [combo.currentData() for combo in self.combos.values()]
        if any(code is None for code in facts):
            self.status_lb.setText('Vui lòng chọn đầy đủ bảy tiêu chí.')
            QMessageBox.warning(self, 'Thiếu lựa chọn', 'Vui lòng chọn đầy đủ bảy tiêu chí.')
            return
        try:
            matches = infer(facts, self.rules, self.events)
            self.results = {match['code']: match for match in matches}
            for match in matches:
                code = match['code']
                item = QListWidgetItem(code + ' · ' + self.destinations[code]['name'])
                item.setData(Qt.ItemDataRole.UserRole, code)
                self.ketqua_list.addItem(item)
            if matches:
                self.status_lb.setText(f'Có {len(matches)} địa điểm khớp hoàn toàn trong cơ sở tri thức.')
                self.ketqua_list.setCurrentRow(0)
            else:
                self.status_lb.setText(NO_RESULT)
        except Exception:
            logger.exception('Lỗi khi tư vấn với các mã %s', facts)
            self.clear_results()
            self.status_lb.setText('Không thể xử lý. Xem tệp log để biết chi tiết.')
            QMessageBox.critical(self, 'Lỗi xử lý', 'Không thể tư vấn. Vui lòng xem tệp log của ứng dụng.')

    def show_destination(self, current, previous=None):
        if current is None:
            return
        code = current.data(Qt.ItemDataRole.UserRole)
        place = self.destinations[code]
        self.mota_text.setPlainText(place['name'] + '\n\n' + place['description'])
        lines = ['Địa điểm khớp đầy đủ bảy lựa chọn theo các luật: ' +
                 ', '.join(str(rid) for rid in self.results[code]['rule_ids']) + '.', '']
        for rid in self.results[code]['rule_ids']:
            rule = self.rule_map[rid]
            lines.append(f'Luật {rid}: ' + ' ∧ '.join(rule['conditions']) + ' → ' + code)
            for fact in rule['conditions']:
                event = self.event_map[fact]
                lines.append(f"• {GROUP_LABELS[event['group']]}: {event['label']} ({fact})")
            lines.append('')
        lines.append('Giải thích được sinh từ mã của biểu thức. Đây là quy ước kỹ thuật; '
                     'chưa phải xác minh dữ liệu du lịch thực tế. Xem reports/knowledge_audit.md.')
        self.giaithich_text.setPlainText('\n'.join(lines))
        self.photo = QPixmap(str(ROOT / place['image']))
        if self.photo.isNull():
            logger.warning('Thiếu hoặc không đọc được ảnh %s: %s', code, place['image'])
        self.update_photo()
        self.load_video(place)

    def setup_video(self):
        self.player = None
        if QMediaPlayer is None:
            logger.warning('Không nạp được PyQt6.QtMultimedia; tab Video bị tắt.')
            self.video_status_lb.setText('Máy này chưa có thành phần phát video của Qt.')
            self.video_play_btt.setEnabled(False)
            self.video_stop_btt.setEnabled(False)
            return

        layout = self.videoTab.layout()
        self.video_tab_layout = layout
        index = layout.indexOf(self.video_host)
        layout.removeWidget(self.video_host)
        self.video_host.deleteLater()
        self.video_host = LandscapeVideoFrame(self.videoTab)
        self.video_host.setObjectName('video_host')
        self.video_host.setStyleSheet('background-color: #101714; border-radius: 8px;')
        layout.insertWidget(index, self.video_host)
        layout.setAlignment(self.video_host, Qt.AlignmentFlag.AlignHCenter)
        self.videoTab.installEventFilter(self)

        self.video_host_layout = QVBoxLayout(self.video_host)
        self.video_host_layout.setContentsMargins(0, 0, 0, 0)
        self.video_widget = QVideoWidget(self.video_host)
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.video_host_layout.addWidget(self.video_widget)
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)
        self.player.errorOccurred.connect(self.video_error)
        self.video_play_btt.clicked.connect(self.toggle_video)
        self.video_stop_btt.clicked.connect(self.player.stop)
        self.player.playbackStateChanged.connect(self.update_video_button)
        self.detailTabs.currentChanged.connect(self.tab_changed)
        self.update_video_frame()
        self.clear_video()

    def update_video_frame(self):
        layout = self.video_tab_layout
        margins = layout.contentsMargins()
        button_layout = layout.itemAt(layout.count() - 1).layout()
        available_height = (
            self.videoTab.height()
            - margins.top()
            - margins.bottom()
            - self.video_status_lb.sizeHint().height()
            - button_layout.sizeHint().height()
            - 2 * layout.spacing()
        )
        available_width = self.videoTab.width() - margins.left() - margins.right()
        height = max(112, min(360, available_height, round(available_width * 9 / 16)))
        width = round(height * 16 / 9)
        self.video_host.setFixedSize(width, height)

    def clear_video(self):
        if self.player is None:
            return
        self.player.stop()
        self.player.setSource(QUrl())
        self.video_status_lb.setText('Chưa có video cho địa điểm này.')
        self.video_play_btt.setEnabled(False)
        self.video_stop_btt.setEnabled(False)

    def load_video(self, place):
        if self.player is None:
            return
        self.clear_video()
        relative = place.get('video')
        if not relative:
            return
        path = ROOT / relative
        if not path.is_file():
            logger.warning('Thiếu video %s: %s', place['code'], relative)
            self.video_status_lb.setText('Không tìm thấy tệp video của địa điểm này.')
            return
        self.player.setSource(QUrl.fromLocalFile(str(path)))
        self.video_status_lb.setText('Video giới thiệu: ' + place['name'])
        self.video_play_btt.setEnabled(True)
        self.video_stop_btt.setEnabled(True)

    def toggle_video(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def update_video_button(self, state):
        playing = state == QMediaPlayer.PlaybackState.PlayingState
        self.video_play_btt.setText('Tạm dừng' if playing else 'Phát')

    def tab_changed(self, index):
        if self.detailTabs.widget(index) is not self.videoTab:
            self.player.pause()

    def video_error(self, error, message):
        logger.error('Lỗi phát video: %s %s', error, message)
        self.video_status_lb.setText('Không phát được video. Xem tệp log để biết chi tiết.')

    def closeEvent(self, event):
        if self.player is not None:
            self.player.stop()
        super().closeEvent(event)

    def update_photo(self):
        if self.photo.isNull():
            self.hinhanh_lb.clear()
            self.hinhanh_lb.setText('Chưa có ảnh địa điểm')
        else:
            self.hinhanh_lb.setPixmap(self.photo.scaled(self.hinhanh_lb.size(),
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def update_background(self, page):
        pixmap = self.backgrounds[page]
        palette = page.palette()
        if not pixmap.isNull():
            scaled = pixmap.scaled(page.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                   Qt.TransformationMode.SmoothTransformation)
            scaled = scaled.copy((scaled.width()-page.width())//2, (scaled.height()-page.height())//2,
                                 page.width(), page.height())
            palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled))
        else:
            from PyQt6.QtGui import QColor
            palette.setColor(QPalette.ColorRole.Window, QColor('#f4f8f1'))
        page.setPalette(palette)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Resize:
            if watched == self.hinhanh_lb:
                self.update_photo()
            elif watched in self.backgrounds:
                self.update_background(watched)
            elif watched is self.videoTab and self.player is not None:
                self.update_video_frame()
        return super().eventFilter(watched, event)
