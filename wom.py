import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QFileDialog,
                           QMessageBox, QLineEdit, QGroupBox, QFormLayout,
                           QTabWidget, QComboBox, QCheckBox, QSpinBox, QDesktopWidget)
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt, QSettings

class WindowsOEMEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_logo = None
        self.username = os.getenv('USERNAME', 'Unknown User')
        self.settings = QSettings('WOM', 'WindowsOEMEditor')
        self.current_language = self.settings.value('language', 'tr')
        self.init_translations()
        self.check_windows_compatibility()
        self.init_ui()
        self.load_current_oem_info()

    def init_translations(self):
        self.translations = {
          
        
        # Update form labels
        self.oem_form.labelForField(self.logo_widget).setText("OEM Logo:")
        self.logo_settings_layout.labelForField(self.logo_size).setText(self.tr('logo_size'))
        self.logo_settings_layout.labelForField(self.logo_position).setText(self.tr('logo_position'))
        
        # Update logo position combo
        current_pos = self.logo_position.currentIndex()
        self.logo_position.blockSignals(True)
        self.logo_position.clear()
        self.logo_position.addItems([self.tr('top_left'), self.tr('top_right'), 
                                   self.tr('bottom_left'), self.tr('bottom_right'), 
                                   self.tr('center')])
        self.logo_position.setCurrentIndex(current_pos)
        self.logo_position.blockSignals(False)
        
        # Update OEM form labels
        self.oem_form.labelForField(self.manufacturer).setText(self.tr('manufacturer'))
        self.oem_form.labelForField(self.model).setText(self.tr('model'))
        self.oem_form.labelForField(self.support_hours).setText(self.tr('support_hours'))
        self.oem_form.labelForField(self.support_url).setText(self.tr('support_url'))
        self.oem_form.labelForField(self.support_phone).setText(self.tr('support_phone'))
        
        # Update Windows tab
        self.windows_group.setTitle(self.tr('windows_settings'))
        self.windows_form.labelForField(self.windows_version).setText(self.tr('windows_version'))
        self.windows_form.labelForField(self.product_key).setText(self.tr('product_key'))
        self.windows_form.labelForField(self.organization).setText(self.tr('organization'))
        self.windows_form.labelForField(self.owner).setText(self.tr('owner'))
        
        # Update checkboxes
        self.auto_activate.setText(self.tr('auto_activate'))
        self.skip_eula.setText(self.tr('skip_eula'))
        self.auto_updates.setText(self.tr('auto_updates'))
        
        # Update drag drop label
        if not self.logo_preview.pixmap():
            self.logo_preview.setText(self.tr('logo_drag_text'))
        
        # Update about tab
        self.update_about_text()

    def update_about_text(self):
        username = self.username if self.current_language == 'tr' else self.username
        if self.current_language == 'tr' and self.username == 'Unknown User':
            username = self.tr('unknown_user')
        
        about_text = f"""
        <div style='text-align: center; font-family: "Segoe UI", sans-serif;'>
            <img src='WOM.png' width='64' height='64' style='margin: 10px;'>
            <h1 style='color: #0078D4; margin: 10px 0; font-size: 24px; font-weight: bold;'>{self.tr('window_title')}</h1>
            <p style='color: #d4d4d4; font-size: 16px; margin: 15px 0;'>{self.tr('description')}</p>
            <p style='color: #0078D4; font-size: 14px; margin: 10px 0;'>{self.tr('version')}</p>
            
            <div style='background-color: #2d2d2d; padding: 15px; margin: 20px 0; border-radius: 8px;'>
                <p style='color: #d4d4d4; margin: 10px 0;'>{self.tr('app_description')}</p>
            </div>

            <div style='text-align: left; margin: 20px 40px;'>
                <h2 style='color: #0078D4; font-size: 18px; margin: 10px 0;'>{self.tr('features')}</h2>
                <ul style='color: #d4d4d4; list-style-type: none; padding: 0;'>
                    <li style='margin: 8px 0;'>{self.tr('feature_logo')}</li>
                    <li style='margin: 8px 0;'>{self.tr('feature_manufacturer')}</li>
                    <li style='margin: 8px 0;'>{self.tr('feature_support')}</li>
                    <li style='margin: 8px 0;'>{self.tr('feature_activation')}</li>
                    <li style='margin: 8px 0;'>{self.tr('feature_config')}</li>
                </ul>
            </div>

            <div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid #3e3e42;'>
                <p style='color: #888888; font-size: 12px; margin-top: 15px;'>{self.tr('copyright')}</p>
                <p style='color: #ff0000; font-size: 14px; margin-top: 20px; font-weight: bold; text-align: center;'>{self.tr('license').format(username)}</p>
            </div>
        </div>
        """
        
        self.about_label.setText(about_text)

    def check_windows_compatibility(self):
        try:
            import ctypes
            import winreg

            # Windows sürüm kontrolü
            win_ver = sys.getwindowsversion()
            if win_ver.major < 6:  # XP ve öncesi
                self.legacy_mode = True
                self.use_bmp_only = True
            else:
                self.legacy_mode = False
                self.use_bmp_only = win_ver.major == 6 and win_ver.minor == 0  # Vista

            # Yönetici hakları kontrolü
            if not ctypes.windll.shell32.IsUserAnAdmin():
                QMessageBox.warning(
                    self,
                    self.tr('admin_required'),
                    self.tr('admin_warning')
                )


                    )
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr('system_check_error'),
                self.tr('system_check_message').format(str(e))
            )

    def init_ui(self):
        # Ana pencere ayarları
        self.setWindowTitle(self.tr('window_title'))
        self.resize(500, 650)  # Pencere boyutu
        
        # Ekranın merkezinde konumlandırma
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
        
        # Pencere ikonu ayarla
        app_icon = QIcon("WOM.png")
        self.setWindowIcon(app_icon)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QGroupBox {
                border: 1px solid #3b3b3b;
                margin-top: 1em;
                padding-top: 0.5em;
            }
            QGroupBox::title {
                color: #ffffff;
            }
            QPushButton {
                background-color: #404040;
                border: 1px solid #505050;
                padding: 5px 15px;
                color: white;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: #333333;
                border: 1px solid #505050;
                color: white;
                padding: 3px;
            }
            QTabWidget::pane {
                border: 1px solid #505050;
            }
            QTabBar::tab {
                background-color: #333333;
                color: white;
                padding: 8px 20px;
            }
            QTabBar::tab:selected {
                background-color: #404040;
            }
        """)
        

        header_container.addWidget(language_widget)
        
        layout.addLayout(header_container)

        # Tab widget oluşturma
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # OEM Bilgileri Sekmesi
        oem_tab = QWidget()
        oem_layout = QFormLayout()
        
        # OEM Bilgileri Grubu
        self.oem_group = QGroupBox(self.tr('oem_info'))
        self.oem_form = QFormLayout()
        
        # Logo seçimi
        logo_widget = QWidget()
        logo_layout = QHBoxLayout(logo_widget)
        
        # Özelleştirilmiş logo önizleme widget'ı
        class DragDropLabel(QLabel):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setAcceptDrops(True)
                self.default_style = "border: 1px solid #505050; background-color: #1b1b1b; color: #666666; font-style: italic;"
                self.hover_style = "border: 2px dashed #0078D4; background-color: #1b1b1b; color: #0078D4;"
                self.setStyleSheet(self.default_style)
                # Ana pencereyi bul ve çeviri metnini ayarla
                main_window = parent
                while main_window and not isinstance(main_window, WindowsOEMEditor):
                    main_window = main_window.parent()
                if main_window:
                    self.setText(main_window.tr('logo_drag_text'))
                else:
                    self.setText("Logo buraya sürüklenebilir\n(veya tıklayarak seçin)")
                self.setWordWrap(True)
                self.setAlignment(Qt.AlignCenter)
                self.main_window = main_window

            def mousePressEvent(self, event):
                if event.button() == Qt.LeftButton:
                    # Ana pencereye referansı bul
                    parent = self.parent()
                    while parent and not isinstance(parent, WindowsOEMEditor):
                        parent = parent.parent()
                    if parent:
                        parent.browse_logo()

            def dragEnterEvent(self, event):
                if event.mimeData().hasUrls():
                    url = event.mimeData().urls()[0]
                    if url.isLocalFile():
                        file_path = url.toLocalFile().lower()
                        if file_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                            event.acceptProposedAction()
                            self.setStyleSheet(self.hover_style)
                            return
                event.ignore()

            def dragLeaveEvent(self, event):
                self.setStyleSheet(self.default_style)

            def dropEvent(self, event):
                self.setStyleSheet(self.default_style)
                if event.mimeData().hasUrls():
                    file_path = event.mimeData().urls()[0].toLocalFile()
                    # Ana pencereye referansı bul
                    parent = self.parent()
                    while parent and not isinstance(parent, WindowsOEMEditor):
                        parent = parent.parent()
                    if parent:
                        parent.browse_logo(file_path)
                    event.acceptProposedAction()
                else:
                    event.ignore()

        self.logo_preview = DragDropLabel()
        self.logo_preview.setFixedSize(120, 60)  # Daha küçük logo önizleme
        self.logo_preview.setStyleSheet("border: 1px solid #505050; background-color: #1b1b1b;")
        self.logo_preview.setAlignment(Qt.AlignCenter)
        
        logo_buttons = QVBoxLayout()
        self.browse_logo_btn = QPushButton(self.tr('select_logo'))
        self.browse_logo_btn.clicked.connect(self.browse_logo)
        self.remove_logo_btn = QPushButton(self.tr('remove_logo'))
        self.remove_logo_btn.clicked.connect(self.remove_logo)
        
        logo_buttons.addWidget(self.browse_logo_btn)
        logo_buttons.addWidget(self.remove_logo_btn)
        logo_buttons.addStretch()
        
        logo_layout.addWidget(self.logo_preview)
        logo_layout.addLayout(logo_buttons)
        
        self.logo_widget = logo_widget
        self.oem_form.addRow("OEM Logo:", logo_widget)
        
        # Logo ayarları
        self.logo_settings = QGroupBox(self.tr('logo_settings'))
        self.logo_settings_layout = QFormLayout(self.logo_settings)
        
        self.logo_size = QSpinBox()
        self.logo_size.setRange(16, 512)
        self.logo_size.setValue(96)
        self.logo_size.setSuffix(" px")
        
        self.logo_position = QComboBox()
        self.logo_position.addItems([self.tr('top_left'), self.tr('top_right'), 
                                   self.tr('bottom_left'), self.tr('bottom_right'), 
                                   self.tr('center')])
        
        self.logo_settings_layout.addRow(self.tr('logo_size'), self.logo_size)
        self.logo_settings_layout.addRow(self.tr('logo_position'), self.logo_position)
        
        self.oem_form.addRow(self.logo_settings)
        
        # Diğer OEM bilgileri
        self.manufacturer = QLineEdit()
        self.model = QLineEdit()
        self.support_hours = QLineEdit()
        self.support_url = QLineEdit()
        self.support_phone = QLineEdit()
        
        self.oem_form.addRow(self.tr('manufacturer'), self.manufacturer)
        self.oem_form.addRow(self.tr('model'), self.model)
        self.oem_form.addRow(self.tr('support_hours'), self.support_hours)
        self.oem_form.addRow(self.tr('support_url'), self.support_url)
        self.oem_form.addRow(self.tr('support_phone'), self.support_phone)
        
        self.oem_group.setLayout(self.oem_form)
        oem_layout.addWidget(self.oem_group)
        oem_tab.setLayout(oem_layout)
        
        # Windows Özelleştirme Sekmesi
        windows_tab = QWidget()
        windows_layout = QVBoxLayout()
        
        # Windows Ayarları Grubu
        self.windows_group = QGroupBox(self.tr('windows_settings'))
        self.windows_form = QFormLayout()
        
        self.windows_version = QComboBox()
        self.windows_version.addItems(["Windows 11", "Windows 10", "Windows 8.1", "Windows 8"])
        
        self.product_key = QLineEdit()
        self.organization = QLineEdit()
        self.owner = QLineEdit()
        
        self.auto_activate = QCheckBox(self.tr('auto_activate'))
        self.skip_eula = QCheckBox(self.tr('skip_eula'))
        self.auto_updates = QCheckBox(self.tr('auto_updates'))
        
        self.windows_form.addRow(self.tr('windows_version'), self.windows_version)
        self.windows_form.addRow(self.tr('product_key'), self.product_key)
        self.windows_form.addRow(self.tr('organization'), self.organization)
        self.windows_form.addRow(self.tr('owner'), self.owner)
        self.windows_form.addRow(self.auto_activate)
        self.windows_form.addRow(self.skip_eula)
        self.windows_form.addRow(self.auto_updates)
        
        self.windows_group.setLayout(self.windows_form)
        windows_layout.addWidget(self.windows_group)
        windows_tab.setLayout(windows_layout)
        


        # Hakkında Sekmesi
        about_tab = QWidget()
        about_layout = QVBoxLayout()
        
        self.about_label = QLabel()
        self.about_label.setTextFormat(Qt.RichText)
        self.about_label.setOpenExternalLinks(True)
        self.about_label.setStyleSheet("background-color: #1e1e1e; padding: 20px; border-radius: 10px;")
        self.about_label.setWordWrap(True)
        self.update_about_text()
        
        about_layout.addWidget(self.about_label)
        about_layout.addStretch()
        about_tab.setLayout(about_layout)

        # Sekmeleri ekleme
        self.tabs.addTab(oem_tab, self.tr('oem_info'))
        self.tabs.addTab(windows_tab, self.tr('windows_settings'))
        self.tabs.addTab(about_tab, self.tr('about'))

        # Alt butonlar
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton(self.tr('export'))
        self.save_button.clicked.connect(self.save_config)
        
        self.build_button = QPushButton(self.tr('apply_oem'))
        self.build_button.clicked.connect(self.build_image)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.build_button)
        
        layout.addLayout(button_layout)


            )
        
        if fname:
            try:
                # Logo boyut kontrolü
                image_size = os.path.getsize(fname)
                if image_size > 1024 * 1024:  # 1MB üzeri
                    result = QMessageBox.question(
                        self,
                        self.tr('large_file_warning'),
                        self.tr('large_file_message'),
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if result == QMessageBox.No:
                        return

                # Logo yükle ve önizleme göster
                pixmap = QPixmap(fname)
                
                # Görüntü formatı kontrolü
                if hasattr(self, 'use_bmp_only') and self.use_bmp_only and not fname.lower().endswith('.bmp'):
                    # BMP'ye dönüştür
                    temp_bmp = os.path.join(os.path.dirname(fname), "temp_logo.bmp")
                    pixmap.save(temp_bmp, "BMP")
                    fname = temp_bmp
                
                # Boyut kontrolü ve ölçekleme
                if pixmap.width() > 512 or pixmap.height() > 512:
                    pixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                scaled_preview = pixmap.scaled(
                    self.logo_preview.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.logo_preview.setPixmap(scaled_preview)
                self.current_logo = fname
            except Exception as e:
                QMessageBox.critical(
                    self,
                    self.tr('logo_load_error'),
                    self.tr('logo_load_message').format(str(e))
                )

    def remove_logo(self):
        self.logo_preview.clear()
        self.logo_preview.setText(self.tr('no_logo'))
        self.current_logo = None




                self,
                self.tr('save_config'),
                "",
                file_filter
            )
            if fname:
                import json
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=4)
                QMessageBox.information(self, self.tr('success'), self.tr('config_saved'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('error'), self.tr('config_save_error').format(str(e)))

    def load_current_oem_info(self):
        try:
            import winreg
            
            # Windows sürümünü algıla
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0, winreg.KEY_READ)
                try:
                    product_name = winreg.QueryValueEx(key, "ProductName")[0]
                    current_build = int(winreg.QueryValueEx(key, "CurrentBuildNumber")[0])
                    
                    # Windows 11 build numarası 22000 ve üzeridir
                    if current_build >= 22000:
                        self.windows_version.setCurrentText("Windows 11")
                    elif "Windows 10" in product_name:
                        self.windows_version.setCurrentText("Windows 10")
                    elif "Windows 8.1" in product_name:
                        self.windows_version.setCurrentText("Windows 8.1")
                    elif "Windows 8" in product_name:
                        self.windows_version.setCurrentText("Windows 8")
                    elif "Windows 7" in product_name:
                        self.windows_version.setCurrentText("Windows 7")
                    elif "Windows Vista" in product_name:
                        self.windows_version.setCurrentText("Windows Vista")
                    elif "Windows XP" in product_name:
                        self.windows_version.setCurrentText("Windows XP")
                except:
                    pass
                
               
                except:
                    pass

                winreg.CloseKey(key)
            except:
                pass

            # OEM bilgilerini al
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\OEMInformation"
            try:
                oem_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
                
                # OEM bilgilerini oku
                try: self.manufacturer.setText(winreg.QueryValueEx(oem_key, "Manufacturer")[0])
                except: pass
                
                try: self.model.setText(winreg.QueryValueEx(oem_key, "Model")[0])
                except: pass
                
                try: self.support_hours.setText(winreg.QueryValueEx(oem_key, "SupportHours")[0])
                except: pass
                
                try: self.support_url.setText(winreg.QueryValueEx(oem_key, "SupportURL")[0])
                except: pass
                
                try: self.support_phone.setText(winreg.QueryValueEx(oem_key, "SupportPhone")[0])
                except: pass
                
                try:
                    logo_path = winreg.QueryValueEx(oem_key, "Logo")[0]
                    if logo_path and os.path.exists(logo_path):
                        pixmap = QPixmap(logo_path)
                        scaled_pixmap = pixmap.scaled(
                            self.logo_preview.size(),
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation
                        )
                        self.logo_preview.setPixmap(scaled_pixmap)
                        self.current_logo = logo_path
                except:
                    pass

                winreg.CloseKey(oem_key)
            except WindowsError:
                pass

            # Organizasyon bilgilerini al
           

        except Exception as e:
            print(f"Sistem bilgileri yüklenirken hata: {str(e)}")

    def build_image(self):
        try:
            import winreg
            import shutil
            import ctypes

            # Yönetici hakları kontrolü
            if not ctypes.windll.shell32.IsUserAnAdmin():
                QMessageBox.critical(
                    self,
                    self.tr('permission_error'),
                    self.tr('admin_required_message')
                )
                return

            # Windows sürümünü ve yolları belirle
            windows_version = self.windows_version.currentText()
            system_root = os.environ.get("SystemRoot")
            
            if not system_root:
                QMessageBox.critical(
                    self,
                    self.tr('system_error'),
                    self.tr('system_dir_not_found')
                )
                return
            

            # OEM dizinini oluştur
            os.makedirs(oem_path, exist_ok=True)

            # Logo işleme
            if self.current_logo:
                target_size = self.logo_size.value()
                logo = QPixmap(self.current_logo)
                scaled_logo = logo.scaled(
                    target_size, target_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                
                # Logo kaydet
                logo_path = os.path.join(oem_path, logo_name)
                scaled_logo.save(logo_path, logo_format)
                winreg.SetValueEx(oem_key, "Logo", 0, winreg.REG_SZ, logo_path)
            else:
                winreg.SetValueEx(oem_key, "Logo", 0, winreg.REG_SZ, "")

   

            # Registry anahtarını kapat
            winreg.CloseKey(oem_key)

            # Başarı mesajı
            logo_location = oem_path if self.current_logo else self.tr('no_logo_text')
            QMessageBox.information(
                self, 
                self.tr('success'),
                self.tr('oem_success').format(self.manufacturer.text(), self.model.text(), logo_location)
            )

        except Exception as e:
            if "access is denied" in str(e).lower():
                QMessageBox.critical(
                    self, 
                    self.tr('error'),
                    self.tr('admin_permission_required')
                )
            else:
                QMessageBox.critical(self, self.tr('error'), self.tr('oem_update_error').format(str(e)))



def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Uygulama ikonu ayarla
    app_icon = QIcon("WOM.png")
    app.setWindowIcon(app_icon)
    
    palette = app.palette()
    palette.setColor(palette.Window, QColor(53, 53, 53))
    palette.setColor(palette.WindowText, Qt.white)
    palette.setColor(palette.Base, QColor(25, 25, 25))
    palette.setColor(palette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(palette.ToolTipBase, Qt.white)
    palette.setColor(palette.ToolTipText, Qt.white)
    palette.setColor(palette.Text, Qt.white)
    palette.setColor(palette.Button, QColor(53, 53, 53))
    palette.setColor(palette.ButtonText, Qt.white)
    palette.setColor(palette.BrightText, Qt.red)
    palette.setColor(palette.Link, QColor(42, 130, 218))
    palette.setColor(palette.Highlight, QColor(42, 130, 218))
    palette.setColor(palette.HighlightedText, Qt.black)
    app.setPalette(palette)
    editor = WindowsOEMEditor()
    editor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
