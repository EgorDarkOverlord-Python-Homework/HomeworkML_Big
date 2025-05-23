from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
from PIL import Image, ImageTk  # pip install pillow
import cv2
import numpy as np
from image_processing import *

loaded_image = None
loaded_image_path = None
zoom = 1


def set_experiment_info(loaded_image_path, experiment_date, counts):
    file_path_label.config(text=loaded_image_path)
    date_label.config(text=experiment_date)
    count_1_label.config(text=counts[0])
    count_2_label.config(text=counts[1])
    count_3_label.config(text=counts[2])


def set_image_to_label(label, image, zoom=1):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(
        image.resize((int(image.width * zoom), int(image.height * zoom)))
    )
    label.configure(image=image)
    label.image = image


def resize_image(scale):
    try:
        global zoom
        zoom *= scale
        set_image_to_label(image_label, loaded_image, zoom)
    except cv2.error as e:
        if e.err == "!_src.empty()":
            showerror("Ошибка", "Изображение не загружено")


def on_load_image_button_click():
    path = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=(
            ("all files", "*.*"),
            ("jpeg files", "*.jpg"),
            ("png files", "*.png"),        
        ),
    )

    if path:
        try:
            global loaded_image
            loaded_image = cv2.imdecode(
                np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED
            )
            global zoom
            zoom = 1
            set_image_to_label(image_label, loaded_image, zoom)

            global loaded_image_path
            loaded_image_path = path
            file_path_label.config(text=loaded_image_path)
        except Exception as e:
            showerror("Ошибка", "Некорректный путь")


def hide_frames():
    image_frame.grid_forget()
    database_frame.grid_forget()

def on_work_image_button_click():
    hide_frames()
    image_frame.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)

def on_database_button_click():
    hide_frames()
    database_frame.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)



def fill_table(rows):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)
    


window = Tk()
window.minsize(800, 600)
window.title("Подсчёт клеток")

window.columnconfigure(0, weight=1)
window.rowconfigure(1, weight=1)



choice_frame = Frame(window)
choice_frame.grid(row=0, column=0, sticky=EW, padx=5, pady=5)

work_image_button = ttk.Button(
    choice_frame,
    text="Работа с изображением",
    command=on_work_image_button_click,
)
work_image_button.pack(fill=X, side=LEFT, expand=True)

database_button = ttk.Button(
    choice_frame,
    text="Чтение базы данных",
    command=on_database_button_click,
)
database_button.pack(fill=X, side=LEFT, expand=True)



image_frame = Frame(window)
image_frame.columnconfigure(0, weight=1)
image_frame.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)

image_button_frame = Frame(image_frame)
image_button_frame.grid(row=0, column=0, sticky=EW, padx=0, pady=5)

load_image_button = ttk.Button(
    image_button_frame,
    text="Загрузка изображения",
    command=on_load_image_button_click,
)
load_image_button.pack(fill=X, side=LEFT, expand=True)

count_cells_button = ttk.Button(
    image_button_frame,
    text="Подсчёт клеток",
    command=None,
)
count_cells_button.pack(fill=X, side=LEFT, expand=True)

write_database_button = ttk.Button(
    image_button_frame,
    text="Запись в базу данных",
    command=None,
)
write_database_button.pack(fill=X, side=LEFT, expand=True)

experiment_result_frame = Frame(image_frame)
experiment_result_frame.grid(row=1, column=0, sticky=EW, padx=0, pady=5)
file_path_text_label = Label(experiment_result_frame, text="Путь к файлу: ", anchor="w")
file_path_text_label.grid(row=0, column=0, sticky=EW, padx=0, pady=5)
date_text_label = Label(experiment_result_frame, text="Дата эксперимента: ", anchor="w")
date_text_label.grid(row=1, column=0, sticky=EW, padx=0, pady=5)
count_1_text_label = Label(experiment_result_frame, text="Количество клеток 1: ", anchor="w")
count_1_text_label.grid(row=2, column=0, sticky=EW, padx=0, pady=5)
count_2_text_label = Label(experiment_result_frame, text="Количество клеток 2: ", anchor="w")
count_2_text_label.grid(row=3, column=0, sticky=EW, padx=0, pady=5)
count_3_text_label = Label(experiment_result_frame, text="Количество клеток 3: ", anchor="w")
count_3_text_label.grid(row=4, column=0, sticky=EW, padx=0, pady=5)
file_path_label = Label(experiment_result_frame, text="Путь к файлу: ", anchor="w")
file_path_label.grid(row=0, column=1, sticky=EW, padx=0, pady=5)
date_label = Label(experiment_result_frame, text="Дата эксперимента: ", anchor="w")
date_label.grid(row=1, column=1, sticky=EW, padx=0, pady=5)
count_1_label = Label(experiment_result_frame, text="Количество клеток 1: ", anchor="w")
count_1_label.grid(row=2, column=1, sticky=EW, padx=0, pady=5)
count_2_label = Label(experiment_result_frame, text="Количество клеток 2: ", anchor="w")
count_2_label.grid(row=3, column=1, sticky=EW, padx=0, pady=5)
count_3_label = Label(experiment_result_frame, text="Количество клеток 3: ", anchor="w")
count_3_label.grid(row=4, column=1, sticky=EW, padx=0, pady=5)

image_frame.rowconfigure(2, weight=1)
canvas = Canvas(image_frame, bg="white")
canvas.grid(row=2, column=0, sticky=NSEW, padx=0, pady=5)
image_label = Label(canvas)
image_label.place(relx=0.5, rely=0.5, anchor="center")

zoom_frame = Frame(image_frame)
zoom_frame.grid(row=3, column=0, sticky=EW, padx=0, pady=5)
zoom_plus_button = ttk.Button(
    zoom_frame,
    text="+",
    command=lambda: resize_image(1.5),
)
zoom_plus_button.pack(side=LEFT)
zoom_minus_button = ttk.Button(
    zoom_frame,
    text="-",
    command=lambda: resize_image(1 / 1.5),
)
zoom_minus_button.pack(side=LEFT)



database_frame = Frame(window)
database_frame.columnconfigure(0, weight=1)
database_frame.rowconfigure(1, weight=1)
database_frame.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)

index_frame = Frame(database_frame)
index_frame.grid(row=0, column=0, sticky=EW, padx=0, pady=0)
index_frame.columnconfigure(1, weight=1)
from_text_label = Label(index_frame, text="От: ", anchor="w")
from_entry = ttk.Entry(index_frame)
to_text_label = Label(index_frame, text="До: ", anchor="w")
to_entry = ttk.Entry(index_frame)
all_checkbox_value = BooleanVar()
all_checkbox = ttk.Checkbutton(index_frame, text="Целиком", variable=all_checkbox_value, onvalue=True, offvalue=False)
all_checkbox_value.set(True)
read_database_button = ttk.Button(
    index_frame,
    text="Считать базу данных",
    command=None,
)
from_text_label.grid(row=0, column=0, sticky=EW, padx=0, pady=0)
from_entry.grid(row=0, column=1, sticky=EW, padx=0, pady=0)
to_text_label.grid(row=1, column=0, sticky=EW, padx=0, pady=5)
to_entry.grid(row=1, column=1, sticky=EW, padx=0, pady=5)
all_checkbox.grid(row=2, column=0, sticky=EW, padx=0, pady=0)
read_database_button.grid(row=2, column=1, sticky=EW, padx=0, pady=0)

table_frame = Frame(database_frame)
table_frame.grid(row=1, column=0, sticky=NSEW, padx=0, pady=5)
table_frame.columnconfigure(0, weight=1)
table_frame.rowconfigure(0, weight=1)

# определяем столбцы
columns = ("number", "date", "path", "method1", "method2", "method3")
 
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.grid(row=0, column=0, sticky=NSEW, padx=0, pady=0)
 
# определяем заголовки
tree.heading("number", text="Номер эксперимента")
tree.heading("date", text="Дата")
tree.heading("path", text="Путь к файлу")
tree.heading("method1", text="Метод 1")
tree.heading("method2", text="Метод 2")
tree.heading("method3", text="Метод 3")

# добавляем вертикальную прокрутку
scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")



image_frame.grid_forget()
database_frame.grid_forget()

#window.mainloop()
