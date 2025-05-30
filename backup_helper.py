from pathlib import Path
from keyring import errors
from keyring.backends import SecretService
from PyQt6.QtGui import QTextCursor, QColor, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QElapsedTimer, QTimer, QObject, QMutex, QMutexLocker, QCoreApplication, QUuid, QDateTime, QWaitCondition, QAbstractListModel, QModelIndex, QVariant
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QListWidgetItem, QListWidget, QTextEdit, QListView,
                             QMainWindow, QGraphicsDropShadowEffect, QDialog, QLabel, QProgressBar, QGridLayout, QScrollArea, QDialogButtonBox, QInputDialog,
                             QCheckBox, QTabWidget, QErrorMessage, QSpacerItem, QFileDialog, QComboBox, QLineEdit, QFormLayout, QSizePolicy, QColorDialog)
import ast, functools, getpass, json, keyring, os, psutil, pwd, re, secrets, shutil, socket, subprocess, sys, tempfile, threading, time, urllib.error, urllib.request

sys.setrecursionlimit(5000)
user = pwd.getpwuid(os.getuid()).pw_name
home_user = os.getenv("HOME")
home_config = Path(home_user).joinpath(".config")

global_style = """
QDialog, QWidget {
    background-color: #232534;
    border-radius: 16px;
    border: 1px solid #2d2d44;
}
QWidget {
    color: #c0caf5;
    font-family: "Noto Sans Mono";
    font-size: 16px;
}
QPushButton, QCheckBox {
    border-radius: 10px;
    outline: none;
    text-align: center;
    padding: 5px;
    font-size: 15px;
    font: bold;
    color: #ffffff;
}
QPushButton {
    border: 2px solid #7dcfff;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #24283b, stop:1 #414868);
}
QPushButton:enabled:hover, QPushButton:enabled:focus {
    border: 2px solid #ffff00;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a425f, stop:1 #606d9c);
    color: #55ffff;
}
QPushButton:disabled {
    border: 2px solid #444;
    color: #616161;
    background-color: #282828;
}
QCheckBox {
    background-color: transparent;
}
QCheckBox:enabled, QCheckBox:disabled {
    border: 2px solid transparent;
}
QCheckBox:enabled:hover, QCheckBox:enabled:focus {
    border: 2px solid #ffff00;
    color: #55ffff;
}
QCheckBox:disabled {
    color: #616161;
}
QCheckBox:indicator {
    width: 8px;
    height: 8px;
    border-radius: 4px;
}
QCheckBox:indicator:checked {
    border: 1px solid #55ff00;
    background-color: #55ff00;
}
QCheckBox:indicator:unchecked {
    border: 1px solid #f7768e;
    background-color: #f7768e;
}
QCheckBox:indicator:indeterminate {
    border: 1px solid #7aa2f7;
    background-color: transparent;
}
QLabel {
    color: #c0caf5;
    border: none;
    border-radius: 2px;
    padding: 5px;
    font-size: 17px;
    qproperty-alignment: 'AlignCenter';
    font-family: "CaskaydiaCove Nerd Font", "Noto Sans", sans-serif;
}
QWidget[class="container"] {
    background-color: #222;
    border-radius: 5px;
}
QLineEdit {
    background-color: #555582;
    color: #aaff00;
    padding: 5px 5px;
    border-radius: 8px;
    font-size: 16px;
}
QTextEdit, QListWidget {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #293147, stop:1 #4d5a83);
    color: #aaff00;
    border: none;
    padding: 5px 5px;
    border-radius: 8px;
    font-size: 16px;
    font-family: "FiraCode Nerd Font Mono", "Noto Sans", sans-serif;
}
QListWidget::item {
    padding: 5px;
    border-radius: 5px;
    border: 1px solid transparent;
}
QScrollBar:vertical {
    border: none;
    background: #2d2d44;
    width: 14px;
    margin: 15px 0;
}
QScrollBar::handle:vertical {
    background-color: #4f4f78;
    min-height: 30px;
    border-radius: 7px;
}
QScrollBar::handle:vertical:hover,
QScrollBar::handle:vertical:pressed {
    background-color: #9090dc;
}
QScrollBar::sub-line:vertical,
QScrollBar::add-line:vertical {
    border: none;
    background-color: #3b3b5a;
    height: 15px;
    border-radius: 7px;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    subcontrol-position: top;
}
QScrollBar::add-line:vertical {
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
    subcontrol-position: bottom;
}
QScrollBar::sub-line:vertical:hover,
QScrollBar::sub-line:vertical:pressed,
QScrollBar::add-line:vertical:hover {
    background-color: #00ddff;
}
QScrollBar::add-line:vertical:pressed {
    background-color: #b9005c;
}
QScrollBar::up-arrow:vertical,
QScrollBar::down-arrow:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}
QProgressBar {
    background-color: #6d7582;
    border-radius: 8px;
    border: 3px solid #7aa2f7;
    height: 25px;
    text-align: center;
    margin: 10px 0;
    font-weight: bold;
    font-size: 18px;
    color: #000000;
}
QProgressBar::chunk {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #7dcfff, stop:1 #6689cf);
    border-radius: 7px;
}
QTabBar::tab {
    background-color: #24283b;
    font-size: 16px;
    padding: 8px 12px;
    border: 1px solid #414868;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-family: "FiraCode Nerd Font Mono", "Noto Sans", sans-serif;
}
QTabBar::tab:selected {
    background-color: #1e1e2e;
    border-bottom: none;
}
"""

MAX_MOUNT_OPTIONS = 3
SESSIONS = ["GNOME", "KDE", "XFCE", "LXQt", "LXDE", "Cinnamon", "Mate", "Deepin", "Budgie", "Enlightenment",
                        "Hyprland", "sway", "i3", "bspwm", "openbox", "awesome", "herbstluftwm", "icewm", "fluxbox", "xmonad", "spectrwm", "qtile", "pekwm", "wmii", "dwm"]
USER_SHELL = ["Bash", "Fish", "Zsh", "Elvish", "Nushell", "Powershell", "Xonsh", "Ngs"]
PACKAGE_INSTALLER_OPERATION_TEXT = {"copy_system_files": "Copy 'System Files' (Using 'sudo cp'.)",
                                    "update_mirrors": "Mirror update<br>(Install 'reflector' and get the 10 fastest servers in your country, or worldwide if not detected.)",
                                    "set_user_shell": "Change shell for current user<br>(Install corresponding package for selected shell and change it for the current user.)",
                                    "update_system": "System update<br>(Using 'sudo pacman -Syu'. If 'yay' is present: using 'yay' instead.)",
                                    "install_kernel_header": "Check kernel version and install corresponding headers",
                                    "install_essential_packages": "Install 'Essential Packages' (Using 'sudo pacman -S'.)",
                                    "install_yay": "Install 'yay' (Necessary for 'Additional Packages'.)",
                                    "install_additional_packages": "Install 'Additional Packages' ('yay' needed.)",
                                    "install_specific_packages": "Install 'Specific Packages' for current session (Using 'sudo pacman -S'.)",
                                    "enable_printer_support": "Initialize printer support<br>(Install 'cups', 'ghostscript', 'system-config-printer', 'print-manager' and 'gutenprint'.<br>Enable && start 'cups.service'.)",
                                    "enable_samba_network_filesharing": "Initialize samba (Network filesharing via samba)<br>(Install 'gvfs-smb' and 'samba'. Enable && start 'smb.service'.)",
                                    "enable_bluetooth_service": "Initialize bluetooth<br>(Install 'bluez'. Enable && start 'bluetooth.service'.)",
                                    "enable_atd_service": "Initialize atd<br>(Install 'at'. Enable && start 'atd.service'.)",
                                    "enable_cronie_service": "Initialize cronie<br>(Install 'cronie'. Enable && start 'cronie.service'.)",
                                    "enable_firewall": "Initialize firewall<br>(Install 'ufw'. Enable && start 'ufw.service' and set to 'deny all by default'.)",
                                    "remove_orphaned_packages": "Remove orphaned package(s)",
                                    "clean_cache": "Clean cache (For 'pacman' and 'yay'.)"}


class DriveManager:
    def __init__(self):
        self.drives_to_unmount = []

    @staticmethod
    def is_drive_mounted(opt):
        try:
            output = subprocess.check_output(['mount'], text=True)
            name = opt.get('drive_name', '')
            paths = [f"/run/media/{user}/{name}", f"/media/{user}/{name}", f"/mnt/{name}", name]
            return any(p in output for p in paths)
        except Exception as e:
            print(f"Error checking mount: {e}")
            return False

    def check_path_requires_mounting(self, path):
        if not path:
            return None
        path = str(path)
        for opt in Options.mount_options:
            name = opt.get('drive_name', '')
            mount_paths = [f"/run/media/{user}/{name}", f"/media/{user}/{name}", f"/mnt/{name}", name]
            if any(p in path for p in mount_paths) and not self.is_drive_mounted(opt):
                return opt
        return None

    def check_drives_to_mount(self, paths_to_check):
        drives, seen = [], set()
        for path in filter(None, paths_to_check):
            for sub_path in (path if isinstance(path, list) else [path]):
                drive = self.check_path_requires_mounting(sub_path)
                if drive and id(drive) not in seen:
                    seen.add(id(drive))
                    drives.append(drive)
        return drives

    def mount_drive(self, drive, parent=None, remember_unmount=True):
        name, cmd = drive.get('drive_name', ''), drive.get('mount_command', '')
        if not cmd:
            return False
        try:
            print(f"Mounting drive: {name}")
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if not self.is_drive_mounted(drive):
                self._show_message("Mount Error", f"Drive '{name}' could not be mounted.", QMessageBox.Icon.Warning, parent)
                return False
            if remember_unmount and drive.get('unmount_command'):
                self.drives_to_unmount.append(drive)
            return True
        except Exception as e:
            self._show_message("Mount Error", f"Drive '{name}' could not be mounted.\nError: {e}", QMessageBox.Icon.Critical, parent)
            return False

    def unmount_drive(self, drive, parent=None):
        name, cmd = drive.get('drive_name', ''), drive.get('unmount_command', '')
        if not cmd:
            return False
        try:
            print(f"Unmounting drive: {name}")
            subprocess.Popen(cmd, shell=True)
            return True
        except Exception as e:
            self._show_message("Unmount Error", f"Drive '{name}' could not be unmounted.\nError: {e}", QMessageBox.Icon.Critical, parent)
            return False

    def mount_required_drives(self, drives, parent=None):
        if not drives:
            return True
        success = True
        for drive in drives:
            name = drive.get('drive_name', '')
            msg = QMessageBox(QMessageBox.Icon.Question, "Drive Mount Required", f"Drive '{name}' needs to be mounted.\nMount now?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, parent)
            checkbox = QCheckBox("Unmount drive when finished")
            checkbox.setChecked(True)
            msg.setCheckBox(checkbox)
            if msg.exec() != QMessageBox.StandardButton.Yes:
                self._show_message("Operation Cancelled", f"Cannot continue without mounting drive '{name}'.", QMessageBox.Icon.Information, parent)
                success = False
                continue
            if not self.mount_drive(drive, parent, checkbox.isChecked()):
                success = False
        return success

    def unmount_drives(self, parent=None):
        success = True
        for drive in self.drives_to_unmount:
            if not self.unmount_drive(drive, parent):
                success = False
        if success:
            self.drives_to_unmount.clear()
        return success

    def mount_drives_at_launch(self):
        if getattr(Options, 'mount_options', None) and getattr(Options, 'run_mount_command_on_launch', False):
            for opt in Options.mount_options:
                if not self.is_drive_mounted(opt):
                    self.mount_drive(opt)

    @staticmethod
    def _show_message(title, text, icon, parent):
        QMessageBox(icon, title, text, QMessageBox.StandardButton.Ok, parent).exec()


class Options(QObject):
    settings_changed = pyqtSignal()
    config_file_path = Path(home_config) / 'Backup Helper' / 'config.json'
    main_window = None
    run_mount_command_on_launch = False
    user_shell = USER_SHELL[0]
    _entries_mutex = QMutex()
    all_entries = []
    entries_sorted = []
    mount_options = []
    headers = []
    header_order = []
    header_inactive = []
    header_colors = {}
    installer_operations = []
    system_files = []
    essential_packages = []
    additional_packages = []
    specific_packages = []
    sublayout_names = {'sublayout_games_1': '', 'sublayout_games_2': '', 'sublayout_games_3': '', 'sublayout_games_4': ''}
    ui_settings = {"backup_window_columns": 2, "restore_window_columns": 2, "settings_window_columns": 2}
    text_replacements = [(home_user, '~'), (f"/run/media/{user}/", ''), ("[1m", ""), ("[0m", "")]
    text_replacements.extend([(env, env) for env in SESSIONS])

    def __init__(self, header, title, source, destination, details=None):
        super().__init__()
        self.drive_manager = DriveManager()
        self.header = header
        self.title = title
        self.source = source
        self.destination = destination
        self.details = details if details else {'no_backup': False, 'no_restore': False, 'sublayout_games_1': False,
                                                'sublayout_games_2': False, 'sublayout_games_3': False, 'sublayout_games_4': False,
                                                'unique_id': QUuid.createUuid().toString(QUuid.StringFormat.WithoutBraces)}

    @staticmethod
    def set_main_window(main_window):
        Options.main_window = main_window

    @staticmethod
    def mount_drives_on_startup():
        if Options.run_mount_command_on_launch:
            DriveManager().mount_drives_at_launch()

    @staticmethod
    def sort_entries():
        header_order_map = {h: i for i, h in enumerate(Options.header_order)}
        Options.entries_sorted = sorted([{'header': entry.header, 'title': entry.title, 'source': entry.source, 'destination': entry.destination,
                                          **{k: entry.details.get(k, False) for k in ('no_backup', 'no_restore', 'sublayout_games_1', 'sublayout_games_2', 'sublayout_games_3', 'sublayout_games_4')},
                                          'unique_id': entry.details.get('unique_id', QUuid.createUuid().toString(QUuid.StringFormat.WithoutBraces))} for entry in Options.all_entries], key=lambda x: (header_order_map.get(x['header'], 999), x['title'].lower()))
        return Options.entries_sorted

    @staticmethod
    def delete_entry(entry):
        try:
            Options.all_entries.remove(entry)
            Options.save_config()
        except ValueError:
            pass

    @staticmethod
    def save_config():
        with QMutexLocker(Options._entries_mutex):
            config_dir = Path(Options.config_file_path).parent
            try:
                config_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                print(f"Error creating config directory: {e}")
                return False
            for entry in Options.all_entries:
                if entry.header not in Options.header_order:
                    Options.header_order.append(entry.header)
            header_data = {header: {"inactive": header in Options.header_inactive, "header_color": Options.header_colors.get(header, '#ffffff')} for header in Options.header_order + Options.header_inactive}
            mount_options = sorted(Options.mount_options, key=lambda x: x.get("drive_name", ""))
            def sort_if_valid(collection, key=None):
                if isinstance(collection, list) and all(isinstance(item, str) for item in collection):
                    return sorted(collection) if key is None else sorted(collection, key=key)
                return collection
            essential_packages = sort_if_valid(Options.essential_packages)
            additional_packages = sort_if_valid(Options.additional_packages)
            specific_packages = []
            if isinstance(Options.specific_packages, list) and all(isinstance(item, dict) for item in Options.specific_packages):
                specific_packages = sorted(Options.specific_packages, key=lambda x: (x.get('package', ''), x.get('session', '')))
            system_files = []
            if isinstance(Options.system_files, list) and all(isinstance(item, dict) for item in Options.system_files):
                system_files = Options.system_files
            entries_data = {"mount_options": mount_options, "run_mount_command_on_launch": Options.run_mount_command_on_launch,
                            "header": header_data, "sublayout_names": Options.sublayout_names, "installer_operations": Options.installer_operations,
                            "system_files": system_files, "essential_packages": essential_packages, "additional_packages": additional_packages,
                            "specific_packages": specific_packages, "ui_settings": Options.ui_settings, "user_shell": Options.user_shell, "entries": []}
            for e in Options.all_entries:
                entry = {"header": e.header, "title": e.title, "source": [str(src) for src in (e.source if isinstance(e.source, list) else [e.source])],
                         "destination": [str(dest) for dest in (e.destination if isinstance(e.destination, list) else [e.destination])],
                         "details": {**{k: e.details.get(k, False) for k in ('no_backup', 'no_restore', 'sublayout_games_1', 'sublayout_games_2', 'sublayout_games_3',
                         'sublayout_games_4')}, "unique_id": e.details.get('unique_id', QUuid.createUuid().toString(QUuid.StringFormat.WithoutBraces))}}
                entries_data["entries"].append(entry)
            temp_path = None
            try:
                with tempfile.NamedTemporaryFile(dir=config_dir, delete=False, mode='w', encoding='utf-8') as temp_file:
                    temp_path = temp_file.name
                    json_data = json.dumps(entries_data, indent=4, ensure_ascii=False)
                    temp_file.write(json_data)
                    temp_file.flush()
                    os.fsync(temp_file.fileno())
                os.replace(temp_path, Options.config_file_path)
                Options.sort_entries()
                if Options.main_window is not None:
                    try:
                        Options.main_window.settings_changed.emit()
                    except Exception as e:
                        print(f"Error emitting settings_changed signal: {e}")
                return True
            except Exception as e:
                error_type = "replacing" if "replace" in str(e) else "writing"
                print(f"Error {error_type} config file: {e}")
                if temp_path:
                    try:
                        os.unlink(temp_path)
                    except OSError:
                        pass
                return False

    @staticmethod
    def load_config(file_path):
        try:
            with open(file_path, encoding='utf-8') as file:
                entries_data = json.load(file)
            header_data = entries_data.get('header', {})
            Options.headers = [h for h in Options.header_order]
            Options.header_order = list(header_data.keys())
            Options.header_colors = {}
            Options.header_inactive = []
            for header, data in header_data.items():
                Options.header_colors[header] = data.get('header_color', '#ffffff')
                if data.get('inactive', False):
                    Options.header_inactive.append(header)
            Options.sublayout_names = entries_data.get("sublayout_names", Options.sublayout_names)
            Options.installer_operations = entries_data.get("installer_operations", [])
            Options.system_files = sorted(entries_data.get("system_files", []), key=lambda x: x.get('source', ''))
            Options.essential_packages = sorted(entries_data.get("essential_packages", []))
            Options.additional_packages = sorted(entries_data.get("additional_packages", []))
            Options.specific_packages = sorted(entries_data.get("specific_packages", []), key=lambda x: x.get('package', ''))
            Options.user_shell = entries_data.get("user_shell", USER_SHELL[0])
            Options.mount_options = entries_data.get("mount_options", [])
            config_changed = False
            if not Options.mount_options and entries_data.get("run_mount_command_on_launch", False):
                config_changed = True
            else:
                Options.run_mount_command_on_launch = entries_data.get("run_mount_command_on_launch", False)
            Options.ui_settings = entries_data.get("ui_settings", Options.ui_settings)
            Options.all_entries = []
            for entry_data in entries_data.get('entries', []):
                header = entry_data.get('header', '')
                if header and header not in Options.header_order:
                    Options.header_order.append(header)
                def normalize_newlines(item):
                    return item.replace('\\n', '\n') if isinstance(item, str) else item
                title = normalize_newlines(entry_data.get('title', ''))
                source_raw = entry_data.get('source', [])
                source = [normalize_newlines(src) for src in (source_raw if isinstance(source_raw, list) else [source_raw])]
                destination_raw = entry_data.get('destination', [])
                destination = [normalize_newlines(dest) for dest in (destination_raw if isinstance(destination_raw, list) else [destination_raw])]
                new_entry = Options(header, title, source, destination)
                details = entry_data.get('details', {})
                for key in ('no_backup', 'no_restore', 'sublayout_games_1', 'sublayout_games_2', 'sublayout_games_3', 'sublayout_games_4'):
                    new_entry.details[key] = details.get(key, False)
                new_entry.details['unique_id'] = details.get('unique_id', QUuid.createUuid().toString(QUuid.StringFormat.WithoutBraces))
                Options.all_entries.append(new_entry)
            if config_changed:
                Options.save_config()
        except (IOError, json.JSONDecodeError) as e:
                error_type = "JSON decoding" if isinstance(e, json.JSONDecodeError) else "loading"
                print(f"Error {error_type} entries from {file_path}: {e}")
        except Exception as e:
            print(f"Unexpected error loading config: {e}")

    @staticmethod
    def generate_tooltip():
        text_replacements = Options.text_replacements
        def format_html(entry_title, entry_source_text, entry_dest_text):
            template = """<table style='border-collapse: collapse; width: 100%; font-family: FiraCode Nerd Font Mono;'>
                <tr style='background-color: #121212;'><td colspan='2' style='font-size: 13px; color: #ffc1c2; text-align: center; padding: 5px 5px; white-space: nowrap;'>{title}</td>
                </tr><tr style='background-color: #2a2a2a;'><td colspan='2' style='font-size: 12px; color: #00fa9a; text-align: left; padding: 6px; font-family: FiraCode Nerd Font Mono; white-space: nowrap;'>
                Source:<br><br>{source}</td></tr><tr style='background-color: #1e1e1e;'><td colspan='2' style='font-size: 12px; color: #00fa9a; text-align: left; padding: 6px; font-family: 
                FiraCode Nerd Font Mono; white-space: nowrap;'>Destination:<br><br>{dest}</td></tr></table>"""
            return template.format(title=entry_title, source=entry_source_text, dest=entry_dest_text)
        def apply_replacements(text, max_iterations=10):
            for _ in range(max_iterations):
                original = text
                text = functools.reduce(lambda t, repl: t.replace(*repl), text_replacements, text)
                if text == original:
                    break
            return text
        backup_tooltips = {}
        restore_tooltips = {}
        for entry in Options.entries_sorted:
            title = entry["title"]
            tooltip_key = f"{title}_tooltip"
            source = entry['source'] if isinstance(entry['source'], list) else [entry['source']]
            destination = entry['destination'] if isinstance(entry['destination'], list) else [entry['destination']]
            source_text = "<br/>".join(map(str, source))
            destination_text = "<br/>".join(map(str, destination))
            backup_tooltips[tooltip_key] = apply_replacements(format_html(title, source_text, destination_text))
            restore_tooltips[tooltip_key] = apply_replacements(format_html(title, destination_text, source_text))
        installer_tooltips = {}
        operation_keys = {"copy_system_files": "system_files", "install_essential_packages": "essential_packages",
                          "install_additional_packages": "additional_packages", "install_specific_packages": "specific_packages", "set_user_shell": "user_shell"}
        for operation, config_key in operation_keys.items():
            if operation not in PACKAGE_INSTALLER_OPERATION_TEXT or not getattr(Options, config_key, None):
                continue
            items = getattr(Options, config_key)
            column_width = 1 if config_key == "system_files" else 4
            label_maps = {"system_files": {"source": "Source:<br>", "destination": "<br>Destination:<br>"},
                          "specific_packages": {"package": lambda v: f"{v}", "session": lambda v: f"<br>({v})"}, "user_shell": lambda v: f"Selected shell: {v}"}
            if config_key in label_maps:
                mapped = label_maps[config_key]
                def apply_map(k, v):
                    if config_key == "user_shell":
                        return mapped(v)
                    value = mapped.get(k)
                    if callable(value):
                        return value(v)
                    elif value is not None:
                        return f"{value}{v}"
                    return f"{k}: {v}"
                if config_key == "user_shell":
                    items = [mapped(items)]
                else:
                    items = [{k: apply_map(k, v) for k, v in item.items()} for item in items]
            item_format = "".join if config_key == "specific_packages" else lambda l: "<br>".join(l)
            item_strings = [item_format([f"{v}" for v in item.values()]) if isinstance(item, dict) else str(item) for item in items]
            rows = []
            for i in range(0, len(item_strings), column_width):
                bg_color = "#2a2a2a" if (i // column_width) % 2 == 0 else "#1e1e1e"
                cells = ''.join( f'<td style="padding: 5px 5px; border: 1px solid #444; color: #00fa9a; font-family: FiraCode Nerd Font Mono;">{item}</td>' for item in item_strings[i:i + column_width])
                rows.append(f'<tr style="background-color: {bg_color};">{cells}</tr>')
            tooltip = ("<div style='white-space: nowrap; font-size: 14px; color: #00fa9a; font-family: FiraCode Nerd Font Mono; "
                       f"background-color: #121212; padding: 5px 5px; border: 1px solid #444;'>" 
                       f"<table style='border-collapse: collapse; table-layout: auto;'>{''.join(rows)}</table></div>")
            installer_tooltips[operation] = apply_replacements(tooltip)
        Options.installer_tooltips = installer_tooltips
        return backup_tooltips, restore_tooltips, installer_tooltips


Options.load_config(Options.config_file_path)
Options.mount_drives_on_startup()


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    settings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backup Helper")
        Options.set_main_window(self)
        self.config = {}
        self.drive_manager = DriveManager()
        self.backup_restore_window = None
        self.settings_window = None
        self.package_installer_launcher = None
        self.btn_exit = QPushButton()
        self.settings_changed.connect(self.set_exit_button)
        self.settings_changed.connect(self.on_settings_changed)
        self.load_config()
        self.init_ui()

    def load_config(self):
        Options.load_config(Options.config_file_path)
        try:
            with open(Options.config_file_path, 'r') as file:
                self.config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}")
            self.config = {}

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setMinimumSize(400, 300)
        button_height = 50
        buttons = [("Create Backup", lambda: self.start_backup_restoring("backup")), ("Restore Backup", lambda: self.start_backup_restoring("restore")),
                   ("Package Installer", self.launch_package_installer), ("Settings", self.open_settings)]
        for text, callback in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(button_height)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        self.btn_exit.setFixedHeight(button_height)
        self.btn_exit.clicked.connect(self.confirm_exit)
        layout.addWidget(self.btn_exit)
        self.set_exit_button()
        self.setCentralWidget(central_widget)

    def set_exit_button(self):
        self.btn_exit.setText("Unmount and Exit" if Options.run_mount_command_on_launch and Options.mount_options else "Exit")

    def start_backup_restoring(self, window_type):
        self.backup_restore_window = BackupRestoreWindow(self, window_type)
        self.backup_restore_window.show()
        self.hide()

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
        self.hide()

    def launch_package_installer(self):
        self.package_installer_launcher = PackageInstallerLauncher(self)
        self.package_installer_launcher.launch()

    def on_settings_changed(self):
        self.load_config()
        self.set_exit_button()
        if self.backup_restore_window:
            self.backup_restore_window.settings_changed.emit()
        if self.settings_window:
            self.settings_window.settings_changed.emit()
        if self.package_installer_launcher:
            self.package_installer_launcher.config = self.config

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            w = self.focusWidget()
            if isinstance(w, QPushButton):
                w.click()
        elif event.key() == Qt.Key.Key_Escape:
            self.confirm_exit()
        else:
            super().keyPressEvent(event)

    def confirm_exit(self):
        drives = [f"'{opt.get('drive_name')}'" for opt in Options.mount_options]
        is_unmounting = Options.run_mount_command_on_launch and drives
        text = f"Unmount drive{'s' if len(drives) > 1 else ''} {' & '.join(drives)} and exit?" if is_unmounting else "Are you sure you want to exit?"
        if self._confirm_dialog("Exit Confirmation", text):
            if is_unmounting:
                self.hide()
                self.drive_manager.drives_to_unmount = Options.mount_options
                self.drive_manager.unmount_drives()
            QCoreApplication.exit(0)

    def closeEvent(self, event):
        drives = [f"'{opt.get('drive_name')}'" for opt in Options.mount_options]
        text = f"Exit without unmounting drive{'s' if len(drives) > 1 else ''} {' & '.join(drives)}?" if Options.run_mount_command_on_launch and drives else "Are you sure you want to exit?"
        if self._confirm_dialog("Exit Confirmation", text):
            event.accept()
            QCoreApplication.exit(0)
        else:
            event.ignore()

    def _confirm_dialog(self, title, text):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(text)
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setDefaultButton(QMessageBox.StandardButton.No)
        return dlg.exec() == QMessageBox.StandardButton.Yes


# noinspection PyUnresolvedReferences
class BaseWindow(QDialog):
    settings_changed = pyqtSignal()

    def __init__(self, parent=None, window_type="base"):
        super().__init__(parent)
        self.content_widget = None
        self.window_type = window_type
        self.setWindowTitle({"backup": "Create Backup", "restore": "Restore Backup", "settings": "Settings"}.get(window_type, "Window"))
        self.main_layout = QVBoxLayout(self)
        self.top_controls = QHBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.main_layout.addLayout(self.top_controls)
        self.main_layout.addWidget(self.scroll_area, stretch=1)
        self.selectall = QCheckBox("Select All")
        self.column_toggle = QPushButton()
        self.columns = 4
        self.checkbox_dirs = []
        self.settings_changed.connect(self.setup_ui)
        self.setup_ui()

    def setup_ui(self):
        Options.sort_entries()
        self.clear_layout_contents()
        key = f"{self.window_type}_window_columns"
        self.columns = 4 if Options.ui_settings.get(key, 2) == 4 else 2
        self.create_top_controls(f"{2 if self.columns == 4 else 4} Columns")
        self.content_widget = QWidget()
        layout = QGridLayout(self.content_widget)
        if self.window_type in ("restore", "settings"):
            sublayout_entries = self.get_sublayout_entries()
            self.setup_sublayouts(sublayout_entries)
            row_counter = self.add_header_checkboxes(layout, sublayout_entries)
        else:
            row_counter = self.add_header_checkboxes(layout)
        self.add_control_buttons(layout, row_counter)
        self.scroll_area.setWidget(self.content_widget)
        self.adjust_window_size()

    def create_top_controls(self, column_text):
        self._clear_layout(self.top_controls)
        self.selectall = QCheckBox("Select All")
        self.selectall.setStyleSheet(f"{global_style} QCheckBox {{color: '#6ffff5'; font-size: 14px;}}")
        self.selectall.clicked.connect(self.toggle_checkboxes_manually)
        self.column_toggle = QPushButton(column_text)
        self.column_toggle.clicked.connect(self.toggle_columns)
        self.top_controls.addWidget(self.selectall)
        self.top_controls.addStretch(1)
        self.top_controls.addWidget(self.column_toggle)

    def add_header_checkboxes(self, layout, sublayout_entries=None):
        row = 0
        self.checkbox_dirs.clear()
        tooltip_text, tooltip_text_entry_restore, _ = Options.generate_tooltip()
        tooltip_dict = tooltip_text_entry_restore if self.window_type == "restore" else tooltip_text
        active_headers = (Options.headers if self.window_type == "settings" else [h for h in Options.headers if h not in Options.header_inactive])
        filter_key = "no_backup" if self.window_type == "backup" else "no_restore"
        header_entries = {header: [e for e in Options.entries_sorted if e["header"] == header and (self.window_type == "settings" or not e.get(filter_key, False))] for header in active_headers}
        header_entries = {h: ents for h, ents in header_entries.items() if ents}
        for header, ents in header_entries.items():
            inactive = self.window_type == "settings" and header in Options.header_inactive
            col = 0
            header_color = "#7f7f7f" if inactive else Options.header_colors.get(header, '#ffffff')
            label = QLabel(f"{header} (Inactive)" if inactive else header)
            label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {header_color};")
            hbox = QHBoxLayout()
            hbox.addWidget(label)
            layout.addLayout(hbox, row, 0, 1, self.columns)
            row += 1
            for entry in ents:
                checkbox = QCheckBox(entry["title"])
                ch_style = f"{global_style} QCheckBox {{color: {header_color}; font-size: 16px; }} QToolTip {{color: '#07e392';}}"
                if header == "Games" and self.window_type in ("restore", "settings") and sublayout_entries:
                    added = False
                    for i in range(1, 5):
                        key = f'sublayout_games_{i}'
                        if entry["title"] in sublayout_entries[key]:
                            checkbox.setStyleSheet(f"{global_style} QCheckBox {{color: {header_color}; font-size: 14px;}} QToolTip {{color: '#07e392';}}")
                            sublayout = getattr(self, key, None)
                            if sublayout:
                                sublayout.addWidget(checkbox)
                                added = True
                            break
                    if not added:
                        layout.addWidget(checkbox, row, col)
                        col += 1
                else:
                    checkbox.setStyleSheet(ch_style)
                    layout.addWidget(checkbox, row, col)
                    col += 1
                checkbox.stateChanged.connect(self.update_select_all_state)
                if col >= self.columns:
                    col = 0
                    row += 1
                src, dst = (entry["source"], entry["destination"]) if self.window_type != "restore" else (
                    entry["destination"], entry["source"])
                self.checkbox_dirs.append((checkbox, src, dst, entry["unique_id"]))
                tip_key = f"{checkbox.text()}_tooltip"
                if tip_key in tooltip_dict:
                    checkbox.setToolTip(tooltip_dict[tip_key])
                    checkbox.setToolTipDuration(600000)
            if col != 0:
                row += 1
            if header == "Games" and self.window_type in ("restore", "settings"):
                row = self.add_game_sublayouts(layout, row)
        return row

    @staticmethod
    def get_sublayout_entries():
        d = {f'sublayout_games_{i}': [] for i in range(1, 5)}
        for e in Options.all_entries:
            for i in range(1, 5):
                if e.details.get(f'sublayout_games_{i}', False):
                    d[f'sublayout_games_{i}'].append(e.title)
        return d

    def setup_sublayouts(self, sublayout_entries):
        for i in range(1, 5):
            key = f'sublayout_games_{i}'
            if not sublayout_entries[key]:
                continue
            layout = QVBoxLayout()
            setattr(self, key, layout)
            widget = QWidget()
            setattr(self, f'sublayout_widget_games_{i}', widget)
            ch_layout = QHBoxLayout()
            name = Options.sublayout_names.get(key, f'Sublayout Games {i}')
            select_all = QCheckBox(name)
            color = "#7f7f7f" if self.window_type == "settings" and "Games" in Options.header_inactive else Options.header_colors.get("Games", "#ffffff")
            select_all.setStyleSheet(f"{global_style} QCheckBox {{color: {color}; font-size: 15px;}}")
            select_all.clicked.connect(lambda checked, idx=i: self._toggle_sublayout_checkboxes(getattr(self, f'sublayout_games_{idx}'), getattr(self, f'select_all_games_{idx}')))
            setattr(self, f'select_all_games_{i}', select_all)
            ch_layout.addStretch(1)
            ch_layout.addWidget(select_all)
            ch_layout.addStretch(1)
            layout.addLayout(ch_layout)
            widget.setLayout(layout)
            widget.setStyleSheet("background-color: #2c2f41;")

    def add_game_sublayouts(self, layout, row):
        sublayouts = [(getattr(self, f'sublayout_widget_games_{i}', None), getattr(self, f'sublayout_games_{i}', None)) for i in range(1, 5)]
        sublayouts = [(w, l) for w, l in sublayouts if l]
        def add_spacer(l):
            if l: l.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        if not sublayouts:
            return row
        if self.columns == 4:
            pairs = [(0, 2), (2, 4)]
            for j, (start, end) in enumerate(pairs):
                if len(sublayouts) > start:
                    for idx in range(start, min(end, len(sublayouts))):
                        layout.addWidget(sublayouts[idx][0], row, (idx-start)*2, 1, 2)
                        add_spacer(sublayouts[idx][1])
                    row += 1
        else:
            for i in range(0, len(sublayouts), 2):
                layout.addWidget(sublayouts[i][0], row, 0)
                add_spacer(sublayouts[i][1])
                if i + 1 < len(sublayouts):
                    layout.addWidget(sublayouts[i + 1][0], row, 1)
                    add_spacer(sublayouts[i + 1][1])
                row += 1
        return row

    def add_control_buttons(self, layout, row):
        if self.window_type in ("backup", "restore"):
            btn = QPushButton("Create Backup" if self.window_type == "backup" else "Restore Backup", self)
            btn.clicked.connect(self.start_process)
            close_btn = QPushButton("Close", self)
            close_btn.clicked.connect(self.go_back)
            layout.addWidget(btn, row, 0, 1, self.columns)
            layout.addWidget(close_btn, row+1, 0, 1, self.columns)
        elif self.window_type == "settings":
            buttons = [('package_installer_settings_button', "Package Installer Options", self.installer_options),
                       ('add_entry_button', "New Entry", lambda: self.entry_dialog(edit_mode=False)),
                       ('entry_editor_button', "Edit Entry", lambda: self.entry_dialog(edit_mode=True)),
                       ('delete_button', "Delete Entry", self.delete_entry),
                       ('header_settings_button', "Header Settings", self.header_settings),
                       ('smb_password_button', "Samba Password", self.open_samba_password_dialog),
                       ('mount_button', "Mount Options", self.manage_mount_options),
                       ('close_button', "Close", self.go_back)]
            for name, text, cb in buttons:
                btn = QPushButton(text, self)
                btn.clicked.connect(cb)
                setattr(self, name, btn)
            layout.addWidget(self.package_installer_settings_button, row, 0, 1, self.columns)
            row += 1
            hbox = QHBoxLayout()
            for btn in [self.add_entry_button, self.entry_editor_button, self.delete_button, self.header_settings_button]:
                hbox.addWidget(btn)
            layout.addLayout(hbox, row, 0, 1, self.columns)
            row += 1
            hbox2 = QHBoxLayout()
            for btn in [self.smb_password_button, self.mount_button]:
                hbox2.addWidget(btn)
            layout.addLayout(hbox2, row, 0, 1, self.columns)
            row += 1
            layout.addWidget(self.close_button, row, 0, 1, self.columns)
        return row + 1

    def toggle_columns(self):
        self.hide()
        self.columns = 4 if self.columns == 2 else 2
        Options.ui_settings[f"{self.window_type}_window_columns"] = self.columns
        Options.save_config()
        self.setup_ui()
        self.show()

    def adjust_window_size(self):
        self.content_widget.adjustSize()
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.content_widget.sizeHint()
        margin = (self.main_layout.contentsMargins().top() + self.main_layout.contentsMargins().bottom() + self.main_layout.spacing() + self.top_controls.sizeHint().height() + 20)
        self.resize(min(size.width() + 165, screen.width()), min(size.height() + margin, screen.height()))
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                BaseWindow._clear_layout(item.layout())

    def clear_layout_contents(self):
        self._clear_layout(self.top_controls)
        if self.scroll_area.widget():
            old_widget = self.scroll_area.takeWidget()
            old_widget.deleteLater()
        self.content_widget = None
        self.checkbox_dirs.clear()

    @staticmethod
    def _set_checkbox_checked(checkbox, checked):
        checkbox.blockSignals(True)
        checkbox.setChecked(checked)
        checkbox.blockSignals(False)

    def update_select_all_state(self):
        all_checked = all(cb.isChecked() for cb, *_ in self.checkbox_dirs if cb != self.selectall)
        self.selectall.blockSignals(True)
        self.selectall.setChecked(all_checked)
        self.selectall.blockSignals(False)
        if self.window_type in ("restore", "settings"):
            self.update_game_sublayout_states()

    def toggle_checkboxes_manually(self):
        is_checked = self.selectall.isChecked()
        for cb, *_ in self.checkbox_dirs:
            if cb != self.selectall:
                cb.setChecked(is_checked)

    def update_game_sublayout_states(self):
        for i in range(1, 5):
            layout = getattr(self, f'sublayout_games_{i}', None)
            widget = getattr(self, f'sublayout_widget_games_{i}', None)
            select_all_cb = getattr(self, f'select_all_games_{i}', None)
            if layout and widget and select_all_cb:
                checkboxes = [cb for cb in widget.findChildren(QCheckBox) if cb != select_all_cb]
                all_checked = all(cb.isChecked() for cb in checkboxes) if checkboxes else False
                self._set_checkbox_checked(select_all_cb, all_checked)

    def _toggle_sublayout_checkboxes(self, layout, select_all_checkbox):
        if layout and select_all_checkbox:
            checked = select_all_checkbox.isChecked()
            for i in range(layout.count()):
                item = layout.itemAt(i)
                cb = item.widget()
                if cb and isinstance(cb, QCheckBox) and cb != select_all_checkbox:
                    self._set_checkbox_checked(cb, checked)
            self.update_select_all_state()

    def keyPressEvent(self, event):
        key = event.key()
        fw = self.focusWidget()
        if key in (Qt.Key.Key_Enter, Qt.Key.Key_Return) and isinstance(fw, QCheckBox):
            fw.toggle()
            if fw == self.selectall:
                self.toggle_checkboxes_manually()
            elif self.window_type in ("restore", "settings"):
                for i in range(1, 5):
                    if fw == getattr(self, f'select_all_games_{i}', None):
                        self._toggle_sublayout_checkboxes(getattr(self, f'sublayout_games_{i}'), fw)
                        break
        elif key == Qt.Key.Key_Escape:
            self.go_back()
        else:
            super().keyPressEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        for cb, *_ in self.checkbox_dirs:
            cb.setChecked(False)
        self.selectall.setFocus()

    def go_back(self):
        self.close()

    def closeEvent(self, event):
        if self.parent():
            self.parent().show()
        super().closeEvent(event)


class BackupRestoreWindow(BaseWindow):
    def __init__(self, parent=None, window_type="backup"):
        super().__init__(parent, window_type)
        self.drive_manager = DriveManager()

    def _get_selected_items(self):
        return [(source_dirs, dest_dirs, label) for checkbox, source_dirs, dest_dirs, label in self.checkbox_dirs if checkbox.isChecked()]

    def start_process(self):
        self.hide()
        selected_items = self._get_selected_items()
        if not selected_items:
            self._show_error_and_return("Cannot start the process. Nothing selected.")
            return
        paths_to_check = self._extract_paths_to_check(selected_items)
        drives_to_mount = self.drive_manager.check_drives_to_mount(paths_to_check)
        if drives_to_mount and not self.drive_manager.mount_required_drives(drives_to_mount, self):
            self.show()
            return
        processable_items, unprocessable_items = self._separate_processable_items(selected_items)
        if not processable_items:
            self._show_error_and_return(f"Selected items cannot be {'copied' if self.window_type == 'backup' else 'restored'}.")
            return
        if unprocessable_items and not self._confirm_continue_with_missing(unprocessable_items):
            self.show()
            return
        processable_checkbox_dirs = self._get_processable_checkbox_dirs()
        operation_type = "Backup" if self.window_type == "backup" else "Restore"
        dialog = BackupRestoreProcessDialog(self, processable_checkbox_dirs, operation_type=operation_type)
        dialog.exec()
        self.show()
        self.drive_manager.unmount_drives()

    @staticmethod
    def _extract_paths_to_check(selected_items):
        paths = []
        for source_dirs, dest_dirs, _ in selected_items:
            if isinstance(source_dirs, list):
                paths.extend(source_dirs)
            else:
                paths.append(source_dirs)
            if isinstance(dest_dirs, list):
                paths.extend(dest_dirs)
            else:
                paths.append(dest_dirs)
        return paths

    @staticmethod
    def _check_path_exists(path):
        if SmbFileHandler.is_smb_path(path):
            return True
        else:
            return Path(path).exists()

    def _separate_processable_items(self, selected_items):
        processable = []
        unprocessable = []
        label_to_title = {entry.get('unique_id'): entry.get('title') for entry in Options.entries_sorted}
        for source_dirs, dest_dirs, label in selected_items:
            sources = source_dirs if isinstance(source_dirs, list) else [source_dirs]
            source_exists = False
            for src in sources:
                if self._check_path_exists(src):
                    source_exists = True
                    break
            if source_exists:
                processable.append((source_dirs, dest_dirs, label))
            else:
                unprocessable.append(label_to_title.get(label, label))
        return processable, unprocessable

    def _show_error_and_return(self, message):
        error_title = f"{'Backup' if self.window_type == 'backup' else 'Restore'} Error"
        QMessageBox(QMessageBox.Icon.Information, error_title, message, QMessageBox.StandardButton.Ok, self).exec()
        self.show()

    def _confirm_continue_with_missing(self, unprocessable_items):
        warning_message = "The following entries could not be processed because they do not exist:\n\n"
        warning_message += "\n".join([f"• {item}" for item in unprocessable_items])
        warning_message += f"\n\nDo you want to continue with the available entries?"
        warning_title = f"{'Backup' if self.window_type == 'backup' else 'Restore'} Warning"
        warning_box = QMessageBox(QMessageBox.Icon.Warning, warning_title, warning_message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, self)
        warning_box.setDefaultButton(QMessageBox.StandardButton.Yes)
        return warning_box.exec() == QMessageBox.StandardButton.Yes

    def _get_processable_checkbox_dirs(self):
        result = []
        for checkbox, source_dirs, dest_dirs, label in self.checkbox_dirs:
            if not checkbox.isChecked():
                continue
            sources = source_dirs if isinstance(source_dirs, list) else [source_dirs]
            source_exists = False
            for src in sources:
                if self._check_path_exists(src):
                    source_exists = True
                    break
            if source_exists:
                result.append((checkbox, source_dirs, dest_dirs, label))
        return result


# noinspection PyUnresolvedReferences
class SettingsWindow(BaseWindow):
    def __init__(self, parent=None):
        super().__init__(parent, "settings")
        self.mount_options_dialog = None

    def get_checked_entries(self):
        return [(checkbox, sources, destinations, unique_id) for checkbox, sources, destinations, unique_id in self.checkbox_dirs if checkbox.isChecked()]

    def show_message(self, title, message, icon=QMessageBox.Icon.Information):
        QMessageBox(icon, title, message, QMessageBox.StandardButton.Ok, self).exec()

    @staticmethod
    def format_list_message(items, suffix):
        if not items:
            return f"{suffix}"
        if len(items) == 1:
            return f"{items[0]}{suffix}"
        if len(items) == 2:
            return f"{items[0]} and {items[1]}{suffix}"
        return f"{', '.join(items[:-1])}, and {items[-1]}{suffix}"

    def installer_options(self):
        self.hide()
        PackageInstallerOptions(self).exec()
        self.show()

    def entry_dialog(self, edit_mode=False):
        checked_entries = self.get_checked_entries()
        if edit_mode and not checked_entries:
            return self.show_message("Entry Editor Error", "Nothing selected or selected items cannot be edited.")
        self.hide()
        entries_to_process = checked_entries if edit_mode else [None]
        for entry_data in entries_to_process:
            dialog = QDialog(self)
            dialog.setFixedSize(1000, 550)
            title_checkbox = entry_data[0].text() if edit_mode else ""
            unique_id = entry_data[3] if edit_mode else None
            dialog.setWindowTitle("Edit Entry" if edit_mode else "Add New Entry")
            main_layout = QVBoxLayout(dialog)
            main_layout.setContentsMargins(5, 5, 5, 5)
            if edit_mode:
                header_label_text = f"\n'{title_checkbox}'\n\nType '\\n' for line break in title.\n\nFor samba shares use:\n'smb://ip/rest of samba path'"
            else:
                header_label_text = "\nCreate a new entry.\n\nType '\\n' for line break in title.\n\nFor samba shares use:\n'smb://ip/rest of samba path'"
            header_label = QLabel(header_label_text)
            header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            main_layout.addWidget(header_label)
            main_layout.addStretch(1)
            form_layout = QFormLayout()
            form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            form_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            field_height = 60
            header_combo = QComboBox()
            header_combo.setStyleSheet("color: #ffffff; background-color: #555582; padding: 5px 5px;")
            header_combo.addItems(Options.headers)
            header_combo.setMaximumHeight(field_height)
            entry_obj = None
            if edit_mode:
                entry_obj = next((e for e in Options.all_entries if e.details.get('unique_id') == unique_id), None)
                if entry_obj:
                    idx = header_combo.findText(entry_obj.header)
                    if idx >= 0:
                        header_combo.setCurrentIndex(idx)
            form_layout.addRow(QLabel("Header:"), header_combo)
            title_edit = QLineEdit(title_checkbox)
            title_edit.setMaximumHeight(field_height)
            form_layout.addRow(QLabel("Title:"), title_edit)
            if edit_mode:
                sources, destinations = entry_data[1], entry_data[2]
                for field_type, data in [("Source", sources), ("Destination", destinations)]:
                    btn = QPushButton(f"Edit {field_type} Entries")
                    btn.setMaximumHeight(field_height)
                    btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    btn.clicked.connect(lambda _, d=data, t=title_checkbox, f=field_type.lower(): self.open_text_editor(d, t, f))
                    form_layout.addRow(QLabel(f"{field_type}:"), btn)
            else:
                for field_type in ["Source", "Destination"]:
                    field_edit = QLineEdit()
                    field_edit.setMaximumHeight(field_height)
                    field_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
                    btn = QPushButton(f"Select {field_type} Directory")
                    btn.setMaximumHeight(field_height)
                    btn.setFixedWidth(300)
                    btn.clicked.connect(lambda _, le=field_edit: self.select_directory(le))
                    hbox = QHBoxLayout()
                    hbox.setSpacing(5)
                    hbox.setContentsMargins(2, 2, 2, 2)
                    hbox.addWidget(field_edit)
                    hbox.addWidget(btn)
                    container = QWidget()
                    container.setLayout(hbox)
                    container.setMaximumHeight(field_height)
                    form_layout.addRow(QLabel(f"{field_type}:"), container)
                    setattr(self, f"{field_type.lower()}_edit", field_edit)
            checkboxes, checkbox_texts = {}, {'no_backup': 'No Backup', 'no_restore': 'No Restoring'}
            for i in range(1, 5):
                key = f'sublayout_games_{i}'
                checkbox_texts[key] = f"Add to Sublayout-Games {i}:\n'{Options.sublayout_names.get(key, f'Sublayout Games {i}')}'"
            for key, text in checkbox_texts.items():
                cb = QCheckBox(text)
                checked = entry_obj.details.get(key, False) if entry_obj else False
                cb.setChecked(checked)
                cb.setStyleSheet(f"{global_style} QCheckBox {{color: '#6ffff5'}}")
                cb.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
                cb.setMaximumHeight(field_height)
                checkboxes[key] = cb
            checkbox_grid = QGridLayout()
            positions = [('no_backup', 0, 0), ('no_restore', 1, 0), ('sublayout_games_1', 0, 1), ('sublayout_games_2', 1, 1), ('sublayout_games_3', 0, 2), ('sublayout_games_4', 1, 2)]
            for key, row, col in positions:
                checkbox_grid.addWidget(checkboxes[key], row, col)
            form_layout.addRow(QLabel(""), QLabel(""))
            form_layout.addRow(checkbox_grid)
            main_layout.addLayout(form_layout)
            def update_restore(state):
                disabled = state == 2
                for entry_i in range(1, 5):
                    sub_key = f'sublayout_games_{entry_i}'
                    checkboxes[sub_key].setChecked(False)
                    checkboxes[sub_key].setEnabled(not disabled)
            def update_sublayout(num, state):
                if state == 2:
                    checkboxes['no_restore'].setChecked(False)
                    for entry_i in range(1, 5):
                        entry_cb = checkboxes[f'sublayout_games_{entry_i}']
                        if entry_i != num:
                            entry_cb.blockSignals(True)
                            entry_cb.setChecked(False)
                            entry_cb.setEnabled(False)
                            entry_cb.blockSignals(False)
                    checkboxes['no_restore'].setEnabled(False)
                else:
                    checkboxes['no_restore'].setEnabled(True)
                    for entry_i in range(1, 5):
                        if entry_i != num:
                            checkboxes[f'sublayout_games_{entry_i}'].setEnabled(True)
            checkboxes['no_restore'].stateChanged.connect(update_restore)
            for i in range(1, 5):
                checkboxes[f'sublayout_games_{i}'].stateChanged.connect(lambda state, num=i: update_sublayout(num, state))
            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
            button_box.button(QDialogButtonBox.StandardButton.Save).setText("Save")
            button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Close")
            button_box.setMaximumHeight(field_height)
            main_layout.addWidget(button_box, alignment=Qt.AlignmentFlag.AlignRight)
            def save_entry():
                header = header_combo.currentText()
                title = title_edit.text()
                if edit_mode:
                    source, destination = sources, destinations
                else:
                    source, destination = self.source_edit.text(), self.destination_edit.text()
                existing_titles = [entry.title.lower() for entry in Options.all_entries if not edit_mode or entry.title.lower() != title_checkbox.lower()]
                if title.lower() in existing_titles:
                    return self.show_message("Duplicate Title", "An entry with this title already exists. Please choose a different title.")
                if not all([title, source, destination]):
                    return self.show_message("Error", "All fields must be filled in to add a new entry.")
                if edit_mode and entry_obj:
                    entry_obj.header = header
                    entry_obj.title = title
                    new_entry = entry_obj
                else:
                    new_entry = Options(header, title, source, destination)
                    Options.all_entries.append(new_entry)
                for entry_key, entry_checkbox in checkboxes.items():
                    new_entry.details[entry_key] = entry_checkbox.isChecked()
                self.show_message("Success", f"Entry '{new_entry.title}' successfully {('updated' if edit_mode else 'added')}!")
                dialog.accept()
                return None
            button_box.accepted.connect(save_entry)
            button_box.rejected.connect(dialog.reject)
            dialog.exec()
        Options.save_config()
        self.show()
        return None

    def delete_entry(self):
        checked_entries = self.get_checked_entries()
        if not checked_entries:
            return self.show_message("Delete Entry Error", "Nothing selected or selected items cannot be deleted.")
        titles = [entry_data[0].text() for entry_data in checked_entries]
        checked_titles_quoted = [f"'{title}'" for title in titles]
        confirm_message = "Are you sure you want to delete" + self.format_list_message(checked_titles_quoted, "?")
        confirm_box = QMessageBox(QMessageBox.Icon.Question, "Confirm Deletion", confirm_message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, self)
        confirm_box.setDefaultButton(QMessageBox.StandardButton.No)
        if confirm_box.exec() == QMessageBox.StandardButton.Yes:
            for checked_entry in checked_entries:
                entry_obj = next((e for e in Options.all_entries if e.details.get('unique_id') == checked_entry[3]), None)
                if entry_obj:
                    Options.delete_entry(entry_obj)
            self.hide()
            Options.save_config()
            info_message = self.format_list_message(checked_titles_quoted, " successfully deleted!")
            self.show_message("Success", info_message)
            self.show()
            return None
        return None

    def select_directory(self, line_edit):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            line_edit.setText(directory)

    def open_text_editor(self, entries_list, title, field):
        dialog = QDialog(self)
        dialog.setMinimumSize(1200, 1000)
        dialog.setWindowTitle(f"Edit {field.capitalize()} Entries for '{title}'")
        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setPlainText("\n".join(map(str, entries_list)) if isinstance(entries_list, list) else entries_list)
        button_layout = QHBoxLayout()
        buttons = [("Back", dialog.reject), ("File Browser", lambda: self.browse_files(text_edit)), ("Save", lambda: self.save_config_from_editor(text_edit, entries_list, field))]
        for btn_text, callback in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(callback)
            button_layout.addWidget(button)
        layout.addWidget(text_edit)
        layout.addLayout(button_layout)
        dialog.exec()

    def browse_files(self, text_edit):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            current_text = text_edit.toPlainText()
            text_edit.setPlainText(current_text + "\n" + "\n".join(files))

    def save_config_from_editor(self, text_edit, entries_list, field):
        new_entries = text_edit.toPlainText().splitlines()
        if not isinstance(entries_list, list):
            new_value = new_entries[0] if new_entries else ""
            text_edit.setPlainText(new_value)
            return new_value
        entries_list.clear()
        entries_list.extend(new_entries)
        self.show_message("Success", f"{field.capitalize()} successfully edited!")
        text_edit.setPlainText("\n".join(entries_list))
        return entries_list

    def header_settings(self):
        self.hide()
        dialog = QDialog(self)
        dialog.setMinimumSize(850, 950)
        dialog.setWindowTitle("Header Settings")
        layout = QVBoxLayout(dialog)
        list_widget = QListWidget(dialog)
        list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        list_widget.setDragEnabled(True)
        list_widget.setAcceptDrops(True)
        list_widget.setDefaultDropAction(Qt.DropAction.MoveAction)
        for header in Options.header_order:
            item_widget = self.create_header_list_item(header, list_widget)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            list_widget.addItem(item)
            list_widget.setItemWidget(item, item_widget)
        layout.addWidget(list_widget)
        layout.addWidget(QLabel("Click and hold headers to move them.\nCreating header 'Games' provides access to sublayouts for this header."))
        new_header_button = QPushButton("New Header")
        new_header_button.clicked.connect(lambda: self.add_new_header(list_widget))
        layout.addWidget(new_header_button)
        sublayout_buttons = [QPushButton(f"Name Sublayout-Games {i}:\n{Options.sublayout_names.get(f'sublayout_games_{i}', f'Sublayout Games {i}')}") for i in range(1, 5)]
        for i, btn in enumerate(sublayout_buttons, 1):
            btn.clicked.connect(lambda _, num=i: self.prompt_for_name(dialog, num))
        for i in range(0, 4, 2):
            hbox = QHBoxLayout()
            hbox.addWidget(sublayout_buttons[i])
            hbox.addWidget(sublayout_buttons[i + 1])
            layout.addLayout(hbox)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.button(QDialogButtonBox.StandardButton.Save).setText("Save")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Close")
        layout.addWidget(button_box)
        button_box.accepted.connect(lambda: (self.save_header_options(list_widget), dialog.accept()))
        button_box.rejected.connect(dialog.reject)
        dialog.exec()
        self.show()

    def create_header_list_item(self, header, list_widget):
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        header_color = Options.header_colors.get(header, '#ffffff')
        darker = self.darken_color(header_color)
        btn_style = "color: black; font-weight: bold; font-size: 17px;"
        color_btn = QPushButton(header)
        color_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        color_btn.setFixedHeight(26)
        color_btn.setStyleSheet(f"QPushButton {{{btn_style} background-color: {darker};}}")
        color_btn.clicked.connect(lambda _, h=header: self.choose_color(h))
        inactive_cb = QCheckBox("Inactive")
        inactive_cb.setObjectName("inactive_checkbox")
        inactive_cb.setStyleSheet("margin-left: 10px;")
        inactive_cb.setChecked(header in Options.header_inactive)
        def update_inactive(checked):
            color_btn.setEnabled(not checked)
            bg = "gray" if checked else darker
            color_btn.setStyleSheet(f"QPushButton {{{btn_style} background-color: {bg}; padding: 0 10;}}")
        inactive_cb.stateChanged.connect(update_inactive)
        update_inactive(inactive_cb.isChecked())
        del_btn = QPushButton("Delete Header")
        del_btn.setStyleSheet("margin-left: 10px;")
        del_btn.clicked.connect(lambda _, h=header: self.delete_header(h, list_widget))
        item_layout.addWidget(color_btn)
        item_layout.addWidget(inactive_cb)
        item_layout.addWidget(del_btn)
        return item_widget

    def add_new_header(self, list_widget):
        dialog = QDialog(self)
        dialog.setWindowTitle("New Header")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Enter new Header:"))
        input_field = QLineEdit(dialog)
        input_field.setMinimumWidth(450)
        layout.addWidget(input_field)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.button(QDialogButtonBox.StandardButton.Save).setText("Save")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Close")
        layout.addWidget(button_box)
        button_box.accepted.connect(lambda: self.handle_new_header(input_field, dialog, list_widget))
        button_box.rejected.connect(dialog.reject)
        dialog.exec()

    def handle_new_header(self, input_field, dialog, list_widget):
        new_header = input_field.text().strip()
        if not new_header:
            return None
        if new_header in Options.header_colors:
            return self.show_message("Duplicate Header", "Header already exists. Please choose a different name.")
        dialog.accept()
        color_dialog = QColorDialog(self)
        if color_dialog.exec() != QColorDialog.DialogCode.Accepted:
            return None
        Options.header_colors[new_header] = color_dialog.currentColor().name()
        item_widget = self.create_header_list_item(new_header, list_widget)
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, item_widget)
        Options.header_order.append(new_header)
        Options.save_config()
        self.show_message("Success", "Header successfully created!")
        return None

    def prompt_for_name(self, parent_dialog, sublayout_num):
        name, ok = QInputDialog.getText(parent_dialog, "Enter Name", "   Enter name for sublayout:   ")
        if ok and name:
            key = f'sublayout_games_{sublayout_num}'
            Options.sublayout_names[key] = name
            for button in parent_dialog.findChildren(QPushButton):
                if button.text().startswith(f"Name Sublayout-Games {sublayout_num}:"):
                    button.setText(f"Name Sublayout-Games {sublayout_num}:\n{name}")
                    break
            self.show_message('Success', 'Sublayout name successfully saved!')
            Options.save_config()

    @staticmethod
    def darken_color(color_str):
        color = QColor(color_str)
        h, s, v, a = color.getHsv()
        v = max(0, v - 120)
        return QColor.fromHsv(h, s, v, a).name()

    def choose_color(self, header):
        current_color = Options.header_colors.get(header, '#ffffff')
        color_dialog = QColorDialog(self)
        color_dialog.setCurrentColor(QColor(current_color))
        if color_dialog.exec() == QColorDialog.DialogCode.Accepted:
            Options.header_colors[header] = color_dialog.currentColor().name()
            self.update_button_color(header)
            Options.save_config()
            self.show_message("Success", "Header color successfully saved!")

    def update_button_color(self, header):
        for child in self.findChildren(QPushButton):
            if child.text() == header:
                color = Options.header_colors.get(header, '#ffffff')
                child.setStyleSheet(f"color: black; font-weight: bold; font-size: 20px; background-color: {self.darken_color(color)};")

    def delete_header(self, header, list_widget):
        if any(entry.header == header for entry in Options.all_entries):
            return self.show_message("Cannot Delete Header", "Header has associated entries and cannot be deleted. Remove them first.", QMessageBox.Icon.Warning)
        confirm_box = QMessageBox(QMessageBox.Icon.Question, "Confirm Deletion", f"Are you sure you want to delete header '{header}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, self)
        confirm_box.setDefaultButton(QMessageBox.StandardButton.No)
        if confirm_box.exec() == QMessageBox.StandardButton.Yes:
            Options.header_colors.pop(header, None)
            if header in Options.header_order:
                Options.header_order.remove(header)
            if header in Options.header_inactive:
                Options.header_inactive.remove(header)
            for i in range(list_widget.count()):
                item_widget = list_widget.itemWidget(list_widget.item(i))
                if item_widget.findChild(QPushButton).text() == header:
                    list_widget.takeItem(i)
                    break
            Options.save_config()
            self.show_message("Success", f"Header '{header}' has been successfully deleted!")
            return None
        return None

    def save_header_options(self, list_widget):
        new_header_order, new_header_inactive = [], []
        for i in range(list_widget.count()):
            item_widget = list_widget.itemWidget(list_widget.item(i))
            header_btn = item_widget.findChild(QPushButton)
            if not header_btn:
                continue
            header = header_btn.text()
            new_header_order.append(header)
            cb = item_widget.findChild(QCheckBox, "inactive_checkbox")
            if cb and cb.isChecked():
                new_header_inactive.append(header)
        Options.header_order = new_header_order
        Options.header_inactive = new_header_inactive
        for entry in Options.all_entries:
            entry.details['inactive'] = entry.header in new_header_inactive
        Options.save_config()
        self.show_message("Success", "Settings successfully saved!")

    def open_samba_password_dialog(self):
        self.hide()
        SambaPasswordDialog(self).exec()
        self.show()

    def manage_mount_options(self):
        self.hide()
        self.mount_options_dialog = QDialog(self)
        dialog = self.mount_options_dialog
        dialog.setMinimumSize(500, 300)
        dialog.setWindowTitle("Mount Options")
        layout = QVBoxLayout(dialog)
        for option in Options.mount_options:
            btn_layout = QHBoxLayout()
            drive_btn = QPushButton(option['drive_name'])
            drive_btn.clicked.connect(lambda _, opt=option: self._edit_mount_option(opt, dialog))
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, opt=option: self._delete_mount_option(opt, dialog))
            btn_layout.addWidget(drive_btn, 3)
            btn_layout.addWidget(delete_btn, 1)
            layout.addLayout(btn_layout)
        layout.addStretch(1)
        if Options.mount_options:
            mount_cb = QCheckBox("Mount drives at startup and unmount at shutdown")
            mount_cb.setStyleSheet("color: #6ffff5;")
            mount_cb.setChecked(Options.run_mount_command_on_launch)
            mount_cb.toggled.connect(self._toggle_auto_mount)
            layout.addWidget(mount_cb)
        if len(Options.mount_options) < 3:
            add_btn = QPushButton("New Mount Option")
            add_btn.clicked.connect(lambda: self._edit_mount_option({}, dialog))
            layout.addWidget(add_btn)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        dialog.exec()
        self.show()

    def _toggle_auto_mount(self, checked):
        Options.run_mount_command_on_launch = checked
        Options.save_config()
        self.show_message('Success', 'Mount Options successfully saved!')

    def _edit_mount_option(self, option=None, parent_dialog=None):
        if parent_dialog:
            parent_dialog.close()
        dialog = QDialog(self)
        dialog.setMinimumSize(500, 300)
        dialog.setWindowTitle(f"Edit Mount Option: {option.get('drive_name','')}" if option and 'drive_name' in option else "New Mount Option")
        layout = QVBoxLayout(dialog)
        fields = {}
        field_labels = [('drive_name', "Drive Name:"), ('mount_command', "Mount Command:"), ('unmount_command', "Unmount Command:")]
        for field, label in field_labels:
            layout.addWidget(QLabel(label))
            value = option.get(field, "") if option else ""
            fields[field] = QLineEdit(value)
            layout.addWidget(fields[field])
        btn_layout = QHBoxLayout()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(lambda: self._save_mount_option(fields, option, dialog))
        btn_layout.addWidget(close_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        dialog.exec()
        self.manage_mount_options()

    def _delete_mount_option(self, option, parent_dialog=None):
        confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete '{option['drive_name']}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            Options.mount_options.remove(option)
            Options.save_config()
            self.show_message("Deleted", f"'{option['drive_name']}' successfully deleted!")
            if parent_dialog:
                parent_dialog.close()
                self.manage_mount_options()

    def _save_mount_option(self, fields, option, dialog):
        new_option = {field: fields[field].text().strip() for field in ['drive_name', 'mount_command', 'unmount_command']}
        field_labels = {'drive_name': 'Drive Name', 'mount_command': 'Mount Command', 'unmount_command': 'Unmount Command'}
        for field, label in field_labels.items():
            if not new_option[field]:
                self.show_message("Incomplete Fields", f"{label} is required.")
                return
        for field, label in field_labels.items():
            if any(existing[field].lower() == new_option[field].lower() and existing != option for existing in Options.mount_options):
                self.show_message(f'Duplicate {label}', f'{label} already exists. Please change your input.')
                return
        if option:
            index = Options.mount_options.index(option)
            Options.mount_options[index] = new_option
        else:
            Options.mount_options.append(new_option)
        Options.save_config()
        dialog.close()
        self.show_message('Success', 'Mount Options successfully saved!')


# noinspection PyUnresolvedReferences
class PackageInstallerOptions(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Package Installer Options")
        self.top_label = QLabel("\nFirst you can select 'System Files' in Package Installer. These files will be copied using 'sudo', "
                                "for root privilege. If you have 'System Files' selected, Package Installer will copy these first. This "
                                "allows you to copy files such as 'pacman.conf' to '/etc'.\n\nUnder 'Installer Operations' you can specify how you would like to proceed."
                                "Each action is executed one after the other. Uncheck actions to disable them.\n\n\nTips:\n\n"
                                "It is possible to copy to and from samba shares. Source and/or destination must be saved as follows:\n\n"
                                "'smb://ip/rest of path'\n\nExample: 'smb://192.168.0.53/rest of smb share path'\n\n"
                                "\n'Essential Packages' will be installed using 'sudo pacman -S'.\n\n'Additional Packages' provides access to the Arch User Repository.\n"
                                "Therefore 'yay' must and will be installed.\n\nYou can also define 'Specific Packages'. These packages will be installed (using 'sudo pacman -S') "
                                "only if the corresponding session has been recognized.\nBoth full desktop environments and window managers such as “Hyprland” and others are supported.\n")
        self.installer_operations_button = QPushButton("Installer Operations")
        self.system_files_button = QPushButton("System Files")
        self.package_buttons = {"essential_packages": QPushButton("Essential Packages"), "additional_packages": QPushButton("Additional Packages"), "specific_packages": QPushButton("Specific Packages")}
        self.close_button = QPushButton("Close")
        self.shell_combo = QComboBox()
        self.system_files_widgets = []
        self.installer_operations_widgets = []
        self.essential_packages_widgets = []
        self.additional_packages_widgets = []
        self.specific_packages_widgets = []
        self.current_option_type = None
        self.original_system_files = []
        self._last_shell = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.top_label.setWordWrap(True)
        self.top_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        layout.addWidget(self.top_label)
        shell_box_layout = QHBoxLayout()
        shell_label = QLabel("Select User Shell:")
        self.shell_combo.addItems(USER_SHELL)
        idx = USER_SHELL.index(Options.user_shell) if Options.user_shell in USER_SHELL else 0
        self.shell_combo.setCurrentIndex(idx)
        self._last_shell = USER_SHELL[idx]
        hbox1_buttons = QHBoxLayout()
        self.installer_operations_button.clicked.connect(self.installer_operations)
        self.system_files_button.clicked.connect(self.edit_system_files)
        hbox1_buttons.addWidget(self.installer_operations_button)
        hbox1_buttons.addWidget(self.system_files_button)
        hbox2_buttons = QHBoxLayout()
        for option_type, button in self.package_buttons.items():
            button.clicked.connect(lambda _, ot=option_type: self.edit_packages(ot))
            hbox2_buttons.addWidget(button)
        self.close_button.clicked.connect(self.go_back)
        layout.addLayout(hbox1_buttons)
        layout.addLayout(hbox2_buttons)
        border_style = "border-radius: 6px; border: 1px solid #7aa2f7;"
        style = "color: #a9b1d6; font-size: 16px; font-weight: 500; padding: 4px 8px; background-color: #1a1b26; " + border_style
        shell_label.setStyleSheet(style)
        self.shell_combo.setStyleSheet(style)
        shell_box_layout.addWidget(shell_label)
        shell_box_layout.addWidget(self.shell_combo)
        layout.addLayout(shell_box_layout)
        self.shell_combo.currentIndexChanged.connect(self._on_shell_changed)
        layout.addWidget(self.close_button)
        self.setFixedSize(1100, 750)

    def _on_shell_changed(self):
        selected_shell = self.shell_combo.currentText()
        if selected_shell != self._last_shell and selected_shell in USER_SHELL:
            Options.user_shell = selected_shell
            Options.save_config()
            self._last_shell = selected_shell
            QMessageBox.information(self, "User Shell Changed", f"User Shell has been set to: {selected_shell}")

    def create_dialog(self, title, content_widget, button_callback=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout(dialog)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Close)
        if button_callback:
            button_box.accepted.connect(lambda: button_callback(dialog))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        self._adjust_dialog_size(dialog, content_widget, scroll_area)
        button_box.button(QDialogButtonBox.StandardButton.Close).setFocus()
        return dialog, layout

    def close_current_dialog(self):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QDialog) and widget.isModal() and widget != self:
                widget.accept()
                return

    @staticmethod
    def _adjust_dialog_size(dialog, content_widget, scroll_area):
        content_widget.adjustSize()
        content_size = content_widget.sizeHint()
        screen = QApplication.primaryScreen().availableGeometry()
        margin_w = dialog.geometry().width() - dialog.contentsRect().width() or 350
        margin_h = dialog.geometry().height() - dialog.contentsRect().height() or 200
        optimal_height = min(content_size.height() + margin_h, screen.height())
        optimal_width = min(content_size.width() + margin_w, screen.width())
        dialog.resize(optimal_width, optimal_height)
        dialog.setMinimumSize(min(optimal_width, screen.width() // 3), min(optimal_height, screen.height() // 4))
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setMaximumHeight(min(content_size.height() + margin_h, screen.height() - margin_h))
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setMaximumWidth(min(content_size.width() + margin_w, screen.width() - margin_w))

    @staticmethod
    def _resize_listwidget_to_contents(listwidget, min_width=120, extra=36):
        fm = listwidget.fontMetrics()
        max_width = min_width
        height = 0
        for i in range(listwidget.count()):
            text = listwidget.item(i).text()
            line_widths = [fm.horizontalAdvance(line) for line in text.splitlines()]
            max_width = max(max_width, max(line_widths, default=0) + extra)
            height += fm.lineSpacing() * (len(text.splitlines()) or 1) + 6
        listwidget.setMinimumWidth(max_width + 8)
        listwidget.setMinimumHeight(height + 12)

    def installer_operations(self):
        self.current_option_type = "installer_operations"
        Options.load_config(Options.config_file_path)
        content_widget = QWidget()
        grid_layout = QGridLayout(content_widget)
        select_all_checkbox = QCheckBox("Check/Uncheck All")
        select_all_checkbox.setStyleSheet(f"{global_style} QCheckBox {{color: '#6ffff5'}}")
        grid_layout.addWidget(select_all_checkbox, 0, 1)
        operations = [(text.replace("<br>", "\n"), key) for key, text in PACKAGE_INSTALLER_OPERATION_TEXT.items()]
        self.installer_operations_widgets = []
        for index, (label, operation_key) in enumerate(operations):
            checkbox = QCheckBox(label)
            checkbox.setChecked(operation_key in Options.installer_operations)
            checkbox.setStyleSheet(f"{global_style} QCheckBox {{ color: #c8beff; }}")
            grid_layout.addWidget(checkbox, index, 0)
            self.installer_operations_widgets.append((checkbox, operation_key))
        install_yay_checkbox = next((cb for cb, key in self.installer_operations_widgets if key == 'install_yay'), None)
        install_additional_packages_checkbox = next((cb for cb, key in self.installer_operations_widgets if key == 'install_additional_packages'), None)
        def handle_dependencies():
            if install_additional_packages_checkbox and install_yay_checkbox:
                if install_additional_packages_checkbox.isChecked():
                    install_yay_checkbox.setEnabled(False)
                    install_yay_checkbox.setChecked(True)
                else:
                    install_yay_checkbox.setEnabled(True)
                    if select_all_checkbox.checkState() == Qt.CheckState.Unchecked:
                        install_yay_checkbox.setChecked(False)
            update_select_all_state()
        def toggle_all_checkboxes():
            checked = select_all_checkbox.checkState() == Qt.CheckState.Checked
            for operation_checkbox, key in self.installer_operations_widgets:
                if key != 'install_yay' and key != 'install_additional_packages':
                    if operation_checkbox.isEnabled():
                        operation_checkbox.setChecked(checked)
            if install_additional_packages_checkbox:
                install_additional_packages_checkbox.setChecked(checked)
        def update_select_all_state():
            enabled_checkboxes = [cb for cb, key in self.installer_operations_widgets if cb.isEnabled() and not (key == 'install_yay' and install_additional_packages_checkbox and install_additional_packages_checkbox.isChecked())]
            if not enabled_checkboxes:
                return
            checked_count = sum(1 for cb in enabled_checkboxes if cb.isChecked())
            block = select_all_checkbox.blockSignals(True)
            if checked_count == 0:
                select_all_checkbox.setCheckState(Qt.CheckState.Unchecked)
            elif checked_count == len(enabled_checkboxes):
                select_all_checkbox.setCheckState(Qt.CheckState.Checked)
            else:
                select_all_checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
            select_all_checkbox.blockSignals(block)
        select_all_checkbox.stateChanged.connect(toggle_all_checkboxes)
        for checkbox, option_key in self.installer_operations_widgets:
            checkbox.stateChanged.connect(update_select_all_state)
            if option_key == 'install_additional_packages':
                checkbox.stateChanged.connect(handle_dependencies)
        handle_dependencies()
        update_select_all_state()
        dialog = QDialog(self)
        dialog.setWindowTitle("Package Installer Operations")
        layout = QVBoxLayout(dialog)
        layout.addWidget(content_widget)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Close)
        button_box.accepted.connect(lambda: self.save_installer_options())
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        button_box.button(QDialogButtonBox.StandardButton.Close).setFocus()
        content_widget.adjustSize()
        dialog.adjustSize()
        dialog.setMinimumSize(dialog.sizeHint())
        dialog.exec()

    @staticmethod
    def _create_package_list_widget(packages, is_specific=False):
        widgets = []
        for package in packages:
            if is_specific and isinstance(package, dict):
                package_name = package['package']
                session = package['session']
                item_text = f"{package_name}\n({session})"
            else:
                item_text = package
            item = QListWidgetItem(item_text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            list_widget = QListWidget()
            list_widget.addItem(item)
            list_widget.setMaximumHeight(40 if not is_specific else 60)
            widgets.append(list_widget)
        return widgets

    def edit_system_files(self):
        Options.load_config(Options.config_file_path)
        content_widget = QWidget()
        grid_layout = QGridLayout(content_widget)
        system_files = Options.system_files
        self.system_files_widgets = []
        self.original_system_files = []
        max_text_width = 0
        for file_index, file_info in enumerate(system_files):
            file_source = file_destination = ""
            if isinstance(file_info, dict):
                file_source = file_info.get('source', '')
                file_destination = file_info.get('destination', '')
            elif isinstance(file_info, str):
                parts = file_info.split(' -> ', 1)
                if len(parts) == 2:
                    file_source, file_destination = parts[0].strip(), parts[1].strip()
            else:
                continue
            self.original_system_files.append({'source': file_source, 'destination': file_destination})
            item_text = f"{file_source}  --->  {file_destination}"
            display_text = item_text
            for old_text, new_text in Options.text_replacements:
                display_text = display_text.replace(old_text, new_text)
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, {'source': file_source, 'destination': file_destination})
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            list_widget = QListWidget()
            list_widget.addItem(item)
            list_widget.setMaximumHeight(40)
            text_width = list_widget.fontMetrics().horizontalAdvance(display_text)
            max_text_width = max(max_text_width, text_width)
            grid_layout.addWidget(list_widget, file_index, 0)
            self.system_files_widgets.append(list_widget)
        for list_widget in self.system_files_widgets:
            list_widget.setMinimumWidth(max_text_width)
        dialog, layout = self.create_dialog("Edit 'System Files' [Uncheck to remove]", content_widget, lambda dlg: self.save_installer_options(dlg, "system_files"))
        add_system_files_button = QPushButton("Add 'System File'")
        add_system_files_button.clicked.connect(self.add_system_files)
        layout.insertWidget(1, add_system_files_button)
        dialog.exec()

    def add_system_files(self):
        self.close_current_dialog()
        try:
            files, _ = QFileDialog.getOpenFileNames(self, "Select 'System File'")
            if not files:
                return
            destination_dir = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
            if not destination_dir:
                return
            if not isinstance(Options.system_files, list):
                Options.system_files = []
            added_files = []
            for file in files:
                source = str(file)
                destination = str(Path(destination_dir).joinpath(Path(file).name))
                if not any(isinstance(item, dict) and str(item.get('source')) == source for item in Options.system_files):
                    Options.system_files.append({'source': source, 'destination': destination})
                    added_files.append(file)
            if added_files:
                Options.save_config()
                msg = "Files successfully added!" if len(added_files) > 1 else f"'{added_files[0]}' successfully added!"
                QMessageBox.information(self, "'System File'", msg, QMessageBox.StandardButton.Ok)
                self.edit_system_files()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while adding 'System File': {str(e)}", QMessageBox.StandardButton.Ok)

    def manage_packages(self, title, option_type, add_button_text, is_specific=False):
        self.current_option_type = option_type
        content_widget = QWidget()
        grid_layout = QGridLayout(content_widget)
        Options.load_config(Options.config_file_path)
        packages = getattr(Options, option_type, [])
        package_widgets = self._create_package_list_widget(packages, is_specific)
        for index, widget in enumerate(package_widgets):
            grid_layout.addWidget(widget, index // 5, index % 5)
        setattr(self, f"{option_type}_widgets", package_widgets)
        dialog, layout = self.create_dialog(title, content_widget, lambda dlg: self.save_installer_options(dlg, option_type))
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Type to filter packages...")
        search_input.textChanged.connect(lambda text: self._filter_packages(text, package_widgets))
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        layout.insertLayout(1, search_layout)
        add_package_button = QPushButton(add_button_text)
        add_package_button.clicked.connect(lambda: self.add_package(option_type))
        layout.insertWidget(2, add_package_button)
        if not is_specific:
            batch_button = QPushButton(f"Add '{option_type.replace('_', ' ').title()}' in Batches")
            batch_button.clicked.connect(lambda: self.batch_add_packages(option_type))
            layout.insertWidget(3, batch_button)
        dialog.exec()

    @staticmethod
    def _filter_packages(search_text, package_widgets):
        search_text = search_text.lower()
        for widget in package_widgets:
            if isinstance(widget, QListWidget) and widget.count() > 0:
                item = widget.item(0)
                widget.setVisible(search_text in item.text().lower())

    def edit_packages(self, option_type):
        Options.load_config(Options.config_file_path)
        is_specific = option_type == "specific_packages"
        title = f"Edit '{option_type.replace('_', ' ').title()}' [Uncheck to remove]"
        add_button_text = f"Add '{option_type.replace('_', ' ').title().replace(' Packages', ' Package')}'"
        self.manage_packages(title, option_type, add_button_text, is_specific)

    def add_package(self, option_type):
        self.close_current_dialog()
        if option_type == "specific_packages":
            self._add_specific_package()
        else:
            package_type_name = option_type.replace("_", " ").title().replace(" Packages", " Package")
            package_name, ok = QInputDialog.getText(self, f"Add '{package_type_name}'", f"                              Enter Package Name:                              ")
            if ok and package_name.strip():
                current_packages = getattr(Options, option_type, [])
                if package_name not in current_packages:
                    current_packages.append(package_name.strip())
                    setattr(Options, option_type, current_packages)
                    Options.save_config()
                    QMessageBox.information(self, "Package Added", f"Package '{package_name}' successfully added!", QMessageBox.StandardButton.Ok)
                else:
                    QMessageBox.warning(self, "Duplicate Package", f"Package '{package_name}' already exists.", QMessageBox.StandardButton.Ok)
                self.edit_packages(option_type)

    def batch_add_packages(self, option_type):
        self.close_current_dialog()
        text, ok = QInputDialog.getMultiLineText(self, f"Add '{option_type.replace('_', ' ').title()}' in Batches", "                         Enter package names (one per line):                         ")
        if ok and text.strip():
            packages = [pkg.strip() for pkg in text.splitlines() if pkg.strip()]
            current_packages = set(getattr(Options, option_type, []))
            added_packages = []
            duplicates = []
            for package in packages:
                if package not in current_packages:
                    added_packages.append(package)
                    current_packages.add(package)
                else:
                    duplicates.append(package)
            setattr(Options, option_type, list(current_packages))
            Options.save_config()
            if duplicates:
                dup_list = "\n".join(duplicates)
                title = "Duplicate Package" if len(duplicates) == 1 else "Duplicate Packages"
                plural = 's already exist' if len(duplicates) > 1 else ' already exists'
                QMessageBox.warning(self, title, f"The following package{plural}:\n\n{dup_list}", QMessageBox.StandardButton.Ok)
            if added_packages:
                added_list = "\n".join(added_packages)
                title = "Add Package" if len(added_packages) == 1 else "Add Packages"
                message = f"The following package{'s have' if len(added_packages) > 1 else ' was'} successfully added:\n\n{added_list}"
                QMessageBox.information(self, title, message, QMessageBox.StandardButton.Ok)
            self.edit_packages(option_type)

    def _add_specific_package(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add 'Specific Package'")
        layout = QVBoxLayout(dialog)
        field_height = 38
        form_layout = QFormLayout()
        package_input = QLineEdit()
        package_input.setFixedHeight(field_height)
        form_layout.addRow("Package Name:", package_input)
        session_combo = QComboBox()
        session_combo.setStyleSheet("color: #ffffff; background-color: #555582; padding: 5px 5px;")
        session_combo.addItems(SESSIONS)
        session_combo.setFixedHeight(field_height)
        form_layout.addRow("Session:", session_combo)
        layout.addLayout(form_layout)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setFixedWidth(650)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            package_name = package_input.text().strip()
            session = session_combo.currentText()
            if not package_name:
                QMessageBox.warning(self, "Missing Information", "Package name is required.", QMessageBox.StandardButton.Ok)
                return
            new_package = {'package': package_name, 'session': session}
            exists = any(isinstance(pkg, dict) and pkg.get('package') == package_name and pkg.get('session') == session for pkg in Options.specific_packages)
            if not exists:
                Options.specific_packages.append(new_package)
                Options.save_config()
                QMessageBox.information(self, "Package Added", f"Package '{package_name}' for '{session}' successfully added!", QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(self, "Duplicate Package", f"Package '{package_name}' for '{session}' already exists.", QMessageBox.StandardButton.Ok)
            self.edit_packages("specific_packages")

    def _get_checked_items(self, widgets, option_type):
        if option_type == "system_files":
            return self._get_system_files_from_widgets()
        elif option_type == "specific_packages":
            return self._get_specific_packages_from_widgets()
        else:
            return self._get_checked_items_from_widgets(widgets)

    @staticmethod
    def _get_checked_items_from_widgets(widget_list):
        return [widget.item(i).text() for widget in widget_list if isinstance(widget, QListWidget)
                for i in range(widget.count())
                if widget.item(i).checkState() == Qt.CheckState.Checked]

    def _get_system_files_from_widgets(self):
        files = []
        for widget in self.system_files_widgets:
            if isinstance(widget, QListWidget):
                for i in range(widget.count()):
                    item = widget.item(i)
                    if item.checkState() == Qt.CheckState.Checked:
                        original_data = item.data(Qt.ItemDataRole.UserRole)
                        if original_data and isinstance(original_data, dict):
                            source = original_data.get('source', '')
                            destination = original_data.get('destination', '')
                            files.append({'source': source, 'destination': destination})
        return files

    def _get_specific_packages_from_widgets(self):
        packages = []
        for widget in self.specific_packages_widgets:
            if isinstance(widget, QListWidget):
                for i in range(widget.count()):
                    item = widget.item(i)
                    if item.checkState() == Qt.CheckState.Checked:
                        item_text = item.text()
                        if '\n' in item_text:
                            package_name, session_part = item_text.split('\n', 1)
                            session = session_part.strip('()')
                        else:
                            parts = item_text.partition('(')
                            package_name = parts[0].strip()
                            session = parts[2].partition(')')[0].strip() if parts[1] else ""
                        packages.append({'package': package_name, 'session': session})
        return packages

    def save_installer_options(self, dialog=None, option_type=None):
        try:
            current_type = option_type or self.current_option_type
            if current_type == "installer_operations":
                updated_list = [option_key for checkbox, option_key in self.installer_operations_widgets if checkbox.isChecked()]
            else:
                widget_list = getattr(self, f"{current_type}_widgets", [])
                updated_list = self._get_checked_items(widget_list, current_type)
            setattr(Options, current_type, updated_list)
            Options.save_config()
            QMessageBox.information(self, "Saved", "Settings have been successfully saved!", QMessageBox.StandardButton.Ok)
            if dialog and option_type:
                dialog.accept()
                if option_type == "installer_operations":
                    self.installer_operations()
                elif option_type == "system_files":
                    self.edit_system_files()
                elif option_type in ["essential_packages", "additional_packages", "specific_packages"]:
                    self.edit_packages(option_type)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving: {str(e)}", QMessageBox.StandardButton.Ok)
            return False

    def go_back(self):
        self.close()
        self.parent().show()


# noinspection PyUnresolvedReferences
class PackageInstallerLauncher:
    def __init__(self, parent=None):
        self.parent = parent
        self.config = getattr(parent, 'config', {}) if parent else {}
        self.drive_manager = DriveManager()
        self.failed_attempts = getattr(parent, 'failed_attempts', 0)
        self.package_installer_thread = None
        self.package_installer_dialog = None
        self.sudo_checkbox = None

    def launch(self):
        if self.parent:
            self.parent.hide()
        try:
            self.confirm_and_start_package_installer()
        finally:
            if self.parent:
                self.parent.show()

    def confirm_and_start_package_installer(self):
        installer_operations = self.config.get('installer_operations', [])
        _, _, installer_tooltips = Options.generate_tooltip()
        operations_text = {k: v.replace("&&", "&") for k, v in PACKAGE_INSTALLER_OPERATION_TEXT.items()}
        dialog, content_widget, content_layout = self._create_installer_dialog()
        self._display_operations(installer_operations, operations_text, installer_tooltips, content_layout)
        if self._show_dialog_and_get_result(dialog, content_widget):
            self._handle_dialog_accepted(installer_operations)

    @staticmethod
    def _create_installer_dialog():
        dialog = QDialog()
        dialog.setWindowTitle('Package Installer')
        layout = QVBoxLayout()
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        header_label = QLabel("<span style='font-size: 18px;'>Package Installer will perform the following operations:<br></span>")
        header_label.setTextFormat(Qt.TextFormat.RichText)
        content_layout.addWidget(header_label)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        dialog.setLayout(layout)
        return dialog, content_widget, content_layout

    def _display_operations(self, installer_operations, operations_text, installer_tooltips, content_layout):
        for i, opt in enumerate(installer_operations):
            if opt in operations_text:
                has_tooltip = opt in installer_tooltips and installer_tooltips[opt]
                self._add_operation_row(i, operations_text[opt], has_tooltip, installer_tooltips.get(opt, ""), content_layout)

    @staticmethod
    def _add_operation_row(index, text, has_tooltip, tooltip_text, layout):
        style_color = "#9891c2;" if has_tooltip else "#c8beff;"
        text_style = "text-decoration: underline dotted;" if has_tooltip else ""
        tooltip_icon = "💡" if has_tooltip else ""
        operation_text = f"{tooltip_icon}<span style='font-size: 16px; padding: 5px; color: {style_color}{text_style}'>{text}</span>"
        row_layout = QHBoxLayout()
        number_label = QLabel(f"{index + 1}:")
        number_label.setStyleSheet("font-size: 16px; padding: 5px; qproperty-alignment: 'AlignLeft'")
        operation_label = QLabel(operation_text)
        operation_label.setTextFormat(Qt.TextFormat.RichText)
        operation_label.setStyleSheet("font-size: 16px; padding: 5px; qproperty-alignment: 'AlignLeft'")
        if has_tooltip:
            operation_label.setToolTip(tooltip_text)
            operation_label.setCursor(Qt.CursorShape.WhatsThisCursor)
            operation_label.setToolTipDuration(30000)
        row_layout.addWidget(number_label)
        row_layout.addWidget(operation_label)
        row_layout.addStretch(1)
        layout.addLayout(row_layout)

    def _show_dialog_and_get_result(self, dialog, content_widget):
        confirm_label = QLabel("<span style='font-size: 16px;'>Start Package Installer?<br>(Check 'Enter sudo password' if a sudo password is set.)<br></span>")
        button_layout = QHBoxLayout()
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)
        button_box.button(QDialogButtonBox.StandardButton.Yes).setText('Yes')
        button_box.button(QDialogButtonBox.StandardButton.No).setText('No')
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        self.sudo_checkbox = QCheckBox("Enter sudo password")
        self.sudo_checkbox.setStyleSheet("font-size: 16px; color: #6ffff5")
        if self.failed_attempts != 0:
            self.sudo_checkbox.setText("Sudo password must be entered!")
            self.sudo_checkbox.setChecked(True)
            self.sudo_checkbox.setEnabled(False)
            self.sudo_checkbox.setStyleSheet("color: #787878")
        button_layout.addWidget(self.sudo_checkbox)
        button_layout.addWidget(button_box)
        content_widget.layout().addWidget(confirm_label)
        content_widget.layout().addLayout(button_layout)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        content_size = content_widget.sizeHint()
        dialog.resize(min(content_size.width() + 40, screen_geometry.width()), min(content_size.height() + 40, screen_geometry.height()))
        button_box.button(QDialogButtonBox.StandardButton.No).setFocus()
        return dialog.exec() == QDialog.DialogCode.Accepted

    def start_package_installer_thread(self, sudo_password):
        self.package_installer_thread = PackageInstallerThread(sudo_password)
        self.package_installer_dialog = PackageInstallerDialog(self.parent)
        self.package_installer_thread.started.connect(self.show_package_installer_dialog)
        self.package_installer_thread.passwordFailed.connect(self.on_password_failed)
        self.package_installer_thread.passwordSuccess.connect(self.on_password_success)
        self.package_installer_thread.outputReceived.connect(self.package_installer_dialog.update_operation_dialog)
        self.package_installer_thread.taskStatusChanged.connect(self.package_installer_dialog.update_task_checklist_status)
        self.package_installer_thread.finished.connect(self.on_package_installer_finished)
        self.package_installer_thread.start()

    def _handle_dialog_accepted(self, installer_operations):
        if "copy_system_files" in installer_operations:
            system_files = self.config.get('system_files', [])
            paths_to_check = []
            for file in system_files:
                if isinstance(file, dict):
                    for key in ('source', 'destination'):
                        if key in file:
                            paths_to_check.append(file[key])
            drives_to_mount = self.drive_manager.check_drives_to_mount(paths_to_check)
            if drives_to_mount and not self.drive_manager.mount_required_drives(drives_to_mount, self.parent):
                return
        if self.sudo_checkbox.isChecked():
            self.show_sudo_password_dialog()
        else:
            self.start_package_installer_thread("")

    def show_package_installer_dialog(self):
        try:
            self.package_installer_dialog.exec()
        finally:
            self.drive_manager.unmount_drives()

    def show_sudo_password_dialog(self):
        dialog = SudoPasswordDialog(self.parent)
        dialog.sudo_password_entered.connect(self.on_sudo_password_entered)
        dialog.update_failed_attempts(self.failed_attempts)
        dialog.exec()

    def on_sudo_password_entered(self, sudo_password):
        self.start_package_installer_thread(sudo_password)

    def on_password_failed(self):
        self.failed_attempts += 1
        if self.parent:
            self.parent.failed_attempts = self.failed_attempts
        if self.package_installer_dialog:
            self.package_installer_dialog.update_failed_attempts(self.failed_attempts)
            self.package_installer_dialog.auth_failed = True
            error_msg = ("<p style='color: #ff4a4d; font-size: 18px; font-weight: bold;'>"
                         "<br>Authentication failed. Canceling process to prevent account lockout."
                         "<br>This could be due to:""<ul>"
                         "<li>Incorrect or missing password</li>"
                         "<li>Password is unauthorized</li>"
                         "<li>User not in sudoers file</li>"
                         "<li>Sudo configuration issue</li>""</ul>"
                         "Package Installer has been aborted to protect your system.""</p>")
            self.package_installer_dialog.update_operation_dialog(error_msg)
            self.package_installer_dialog.completed_message_shown = True
            self.package_installer_dialog.update_timer.stop()
            self.package_installer_dialog.has_error = True
            self.package_installer_dialog.ok_button.setEnabled(True)
        if self.package_installer_thread:
            self.package_installer_thread.terminated = True
            self.package_installer_thread.quit()
            try:
                if not self.package_installer_thread.wait(1500):
                    self.package_installer_thread.terminate()
            except RuntimeError:
                pass

    def on_password_success(self):
        self.failed_attempts = 0
        if self.parent:
            self.parent.failed_attempts = 0
        if self.package_installer_dialog:
            self.package_installer_dialog.update_failed_attempts(self.failed_attempts)
            self.package_installer_dialog.auth_failed = False

    def on_package_installer_finished(self):
        self.package_installer_thread = None
        self.package_installer_dialog = None


# noinspection PyUnresolvedReferences
class PackageInstallerDialog(QDialog):
    outputReceived = pyqtSignal(str, str)
    font_main = "DejaVu Sans Mono"
    font_subprocess = "Hack"
    STYLE_MAP = {style: f"font-family: {font}; font-size: {size}px; color: {color}; padding: 5px; line-height: {line};" for style, (font, size, color, line) in {
        "operation": (font_main, 16, "#6ffff5", 1.2), "info": (font_main, 15, "#ceec9e", 1.0), "subprocess": (font_subprocess, 13, "#f9e7ff", 0.6), "success": (font_main, 15, "#8fffab", 1.0),
        "warning": (font_main, 15, "#ffaa00", 1.0), "error": (font_main, 15, "#ff5555", 1.0)}.items()}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(80)
        self.shadow.setXOffset(15)
        self.shadow.setYOffset(15)
        self.shadow.setColor(QColor(0, 0, 0, 160))
        self.task_status = {}
        self.task_descriptions = {}
        self.installer_thread = None
        self.current_task = None
        self.completed_message_shown = False
        self.has_error = False
        self.auth_failed = False
        self.layout = QHBoxLayout(self)
        self.left_panel = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.text_edit = QTextEdit()
        self.failed_attempts_label = QLabel(self)
        self.right_panel = QVBoxLayout()
        self.checklist_label = QLabel("Pending Operations:")
        self.checklist = QListWidget()
        self.elapsed_time_label = QLabel("\nElapsed time:\n00s\n")
        self.elapsed_time_label.setGraphicsEffect(self.shadow)
        self.ok_button = QPushButton("Close")
        self.ok_button.setFixedSize(145, 40)
        self.setFixedSize(1400, 1100)
        self.update_timer = QTimer(self)
        self.timer = QElapsedTimer()
        self.setup_ui()

    def setup_ui(self):
        self._apply_global_styles()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.text_edit.setReadOnly(True)
        self.text_edit.setHtml("<p style='color: #55ff55; font-size: 20px; text-align: center; margin-top: 25px;'><b>Package Installer</b><br>Initialization completed. Starting Package Installer</span></p>")
        self.scroll_area.setWidget(self.text_edit)
        self.left_panel.addWidget(self.scroll_area)
        border_style = "border-radius: 8px; border-right: 1px solid #7aa2f7; border-top: 1px solid #7aa2f7; border-bottom: 1px solid #7aa2f7; border-left: 4px solid #7aa2f7;"
        self.checklist_label.setStyleSheet(f"""color: #7dcfff; font-size: 18px; font-weight: bold; padding: 10px; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #24283b, stop:1 #414868); {border_style}""")
        self.checklist.setStyleSheet(f"""QListWidget {{background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #24283b, stop:1 #414868); font-size: 15px; padding: 4px; {border_style}}} QListWidget::item {{padding: 4px; border-radius: 4px; border: 1px solid transparent;}}""")
        self.checklist.setFixedWidth(370)
        self.update_timer.timeout.connect(self.update_elapsed_time)
        self.timer.start()
        self.update_timer.start(1000)
        self._setup_layout()

    def _apply_global_styles(self):
        self.setStyleSheet("""QDialog {background-color: #1a1b26; border-radius: 15px; border: 1px solid #2d2d44;} QScrollArea {background-color: #181b28; border: 1px solid #414868; border-radius: 10px;}
        QTextEdit {background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #11141d, stop:1 #222a3b); color: #c0caf5; border: none; border-radius: 8px;} QLabel {color: #c0caf5; font-size: 16px;}""")

    def _setup_layout(self):
        label_border_style = "border-radius: 8px; border-right: 1px solid #7aa2f7; border-top: 1px solid #7aa2f7; border-bottom: 1px solid #7aa2f7; border-left: 4px solid #7aa2f7;"
        self.right_panel.addWidget(self.checklist_label)
        self.right_panel.addWidget(self.checklist)
        self.right_panel.addStretch(1)
        self.elapsed_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.elapsed_time_label.setStyleSheet(f"""color: #7dcfff; font-size: 17px; {label_border_style} background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #24283b, stop:1 #414868); text-align: center; font-weight: bold; padding: 3px;""")
        self.right_panel.addWidget(self.elapsed_time_label)
        self.right_panel.addStretch(1)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setEnabled(False)
        button_container = QHBoxLayout()
        button_container.addStretch()
        button_container.addWidget(self.ok_button)
        self.right_panel.addLayout(button_container)
        self.failed_attempts_label.setStyleSheet("""color: #f7768e; font-size: 16px; font-weight: bold; padding: 10px; margin-top: 8px; border-radius: 8px; background-color: rgba(247, 118, 142, 0.15); border-left: 4px solid #f7768e;""")
        self.left_panel.addWidget(self.failed_attempts_label)
        self.failed_attempts_label.setVisible(False)
        self.layout.addLayout(self.left_panel, 3)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.right_panel, 1)

    def initialize_checklist(self):
        self.checklist.clear()
        self.task_status.clear()
        cleaned_tasks = [(tid, desc.replace("...", "").replace("with 'yay'", "")) for tid, desc in self.task_descriptions]
        for task_id, desc in cleaned_tasks:
            item = QListWidgetItem(desc)
            item.setData(Qt.ItemDataRole.UserRole, task_id)
            item.setIcon(QIcon.fromTheme("dialog-question"))
            item.setForeground(QColor("#7c7c7c"))
            self.checklist.addItem(item)
            self.task_status[task_id] = "pending"
        total_height = sum(self.checklist.sizeHintForRow(i) for i in range(self.checklist.count()))
        total_height += 2 * self.checklist.frameWidth()
        self.checklist.setFixedHeight(max(total_height, 40))

    def update_task_checklist_status(self, task_id, status):
        if task_id not in self.task_status:
            return
        self.task_status[task_id] = status
        if status in ("error", "warning"):
            self.has_error = True
        status_config = {"success": ("#8fffab", "dialog-ok-apply"), "error": ("#ff5555", "dialog-error"), "warning": ("#e0af68", "dialog-warning"), "in_progress": ("#7dcfff", "media-playback-start")}
        if status in status_config:
            color, icon_name = status_config[status]
            for i in range(self.checklist.count()):
                item = self.checklist.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == task_id:
                    item.setIcon(QIcon.fromTheme(icon_name))
                    item.setForeground(QColor(color))
                    item.setBackground(QColor(*QColor(color).getRgb()[:3], 25))
                    self.checklist.scrollToItem(item)
                    break

    def update_operation_dialog(self, output: str, message_type: str = "info"):
        cursor = self.text_edit.textCursor()
        if "/var/lib/pacman/db.lck" in output:
            cursor.insertHtml(f"""<hr style='border: none; margin: 10px 20px; border-top: 1px dashed rgba(247, 118, 142, 0.4);'>
            <div style='padding: 15px; margin: 10px; border-radius: 10px; border-left: 4px solid #f7768e;'><p style='color: #f7768e; font-size: 18px; text-align: center;'><b>⚠️ Installation Aborted</b><br>
            <span style='font-size: 16px;'>'/var/lib/pacman/db.lck' detected!</span><br><span style='color: #c0caf5; font-size: 14px;'>Remove using: <code>sudo rm -r /var/lib/pacman/db.lck</code></span></p></div>""")
            self._finalize_text_edit(cursor)
            self.ok_button.setEnabled(True)
            self.ok_button.setFocus()
            self.update_timer.stop()
            if hasattr(self, 'installer_thread') and self.installer_thread and self.installer_thread.isRunning():
                self.installer_thread.terminate()
            return
        elif message_type == "finish":
            if not self.auth_failed:
                self._show_completion_message()
            return
        elif message_type == "task_list":
            try:
                self.task_descriptions = ast.literal_eval(output)
                self.initialize_checklist()
            except (SyntaxError, ValueError):
                pass
            return
        if message_type not in self.STYLE_MAP and "<span " not in output:
            return
        style = self.STYLE_MAP.get(message_type, "")
        if message_type == "operation":
            html_content = f"""<hr style='border: none; margin: 15px 30px; border-top: 1px dashed rgba(111, 255, 245, 0.3);'><div style='padding: 10px; border-radius: 8px; margin: 5px 0;'><p style='{style}'>{output}</p></div><br>"""
        else:
            lines = [f"<p style='{style}'>{line}</p>" for line in output.splitlines() if line.strip()]
            html_content = "\n".join(lines) + "<br>"
        if "<span " in output:
            html_content = output
        for old, new in Options.text_replacements:
            html_content = html_content.replace(old, new)
        self._finalize_text_edit(cursor, html_content)

    def _finalize_text_edit(self, cursor, html_content=None):
        cursor.movePosition(QTextCursor.MoveOperation.End)
        if html_content:
            cursor.insertHtml(html_content)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.verticalScrollBar().setValue(self.text_edit.verticalScrollBar().maximum())

    def _show_completion_message(self):
        if self.completed_message_shown or self.auth_failed:
            return
        self.completed_message_shown = True
        self.update_timer.stop()
        color = "#e0af68" if self.has_error else "#8fffab"  # Amber für warning, green für success
        summary_text = "Completed with issues" if self.has_error else "Successfully Completed"
        icon = "⚠️" if self.has_error else "✅"
        message = f"Package Installer {'completed with warnings/errors' if self.has_error else 'successfully completed all operations<br>'}"
        r, g, b = (224, 175, 104) if self.has_error else (158, 206, 106)
        cursor = self.text_edit.textCursor()
        cursor.insertHtml(f"""<hr style='border: none; margin: 25px 50px; border-top: 2px solid {color};'><div style='text-align: center; padding: 20px; margin: 15px 30px;
        border-radius: 15px; border: 1px solid rgba({r}, {g}, {b}, 0.3);'><p style='color: {color}; font-size: 20px; font-weight: bold;'>{icon} {summary_text}</p><p style='color: {color}; font-size: 18px;'>{message}</p></div>""")
        self.ok_button.setEnabled(True)
        self.ok_button.setFocus()
        self.checklist_label.setText(f"{icon} {summary_text}")
        base_style = f"""color: {color}; font-size: 18px; font-weight: bold; padding: 10px; background-color: rgba({r}, {g}, {b}, 0.15); border-radius: 8px; border-right: 1px solid #7aa2f7; border-top: 1px solid #7aa2f7; border-bottom: 1px solid #7aa2f7; border-left: 4px solid #7aa2f7;"""
        self.checklist_label.setStyleSheet(base_style)
        self.text_edit.setTextCursor(cursor)

    def update_elapsed_time(self):
        elapsed = int(self.timer.elapsed() / 1000)
        h, remainder = divmod(elapsed, 3600)
        m, s = divmod(remainder, 60)
        if h:
            time_text = f"\nElapsed time:\n{h:02}h {m:02}m {s:02}s\n"
        elif m:
            time_text = f"\nElapsed time:\n{m:02}m {s:02}s\n"
        else:
            time_text = f"\nElapsed time:\n{s:02}s\n"
        self.elapsed_time_label.setText(time_text)

    def update_failed_attempts(self, failed_attempts):
        if failed_attempts > 0:
            text = f"⚠️ Failed Authentication Attempts: {failed_attempts}"
            self.failed_attempts_label.setText(text)
            self.failed_attempts_label.setVisible(True)
            self.auth_failed = True
            self.ok_button.setEnabled(True)
            self.failed_attempts_label.setStyleSheet("""color: #f7768e; font-size: 16px; font-weight: bold; padding: 12px; margin-top: 10px; border-radius: 8px; background-color: rgba(247, 118, 142, 0.15);
            border-left: 4px solid #f7768e; border-bottom: 1px solid rgba(247, 118, 142, 0.3);""")

    def keyPressEvent(self, event):
        key_map = {Qt.Key.Key_Down: lambda: (self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum()), self.ok_button.setFocus()),
                   Qt.Key.Key_Escape: lambda: (event.ignore() if not self.completed_message_shown else self.close()), Qt.Key.Key_Tab: self.focusNextChild}
        handler = key_map.get(event.key())
        if handler:
            handler()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        if not self.completed_message_shown and not self.auth_failed:
            event.ignore()
        else:
            if hasattr(self, 'installer_thread') and self.installer_thread and self.installer_thread.isRunning():
                self.installer_thread.terminated = True
                self.installer_thread.quit()
                if not self.installer_thread.wait(1000):
                    self.installer_thread.terminate()
            super().closeEvent(event)


# noinspection PyUnresolvedReferences
class PackageInstallerThread(QThread):
    started = pyqtSignal()
    outputReceived = pyqtSignal(str, str)
    passwordFailed = pyqtSignal()
    passwordSuccess = pyqtSignal()
    taskStatusChanged = pyqtSignal(str, str)
    finished = pyqtSignal()

    def __init__(self, sudo_password):
        super().__init__()
        self.enabled_tasks = None
        self.task_descriptions = None
        self.sudo_password = SecureString(sudo_password)
        self.auth_failed = self.has_error = self.terminated = False
        self.temp_dir = self.askpass_script_path = self.current_task = None
        self.task_status = {}
        self._installed_packages_cache = {}

    def run(self):
        self.started.emit()
        self.prepare_tasks()
        try:
            if self.terminated:
                return
            if not self.test_sudo_access():
                self.auth_failed = True
                self.passwordFailed.emit()
                return
            self.passwordSuccess.emit()
            if not self.auth_failed and not self.terminated:
                self.start_package_installer()
        except Exception as e:
            self.outputReceived.emit(f"Critical error during execution: {e}", "error")
            self.has_error = True
        finally:
            self.cleanup_temp_files()
            self.sudo_password.clear()

    def prepare_tasks(self):
        Options.load_config(Options.config_file_path)
        installer_operations = Options.installer_operations
        tasks = self._define_base_tasks()
        for service_task_id, (desc, name, pkgs) in self._define_service_tasks().items():
            def make_task(task_name, task_pkgs):
                return lambda: self.setup_service_with_packages(task_name, list(task_pkgs))
            tasks[service_task_id] = (desc, make_task(name, pkgs))
        tasks.update({"remove_orphaned_packages": ("Removing orphaned packages...", self.remove_orphaned_packages), "clean_cache": ("Cleaning cache...", self.clean_cache)})
        self.enabled_tasks = {tid: t for tid, t in tasks.items() if tid in installer_operations}
        self.task_descriptions = [(tid, desc) for tid, (desc, _) in self.enabled_tasks.items()]
        self.outputReceived.emit(str(self.task_descriptions), "task_list")

    def _define_base_tasks(self):
        return {"copy_system_files": ("Copying 'System Files'...", lambda: self.copy_files(self.parse_system_files(Options.system_files))),
                "update_mirrors": ("Updating mirrors...", lambda: self.update_mirrors("update_mirrors")),
                "set_user_shell": ("Setting user shell...", lambda: self.set_user_shell("set_user_shell")),
                "update_system": ("Updating system...", lambda: self.update_system("update_system")),
                "install_kernel_header": ("Installing kernel headers...", lambda: self.install_kernel_header("install_kernel_header")),
                "install_essential_packages": ("Installing 'Essential Packages'...", lambda: self.batch_install(Options.essential_packages, "Essential Package")),
                "install_yay": ("Installing 'yay'...", self.install_yay),
                "install_additional_packages": ("Installing 'Additional Packages' with 'yay'...", lambda: self.batch_install(Options.additional_packages, "Additional Package", "yay")),
                "install_specific_packages": ("Installing 'Specific Packages'...", self.install_specific_packages_based_on_session)}

    @staticmethod
    def _define_service_tasks():
        return {"enable_printer_support": ("Initializing printer support...", "cups", ["cups", "ghostscript", "system-config-printer", "print-manager", "gutenprint"]),
                "enable_samba_network_filesharing": ("Initializing samba...", "smb", ["gvfs-smb", "samba"]), "enable_bluetooth_service": ("Initializing bluetooth...", "bluetooth", ["bluez", "bluez-utils"]),
                "enable_atd_service": ("Initializing atd...", "atd", ["at"]),  "enable_cronie_service": ("Initializing cronie...", "cronie", ["cronie"]), "enable_firewall": ("Initializing firewall...", "ufw", ["ufw"])}

    def reset_sudo_timeout(self):
        try:
            subprocess.run(['sudo', '-K'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            time.sleep(0.5)
        except Exception as e:
            self.outputReceived.emit(f"Warning: Could not reset sudo state: {e}")

    def test_sudo_access(self):
        self.outputReceived.emit("Verifying sudo access...", "operation")
        self.reset_sudo_timeout()
        self.cleanup_temp_files()
        if not self.create_askpass_script():
            self.auth_failed = True
            return False
        try:
            env = os.environ.copy()
            env['SUDO_ASKPASS'] = self.askpass_script_path
            process = subprocess.run(['sudo', '-A', 'echo', 'Sudo access successfully verified...'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env, timeout=0.2)
            if process.stdout:
                self.outputReceived.emit(process.stdout.strip(), "success")
            if process.stderr:
                self.outputReceived.emit(process.stderr.strip(), "error")
            return process.returncode == 0
        except subprocess.TimeoutExpired:
            self.auth_failed = self.has_error = True
            return False
        except Exception as e:
            self.auth_failed = self.has_error = True
            self.outputReceived.emit(f"Error during sudo authentication test: {e}", "error")
            return False

    def create_askpass_script(self):
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="installer_")
            os.chmod(self.temp_dir, 0o700)
            self.askpass_script_path = Path(self.temp_dir, 'askpass.sh')
            self.askpass_script_path.write_text('#!/bin/sh\ncat "$SUDO_PASSWORD_FILE"', encoding='utf-8')
            os.chmod(self.askpass_script_path, 0o700)
            password_file = Path(self.temp_dir, 'sudo_pass')
            password_file.write_text(self.sudo_password.get_value(), encoding='utf-8')
            os.chmod(password_file, 0o600)
            os.environ['SUDO_PASSWORD_FILE'] = str(password_file)
            return True
        except Exception as e:
            self.outputReceived.emit(f"Error creating askpass script: {e}", "error")
            return False

    def cleanup_temp_files(self):
        if not self.temp_dir or not Path(self.temp_dir).exists():
            return
        try:
            for filename in ('sudo_pass', 'askpass.sh'):
                file_path = Path(self.temp_dir, filename)
                if file_path.exists():
                    try:
                        with open(file_path, 'wb') as f:
                            f.write(os.urandom(3072))
                        file_path.unlink()
                    except Exception as e:
                        self.outputReceived.emit(f"Error securely removing {filename}: {e}", "warning")
            for file_path in Path(self.temp_dir).glob('*'):
                if file_path.is_file():
                    try:
                        file_path.unlink()
                    except Exception as e:
                        self.outputReceived.emit(f"Error removing temporary file {file_path}: {e}", "warning")
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = self.askpass_script_path = None
        except Exception as e:
            self.outputReceived.emit(f"Error cleaning up temporary files: {e}", "warning")

    def run_sudo_command(self, command):
        if self.terminated:
            return False
        try:
            env = os.environ.copy()
            env['SUDO_ASKPASS'] = self.askpass_script_path
            if isinstance(command, list):
                if command[0] == 'sudo' and '-A' not in command:
                    command.insert(1, '-A')
                elif command[0] == 'yay' and not any(arg.startswith('--sudoflags=') for arg in command):
                    command.insert(1, '--sudoflags=-A')
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env, bufsize=4096)
            return self._process_command_output(process)
        except Exception as e:
            self.outputReceived.emit(f"<span>Error during command execution: {e}</span>", "error")
            return False

    def _process_command_output(self, process):
        output_buffer, error_buffer = [], []
        def read_stream(stream, buffer, name):
            try:
                for line in iter(stream.readline, ''):
                    if not line or self.terminated:
                        break
                    line = line.strip()
                    if line:
                        buffer.append(line)
                        self.outputReceived.emit(f"<span>{line}</span>", "subprocess")
            except Exception as error:
                self.outputReceived.emit(f"<span>Error reading {name} stream: {error}</span>", "error")
        threads = [threading.Thread(target=read_stream, args=(process.stdout, output_buffer, "stdout"), daemon=True),
                   threading.Thread(target=read_stream, args=(process.stderr, error_buffer, "stderr"), daemon=True)]
        for t in threads: t.start()
        try:
            process.wait(timeout=600)
            for t in threads: t.join()
        except subprocess.TimeoutExpired:
            self.outputReceived.emit("<span>Command Timeout. Process is terminated...</span>", "error")
            process.kill()
            process.wait()
            return False
        if process.returncode != 0:
            self.outputReceived.emit(f"<span>Command error: {process.returncode}</span>", "error")
            if error_buffer:
                self.outputReceived.emit(f"<span>Error details: {' '.join(error_buffer)}</span>", "error")
        return process

    def start_package_installer(self):
        for task_id, (description, function) in self.enabled_tasks.items():
            if self.terminated:
                break
            self.current_task = task_id
            self.taskStatusChanged.emit(task_id, "in_progress")
            self.outputReceived.emit(description, "operation")
            try:
                success = function()
                status = "success" if success is not False else "error"
                self.taskStatusChanged.emit(task_id, status)
                if status == "error":
                    self.has_error = True
            except Exception as e:
                self.has_error = True
                self.outputReceived.emit(f"Task '{task_id}' failed: {e}", "error")
                self.taskStatusChanged.emit(task_id, "error")
        self.outputReceived.emit("", "finish")

    def parse_system_files(self, files):
        parsed_files = []
        for file in files:
            if not isinstance(file, dict):
                self.outputReceived.emit(f"Expected Dictionary but got: {type(file)}", "error")
                continue
            src, dest = file.get('source', '').strip(), file.get('destination', '').strip()
            if src and dest:
                parsed_files.append((src, dest))
            else:
                self.outputReceived.emit(f"Invalid Dictionary Format: {file}", "error")
        return parsed_files

    def copy_files(self, files):
        task_id, success = "copy_system_files", True
        if not files:
            self.outputReceived.emit("No 'System Files' to copy", "warning")
            self.taskStatusChanged.emit(task_id, "warning")
            return True
        for src, dest in files:
            if not Path(src).exists():
                self.outputReceived.emit(f"Source file does not exist: '{src}'", "error")
                success = False
                continue
            dest_dir = Path(dest).parent
            if not dest_dir.exists() and not self._create_directory(dest_dir):
                success = False
                continue
            filename = os.path.basename(src)
            self.outputReceived.emit(f"Copying: '{src}'", "info")
            cmd = ['sudo', 'cp', '-r'] if Path(src).is_dir() else ['sudo', 'cp']
            cmd.extend([str(src), str(dest)])
            result = self.run_sudo_command(cmd)
            if result and result.returncode == 0:
                self.outputReceived.emit(f"Successfully copied: '{filename}' to '{dest}'", "success")
            else:
                self.outputReceived.emit(f"Error copying: '{filename}'", "error")
                success = False
        self.taskStatusChanged.emit(task_id, "success" if success else "error")
        return success

    def _create_directory(self, dest_dir):
        result = self.run_sudo_command(['sudo', 'mkdir', '-p', str(dest_dir)])
        success = result and result.returncode == 0
        self.outputReceived.emit(f"{'Created' if success else 'Error creating'} directory: '{dest_dir}'", "info" if success else "error")
        return success

    @staticmethod
    def package_is_installed(package):
        try:
            return subprocess.run(['pacman', '-Qi', package], capture_output=True).returncode == 0
        except (FileNotFoundError, subprocess.SubprocessError):
            return False

    def install_package_generic(self, package, installer='pacman', package_type=None):
        type_str = package_type or "package"
        self.outputReceived.emit(f"Installing '{type_str}': '{package}'...", "info")
        if self.package_is_installed(package):
            self.outputReceived.emit(f"'{package}' already present...", "success")
            return True
        cmd_templates = {'pacman': ['sudo', 'pacman', '-S', '--noconfirm', package], 'yay': ['yay', '-S', '--noconfirm', package]}
        cmd = cmd_templates.get(installer, [])
        if not cmd:
            self.outputReceived.emit(f"Unknown installer '{installer}'", "error")
            return False
        result = self.run_sudo_command(cmd)
        success = result and result.returncode == 0 and self.package_is_installed(package)
        self.outputReceived.emit(f"'{package}' {'successfully installed' if success else 'failed to install'}...", "success" if success else "error")
        return success

    def batch_install(self, packages, package_type, installer='pacman'):
        task_id_map = {"Essential Package": "install_essential_packages", "Additional Package": "install_additional_packages"}
        task_id = task_id_map.get(package_type)
        pkgs = [p.strip() for p in (packages or []) if isinstance(p, str) and p.strip()]
        if not pkgs:
            self.outputReceived.emit(f"No valid {package_type}s to install", "warning")
            if task_id: self.taskStatusChanged.emit(task_id, "warning")
            return True
        results = [(pkg, self.install_package_generic(pkg, installer, package_type)) for pkg in pkgs]
        failed = [pkg for pkg, ok in results if not ok]
        installed = [pkg for pkg, ok in results if ok]
        if failed:
            self.outputReceived.emit(f"Warning: Failed to install the following '{package_type}(s)': {', '.join(failed)}", "warning")
        if installed:
            self.outputReceived.emit(f"Successfully installed {len(installed)} of {len(pkgs)} '{package_type}(s)'", "success")
        elif pkgs:
            self.outputReceived.emit(f"No '{package_type}(s)' were installed", "warning")
        if task_id:
            status = "success" if not failed else "warning" if installed else "error"
            if status == "warning":
                self.outputReceived.emit(f"Task completed with warnings: {len(failed)} package(s) failed to install", "warning")
                self.has_error = True
            self.taskStatusChanged.emit(task_id, status)
        return not failed

    def update_mirrors(self, task_id):
        self.install_package_generic("reflector", installer="pacman", package_type="Service Package")
        country = self._detect_country()
        command = ['sudo', 'reflector', '--verbose', '--latest', '10', '--protocol', 'https', '--sort', 'rate', '--save', '/etc/pacman.d/mirrorlist']
        if country:
            self.outputReceived.emit(f"<br>Detected country: {country}", "success")
            command.extend(['--country', country])
        else:
            self.outputReceived.emit("Unable to detect country. Searching globally instead.", "info")
        result = self.run_sudo_command(command)
        success = result and result.returncode == 0
        status = "success" if success else "error"
        self.outputReceived.emit(f"Mirrors {'successfully updated' if success else 'failed to update'}...", status)
        self.taskStatusChanged.emit(task_id, status)
        return success

    @staticmethod
    def _detect_country():
        urls = ['https://ipinfo.io/country', 'https://ifconfig.co/country-iso']
        for url in urls:
            try:
                with urllib.request.urlopen(url, timeout=5) as response:
                    if response.status == 200:
                        country = response.read().decode().strip()
                        if country and len(country) <= 3:
                            return country
            except (urllib.error.URLError, socket.timeout):
                continue
        return None

    def set_user_shell(self, task_id):
        config_shell = getattr(Options, "user_shell", "Bash").strip()
        shell_map = {"Bash": ("bash", "/bin/bash", "bash"), "Fish": ("fish", "/usr/bin/fish", "fish"), "Zsh": ("zsh", "/usr/bin/zsh", "zsh"), "Elvish": ("elvish", "/usr/bin/elvish", "elvish"),
                     "Nushell": ("nu", "/usr/bin/nu", "nushell"), "Powershell": ("pwsh", "/usr/bin/pwsh", "powershell"), "Xonsh": ("xonsh", "/usr/bin/xonsh", "xonsh"), "Ngs": ("ngs", "/usr/bin/ngs", "ngs")}
        shell_bin_name, shell_path, shell_pkg = shell_map.get(config_shell, shell_map["Bash"])
        try:
            actual_user = os.environ.get('SUDO_USER') or os.environ.get('USER') or os.environ.get('LOGNAME') or getpass.getuser()
            current_shell = pwd.getpwnam(actual_user).pw_shell
            self.outputReceived.emit(f"Target user: '{actual_user}' (current shell: {current_shell})", "info")
        except Exception as e:
            self.outputReceived.emit(f"Error when determining the target user: {e}", "error")
            self.taskStatusChanged.emit(task_id, "error")
            return False
        if current_shell == shell_path:
            self.outputReceived.emit(f"Current user shell already '{config_shell}'. No changes required...", "success")
            self.taskStatusChanged.emit(task_id, "success")
            return True
        if not self.package_is_installed(shell_pkg):
            if not self.install_package_generic(shell_pkg, "pacman", "Shell Package"):
                self.outputReceived.emit(f"Error when installing '{shell_pkg}'.", "error")
                self.taskStatusChanged.emit(task_id, "error")
                return False
        if not Path(shell_path).exists():
            self.outputReceived.emit(f"Shell binary '{shell_path}' does not exist after installation.", "error")
            self.taskStatusChanged.emit(task_id, "error")
            return False
        with open("/etc/shells", "r") as f:
            shells = [line.strip() for line in f if line.strip()]
        if shell_path not in shells:
            self.outputReceived.emit(f"Adding '{shell_path}' to /etc/shells...", "info")
            append_cmd = ['sudo', 'sh', '-c', f'echo "{shell_path}" >> /etc/shells']
            append_result = self.run_sudo_command(append_cmd)
            if not append_result or append_result.returncode != 0:
                self.outputReceived.emit(f"Error when adding the shell to /etc/shells.", "error")
                self.taskStatusChanged.emit(task_id, "error")
                return False
        self.outputReceived.emit(f"Changing user shell for '{actual_user}' to '{shell_path}'...", "info")
        chsh_cmd = ['sudo', 'chsh', '-s', shell_path, actual_user]
        chsh_result = self.run_sudo_command(chsh_cmd)
        if chsh_result and chsh_result.returncode == 0:
            self.outputReceived.emit(f"Shell for user '{actual_user}' successfully changed to '{config_shell}'...", "success")
            self.taskStatusChanged.emit(task_id, "success")
            return True
        else:
            self.outputReceived.emit(f"Error when changing the shell for user '{actual_user}'.", "error")
            self.taskStatusChanged.emit(task_id, "error")
            return False

    def update_system(self, task_id):
        command = ['yay', '--noconfirm'] if self.package_is_installed("yay") else ['sudo', 'pacman', '-Syu', '--noconfirm']
        result = self.run_sudo_command(command)
        success = result and result.returncode == 0
        status = "success" if success else "error"
        self.outputReceived.emit(f"System {'successfully updated' if success else 'update failed'}...", status)
        self.taskStatusChanged.emit(task_id, status)
        return success

    def install_kernel_header(self, task_id):
        kernel_version = subprocess.run(['uname', '-r'], stdout=subprocess.PIPE, text=True).stdout.strip()
        self.outputReceived.emit(f"Detected kernel: {kernel_version}", "success")
        header_map = {"linux": "linux-headers", "lts": "linux-lts-headers", "zen": "linux-zen-headers", "hardened": "linux-hardened-headers"}
        package = next((header_map[k] for k in header_map if k in kernel_version), "linux-headers")
        success = self.install_package_generic(package, installer="pacman", package_type="Header Package")
        status = "success" if success else "error"
        self.taskStatusChanged.emit(task_id, status)
        return success

    def setup_service_with_packages(self, service, packages):
        task_id = {'cups': "enable_printer_support", 'smb': "enable_samba_network_filesharing", 'bluetooth': "enable_bluetooth_service",
                   'atd': "enable_atd_service", 'cronie': "enable_cronie_service", 'ufw': "enable_firewall"}.get(service)
        success = all(self.install_package_generic(pkg, installer="pacman", package_type="Service Package") for pkg in packages)
        service_success = self.enable_service(service)
        if task_id:
            self.taskStatusChanged.emit(task_id, "success" if success and service_success else "error")
        return success and service_success

    def enable_service(self, service):
        self.outputReceived.emit(f"Enabling: '{service}.service'...", "info")
        is_active = subprocess.run(['systemctl', 'is-active', '--quiet', f'{service}.service'], check=False).returncode == 0
        if is_active:
            self.outputReceived.emit(f"'{service}.service' already enabled...", "success")
            return True
        self.outputReceived.emit("\n", "info")
        result = self.run_sudo_command(['sudo', 'systemctl', 'enable', '--now', f'{service}.service'])
        success = result and result.returncode == 0
        if success:
            self.outputReceived.emit(f"'{service}.service' successfully enabled...", "success")
            if service == "ufw":
                for ufw_cmd in (['sudo', 'ufw', 'default', 'deny'], ['sudo', 'ufw', 'enable'], ['sudo', 'ufw', 'reload']):
                    if not (self.run_sudo_command(ufw_cmd) or False):
                        success = False
        else:
            error = getattr(result, 'stderr', 'Unknown error')
            self.outputReceived.emit(f"Error enabling '{service}.service': {error}", "error")
        return success

    def install_yay(self):
        task_id = "install_yay"
        if self.package_is_installed("yay"):
            self.outputReceived.emit("'yay' already present...", "success")
            self.taskStatusChanged.emit(task_id, "success")
            return True
        if not (self.run_sudo_command(['sudo', 'pacman', '-S', '--needed', '--noconfirm', 'base-devel', 'git', 'go']) or False):
            self.taskStatusChanged.emit(task_id, "error")
            return False
        yay_build_path = Path(home_user) / "yay"
        if yay_build_path.exists():
            shutil.rmtree(yay_build_path) if yay_build_path.is_dir() else yay_build_path.unlink()
        def run_and_stream(cmd, cwd):
            try:
                with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=cwd) as proc:
                    for line in proc.stdout:
                        self.outputReceived.emit(line.rstrip(), "subprocess")
                    return proc.wait() == 0
            except Exception as e:
                self.outputReceived.emit(f"Exception: {e}", "error")
                return False
        self.outputReceived.emit("Cloning 'yay' from git...", "subprocess")
        if not run_and_stream(['git', 'clone', 'https://aur.archlinux.org/yay.git'], home_user):
            self.taskStatusChanged.emit(task_id, "error")
            return False
        self.outputReceived.emit("Building package 'yay'...", "subprocess")
        if not run_and_stream(['makepkg', '-c', '--noconfirm'], yay_build_path):
            self.taskStatusChanged.emit(task_id, "error")
            return False
        to_remove = [pkg for pkg in ['yay-debug', 'go'] if self.package_is_installed(pkg)]
        if to_remove:
            result = self.run_sudo_command(['sudo', 'pacman', '-R', '--noconfirm'] + to_remove)
            self.outputReceived.emit(f"{'Successfully removed' if result and result.returncode == 0 else 'Error during uninstallation of'}: '{', '.join(to_remove)}'", "subprocess" if result and result.returncode == 0 else "warning")
        pkg_files = sorted(f for f in os.listdir(yay_build_path) if f.endswith('.pkg.tar.zst'))
        if not pkg_files:
            self.outputReceived.emit("No package file found for installation.", "warning")
            self.taskStatusChanged.emit(task_id, "error")
            return False
        pkg_path = os.path.join(str(yay_build_path), pkg_files[0])
        result = self.run_sudo_command(['sudo', 'pacman', '-U', '--noconfirm', str(pkg_path)])
        success = result and result.returncode == 0
        shutil.rmtree(yay_build_path, ignore_errors=True)
        shutil.rmtree(Path(home_config) / "go", ignore_errors=True)
        self.outputReceived.emit(f"'yay' {'successfully installed' if success else 'installation failed'}...", "success" if success else "error")
        self.taskStatusChanged.emit(task_id, "success" if success else "error")
        return success

    def install_specific_packages_based_on_session(self):
        task_id = "install_specific_packages"
        session = None
        for var in ['XDG_CURRENT_DESKTOP', 'XDG_SESSION_DESKTOP', 'DESKTOP_SESSION']:
            val = os.getenv(var)
            if val:
                parts = [p.strip() for p in val.split(':') if p.strip()]
                for part in parts:
                    for env in SESSIONS:
                        if part.lower() == env.lower():
                            session = env
                            break
                    if session:
                        break
            if session:
                break
        if not session:
            self.outputReceived.emit("Unable to determine current desktop environment or window manager.", "warning")
            self.taskStatusChanged.emit(task_id, "error")
            return False
        self.outputReceived.emit(f"Detected session: {session}", "success")
        matching_packages = [spec_pkg.get('package') for spec_pkg in Options.specific_packages if spec_pkg.get('session') == session and 'package' in spec_pkg]
        if not matching_packages:
            self.outputReceived.emit(f"No specific packages found for {session}.", "info")
            self.taskStatusChanged.emit(task_id, "success")
            return True
        success = all(self.install_package_generic(pkg, installer="pacman", package_type="Specific Package") for pkg in matching_packages)
        self.taskStatusChanged.emit(task_id, "success" if success else "error")
        return success

    def remove_orphaned_packages(self):
        task_id = "remove_orphaned_packages"
        orphaned_packages = subprocess.run(['pacman', '-Qdtq'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()
        if orphaned_packages:
            packages_list = orphaned_packages.split('\n')
            result = self.run_sudo_command(['sudo', 'pacman', '-Rns', '--noconfirm'] + packages_list)
            success = result and result.returncode == 0
            self.outputReceived.emit(f"Orphaned package(s) {'successfully removed' if success else 'could not be removed'}...", "success" if success else "error")
        else:
            self.outputReceived.emit("No orphaned packages found...", "success")
            success = True
        self.taskStatusChanged.emit(task_id, "success" if success else "error")
        return success

    def clean_cache(self):
        task_id = "clean_cache"
        success = True
        pacman_cmd = ['sudo', 'pacman', '-Scc', '--noconfirm']
        result_pacman = self.run_sudo_command(pacman_cmd)
        if result_pacman and result_pacman.returncode == 0:
            self.outputReceived.emit("'Pacman' cache successfully cleaned...", "success")
        else:
            error = getattr(result_pacman, 'stderr', 'Unknown error')
            self.outputReceived.emit(f"Error cleaning 'pacman' cache: {error}", "error")
            success = False
        if self.package_is_installed('yay'):
            self.outputReceived.emit("<br>Cleaning 'yay' cache...", "info")
            result_yay = self.run_sudo_command(['yay', '-Scc', '--noconfirm'])
            if result_yay and result_yay.returncode == 0:
                self.outputReceived.emit("'Yay' cache successfully cleaned...", "success")
            else:
                self.outputReceived.emit("Error cleaning 'yay' cache...", "error")
                success = False
        self.taskStatusChanged.emit(task_id, "success" if success else "error")
        return success


# noinspection PyUnresolvedReferences
class FileProcessDialog(QDialog):
    TAB_CONFIG = {'summary': {'index': 0, 'color': '#6ffff5', 'display': 'Summary'}, 'copied':  {'index': 1, 'color': 'lightgreen', 'display': 'Copied'},
                  'skipped': {'index': 2, 'color': '#ffff7f', 'display': 'Skipped'}, 'error':   {'index': 3, 'color': '#ff8587', 'display': 'Errors'}}

    def __init__(self, parent, checkbox_dirs, operation_type):
        super().__init__(parent)
        self.operation_type = operation_type
        self.checkbox_dirs = checkbox_dirs
        self.setWindowTitle(operation_type)
        self._last_summary_update_time = 0
        self.sudo_password = None
        self.sudo_password_event = QWaitCondition()
        self.sudo_password_mutex = QMutex()
        self.sudo_dialog_open = False
        self.status_label = QLabel(f"{self.operation_type} in progress...\n")
        self.status_label.setStyleSheet("color: #6ffff5; font-weight: bold; font-size: 20px; background-color: transparent;")
        self.current_file_label = QLabel(f"Preparing:\n{self.operation_type}")
        self.current_file_label.setStyleSheet("font-weight: bold; font-size: 17px;")
        self.elapsed_time_label = QLabel("\nElapsed time:\n00s\n")
        self.elapsed_time_label.setStyleSheet("font-weight: bold; font-size: 17px;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(global_style)
        self.tab_widget = QTabWidget()
        self.copied_tab = VirtualLogTabWidget()
        self.skipped_tab = VirtualLogTabWidget()
        self.error_tab = VirtualLogTabWidget()
        self.summary_tab = QWidget()
        self.timer = QElapsedTimer()
        self.paused_elapsed = 0
        self.update_timer = QTimer(self)
        self.thread = FileCopyThread(self.checkbox_dirs, self.operation_type)
        self.thread.set_parent_dialog(self)
        self.container = QWidget(self)
        self.container.setProperty("class", "container")
        self.info_layout = QVBoxLayout()
        self.cancel_button = QPushButton()
        self.cancel_button.setStyleSheet(global_style)
        self.summary_table = QWidget()
        self.summary_layout = QVBoxLayout(self.summary_table)
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(100)
        self.shadow.setColor(QColor(0, 0, 0, 250))
        self.shadow.setOffset(0.0, 1.0)
        self.total_bytes_copied = 0
        self.total_files = 0
        self.copied_count = 0
        self.skipped_count = 0
        self.error_count = 0
        self.color_step = 0
        self.cancelled = False
        self._smb_error_occurred = False
        self._error_keys = set()
        self.setup_ui_layout()
        self.setup_tabs()
        self.setup_connections()
        self.start_process()

    def handle_sudo_password_request(self):
        if self.sudo_dialog_open:
            return
        self.sudo_dialog_open = True
        try:
            if self.timer.isValid():
                self.paused_elapsed += self.timer.elapsed()
            self.update_timer.stop()
            password, ok = QInputDialog.getText(self, "Sudo Password", "Enter sudo password for mounting SMB shares:", QLineEdit.EchoMode.Password)
            with QMutexLocker(self.sudo_password_mutex):
                self.sudo_password = password if ok and password else None
                self.sudo_password_event.wakeAll()
            self.timer.restart()
            self.update_timer.start(250)
        finally:
            self.sudo_dialog_open = False

    def get_sudo_password(self):
        with QMutexLocker(self.sudo_password_mutex):
            if self.sudo_password is not None:
                return self.sudo_password
            self.thread.sudo_password_requested.emit()
            self.sudo_password_event.wait(self.sudo_password_mutex)
            if self.sudo_password is None:
                raise RuntimeError("Sudo password required for mounting SMB shares")
            return self.sudo_password

    def setup_connections(self):
        t = self.thread
        t.workers_ready.connect(self.enable_cancel_button)
        t.file_copied.connect(self.log_file_copied)
        t.file_skipped.connect(self.log_file_skipped)
        t.file_error.connect(self.log_file_error)
        t.progress_updated.connect(self.update_progress)
        t.operation_completed.connect(self.operation_completed)
        t.smb_error_cancel.connect(self._on_smb_error_cancel)
        t.sudo_password_requested.connect(self.handle_sudo_password_request)
        self.update_timer.timeout.connect(self.update_elapsed_time)

    def setup_ui_layout(self):
        main_layout = QVBoxLayout(self)
        self.info_layout.addWidget(self.current_file_label)
        self.info_layout.addWidget(self.elapsed_time_label)
        self.info_layout.addWidget(self.progress_bar)
        button_box = QDialogButtonBox()
        self.cancel_button = button_box.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        self.cancel_button.setFixedSize(125, 35)
        self.cancel_button.clicked.connect(self.cancel_operation)
        self.cancel_button.setEnabled(False)
        container_layout = QVBoxLayout(self.container)
        container_layout.addWidget(self.status_label)
        container_layout.addWidget(self.tab_widget)
        container_layout.addWidget(button_box)
        main_layout.addWidget(self.container)
        self.setFixedSize(1200, 700)

    def start_process(self):
        self.timer.start()
        self.update_timer.start(350)
        self.thread.start()

    def setup_tabs(self):
        tab_style = "font-family: FiraCode Nerd Font Mono; font-size: 14px; padding: 10px;"
        tab_bar = self.tab_widget.tabBar()
        for tab_type, config in self.TAB_CONFIG.items():
            if tab_type == 'summary':
                self.setup_summary_tab()
                self.tab_widget.addTab(self.summary_tab, config['display'])
            else:
                tab = getattr(self, f"{tab_type}_tab")
                tab.setStyleSheet(f"color: {config['color']}; {tab_style}")
                self.tab_widget.addTab(tab, f"{config['display']} (0)")
            tab_bar.setTabTextColor(config['index'], QColor(config['color']))

    def setup_summary_tab(self):
        layout = QVBoxLayout(self.summary_tab)
        center_wrapper = QWidget()
        center_layout = QHBoxLayout(center_wrapper)
        self.summary_table.setLayout(self.summary_layout)
        self.summary_layout.setContentsMargins(5, 5, 5, 5)
        center_layout.addStretch(1)
        center_layout.addWidget(self.summary_table)
        center_layout.addStretch(1)
        center_wrapper.setGraphicsEffect(self.shadow)
        self.summary_table.setGraphicsEffect(self.shadow)
        layout.addStretch(1)
        layout.addWidget(center_wrapper)
        layout.addStretch(1)
        layout.addLayout(self.info_layout)
        self.summary_tab.setStyleSheet("background-color: #2c3042;")
        center_wrapper.setContentsMargins(10, 10, 10, 10)

    @staticmethod
    def create_summary_row(label_text, value_text, text_color, bg_color):
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(5, 5, 5, 5)
        base_style = f"font-family: 'FiraCode Nerd Font Mono', 'Fira Code', monospace; padding: 2px 2px; border-radius: 5px; font-size: 18px; background-color: {bg_color}; color: {text_color}; border: 2px solid rgba(0, 0, 0, 50%);"
        label = QLabel(label_text)
        label.setStyleSheet(base_style + " qproperty-alignment: AlignLeft;")
        label.setFixedWidth(425)
        value = QLabel(value_text)
        value.setStyleSheet(base_style + " qproperty-alignment: AlignCenter;")
        value.setFixedWidth(425)
        row_layout.addWidget(label)
        row_layout.addWidget(value)
        return row_layout

    def update_summary_widget(self, copied: int, skipped: int, error: int):
        self.clear_layout(self.summary_layout)
        total = copied + skipped + error
        size_formatted = self.format_file_size(self.total_bytes_copied)
        copied_size_text = f"({size_formatted})" if copied else "(0.00 MB)"
        add = self.summary_layout.addLayout
        add(self.create_summary_row("Processed files/directories (Total):", f"{total}", "#c1ffe3", "#2c2f33"))
        add(self.create_summary_row("Copied:", f"{copied} {copied_size_text}", "#55ff55", "#1f3a1f"))
        add(self.create_summary_row("Skipped (Up to date, symlinks etc):", f"{skipped}", "#ffff7f", "#3a3a1f"))
        add(self.create_summary_row("Errors:", f"{error}", "#ff8587", "#3a1f1f"))

    @staticmethod
    def format_file_size(size_bytes):
        units = ["bytes", "KB", "MB", "GB", "TB"]
        size = float(size_bytes)
        unit_index = 0
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        return f"{size:.2f} {units[unit_index]}"

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                FileProcessDialog.clear_layout(item.layout())

    def enable_cancel_button(self):
        self.cancel_button.setEnabled(True)

    def update_progress(self, progress, status_text):
        if not self.cancelled:
            self.progress_bar.setValue(progress)
            self.current_file_label.setText(status_text)

    def update_elapsed_time(self):
        if self.timer.isValid():
            total_elapsed = (self.paused_elapsed + self.timer.elapsed()) // 1000
            h, rem = divmod(total_elapsed, 3600)
            m, s = divmod(rem, 60)
            if h:
                time_text = f"\nElapsed time:\n{h:02}h {m:02}m {s:02}s\n"
            elif m:
                time_text = f"\nElapsed time:\n{m:02}m {s:02}s\n"
            else:
                time_text = f"\nElapsed time:\n{s:02}s\n"
            self.elapsed_time_label.setText(time_text)
        self.update_summary()

    def update_summary(self):
        now = QDateTime.currentMSecsSinceEpoch()
        if self.thread and self.thread.isRunning() and now - self._last_summary_update_time < 250:
            return
        self._last_summary_update_time = now
        self.update_summary_widget(self.copied_count, self.skipped_count, self.error_count)

    def log_file_copied(self, source, destination, file_size=0):
        self.copied_count += 1
        self.total_bytes_copied += file_size
        entry = f"{self.copied_count}:\n'{source}'\nCopied to ⤵ \n'{destination}'\n"
        self.copied_tab.add_entry(entry, "copied")
        self.tab_widget.setTabText(1, f"Copied ({self.copied_count})")

    def log_file_skipped(self, source, reason=""):
        self.skipped_count += 1
        entry = f"{self.skipped_count}:\n'{source}'\nSkipped {reason}\n"
        self.skipped_tab.add_entry(entry, "skipped")
        self.tab_widget.setTabText(2, f"Skipped ({self.skipped_count})")

    def log_file_error(self, source, error=""):
        key = f"{source}::{error}"
        if key in self._error_keys:
            return
        self._error_keys.add(key)
        self.error_count += 1
        entry = f"{self.error_count}:\n'{source}'\nError: {error}\n"
        self.error_tab.add_entry(entry, "error")
        self.tab_widget.setTabText(3, f"Errors ({self.error_count})")

    def _on_smb_error_cancel(self):
        self._smb_error_occurred = True
        self.cancelled = True
        if self.thread and self.thread.isRunning():
            self.thread.cancel()

    def operation_completed(self):
        self.update_timer.stop()
        if self.thread:
            self.thread.cleanup_resources()
        if self.cancelled:
            self.handle_cancelled_completion()
        else:
            self.handle_successful_completion()
        self.cancel_button.setText("Close")
        self.cancel_button.clicked.disconnect()
        self.cancel_button.clicked.connect(self.accept)
        self.cancel_button.setFocus()
        self.update_summary()
        for tab in (self.copied_tab, self.skipped_tab, self.error_tab):
            tab.flush_entries()
            tab.sort_entries()

    def handle_successful_completion(self):
        self.status_label.setText(f"{self.operation_type} successfully completed!\n")
        self.status_label.setStyleSheet("color: #6ffff5; font-weight: bold; font-size: 20px; background-color: transparent;")
        self.current_file_label.setText("⇪ \nCheck details above.")
        self.progress_bar.setValue(100)
        self.animate_text_effect()

    def handle_cancelled_completion(self):
        self.status_label.setText(f"{self.operation_type} canceled!\n")
        self.status_label.setStyleSheet("color: #ff8587; font-weight: bold; font-size: 20px; background-color: transparent;")
        text = "󰜺 \nProcess aborted due to samba file error." if self._smb_error_occurred else "󰜺 \nProcess aborted by user."
        self.current_file_label.setText(text)
        err_style = "color: #ff8587; font-weight: bold; font-size: 17px;"
        self.current_file_label.setStyleSheet(err_style)
        self.elapsed_time_label.setStyleSheet(err_style)
        self.progress_bar.setStyleSheet(f"""{global_style} QProgressBar::chunk {{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #fd7e14, stop:1 #ff8587); border-radius: 2px;}}""")

    def animate_text_effect(self):
        color_timer = QTimer(self)
        color_timer.timeout.connect(self.update_label_color)
        color_timer.start(50)

    def update_label_color(self):
        self.color_step = (self.color_step + 0.0175) % 1
        start_color, end_color = (102, 255, 245), (85, 255, 85)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * self.color_step)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * self.color_step)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * self.color_step)
        color_hex = f"#{r:02x}{g:02x}{b:02x}"
        style = f"color: {color_hex}; font-weight: bold;"
        self.status_label.setStyleSheet(f"{style} font-size: 20px; background-color: transparent;")
        self.current_file_label.setStyleSheet(f"{style} font-size: 17px;")
        self.elapsed_time_label.setStyleSheet(f"{style} font-size: 17px;")

    def cancel_operation(self):
        confirm_box = QMessageBox(QMessageBox.Icon.Question, "Confirm Cancellation", f"Are you sure you want to cancel the {self.operation_type} process?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, self)
        confirm_box.setDefaultButton(QMessageBox.StandardButton.No)
        if confirm_box.exec() == QMessageBox.StandardButton.Yes:
            if self.thread and self.thread.isRunning():
                self.cancelled = True
                self.thread.cancel()
                self.status_label.setText(f"Cancelling {self.operation_type}...\n")
                self.status_label.setStyleSheet("color: #ff8587; font-weight: bold; font-size: 20px; background-color: transparent;")
                self.current_file_label.setText("Please wait while operations are being cancelled...\n")
                self.progress_bar.setStyleSheet(f"""{global_style} QProgressBar::chunk 
                {{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #fd7e14, stop:1 #ff8587); border-radius: 2px;}}""")
                QCoreApplication.processEvents()
                if not self.thread.wait(1000):
                    self.thread.terminate()
                    self.thread.wait(500)

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            confirm_box = QMessageBox(QMessageBox.Icon.Question, "Confirm Close", f"The {self.operation_type} process is still running. Are you sure you want to close?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, self)
            confirm_box.setDefaultButton(QMessageBox.StandardButton.No)
            if confirm_box.exec() == QMessageBox.StandardButton.Yes:
                self.cancelled = True
                self.thread.cancel()
                if not self.thread.wait(100):
                    self.thread.terminate()
                    if not self.thread.wait(100):
                        print("WARNING: Thread could not be terminated")
                event.accept()
            else:
                event.ignore()
        event.accept()


# noinspection PyUnresolvedReferences
class FileCopyThread(QThread):
    progress_updated = pyqtSignal(int, str)
    workers_ready = pyqtSignal()
    file_copied = pyqtSignal(str, str, int)
    file_skipped = pyqtSignal(str, str)
    file_error = pyqtSignal(str, str)
    smb_error_cancel = pyqtSignal()
    operation_completed = pyqtSignal()
    SKIP_PATTERNS = ["Singleton", "SingletonCookie", "SingletonLock", "lockfile", "lock", "Cache-Control", ".parentlock",
                     "cookies.sqlite-wal", "cookies.sqlite-shm", "places.sqlite-wal", "places.sqlite-shm", "SingletonSocket"]
    sudo_password_requested = pyqtSignal()

    def __init__(self, checkbox_dirs, operation_type):
        super().__init__()
        self.checkbox_dirs = checkbox_dirs
        self.operation_type = operation_type
        self.cancelled = False
        self.total_files = 0
        self.processed_files = 0
        self.file_batches = []
        self.batch_index = 0
        self.worker_threads = []
        self.mutex = QMutex()
        self.buffer_size = min(64 * 1024 * 1024, max(4 * 1024 * 1024, int(psutil.virtual_memory().available * 0.1)))
        self.num_workers = min(os.cpu_count() or 4, 8)
        self.total_bytes = 0
        self.processed_bytes = 0
        self.file_sizes = {}
        self._smb_handler = None
        self._samba_password_manager = None
        self._smb_credentials = None
        self.parent_dialog = None

    def set_parent_dialog(self, dialog):
        self.parent_dialog = dialog

    def run(self):
        try:
            if self.cancelled:
                return
            self.collect_files()
            if self.total_files == 0:
                self.progress_updated.emit(100, "No files to process")
                return
            workers_count = min(self.num_workers, os.cpu_count() or 4)
            for i in range(workers_count):
                worker = FileWorkerThread(self, i)
                self.worker_threads.append(worker)
                worker.start()
                self.workers_ready.emit()
            for worker in self.worker_threads:
                worker.wait()
        except Exception as e:
            print(f"Error in file copy thread: {e}")
        finally:
            self.operation_completed.emit()

    def collect_files(self):
        all_files = []
        file_sizes = {}
        total_bytes = 0
        for checkbox, sources, destinations, _ in self.checkbox_dirs:
            sources = sources if isinstance(sources, list) else [sources]
            destinations = destinations if isinstance(destinations, list) else [destinations]
            for source, destination in zip(sources, destinations):
                if SmbFileHandler.is_smb_path(source):
                    if self.smb_handler.is_directory(source):
                        for smb_file in self.smb_handler.list_smb_directory(source):
                            full_smb_path = os.path.join(source.rstrip("/"), smb_file)
                            if not self._should_skip_file(full_smb_path):
                                dst_file = str(Path(destination))
                                file_size = self._get_file_size(full_smb_path)
                                all_files.append((full_smb_path, dst_file))
                                file_sizes[full_smb_path] = file_size
                                total_bytes += file_size
                            else:
                                self.file_skipped.emit(smb_file, "(Protected/locked file)")
                    else:
                        file_size = self._get_file_size(source)
                        all_files.append((source, destination))
                        file_sizes[source] = file_size
                        total_bytes += file_size
                else:
                    src = Path(source)
                    if not src.exists():
                        continue
                    if src.is_file():
                        if not self._should_skip_file(str(src)):
                            file_size = self._get_file_size(str(src))
                            all_files.append((str(src), str(destination)))
                            file_sizes[str(src)] = file_size
                            total_bytes += file_size
                        else:
                            self.file_skipped.emit(str(src), "(Protected/locked file)")
                    else:
                        for dirpath, _, filenames in os.walk(src):
                            rel_path = Path(dirpath).relative_to(src)
                            for file in filenames:
                                src_file = Path(dirpath) / file
                                src_file_str = str(src_file)
                                if not self._should_skip_file(src_file_str):
                                    dst_file = Path(destination) / rel_path / file
                                    file_size = self._get_file_size(src_file_str)
                                    all_files.append((src_file_str, str(dst_file)))
                                    file_sizes[src_file_str] = file_size
                                    total_bytes += file_size
                                else:
                                    self.file_skipped.emit(src_file_str, "(Protected/locked file)")
        self.total_files = len(all_files)
        self.file_sizes = file_sizes
        self.total_bytes = total_bytes
        workers = max(1, min(self.num_workers, os.cpu_count() or 4))
        batch_size = max(100, min(500, self.total_files // (workers * 4) or 250))
        def batch_gen():
            for i in range(0, len(all_files), batch_size):
                yield all_files[i:i + batch_size]
        self.file_batches = batch_gen()

    def get_next_batch(self):
        with QMutexLocker(self.mutex):
            try:
                return next(self.file_batches)
            except StopIteration:
                return None

    def _should_skip_file(self, file_path):
        file_name = Path(file_path).name
        return any(pattern == file_name for pattern in self.SKIP_PATTERNS)

    def _skip_file(self, source_file, reason):
        self.mutex.lock()
        try:
            self.processed_files += 1
            file_size = self.file_sizes.get(source_file, 0)
            self.processed_bytes += file_size
            progress = int((self.processed_bytes / self.total_bytes) * 100) if self.total_bytes > 0 else 0
            self.file_skipped.emit(source_file, reason)
            self.progress_updated.emit(progress, f"Skipping {reason}:\n{Path(source_file).name}")
        finally:
            self.mutex.unlock()

    def copy_file(self, source_file, dest_file):
        if self.cancelled:
            return
        file_name = Path(source_file).name
        dest_path = Path(dest_file)
        if SmbFileHandler.is_smb_path(source_file) or SmbFileHandler.is_smb_path(dest_file):
            if self.cancelled:
                return
            self.smb_handler.copy_file(source_file, dest_file, lambda success, smb_file_name, size_or_error:
            (self._handle_smb_result(success, source_file, dest_file, smb_file_name, size_or_error) if not self.cancelled else None))
            return
        try:
            if not Path(source_file).exists():
                self.handle_file_error(source_file, "Source file not found")
                return
            src_stat = Path(source_file).stat()
            file_size = src_stat.st_size
            if dest_path.exists():
                dest_stat = dest_path.stat()
                if src_stat.st_size == dest_stat.st_size and src_stat.st_mtime <= dest_stat.st_mtime:
                    self._skip_file(source_file, "(Up to date)")
                    return
            self.fast_copy(source_file, dest_file)
            self._update_file_progress(True, source_file, dest_file, file_name, file_size)
        except (OSError, FileNotFoundError) as e:
            self.handle_file_error(source_file, f"Source error: {e}")
        except Exception as e:
            self.handle_file_error(source_file, str(e))

    def fast_copy(self, source, destination):
        if self.cancelled:
            return
        try:
            file_size = os.path.getsize(source)
            buffer_size = 64 * 1024
            if file_size > 1024 * 1024:
                buffer_size = 1024 * 1024
            if file_size > 64 * 1024 * 1024:
                buffer_size = 8 * 1024 * 1024
            dest_dir = os.path.dirname(destination)
            if dest_dir and not os.path.exists(dest_dir):
                Path(dest_dir).mkdir(parents=True, exist_ok=True)
            try:
                with open(source, 'rb') as fsrc, open(destination, 'wb') as fdst:
                    buffer = memoryview(bytearray(buffer_size))
                    while not self.cancelled:
                        n = fsrc.readinto(buffer)
                        if not n:
                            break
                        fdst.write(buffer[:n])
                shutil.copystat(source, destination)
            except MemoryError:
                shutil.copy2(source, destination)
        except (OSError, IOError) as e:
            error_msg = str(e).lower()
            if any(term in error_msg for term in SKIP_PATTERNS):
                raise OSError("Skipping access-protected file")
            else:
                raise OSError(f"Failed to copy {source} to {destination}:\n{str(e)}")

    def _get_file_size(self, file_path):
        try:
            if SmbFileHandler.is_smb_path(file_path):
                if not self._smb_handler:
                    self._smb_handler = SmbFileHandler(self.samba_password_manager, self)
                return self.smb_handler.get_smb_file_size(file_path)
            else:
                return Path(file_path).stat().st_size
        except Exception as e:
            print(f"Error getting file size for {file_path}: {e}")
            if self._smb_handler:
                self.file_error.emit(file_path, str(f"File size cannot be determined. {e}"))
                self.smb_error_cancel.emit()
            return 0

    def _update_file_progress(self, should_copy, source_file, dest_file, file_name, file_size):
        try:
            success = False
            message = "(Up to date)"
            if should_copy:
                dest_dir = os.path.dirname(dest_file)
                if dest_dir and not os.path.exists(dest_dir):
                    Path(dest_dir).mkdir(parents=True, exist_ok=True)
                try:
                    self.fast_copy(source_file, dest_file)
                    success = True
                    message = "(Copied successfully)"
                except OSError as e:
                    error_msg = str(e)
                    if "Skipping access-protected file" in error_msg or "Permission denied" in error_msg:
                        message = "(Protected/locked file)"
                    else:
                        raise
                except Exception:
                    raise
            self.mutex.lock()
            try:
                self.processed_files += 1
                self.processed_bytes += self.file_sizes.get(source_file, file_size)
                progress = int((self.processed_bytes / self.total_bytes) * 100) if self.total_bytes > 0 else 0
                if should_copy and success:
                    self.file_copied.emit(source_file, dest_file, file_size)
                    self.progress_updated.emit(progress, f"Copying:\n{file_name}")
                else:
                    self.file_skipped.emit(source_file, message)
                    self.progress_updated.emit(progress, f"Skipping {message}:\n{file_name}")
            finally:
                self.mutex.unlock()
        except Exception as e:
            self.handle_file_error(source_file, str(e))

    def handle_file_error(self, source_file, error_msg):
        self.mutex.lock()
        try:
            self.processed_files += 1
            if source_file in self.file_sizes:
                self.processed_bytes += self.file_sizes[source_file]
            progress = int((self.processed_bytes / self.total_bytes) * 100) if self.total_bytes > 0 else 0
            self.file_error.emit(source_file, error_msg)
            self.progress_updated.emit(progress, f"Error copying:\n{Path(source_file).name}")
        finally:
            self.mutex.unlock()

    def _handle_smb_result(self, success, source_file, dest_file, file_name, size_or_error):
        self.mutex.lock()
        try:
            self.processed_files += 1
            try:
                file_size = int(size_or_error) if isinstance(size_or_error, (int, str)) else 0
            except (ValueError, TypeError):
                file_size = 0
            self.processed_bytes += file_size
            progress = int((self.processed_bytes / self.total_bytes) * 100) if self.total_bytes > 0 else 0
            if success:
                self.file_copied.emit(source_file, dest_file, file_size)
                self.progress_updated.emit(progress, f"Copying:\n{file_name}")
            else:
                self.file_error.emit(source_file, str(size_or_error))
                self.progress_updated.emit(progress, f"Error copying:\n{file_name}")
                self.smb_error_cancel.emit()
        finally:
            self.mutex.unlock()

    @property
    def smb_handler(self):
        if self._smb_handler is None:
            self._smb_handler = SmbFileHandler(self.samba_password_manager, self)
        return self._smb_handler

    @property
    def samba_password_manager(self):
        if self._samba_password_manager is None:
            self._samba_password_manager = SambaPasswordManager()
        return self._samba_password_manager

    def get_smb_credentials(self):
        with QMutexLocker(self.mutex):
            return self._smb_credentials

    def set_smb_credentials(self, credentials):
        with QMutexLocker(self.mutex):
            self._smb_credentials = credentials

    def cleanup_resources(self):
        for worker in list(self.worker_threads):
            if worker.isRunning():
                worker.requestInterruption()
                if not worker.wait(100):
                    worker.terminate()
                    worker.wait(100)
        self.worker_threads.clear()
        if self._smb_handler:
            self._smb_handler.force_cleanup()
            self._smb_handler = None
            self._smb_credentials = None

    def cancel(self):
        self.cancelled = True
        for worker in self.worker_threads:
            worker.requestInterruption()
        if self._smb_handler:
            self._smb_handler.force_cleanup()
        for worker in self.worker_threads:
            if not worker.wait(200):
                worker.terminate()
        self.cleanup_resources()


class FileWorkerThread(QThread):
    def __init__(self, main_thread, worker_id):
        super().__init__()
        self.main_thread = main_thread
        self.worker_id = worker_id
        self.setObjectName(f"FileWorker-{worker_id}")

    def run(self):
        while not self.main_thread.cancelled and not self.isInterruptionRequested():
            batch = self.main_thread.get_next_batch()
            if batch is None:
                break
            for source_file, dest_file in batch:
                if self.main_thread.cancelled or self.isInterruptionRequested() or (self.main_thread.thread and getattr(self.main_thread.thread, 'cancelled', False)):
                    return
                try:
                    self.main_thread.copy_file(source_file, dest_file)
                except Exception as e:
                    if not self.main_thread.cancelled:
                        self.main_thread.handle_file_error(source_file, str(e))


class SmbFileHandler:
    def __init__(self, samba_password_manager, thread=None):
        self.samba_password_manager = samba_password_manager
        self.thread = thread
        self._smb_credentials = None
        self._sudo_password = None
        self.mutex = QMutex()
        self._mount_wait_conditions = {}
        self._mounted_shares = {}
        self._mounting_shares = set()

    def initialize(self):
        if self._smb_credentials:
            return
        with QMutexLocker(self.mutex):
            if self._smb_credentials:
                return
            creds = getattr(self.thread, 'get_smb_credentials', lambda: None)() if self.thread else None
            self._smb_credentials = creds if creds and all(creds) else self.samba_password_manager.get_samba_credentials()
            if self.thread and hasattr(self.thread, 'set_smb_credentials') and (not creds or not all(creds)):
                self.thread.set_smb_credentials(self._smb_credentials)

    @staticmethod
    def is_smb_path(path):
        return str(path).startswith(("smb:", "//"))

    @staticmethod
    def parse_smb_url(path):
        path = str(path)
        if path.startswith("smb:/") and not path.startswith("smb://"):
            path = f"smb://{path[5:]}"
        if path.startswith("//"):
            path = f"smb://{path[2:]}"
        m = re.match(r"smb://([^/]+)/([^/]+)(/?.*)", path)
        if not m:
            raise ValueError(f"Invalid SMB-URL: {path}")
        return m.group(1), m.group(2), m.group(3).lstrip('/')

    def _get_sudo_password(self):
        if self._sudo_password:
            return self._sudo_password
        if self.thread and getattr(self.thread, 'parent_dialog', None):
            try:
                self._sudo_password = self.thread.parent_dialog.get_sudo_password()
                return self._sudo_password
            except RuntimeError as e:
                raise e
        raise RuntimeError("Cannot request sudo password - no parent dialog available")

    def _mount_smb_share(self, server, share):
        if self.thread and getattr(self.thread, 'cancelled', False):
            raise RuntimeError("Operation cancelled")
        key = (server, share)
        mount_point = tempfile.mkdtemp(prefix=f"smb_{server}_{share}_")
        with QMutexLocker(self.mutex):
            if key in self._mounted_shares and os.path.ismount(self._mounted_shares[key]):
                return self._mounted_shares[key]
            self._mounted_shares.pop(key, None)
            if key in self._mounting_shares:
                if key not in self._mount_wait_conditions:
                    self._mount_wait_conditions[key] = QWaitCondition()
                wait_condition = self._mount_wait_conditions[key]
                wait_count = 0
                while key in self._mounting_shares and wait_count < 5:
                    if self.thread and getattr(self.thread, 'cancelled', False):
                        raise RuntimeError("Operation cancelled during mount wait")
                    wait_condition.wait(self.mutex, 1000)
                    wait_count += 1
                if key in self._mounted_shares and os.path.ismount(self._mounted_shares[key]):
                    return self._mounted_shares[key]
            self._mounting_shares.add(key)
            if key not in self._mount_wait_conditions:
                self._mount_wait_conditions[key] = QWaitCondition()
        try:
            if self.thread and getattr(self.thread, 'cancelled', False):
                raise RuntimeError("Operation cancelled before mount")
            self.initialize()
            username, password = self._smb_credentials[:2]
            domain = self._smb_credentials[2] if len(self._smb_credentials) > 2 else None
            cmd = ['sudo', 'mount.cifs', f'//{server}/{share}', mount_point]
            opts = [f'username={username}', f'password={password}']
            if domain:
                opts.append(f'domain={domain}')
            opts += ['uid=1000', 'gid=1000', 'iocharset=utf8']
            cmd.extend(['-o', ','.join(opts)])
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if proc.returncode == 0:
                with QMutexLocker(self.mutex):
                    self._mounted_shares[key] = mount_point
            else:
                if self.thread and getattr(self.thread, 'cancelled', False):
                    raise RuntimeError("Operation cancelled")
                sudo_password = self._get_sudo_password()
                cmd = ['sudo', '-S', 'mount.cifs', f'//{server}/{share}', mount_point, '-o', ','.join(opts)]
                proc_2 = subprocess.run(cmd, input=f"{sudo_password}\n", capture_output=True, text=True, timeout=10)
                if proc_2.returncode != 0:
                    os.rmdir(mount_point)
                    raise RuntimeError(f"Mount failed: {proc_2.stderr}")
                with QMutexLocker(self.mutex):
                    self._mounted_shares[key] = mount_point
            return mount_point
        except subprocess.TimeoutExpired:
            if os.path.exists(mount_point):
                os.rmdir(mount_point)
            raise RuntimeError("Mount operation timed out")
        except Exception as e:
            if os.path.exists(mount_point):
                os.rmdir(mount_point)
            raise e
        finally:
            with QMutexLocker(self.mutex):
                self._mounting_shares.discard(key)
                if key in self._mount_wait_conditions:
                    self._mount_wait_conditions[key].wakeAll()

    @staticmethod
    def _unmount_smb_share(mount_point, sudo_password=None):
        try:
            cmd = ['sudo', '-S', 'umount', mount_point] if sudo_password else ['sudo', 'umount', mount_point]
            subprocess.run(cmd, input=f"{sudo_password}\n" if sudo_password else None, capture_output=True, text=True)
            os.rmdir(mount_point)
        except Exception as e:
            print(f"Warning: Could not unmount {mount_point}: {e}")

    def _smb_path_to_local(self, smb_path):
        server, share, path = self.parse_smb_url(smb_path)
        mount_point = self._mount_smb_share(server, share)
        return os.path.join(mount_point, path) if path else mount_point

    def copy_file(self, source, destination, progress_callback=None):
        if self.thread and getattr(self.thread, "cancelled", False):
            return None
        src_is_smb = self.is_smb_path(source)
        dst_is_smb = self.is_smb_path(destination)
        try:
            if src_is_smb and not dst_is_smb:
                return self._copy_smb_to_local(source, destination, progress_callback)
            if not src_is_smb and dst_is_smb:
                return self._copy_local_to_smb(source, destination, progress_callback)
            return self._copy_local(source, destination, progress_callback)
        except Exception as e:
            fn = Path(source).name
            if progress_callback:
                progress_callback(False, fn, str(e))
            raise

    def _copy_smb_to_local(self, source, destination, progress_callback):
        if self.thread and getattr(self.thread, "cancelled", False):
            return None
        local_source = self._smb_path_to_local(source)
        fn = Path(source).name or "directory"
        try:
            if os.path.isdir(local_source):
                dest_path = os.path.join(destination, os.path.basename(local_source))
                shutil.copytree(local_source, dest_path, dirs_exist_ok=True)
                total = sum(f.stat().st_size for f in Path(dest_path).rglob('*') if f.is_file())
            else:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                shutil.copy2(local_source, destination)
                total = os.path.getsize(destination)
            if progress_callback:
                progress_callback(True, fn, total)
            return total
        except Exception as e:
            if progress_callback:
                progress_callback(False, fn, str(e))
            raise

    def _copy_local_to_smb(self, source, destination, progress_callback):
        if self.thread and getattr(self.thread, "cancelled", False):
            return None
        local_destination = self._smb_path_to_local(destination)
        fn = Path(source).name
        try:
            if os.path.isdir(source):
                dest_path = os.path.join(local_destination, os.path.basename(source))
                shutil.copytree(source, dest_path, dirs_exist_ok=True)
                total = sum(f.stat().st_size for f in Path(source).rglob('*') if f.is_file())
            else:
                os.makedirs(os.path.dirname(local_destination), exist_ok=True)
                shutil.copy2(source, local_destination)
                total = os.path.getsize(source)
            if progress_callback:
                progress_callback(True, fn, total)
            return total
        except Exception as e:
            if progress_callback:
                progress_callback(False, fn, str(e))
            raise

    def _copy_local(self, source, destination, progress_callback):
        if self.thread and getattr(self.thread, "cancelled", False):
            return None
        fn = Path(source).name
        try:
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            if Path(source).is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=True)
                total = sum(f.stat().st_size for f in Path(destination).rglob('*') if f.is_file())
            else:
                shutil.copy2(source, destination)
                total = os.path.getsize(destination)
            if progress_callback:
                progress_callback(True, fn, total)
            return total
        except Exception as e:
            if progress_callback:
                progress_callback(False, fn, str(e))
            raise

    def is_directory(self, path):
        if self.is_smb_path(path):
            try:
                return os.path.isdir(self._smb_path_to_local(path))
            except Exception as e:
                print(f"Error in is_directory: {e}")
                return False
        return Path(path).is_dir()

    def get_smb_file_size(self, path):
        if not self.is_smb_path(path):
            return 0
        try:
            local_path = self._smb_path_to_local(path)
            if os.path.isfile(local_path):
                return os.path.getsize(local_path)
            if os.path.isdir(local_path):
                return sum(f.stat().st_size for f in Path(local_path).rglob('*') if f.is_file())
            return 0
        except Exception as e:
            print(f"Error in get_smb_file_size: {e}")
            return 0

    def list_smb_directory(self, path):
        if not self.is_smb_path(path):
            return []
        try:
            local_path = self._smb_path_to_local(path)
            return [f for f in os.listdir(local_path) if not f.startswith('.')] if os.path.isdir(local_path) else []
        except Exception as e:
            print(f"Error in list_smb_directory: {e}")
            return []

    def cleanup(self):
        for (server, share), mount_point in list(self._mounted_shares.items()):
            try:
                time.sleep(0.5)
                self._unmount_smb_share(mount_point, self._sudo_password)
            except Exception as e:
                print(f"Cleanup warning: {e}")
                try:
                    subprocess.run(['sudo', 'umount', '-l', mount_point], timeout=1, capture_output=True)
                    if os.path.exists(mount_point):
                        os.rmdir(mount_point)
                except Exception as e:
                    print(f"Cleanup warning: {e}")
        self._mounted_shares.clear()
        self._mounting_shares.clear()
        self._mount_wait_conditions.clear()

    def force_cleanup(self):
        try:
            for (server, share), mount_point in list(self._mounted_shares.items()):
                try:
                    subprocess.run(['sudo', 'umount', '-l', mount_point], timeout=2, capture_output=True)
                    if os.path.exists(mount_point):
                        os.rmdir(mount_point)
                except Exception as e:
                    print(f"Force cleanup error (ignored): {e}")
            self._mounted_shares.clear()
            self._mounting_shares.clear()
            with QMutexLocker(self.mutex):
                for condition in self._mount_wait_conditions.values():
                    condition.wakeAll()
            self._mount_wait_conditions.clear()
        except Exception as e:
            print(f"Force cleanup error (ignored): {e}")


class LogEntryListModel(QAbstractListModel):
    def __init__(self, entries, entry_types, parent=None):
        super().__init__(parent)
        self._entries = entries
        self._types = entry_types
        self.filter = ""
        self._filtered_indices = list(range(len(entries)))

    def rowCount(self, parent=QModelIndex()):
        return len(self._filtered_indices)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return QVariant()
        row = self._filtered_indices[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return self._entries[row]
        if role == Qt.ItemDataRole.ForegroundRole:
            t = self._types[row]
            if t == "error":
                return Qt.GlobalColor.red
            elif t == "skipped":
                return Qt.GlobalColor.yellow
            elif t == "copied":
                return Qt.GlobalColor.green
        return QVariant()

    def setFilter(self, text):
        self.filter = text.lower()
        if self.filter:
            self._filtered_indices = [i for i, e in enumerate(self._entries) if self.filter in e.lower()]
        else:
            self._filtered_indices = list(range(len(self._entries)))
        self.layoutChanged.emit()

    def addEntry(self, entry, entry_type):
        self.beginInsertRows(QModelIndex(), len(self._entries), len(self._entries))
        self._entries.append(entry)
        self._types.append(entry_type)
        self.endInsertRows()
        self.setFilter(self.filter)

    def sort_entries(self):
        replaced = []
        for entry, entry_type in zip(self._entries, self._types):
            e = entry
            for old, new in getattr(Options, 'text_replacements', []):
                e = e.replace(old, new)
            replaced.append((e, entry_type))
        def extract_path(sorted_entry):
            m = re.match(r"^\d+:<br>'([^']+)'<br>", sorted_entry)
            if m:
                return m.group(1).lower()
            m2 = re.match(r"^\d+:\s*'([^']+)'", sorted_entry)
            if m2:
                return m2.group(1).lower()
            idx = sorted_entry.find('/')
            if idx != -1:
                end = sorted_entry.find('<br>', idx)
                if end == -1:
                    end = sorted_entry.find("'", idx)
                if end == -1:
                    end = sorted_entry.find(' ', idx)
                if end == -1:
                    end = len(sorted_entry)
                return sorted_entry[idx:end].lower()
            return sorted_entry.lower()
        replaced_sorted = sorted(replaced, key=lambda x: extract_path(x[0]))
        new_entries, new_types = [], []
        for i, (entry, entry_type) in enumerate(replaced_sorted):
            entry = re.sub(r"^\d+:(<br>)?", f"{i + 1}:<br>" if '<br>' in entry else f"{i + 1}:", entry, count=1)
            new_entries.append(entry)
            new_types.append(entry_type)
        self._entries[:] = new_entries
        self._types[:] = new_types
        self.layoutChanged.emit()
        self.setFilter(self.filter)


# noinspection PyUnresolvedReferences
class VirtualLogTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.entries = []
        self.entry_types = []
        self.pending_entries = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        search_label = QLabel("Search:")
        search_label.setStyleSheet("color: #e0e0e0;")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Filter entries...")
        layout.addWidget(search_label)
        layout.addWidget(self.search_box)
        self.model = LogEntryListModel(self.entries, self.entry_types)
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        self.list_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_view.setWordWrap(True)
        layout.addWidget(self.list_view)
        self.search_box.textChanged.connect(self.model.setFilter)
        self._flush_timer = QTimer(self)
        self._flush_timer.setInterval(300)
        self._flush_timer.timeout.connect(self.flush_entries)
        self._flush_timer.start()

    def add_entry(self, entry, entry_type):
        self.pending_entries.append((entry, entry_type))
        if not self._flush_timer.isActive():
            self._flush_timer.start()

    def flush_entries(self):
        if not self.pending_entries:
            return
        start = len(self.entries)
        entries, types = zip(*self.pending_entries)
        self.model.beginInsertRows(QModelIndex(), start, start + len(entries) - 1)
        self.entries.extend(entries)
        self.entry_types.extend(types)
        self.model.endInsertRows()
        self.pending_entries.clear()
        self.model.setFilter(self.model.filter)

    def sort_entries(self):
        self.model.sort_entries()


# noinspection PyUnresolvedReferences
class BackupRestoreProcessDialog(FileProcessDialog):
    def __init__(self, parent, checkbox_dirs, operation_type="Backup"):
        super().__init__(parent, checkbox_dirs, operation_type)


# noinspection PyUnresolvedReferences
class SudoPasswordDialog(QDialog):
    sudo_password_entered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sudo-Authentication")
        self.layout = QVBoxLayout(self)
        self.failed_attempts = 0
        self.label = QLabel("Please enter your sudo password to run Package Installer.\nThis will be used for all sudo commands during execution.")
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)
        self.password_layout = QHBoxLayout()
        self.password_label = QLabel("Password:")
        self.password_layout.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your sudo password")
        self.password_layout.addWidget(self.password_input)
        self.layout.addLayout(self.password_layout)
        self.info_label = QLabel("Note: For security, only one authentication attempt will be made.")
        self.info_label.setStyleSheet("color: #666; font-style: italic;")
        self.layout.addWidget(self.info_label)
        self.layout.addSpacing(10)
        self.button_layout = QHBoxLayout()
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.close_button)
        self.ok_button = QPushButton("Authenticate", self)
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.ok_button.setDefault(True)
        self.button_layout.addWidget(self.ok_button)
        self.layout.addLayout(self.button_layout)
        self.password_input.setFocus()
        self.password_input.returnPressed.connect(self.ok_button.click)

    def on_ok_clicked(self):
        sudo_password = self.password_input.text()
        if sudo_password:
            self.sudo_password_entered.emit(sudo_password)
            self.password_input.clear()
            self.accept()
        else:
            QMessageBox.warning(self, "Empty Password", "Please enter your sudo password or click Close.")

    def update_failed_attempts(self, failed_attempts):
        self.failed_attempts = failed_attempts
        if str(self.failed_attempts) == "2":
            msg = "Attention! Third attempt!\nPassword could be blocked temporarily if entered incorrectly."
            self.info_label.setStyleSheet("color: red; font-style: italic; font-weight: bold;")
        else:
            msg = f"Note: For security, only one authentication attempt will be made.\nFailed attempts: {self.failed_attempts}"
            self.info_label.setStyleSheet("color: #6b811b; font-style: italic; font-weight: normal;")
        self.info_label.setText(msg)
        self.adjustSize()


class SecureString:
    def __init__(self, initial_value=None):
        self._value = bytearray(initial_value.encode('utf-8')) if initial_value else bytearray()

    def get_value(self):
        return self._value.decode('utf-8') if self._value else ''

    def clear(self):
        if self._value:
            try:
                for i in range(len(self._value)):
                    self._value[i] = secrets.randbelow(256)
            finally:
                del self._value[:]
                self._value = None


# noinspection PyUnresolvedReferences
class SambaPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Samba Credentials")
        self.samba_password_manager = SambaPasswordManager()
        self.has_existing_credentials = False
        self.password_from_keyring = False
        self.error_dialog = QErrorMessage(self)
        layout = QVBoxLayout()
        try:
            current_user = os.getlogin()
        except OSError:
            current_user = getpass.getuser() if hasattr(__builtins__, 'getpass') else "user"
        try:
            username, password = self.samba_password_manager.get_samba_credentials()
            if password:
                keyring_source = "KWallet" if self.samba_password_manager.kwallet_entry else "system keyring"
                self.password_from_keyring = self.samba_password_manager.kwallet_entry is None
                info_text = f"(Password extracted from {keyring_source}.)"
                self.has_existing_credentials = True
            else:
                info_text = "(No password found. Create new entry in system keyring.)"
        except Exception as e:
            username = current_user
            password = None
            info_text = f"(Error retrieving credentials: {type(e).__name__})"
        self.info_label = QLabel(info_text)
        self.username_label = QLabel("Username:")
        self.username_field = QLineEdit()
        self.username_field.setText(username or current_user)
        self.password_label = QLabel("Password:")
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        if password:
            self.password_field.setText(password)
        self.show_password = QCheckBox("Show password")
        self.show_password.setStyleSheet("color: lightgreen;")
        self.show_password.clicked.connect(self.toggle_password_visibility)
        button_box = QHBoxLayout()
        self.save_button = QPushButton()
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.reject)
        button_box.addWidget(self.close_button)
        if self.password_from_keyring:
            credentials_available_label = QLabel("Credentials already available.\nNo need to save again unless you want to change them.")
            credentials_available_label.setStyleSheet("color: lightgreen;")
            layout.addWidget(credentials_available_label)
            self.delete_button = QPushButton("Delete credentials")
            self.delete_button.clicked.connect(self.del_samba_credentials)
            button_box.addWidget(self.delete_button)
        self.save_button.setText("Update credentials") if self.has_existing_credentials else self.save_button.setText("Save")
        button_box.addWidget(self.save_button)
        self.setMinimumSize(475, 325)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_field)
        layout.addWidget(self.info_label)
        layout.addWidget(self.show_password)
        self.save_button.clicked.connect(self.save_password)
        layout.addLayout(button_box)
        self.setLayout(layout)

    def toggle_password_visibility(self):
        if self.show_password.isChecked():
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

    def save_password(self):
        username = self.username_field.text()
        password = self.password_field.text()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return
        try:
            self.samba_password_manager.save_samba_credentials(username, password)
            self.accept()
            QMessageBox.information(self, "Success", "Samba credentials successfully saved!")
        except Exception as e:
            self.error_dialog.showMessage(f"Failed to save credentials.\n{e}")

    def del_samba_credentials(self):
        username = self.username_field.text()
        try:
            self.samba_password_manager.delete_samba_credentials(username)
            self.accept()
            QMessageBox.information(self, "Success", "Samba credentials successfully deleted!")
        except Exception as e:
            self.error_dialog.showMessage(f"Failed to delete credentials: {str(e)}")


class SambaPasswordManager:
    def __init__(self):
        self.keyring_service = "backup-helper-samba"
        self.kwallet_wallet = "kdewallet"
        self.kwallet_entry = None
        self._set_system_keyring()

    @staticmethod
    def _set_system_keyring():
        try:
            keyring.set_keyring(SecretService.Keyring())
        except keyring.errors.KeyringError:
            pass

    def _find_kwallet_entry(self):
        if self.kwallet_entry:
            return self.kwallet_entry
        try:
            result = subprocess.run(["kwallet-query", "--list-entries", self.kwallet_wallet], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=2)
            entries = result.stdout.strip().splitlines()
            for entry in entries:
                if entry.startswith("smb-"):
                    self.kwallet_entry = entry
                    print(f"Found KWallet entry: {entry}")
                    return entry
        except Exception as e:
            print(f"Failed to list KWallet entries: {e}")
        return None

    def _get_password_from_kwallet(self):
        entry = self._find_kwallet_entry()
        if not entry:
            return None, None
        try:
            result = subprocess.run(["kwallet-query", "--read-password", entry, self.kwallet_wallet], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=2)
            raw = result.stdout.strip()
            if not raw:
                return None, None
            credentials = json.loads(raw)
            return credentials.get("login"), credentials.get("password")
        except Exception as e:
            print(f"Failed to retrieve password from KWallet: {e}")
            return None, None

    def _save_password_to_kwallet(self, username, password):
        entry = self._find_kwallet_entry()
        if not entry:
            entry = f"smb-{username}-backup"
            self.kwallet_entry = entry
        try:
            data = json.dumps({"login": username, "password": password})
            with subprocess.Popen(["kwallet-query", "--write-password", entry, self.kwallet_wallet], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as proc:
                proc.communicate(input=data.encode(), timeout=2)
            print(f"Saved samba credentials to KWallet entry: {entry}")
        except Exception as e:
            print(f"Failed to save credentials to KWallet: {type(e).__name__}")

    def get_samba_credentials(self):
        print("get_samba_credentials was called")
        username, password = self._get_password_from_kwallet()
        if password:
            print("Retrieved samba password from KWallet")
            return username, password
        try:
            username = os.getlogin()
            password = keyring.get_password(self.keyring_service, username)
            if password:
                print("Retrieved samba password from system keyring")
                return username, password
        except Exception as e:
            print(f"Failed to retrieve from keyring: {e}")
        return None, None

    def save_samba_credentials(self, username, password):
        kwallet_username, kwallet_password = self._get_password_from_kwallet()
        if kwallet_password:
            self._save_password_to_kwallet(username, password)
        else:
            try:
                keyring.set_password(self.keyring_service, username, password)
                print("Saved samba password to system keyring")
            except Exception as e:
                print(f"Failed to save to keyring: {e}")

    def delete_samba_credentials(self, username):
        success = True
        try:
            keyring.delete_password(self.keyring_service, username)
            print(f"Deleted samba password for {username} from keyring")
        except Exception as e:
            print(f"Failed to delete from keyring for {username}: {e}")
            success = False
        return success


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(global_style)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
