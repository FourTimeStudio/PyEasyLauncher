import tkinter as tk
from tkinter import filedialog, Toplevel, Label, Entry, Button, Menu, messagebox, StringVar
import json
import os
import webbrowser

class AppLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyEasyLauncher")
        self.geometry("800x600")
        self.configure(bg="black")
        self.resizable(False, False) 

        self.apps = []
        self.quick_access_apps = []
        self.current_section = 'all'  
        self.language = StringVar(value="en")  
        self.load_apps()
        self.load_settings()

        self.create_widgets()

    def create_widgets(self):
       
        search_frame = tk.Frame(self, bg="black")
        search_frame.pack(pady=10, padx=10, fill=tk.X)

        self.search_label = tk.Label(search_frame, text=self.translate("Поиск:"), bg="black", fg="white")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.search_apps)

        
        self.line_frame = tk.Frame(self, bg="white", height=1)
        self.line_frame.pack(fill=tk.X, padx=10)

        
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        
        self.sections_frame = tk.Frame(self.main_frame, bg="black")
        self.sections_frame.pack(fill=tk.X)

        
        self.all_apps_button = tk.Button(self.sections_frame, text=self.translate("Все программы"), command=self.show_all_apps, bg="#333", fg="white")
        self.all_apps_button.pack(side=tk.LEFT, padx=10)
        self.quick_access_button = tk.Button(self.sections_frame, text=self.translate("Быстрый доступ"), command=self.show_quick_access_apps, bg="#333", fg="white")
        self.quick_access_button.pack(side=tk.LEFT, padx=10)
        self.about_button = tk.Button(self.sections_frame, text=self.translate("О программе"), command=self.show_about, bg="#333", fg="white")
        self.about_button.pack(side=tk.LEFT, padx=10)

        
        self.settings_button = tk.Button(self.sections_frame, text=self.translate("Настройки"), command=self.open_settings_window, bg="#333", fg="white")
        self.settings_button.pack(side=tk.RIGHT, padx=10)

        
        self.canvas = tk.Canvas(self.main_frame, bg="black")
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        
        self.apps_frame = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window((0, 0), window=self.apps_frame, anchor='nw')

        
        self.add_button = tk.Button(self, text="+", command=self.open_add_app_window, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.add_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SE)

        self.show_all_apps()

    def open_settings_window(self):
        self.settings_window = Toplevel(self)
        self.settings_window.title(self.translate("Настройки"))
        self.settings_window.geometry("400x200")
        self.settings_window.configure(bg="black")
        self.settings_window.resizable(False, False)

        Label(self.settings_window, text=self.translate("Выбор языка:"), bg="black", fg="white").pack(pady=10)

        
        languages = {"ru": "Русский", "en": "English", "uk": "Українська"}
        for code, lang in languages.items():
            tk.Radiobutton(self.settings_window, text=lang, variable=self.language, value=code, bg="black", fg="white",
                           command=self.change_language).pack(anchor=tk.W, padx=20, pady=5)

    def change_language(self):
        self.save_settings()
        self.refresh_ui()

    def refresh_ui(self):
        
        self.search_label.config(text=self.translate("Поиск:"))
        self.all_apps_button.config(text=self.translate("Все программы"))
        self.quick_access_button.config(text=self.translate("Быстрый доступ"))
        self.about_button.config(text=self.translate("О программе"))
        self.settings_button.config(text=self.translate("Настройки"))
        if self.current_section == 'all':
            self.show_all_apps()
        elif self.current_section == 'quick_access':
            self.show_quick_access_apps()
        elif self.current_section == 'about':
            self.show_about()

    def translate(self, text):
        translations = {
            "ru": {
                "Поиск:": "Поиск:",
                "Все программы": "Все программы",
                "Быстрый доступ": "Быстрый доступ",
                "О программе": "О программе",
                "Настройки": "Настройки",
                "Выбор языка:": "Выбор языка:",
                "about_text": """
                FourTime Studio Launcher v1.0

                Программа разработана для удобного запуска ваших приложений.
                Вы можете добавлять, редактировать, удалять программы, а также
                просматривать местоположение файлов.

                Открытый код: https://github.com/FourTimeStudio/PyEasyLauncher/tree/main
                """
            },
            "en": {
                "Поиск:": "Search:",
                "Все программы": "All Applications",
                "Быстрый доступ": "Quick Access",
                "О программе": "About",
                "Настройки": "Settings",
                "Выбор языка:": "Select Language:",
                "about_text": """
                FourTime Studio Launcher v1.0

                The program is designed for easy launching of your applications.
                You can add, edit, delete programs, and also
                view the location of files.

                Open source: https://github.com/FourTimeStudio/PyEasyLauncher/tree/main
                """
            },
            "uk": {
                "Поиск:": "Пошук:",
                "Все программы": "Усі програми",
                "Быстрый доступ": "Швидкий доступ",
                "О программе": "Про програму",
                "Настройки": "Налаштування",
                "Выбор языка:": "Вибір мови:",
                "about_text": """
                FourTime Studio Launcher v1.0

                Програма розроблена для зручного запуску ваших додатків.
                Ви можете додавати, редагувати, видаляти програми, а також
                переглядати місцезнаходження файлів.

                Відкритий код: https://github.com/FourTimeStudio/PyEasyLauncher/tree/main
                """
            }
        }
        return translations.get(self.language.get(), translations["ru"]).get(text, text)

    def save_settings(self):
        settings = {"language": self.language.get()}
        with open("settings.json", "w") as file:
            json.dump(settings, file, indent=4)

    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.language.set(settings.get("language", "ru"))
        else:
            self.language.set("en")

    def open_add_app_window(self):
        self.add_app_window = Toplevel(self)
        self.add_app_window.title("Добавить приложение")
        self.add_app_window.geometry("400x300")
        self.add_app_window.configure(bg="black")
        self.add_app_window.resizable(False, False)  

        Label(self.add_app_window, text="Путь к программе:", bg="black", fg="white").pack(pady=5)
        self.app_path_frame = tk.Frame(self.add_app_window, bg="black")
        self.app_path_frame.pack(pady=5)
        self.app_path_entry = Entry(self.app_path_frame, width=40)
        self.app_path_entry.pack(side=tk.LEFT)
        browse_button = Button(self.app_path_frame, text="Обзор...", command=self.browse_app)
        browse_button.pack(side=tk.RIGHT)

        Label(self.add_app_window, text="Название программы:", bg="black", fg="white").pack(pady=5)
        self.app_name_entry = Entry(self.add_app_window, width=50)
        self.app_name_entry.pack(pady=5)

        Label(self.add_app_window, text="Путь к иконке (необязательно):", bg="black", fg="white").pack(pady=5)
        self.icon_path_frame = tk.Frame(self.add_app_window, bg="black")
        self.icon_path_frame.pack(pady=5)
        self.icon_path_entry = Entry(self.icon_path_frame, width=40)
        self.icon_path_entry.pack(side=tk.LEFT)
        browse_icon_button = Button(self.icon_path_frame, text="Обзор...", command=self.browse_icon)
        browse_icon_button.pack(side=tk.RIGHT)

        add_button = Button(self.add_app_window, text="Добавить", command=self.add_app, bg="green", fg="white")
        add_button.pack(pady=20)

    def browse_app(self):
        file_path = filedialog.askopenfilename(title="Выбрать файл", filetypes=[("Программы", "*.exe"), ("Все файлы", "*.*")])
        if file_path:
            self.app_path_entry.delete(0, tk.END)
            self.app_path_entry.insert(0, file_path)
            if not self.app_name_entry.get():
                app_name = os.path.splitext(os.path.basename(file_path))[0]
                self.app_name_entry.insert(0, app_name)

    def browse_icon(self):
        icon_path = filedialog.askopenfilename(title="Выбрать иконку", filetypes=[("Изображения", "*.png;*.jpeg;*.ico")])
        if icon_path:
            self.icon_path_entry.delete(0, tk.END)
            self.icon_path_entry.insert(0, icon_path)

    def add_app(self):
        file_path = self.app_path_entry.get()
        app_name = self.app_name_entry.get()
        icon_path = self.icon_path_entry.get()

        if file_path and app_name:
            new_app = {"id": len(self.apps) + 1, "name": app_name, "path": file_path, "icon": icon_path}
            self.apps.append(new_app)
            self.save_apps()
            self.show_all_apps()
            self.add_app_window.destroy()

    def show_all_apps(self):
        self.current_section = 'all'
        self.clear_content(self.apps_frame)
        for app in self.apps:
            self.create_app_frame(app, self.apps_frame)
        self.update_scroll_region()

    def show_quick_access_apps(self):
        self.current_section = 'quick_access'
        self.clear_content(self.apps_frame)
        for app in self.quick_access_apps:
            self.create_app_frame(app, self.apps_frame)
        self.update_scroll_region()

    def show_about(self):
        self.current_section = 'about'
        self.clear_content(self.apps_frame)

        about_text = """
        PyEasyLauncher v1.2

        The program is designed for easy launching of your applications.
        You can add, edit, delete programs, and also
        view the location of files.

        Open source (Click the link or text): https://github.com/FourTimeStudio/PyEasyLauncher/tree/main
        """

        about_label = tk.Label(self.apps_frame, text=about_text, bg="black", fg="white", justify=tk.LEFT)
        about_label.pack(pady=20, padx=20, anchor="nw")

        self.update_scroll_region()
        self.make_url_clickable(about_label)

    def make_url_clickable(self, label):
        def on_click(event):
            webbrowser.open_new("https://github.com/FourTimeStudio/PyEasyLauncher/tree/main")  # Replace with your URL

        
        label.bind("<Button-1>", on_click)

    def create_app_frame(self, app, parent_frame):
        frame = tk.Frame(parent_frame, bg="#333", bd=2, relief=tk.RAISED)
        frame.pack(pady=10, padx=10, fill=tk.X)

        if app.get("icon"):
            
            icon_label = tk.Label(frame, bg="#333", fg="white", width=10)
            try:
                icon_image = tk.PhotoImage(file=app["icon"])
                icon_image = icon_image.subsample(icon_image.width() // 32, icon_image.height() // 32)
                icon_label.configure(image=icon_image)
                icon_label.image = icon_image
            except tk.TclError:
                icon_label.configure(text="Icon not found", bg="#666", fg="white")
            icon_label.pack(side=tk.LEFT, padx=20)
            
            
            name_label = tk.Button(frame, text=app["name"], bg="#333", fg="white", command=lambda: self.open_app_details(app))
            name_label.pack(side=tk.LEFT, padx=10)
        else:
            
            name_label = tk.Button(frame, text=app["name"], bg="#333", fg="white", command=lambda: self.open_app_details(app))
            name_label.pack(side=tk.LEFT, padx=30)

        play_button = tk.Button(frame, text="Play", command=lambda p=app['path']: self.run_app(p), bg="green", fg="white")
        play_button.pack(side=tk.RIGHT, padx=10)

        menu_button = tk.Menubutton(frame, text="⋮", relief=tk.FLAT, bg="#333", fg="white")
        menu_button.menu = Menu(menu_button, tearoff=0)
        menu_button["menu"] = menu_button.menu
        menu_button.menu.add_command(label="Показать в папке", command=lambda p=app['path']: self.show_in_folder(p))
        menu_button.menu.add_command(label="Добавить в быстрый доступ", command=lambda: self.add_to_quick_access(app))
        menu_button.menu.add_command(label="Изменить информацию", command=lambda: self.edit_app(app))
        menu_button.menu.add_command(label="Удалить", command=lambda: self.delete_app(app['id']))
        menu_button.pack(side=tk.RIGHT, padx=10)

    def open_app_details(self, app):
        details_window = Toplevel(self)
        details_window.title(app["name"])
        details_window.geometry("400x300")
        details_window.configure(bg="black")
        Label(details_window, text=f"Название: {app['name']}", bg="black", fg="white").pack(pady=10)
        Label(details_window, text=f"Путь: {app['path']}", bg="black", fg="white").pack(pady=10)
        Label(details_window, text=f"Иконка: {app.get('icon', 'Не указано')}", bg="black", fg="white").pack(pady=10)

    def edit_app(self, app):
        self.edit_app_window = Toplevel(self)
        self.edit_app_window.title("Изменить информацию")
        self.edit_app_window.geometry("400x300")
        self.edit_app_window.configure(bg="black")

        Label(self.edit_app_window, text="Путь к программе:", bg="black", fg="white").pack(pady=5)
        self.edit_app_path_frame = tk.Frame(self.edit_app_window, bg="black")
        self.edit_app_path_frame.pack(pady=5)
        self.edit_app_path_entry = Entry(self.edit_app_path_frame, width=40)
        self.edit_app_path_entry.pack(side=tk.LEFT)
        self.edit_app_path_entry.insert(0, app["path"])
        browse_button = Button(self.edit_app_path_frame, text="Обзор...", command=self.browse_app_edit)
        browse_button.pack(side=tk.RIGHT)

        Label(self.edit_app_window, text="Название программы:", bg="black", fg="white").pack(pady=5)
        self.edit_app_name_entry = Entry(self.edit_app_window, width=50)
        self.edit_app_name_entry.pack(pady=5)
        self.edit_app_name_entry.insert(0, app["name"])

        Label(self.edit_app_window, text="Путь к иконке (необязательно):", bg="black", fg="white").pack(pady=5)
        self.edit_icon_path_frame = tk.Frame(self.edit_app_window, bg="black")
        self.edit_icon_path_frame.pack(pady=5)
        self.edit_icon_path_entry = Entry(self.edit_icon_path_frame, width=40)
        self.edit_icon_path_entry.pack(side=tk.LEFT)
        self.edit_icon_path_entry.insert(0, app.get("icon", ""))
        browse_icon_button = Button(self.edit_icon_path_frame, text="Обзор...", command=self.browse_icon_edit)
        browse_icon_button.pack(side=tk.RIGHT)

        edit_button = Button(self.edit_app_window, text="Сохранить", command=lambda: self.save_edit_app(app), bg="blue", fg="white")
        edit_button.pack(pady=20)

    def browse_app_edit(self):
        file_path = filedialog.askopenfilename(title="Выбрать файл", filetypes=[("Программы", "*.exe"), ("Все файлы", "*.*")])
        if file_path:
            self.edit_app_path_entry.delete(0, tk.END)
            self.edit_app_path_entry.insert(0, file_path)

    def browse_icon_edit(self):
        icon_path = filedialog.askopenfilename(title="Выбрать иконку", filetypes=[("Изображения", "*.png;*.jpeg;*.ico")])
        if icon_path:
            self.edit_icon_path_entry.delete(0, tk.END)
            self.edit_icon_path_entry.insert(0, icon_path)

    def save_edit_app(self, app):
        app["path"] = self.edit_app_path_entry.get()
        app["name"] = self.edit_app_name_entry.get()
        app["icon"] = self.edit_icon_path_entry.get()
        self.save_apps()
        self.show_all_apps() if self.current_section == 'all' else self.show_quick_access_apps()
        self.edit_app_window.destroy()

    def run_app(self, path):
        os.startfile(path)

    def show_in_folder(self, path):
        folder = os.path.dirname(path)
        os.startfile(folder)

    def add_to_quick_access(self, app):
        if app not in self.quick_access_apps:
            self.quick_access_apps.append(app)
            self.save_apps()
            self.show_quick_access_apps()

    def delete_app(self, app_id):
        if self.current_section == 'all':
            self.apps = [app for app in self.apps if app['id'] != app_id]
        elif self.current_section == 'quick_access':
            self.quick_access_apps = [app for app in self.quick_access_apps if app['id'] != app_id]
        self.save_apps()
        self.show_all_apps() if self.current_section == 'all' else self.show_quick_access_apps()

    def clear_content(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def save_apps(self):
        data = {
            "apps": self.apps,
            "quick_access": self.quick_access_apps
        }
        with open("launcher_data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_apps(self):
        if os.path.exists("launcher_data.json"):
            with open("launcher_data.json", "r") as file:
                data = json.load(file)
                self.apps = data.get("apps", [])
                self.quick_access_apps = data.get("quick_access", [])

    def update_scroll_region(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def search_apps(self, event=None):
        search_term = self.search_entry.get().lower()
        if search_term:
            filtered_apps = [app for app in self.apps if search_term in app['name'].lower()]
            self.clear_content(self.apps_frame)
            for app in filtered_apps:
                self.create_app_frame(app, self.apps_frame)
        else:
            self.show_all_apps()
        self.update_scroll_region()

if __name__ == "__main__":
    app = AppLauncher()
    app.mainloop()
