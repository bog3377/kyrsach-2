import sys
from datetime import datetime

from PyQt6.QtCore import QDate, QTime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QTabWidget, QPushButton, QLabel, QComboBox,
                             QSpinBox, QTableWidget, QTableWidgetItem,
                             QMessageBox, QCalendarWidget, QTimeEdit, QDialog,
                             QHBoxLayout, QHeaderView, QLineEdit)

import database as db
import validation as val


class EditExamDialog(QDialog):
    def __init__(self, parent=None, exam_data=None, groups=None, examiners=None, rooms=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать экзамен")
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Название экзамена
        self.name_edit = QLineEdit()
        layout.addWidget(QLabel("Название экзамена:"))
        layout.addWidget(self.name_edit)

        # Создаем и заполняем поля формы
        self.group_combo = QComboBox()
        self.group_combo.addItems([g[1] for g in groups])
        layout.addWidget(QLabel("Группа:"))
        layout.addWidget(self.group_combo)

        # Календарь для выбора даты
        self.calendar = QCalendarWidget()
        layout.addWidget(QLabel("Дата:"))
        layout.addWidget(self.calendar)

        # Время начала
        self.time_edit = QTimeEdit()
        layout.addWidget(QLabel("Время:"))
        layout.addWidget(self.time_edit)

        # Длительность (часы и минуты)
        duration_layout = QHBoxLayout()
        self.duration_hours = QSpinBox()
        self.duration_hours.setRange(0, 8)
        self.duration_minutes = QSpinBox()
        self.duration_minutes.setRange(0, 59)
        self.duration_minutes.setSingleStep(5)

        duration_layout.addWidget(QLabel("Длительность:"))
        duration_layout.addWidget(self.duration_hours)
        duration_layout.addWidget(QLabel("ч"))
        duration_layout.addWidget(self.duration_minutes)
        duration_layout.addWidget(QLabel("мин"))
        layout.addLayout(duration_layout)

        self.examiner_combo = QComboBox()
        self.examiner_combo.addItems([e[1] for e in examiners])
        layout.addWidget(QLabel("Экзаменатор:"))
        layout.addWidget(self.examiner_combo)

        self.room_combo = QComboBox()
        self.room_combo.addItems([r[1] for r in rooms])
        layout.addWidget(QLabel("Аудитория:"))
        layout.addWidget(self.room_combo)

        # Кнопки
        button_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Если переданы данные для редактирования, заполняем поля
        if exam_data:
            self.name_edit.setText(exam_data['name'])
            self.group_combo.setCurrentText(exam_data['group'])
            exam_datetime = datetime.strptime(exam_data['datetime'], "%Y-%m-%d %H:%M")
            self.calendar.setSelectedDate(QDate(exam_datetime.year, exam_datetime.month, exam_datetime.day))
            self.time_edit.setTime(QTime(exam_datetime.hour, exam_datetime.minute))
            self.duration_hours.setValue(exam_data['duration_hours'])
            self.duration_minutes.setValue(exam_data['duration_minutes'])
            self.examiner_combo.setCurrentText(exam_data['examiner'])
            self.room_combo.setCurrentText(exam_data['room'])


class ExamSchedulerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name_edit = QLineEdit()
        self.group_combo = QComboBox()
        self.calendar = QCalendarWidget()
        self.time_edit = QTimeEdit()
        self.duration_hours = QSpinBox()
        self.duration_minutes = QSpinBox()
        self.examiner_combo = QComboBox()
        self.room_combo = QComboBox()
        self.exams_table = QTableWidget()
        self.new_group_edit = QComboBox()
        self.new_examiner_edit = QComboBox()
        self.new_room_edit = QComboBox()
        self.setWindowTitle("Планировщик демонстрационных экзаменов")
        self.setGeometry(100, 100, 1200, 800)

        # Инициализация базы данных
        self.db = db.Database()

        # Создаем главный виджет и layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Создаем вкладки
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Создаем вкладки
        self.schedule_tab = QWidget()
        self.manage_tab = QWidget()

        tabs.addTab(self.schedule_tab, "Расписание")
        tabs.addTab(self.manage_tab, "Управление данными")

        self.setup_schedule_tab()
        self.setup_manage_tab()

        # Загружаем данные
        self.load_data()

    def setup_schedule_tab(self):
        layout = QVBoxLayout(self.schedule_tab)

        # Форма добавления экзамена
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)

        # Название экзамена
        form_layout.addWidget(QLabel("Название экзамена:"))
        form_layout.addWidget(self.name_edit)

        # Выбор группы
        form_layout.addWidget(QLabel("Группа:"))
        form_layout.addWidget(self.group_combo)

        # Календарь
        form_layout.addWidget(QLabel("Дата:"))
        form_layout.addWidget(self.calendar)

        # Время
        form_layout.addWidget(QLabel("Время:"))
        form_layout.addWidget(self.time_edit)

        # Длительность (часы и минуты)
        duration_layout = QHBoxLayout()
        self.duration_hours.setRange(0, 8)
        self.duration_minutes.setRange(0, 59)
        self.duration_minutes.setSingleStep(5)

        duration_layout.addWidget(QLabel("Длительность:"))
        duration_layout.addWidget(self.duration_hours)
        duration_layout.addWidget(QLabel("ч"))
        duration_layout.addWidget(self.duration_minutes)
        duration_layout.addWidget(QLabel("мин"))
        form_layout.addLayout(duration_layout)

        # Экзаменатор
        form_layout.addWidget(QLabel("Экзаменатор:"))
        form_layout.addWidget(self.examiner_combo)

        # Аудитория
        form_layout.addWidget(QLabel("Аудитория:"))
        form_layout.addWidget(self.room_combo)

        # Кнопки
        add_button = QPushButton("Добавить экзамен")
        add_button.clicked.connect(self.add_exam)
        form_layout.addWidget(add_button)

        layout.addWidget(form_widget)

        # Таблица экзаменов
        self.exams_table.setColumnCount(8)
        self.exams_table.setHorizontalHeaderLabels(
            ["ID", "Название", "Группа", "Дата и время", "Длительность", "Экзаменатор", "Аудитория", "Действия"])
        self.exams_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.exams_table)

        # Кнопка обновления
        refresh_button = QPushButton("Обновить")
        refresh_button.clicked.connect(self.load_data)
        layout.addWidget(refresh_button)

    def update_exams_table(self):
        exams = self.db.get_exams()
        self.exams_table.setRowCount(len(exams))

        for i, exam in enumerate(exams):
            exam_id = exam[0]
            self.exams_table.setItem(i, 0, QTableWidgetItem(str(exam_id)))
            self.exams_table.setItem(i, 1, QTableWidgetItem(exam[1]))  # name
            self.exams_table.setItem(i, 2, QTableWidgetItem(exam[2]))  # group
            self.exams_table.setItem(i, 3, QTableWidgetItem(exam[5]))  # datetime
            duration_str = f"{exam[6]} ч {exam[7]} мин"
            self.exams_table.setItem(i, 4, QTableWidgetItem(duration_str))  # duration
            self.exams_table.setItem(i, 5, QTableWidgetItem(exam[3]))  # examiner
            self.exams_table.setItem(i, 6, QTableWidgetItem(exam[4]))  # room

            # Добавляем кнопки редактирования и удаления
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)

            edit_btn = QPushButton("Редактировать")
            edit_btn.clicked.connect(lambda checked, x=exam_id: self.edit_exam(x))

            delete_btn = QPushButton("Удалить")
            delete_btn.clicked.connect(lambda checked, x=exam_id: self.delete_exam(x))

            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.setContentsMargins(0, 0, 0, 0)

            self.exams_table.setCellWidget(i, 7, actions_widget)

    def add_exam(self):
        date = self.calendar.selectedDate()
        time = self.time_edit.time()
        datetime_str = f"{date.year()}-{date.month():02d}-{date.day():02d} {time.hour():02d}:{time.minute():02d}"

        exam_data = {
            'name': self.name_edit.text(),
            'group': self.group_combo.currentText(),
            'datetime': datetime_str,
            'duration_hours': self.duration_hours.value(),
            'duration_minutes': self.duration_minutes.value(),
            'examiner': self.examiner_combo.currentText(),
            'room': self.room_combo.currentText()
        }

        if not exam_data['name']:
            QMessageBox.warning(self, "Ошибка", "Введите название экзамена")
            return

        if self.validate_exam(exam_data):
            group_id = [g[0] for g in self.db.get_groups() if g[1] == exam_data['group']][0]
            examiner_id = [e[0] for e in self.db.get_examiners() if e[1] == exam_data['examiner']][0]
            room_id = [r[0] for r in self.db.get_rooms() if r[1] == exam_data['room']][0]

            self.db.add_exam(
                exam_data['name'],
                group_id,
                examiner_id,
                room_id,
                datetime_str,
                exam_data['duration_hours'],
                exam_data['duration_minutes']
            )
            self.update_exams_table()
            self.name_edit.clear()
            QMessageBox.information(self, "Успех", "Экзамен успешно добавлен")
        else:
            QMessageBox.warning(self, "Ошибка", "Обнаружен конфликт в расписании")

    def edit_exam(self, exam_id):
        exam_row = None
        for row in range(self.exams_table.rowCount()):
            if self.exams_table.item(row, 0).text() == str(exam_id):
                exam_row = row
                break

        if exam_row is not None:
            duration_text = self.exams_table.item(exam_row, 4).text()
            duration_parts = duration_text.split()
            hours = int(duration_parts[0])
            minutes = int(duration_parts[2])

            exam_data = {
                'name': self.exams_table.item(exam_row, 1).text(),
                'group': self.exams_table.item(exam_row, 2).text(),
                'datetime': self.exams_table.item(exam_row, 3).text(),
                'duration_hours': hours,
                'duration_minutes': minutes,
                'examiner': self.exams_table.item(exam_row, 5).text(),
                'room': self.exams_table.item(exam_row, 6).text()
            }

            dialog = EditExamDialog(
                self,
                exam_data,
                self.db.get_groups(),
                self.db.get_examiners(),
                self.db.get_rooms()
            )

            if dialog.exec() == QDialog.DialogCode.Accepted:
                date = dialog.calendar.selectedDate()
                time = dialog.time_edit.time()
                datetime_str = f"{date.year()}-{date.month():02d}-{date.day():02d} {time.hour():02d}:{time.minute():02d}"

                new_exam_data = {
                    'name': dialog.name_edit.text(),
                    'group': dialog.group_combo.currentText(),
                    'datetime': datetime_str,
                    'duration_hours': dialog.duration_hours.value(),
                    'duration_minutes': dialog.duration_minutes.value(),
                    'examiner': dialog.examiner_combo.currentText(),
                    'room': dialog.room_combo.currentText()
                }

                if not new_exam_data['name']:
                    QMessageBox.warning(self, "Ошибка", "Введите название экзамена")
                    return

                if self.validate_exam(new_exam_data, exclude_id=exam_id):
                    group_id = [g[0] for g in self.db.get_groups() if g[1] == new_exam_data['group']][0]
                    examiner_id = [e[0] for e in self.db.get_examiners() if e[1] == new_exam_data['examiner']][0]
                    room_id = [r[0] for r in self.db.get_rooms() if r[1] == new_exam_data['room']][0]

                    self.db.update_exam(
                        exam_id,
                        new_exam_data['name'],
                        group_id,
                        examiner_id,
                        room_id,
                        datetime_str,
                        new_exam_data['duration_hours'],
                        new_exam_data['duration_minutes']
                    )
                    self.update_exams_table()
                    QMessageBox.information(self, "Успех", "Экзамен успешно обновлен")
                else:
                    QMessageBox.warning(self, "Ошибка", "Обнаружен конфликт в расписании")

    def delete_exam(self, exam_id):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить этот экзамен?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_exam(exam_id)
            self.update_exams_table()
            QMessageBox.information(self, "Успех", "Экзамен успешно удален")

    def validate_exam(self, exam_data, exclude_id=None):
        # Получаем все экзамены кроме исключаемого
        all_exams = self.db.get_exams()
        existing_exams = []

        for exam in all_exams:
            if exclude_id is None or str(exam[0]) != str(exclude_id):
                existing_exams.append({
                    'group': exam[2],
                    'datetime': datetime.strptime(exam[5], "%Y-%m-%d %H:%M"),
                    'duration': exam[6] + exam[7] / 60,  # Преобразуем в часы
                    'examiner': exam[3],
                    'room': exam[4]
                })

        new_exam = {
            'group': exam_data['group'],
            'datetime': datetime.strptime(exam_data['datetime'], "%Y-%m-%d %H:%M"),
            'duration': exam_data['duration_hours'] + exam_data['duration_minutes'] / 60,  # Преобразуем в часы
            'examiner': exam_data['examiner'],
            'room': exam_data['room']
        }

        return val.validate_exam(new_exam, existing_exams)

    def add_group(self):
        group = self.new_group_edit.currentText()
        if group:
            self.db.add_group(group)
            self.load_data()
            self.new_group_edit.setCurrentText("")

    def add_examiner(self):
        examiner = self.new_examiner_edit.currentText()
        if examiner:
            self.db.add_examiner(examiner)
            self.load_data()
            self.new_examiner_edit.setCurrentText("")

    def add_room(self):
        room = self.new_room_edit.currentText()
        if room:
            self.db.add_room(room)
            self.load_data()
            self.new_room_edit.setCurrentText("")

    def load_data(self):
        # Загружаем группы
        groups = self.db.get_groups()
        self.group_combo.clear()
        self.group_combo.addItems([g[1] for g in groups])

        # Загружаем экзаменаторов
        examiners = self.db.get_examiners()
        self.examiner_combo.clear()
        self.examiner_combo.addItems([e[1] for e in examiners])

        # Загружаем аудитории
        rooms = self.db.get_rooms()
        self.room_combo.clear()
        self.room_combo.addItems([r[1] for r in rooms])

        # Обновляем таблицу экзаменов
        self.update_exams_table()

    def setup_manage_tab(self):
        layout = QVBoxLayout(self.manage_tab)

        # Управление группами
        group_widget = QWidget()
        group_layout = QVBoxLayout(group_widget)
        group_layout.addWidget(QLabel("Добавить группу:"))
        self.new_group_edit.setEditable(True)
        group_layout.addWidget(self.new_group_edit)
        add_group_btn = QPushButton("Добавить")
        add_group_btn.clicked.connect(self.add_group)
        group_layout.addWidget(add_group_btn)
        layout.addWidget(group_widget)

        # Управление экзаменаторами
        examiner_widget = QWidget()
        examiner_layout = QVBoxLayout(examiner_widget)
        examiner_layout.addWidget(QLabel("Добавить экзаменатора:"))
        self.new_examiner_edit.setEditable(True)
        examiner_layout.addWidget(self.new_examiner_edit)
        add_examiner_btn = QPushButton("Добавить")
        add_examiner_btn.clicked.connect(self.add_examiner)
        examiner_layout.addWidget(add_examiner_btn)
        layout.addWidget(examiner_widget)

        # Управление аудиториями
        room_widget = QWidget()
        room_layout = QVBoxLayout(room_widget)
        room_layout.addWidget(QLabel("Добавить аудиторию:"))
        self.new_room_edit.setEditable(True)
        room_layout.addWidget(self.new_room_edit)
        add_room_btn = QPushButton("Добавить")
        add_room_btn.clicked.connect(self.add_room)
        room_layout.addWidget(add_room_btn)
        layout.addWidget(room_widget)


def main():
    app = QApplication(sys.argv)
    window = ExamSchedulerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
