"""Kiem tra widget Qt thuc; co the chay headless bang QT_QPA_PLATFORM=offscreen."""
import unittest
from unittest.mock import patch
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox
from app.knowledge import ROOT, load_knowledge
from app.main_window import MainWindow
from app.inference import NO_RESULT


class GuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])
        cls.data = load_knowledge()

    def setUp(self):
        self.window = MainWindow(*self.data[:3])
        self.window.show()
        self.application.processEvents()

    def tearDown(self):
        self.window.close()
        self.application.processEvents()

    def choose(self, facts):
        for combo, code in zip(self.window.combos.values(), facts.split()):
            index = combo.findData(code)
            self.assertGreater(index, 0)
            combo.setCurrentIndex(index)

    def test_navigation_consult_select_clear_back(self):
        w = self.window
        self.assertEqual(w.pages.currentWidget(), w.home_page)
        w.start_btt.click()
        self.assertEqual(w.pages.currentWidget(), w.consult_page)
        self.choose('R3 K2 N2 V5 L7 DT5 TG2')
        w.tuvan_btt.click()
        self.assertEqual(w.ketqua_list.count(), 2)
        self.assertEqual(w.ketqua_list.currentRow(), 0)
        self.assertIn('Mỹ Xương', w.mota_text.toPlainText())
        self.assertIn('Luật 75:', w.giaithich_text.toPlainText())
        self.assertFalse(w.photo.isNull())
        w.ketqua_list.setCurrentRow(1)
        self.assertIn('Sa Đéc', w.mota_text.toPlainText())
        self.assertIn('Luật 87:', w.giaithich_text.toPlainText())
        expected = QPixmap(str(ROOT / self.data[1][5]['image']))
        self.assertEqual(w.photo.toImage(), expected.toImage())
        w.detailTabs.setCurrentIndex(1)
        w.xoa_btt.click()
        self.assertTrue(all(cb.currentData() is None for cb in w.combos.values()))
        self.assertEqual(w.ketqua_list.count(), 0)
        self.assertEqual(w.mota_text.toPlainText(), '')
        self.assertEqual(w.giaithich_text.toPlainText(), '')
        self.assertTrue(w.photo.isNull())
        w.quaylai_btt.click()
        self.assertEqual(w.pages.currentWidget(), w.home_page)

    def test_no_match_removes_previous_result(self):
        self.choose('R1 K1 N1 V1 L3 DT1 TG2')
        self.window.tuvan_btt.click()
        self.assertGreater(self.window.ketqua_list.count(), 0)
        self.choose('R6 K4 N4 V20 L1 DT6 TG4')
        self.window.tuvan_btt.click()
        self.assertEqual(self.window.status_lb.text(), NO_RESULT)
        self.assertEqual(self.window.ketqua_list.count(), 0)
        self.assertEqual(self.window.mota_text.toPlainText(), '')
        self.assertEqual(self.window.giaithich_text.toPlainText(), '')
        self.assertTrue(self.window.photo.isNull())

    def test_incomplete_input_and_guide(self):
        with patch.object(QMessageBox, 'warning') as warning:
            self.window.tuvan_btt.click()
            warning.assert_called_once()
        with patch.object(QMessageBox, 'information') as info:
            self.window.guide_btt.click()
            info.assert_called_once()

    def test_all_photos_and_backgrounds_readable(self):
        for place in self.data[1]:
            with self.subTest(place=place['code']):
                self.assertFalse(QPixmap(str(ROOT / place['image'])).isNull())
        self.assertTrue(all(not pix.isNull() for pix in self.window.backgrounds.values()))

    def test_resize_and_photo_ratio(self):
        w = self.window
        w.start_btt.click()
        self.choose('R1 K1 N1 V1 L3 DT1 TG2')
        w.tuvan_btt.click()
        for width, height in [(850, 600), (1200, 780), (1500, 900)]:
            w.resize(width, height)
            self.application.processEvents()
            self.assertTrue(w.tuvan_btt.isVisible())
            self.assertGreater(w.hinhanh_lb.width(), 0)
            pix = w.hinhanh_lb.pixmap()
            self.assertIsNotNone(pix)
            self.assertAlmostEqual(pix.width()/pix.height(), w.photo.width()/w.photo.height(), delta=0.025)
            self.assertLessEqual(pix.width(), w.hinhanh_lb.width())
            self.assertLessEqual(pix.height(), w.hinhanh_lb.height())

    def test_video_frame_stays_landscape(self):
        w = self.window
        if w.player is None:
            self.skipTest('PyQt6.QtMultimedia không khả dụng.')
        w.start_btt.click()
        w.detailTabs.setCurrentWidget(w.videoTab)
        for width, height in [(850, 600), (1200, 780), (1500, 900)]:
            w.resize(width, height)
            self.application.processEvents()
            frame = w.video_host
            self.assertGreater(frame.width(), 0)
            self.assertAlmostEqual(frame.width() / frame.height(), 16 / 9, delta=0.03)

    def test_missing_photo_placeholder(self):
        w = self.window
        w.destinations['T1'] = {**w.destinations['T1'], 'image': 'assets/destinations/not_found.jpg'}
        self.choose('R1 K1 N1 V1 L3 DT1 TG2')
        with self.assertLogs('app.main_window', level='WARNING'):
            w.tuvan_btt.click()
        self.assertTrue(w.photo.isNull())
        self.assertEqual(w.hinhanh_lb.text(), 'Chưa có ảnh địa điểm')


if __name__ == '__main__':
    unittest.main()
