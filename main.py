from tkinter.messagebox import showerror

import ui
from experiment import *
from database import *

exp = None

def set_experiment():
    global exp
    exp = Experiment(ui.loaded_image_path)
    exp.execute()
    ui.set_experiment_info(exp.path, exp.date, exp.counts)

def write_to_db():
    add_record(exp.date, exp.path, exp.counts)

def read_db():
    if (ui.all_checkbox_value.get()):
        rows = get_all_records()
        ui.fill_table(rows)
    else:
        try:
            id_from = int(ui.from_entry.get())
            id_to = int(ui.to_entry.get())
            rows = get_records_index(id_from, id_to)
            ui.fill_table(rows)
        except ValueError as e:
            showerror("Ошибка", "Некорректно введённые данные")

ui.count_cells_button.config(command = set_experiment)
ui.write_database_button.config(command = write_to_db)
ui.read_database_button.config(command = read_db)

ui.window.mainloop()

