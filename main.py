import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import qrcode
from PIL import Image, ImageTk
import json
from datetime import datetime

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Настройки языка
        self.language = tk.StringVar(value="ru")
        self.translations = {
            "ru": {
                "title": "Генератор QR-кодов",
                "tab_text": "Текст",
                "tab_wifi": "Wi-Fi",
                "tab_vcard": "Визитка",
                "tab_phone": "Телефон",
                "tab_email": "Email",
                "url_label": "URL или текст:",
                "generate_btn": "Сгенерировать QR-код",
                "save_btn": "Сохранить QR-код",
                "settings": "Настройки",
                "qr_color": "Цвет QR-кода:",
                "bg_color": "Цвет фона:",
                "choose_color": "Выбрать",
                "logo": "Логотип:",
                "load_logo": "Загрузить",
                "remove_logo": "Удалить",
                "module_size": "Размер модуля:",
                "border": "Граница:",
                "version": "Версия:",
                "preview": "Предпросмотр",
                "preview_text": "QR-код появится здесь после генерации",
                "wifi_ssid": "Имя сети (SSID):",
                "wifi_password": "Пароль:",
                "wifi_encryption": "Шифрование:",
                "wifi_hidden": "Скрытая сеть",
                "vcard_name": "Имя:",
                "vcard_lastname": "Фамилия:",
                "vcard_company": "Компания:",
                "vcard_title": "Должность:",
                "vcard_phone": "Телефон:",
                "vcard_email": "Email:",
                "vcard_website": "Веб-сайт:",
                "vcard_address": "Адрес:",
                "phone_number": "Номер телефона:",
                "email_address": "Email адрес:",
                "email_subject": "Тема:",
                "email_body": "Текст письма:",
                "menu_file": "Файл",
                "menu_save": "Сохранить QR-код",
                "menu_exit": "Выход",
                "menu_settings": "Настройки",
                "menu_language": "Язык",
                "menu_help": "Помощь",
                "menu_about": "О программе",
                "about_title": "О программе",
                "about_text": "Генератор QR-кодов\n\nВерсия 1.0\n\nРазработчик: Ванёк\n\nGitHub: https://github.com/Ivan2812446/generator_qr\n\nТелеграмм канал: t.me/Ivans_Tech_Notes\n\nЭто приложение позволяет создавать QR-коды для различных целей: текста, Wi-Fi, визиток, телефона и email."
            },
            "en": {
                "title": "QR Code Generator",
                "tab_text": "Text",
                "tab_wifi": "Wi-Fi",
                "tab_vcard": "Business Card",
                "tab_phone": "Phone",
                "tab_email": "Email",
                "url_label": "URL or text:",
                "generate_btn": "Generate QR Code",
                "save_btn": "Save QR Code",
                "settings": "Settings",
                "qr_color": "QR Code Color:",
                "bg_color": "Background Color:",
                "choose_color": "Choose",
                "logo": "Logo:",
                "load_logo": "Load",
                "remove_logo": "Remove",
                "module_size": "Module Size:",
                "border": "Border:",
                "version": "Version:",
                "preview": "Preview",
                "preview_text": "QR code will appear here after generation",
                "wifi_ssid": "Network Name (SSID):",
                "wifi_password": "Password:",
                "wifi_encryption": "Encryption:",
                "wifi_hidden": "Hidden Network",
                "vcard_name": "First Name:",
                "vcard_lastname": "Last Name:",
                "vcard_company": "Company:",
                "vcard_title": "Title:",
                "vcard_phone": "Phone:",
                "vcard_email": "Email:",
                "vcard_website": "Website:",
                "vcard_address": "Address:",
                "phone_number": "Phone Number:",
                "email_address": "Email Address:",
                "email_subject": "Subject:",
                "email_body": "Message:",
                "menu_file": "File",
                "menu_save": "Save QR Code",
                "menu_exit": "Exit",
                "menu_settings": "Settings",
                "menu_language": "Language",
                "menu_help": "Help",
                "menu_about": "About",
                "about_title": "About",
                "about_text": "QR Code Generator\n\nVersion 1.0\n\nDeveloper: Vanek\n\nGitHub: https://github.com/Ivan2812446/generator_qr\n\nTelegram chanel: t.me/Ivans_Tech_Notes\n\nThis application allows you to create QR codes for various purposes: text, Wi-Fi, business cards, phone, and email."
            }
        }
        
        # Переменные для хранения настроек
        self.fill_color_var = tk.StringVar(value="#000000")
        self.back_color_var = tk.StringVar(value="#FFFFFF")
        self.border_var = tk.IntVar(value=4)
        self.box_size_var = tk.IntVar(value=10)
        self.version_var = tk.IntVar(value=1)
        
        # Переменные для разных типов данных
        self.text_var = tk.StringVar()
        self.wifi_ssid_var = tk.StringVar()
        self.wifi_password_var = tk.StringVar()
        self.wifi_encryption_var = tk.StringVar(value="WPA")
        self.wifi_hidden_var = tk.BooleanVar(value=False)
        self.vcard_name_var = tk.StringVar()
        self.vcard_lastname_var = tk.StringVar()
        self.vcard_company_var = tk.StringVar()
        self.vcard_title_var = tk.StringVar()
        self.vcard_phone_var = tk.StringVar()
        self.vcard_email_var = tk.StringVar()
        self.vcard_website_var = tk.StringVar()
        self.vcard_address_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_address_var = tk.StringVar()
        self.email_subject_var = tk.StringVar()
        self.email_body_var = tk.StringVar()
        
        # Изображение для отображения QR-кода
        self.qr_image = None
        self.logo_image = None
        self.logo_path = None
        
        self.create_menu()
        self.create_widgets()
    
    def create_menu(self):
        # Удаляем старое меню если существует
        if hasattr(self, 'menubar'):
            self.root.config(menu=None)
            del self.menubar
        
        self.menubar = tk.Menu(self.root)
        
        # Меню Файл
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label=self.translations[self.language.get()]["menu_save"], 
                             command=self.save_qr, accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.translations[self.language.get()]["menu_exit"], 
                             command=self.root.quit, accelerator="Ctrl+Q")
        self.menubar.add_cascade(label=self.translations[self.language.get()]["menu_file"], menu=self.file_menu)
        
        # Меню Настройки
        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.language_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.language_menu.add_radiobutton(label="Русский", variable=self.language, value="ru", 
                                     command=self.change_language)
        self.language_menu.add_radiobutton(label="English", variable=self.language, value="en", 
                                     command=self.change_language)
        self.settings_menu.add_cascade(label=self.translations[self.language.get()]["menu_language"], menu=self.language_menu)
        self.menubar.add_cascade(label=self.translations[self.language.get()]["menu_settings"], menu=self.settings_menu)
        
        # Меню Помощь
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label=self.translations[self.language.get()]["menu_about"], 
                             command=self.show_about)
        self.menubar.add_cascade(label=self.translations[self.language.get()]["menu_help"], menu=self.help_menu)
        
        self.root.config(menu=self.menubar)
        
        # Горячие клавиши
        self.root.bind('<Control-s>', lambda e: self.save_qr())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        self.title_label = ttk.Label(main_frame, text=self.translations[self.language.get()]["title"], 
                                    font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(0, 10))
        
        # Создание вкладок
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Вкладка Текст
        self.text_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.text_frame, text=self.translations[self.language.get()]["tab_text"])
        self.create_text_tab()
        
        # Вкладка Wi-Fi
        self.wifi_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.wifi_frame, text=self.translations[self.language.get()]["tab_wifi"])
        self.create_wifi_tab()
        
        # Вкладка Визитка
        self.vcard_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.vcard_frame, text=self.translations[self.language.get()]["tab_vcard"])
        self.create_vcard_tab()
        
        # Вкладка Телефон
        self.phone_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.phone_frame, text=self.translations[self.language.get()]["tab_phone"])
        self.create_phone_tab()
        
        # Вкладка Email
        self.email_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.email_frame, text=self.translations[self.language.get()]["tab_email"])
        self.create_email_tab()
        
        # Фрейм настроек
        self.settings_frame = ttk.LabelFrame(main_frame, text=self.translations[self.language.get()]["settings"], padding="10")
        self.settings_frame.pack(fill=tk.X, pady=5)
        self.create_settings()
        
        # Кнопки генерации и сохранения
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.generate_btn = ttk.Button(buttons_frame, text=self.translations[self.language.get()]["generate_btn"], 
                                      command=self.generate_qr)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(buttons_frame, text=self.translations[self.language.get()]["save_btn"], 
                                  command=self.save_qr)
        self.save_btn.pack(side=tk.LEFT)
        
        # Область предпросмотра QR-кода
        self.preview_frame = ttk.LabelFrame(main_frame, text=self.translations[self.language.get()]["preview"], padding="10")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preview_label = ttk.Label(self.preview_frame, text=self.translations[self.language.get()]["preview_text"],
                                      anchor=tk.CENTER, font=("Arial", 12))
        self.preview_label.pack(fill=tk.BOTH, expand=True)
    
    def create_text_tab(self):
        # Очищаем старые виджеты
        for widget in self.text_frame.winfo_children():
            widget.destroy()
            
        ttk.Label(self.text_frame, text=self.translations[self.language.get()]["url_label"]).pack(anchor=tk.W, pady=5)
        text_entry = ttk.Entry(self.text_frame, textvariable=self.text_var, width=60, font=("Arial", 10))
        text_entry.pack(fill=tk.X, pady=5)
        
        # Подсказка
        hint_text = "Введите любой текст или URL-адрес" if self.language.get() == "ru" else "Enter any text or URL"
        hint_label = ttk.Label(self.text_frame, text=hint_text, font=("Arial", 9), foreground="gray")
        hint_label.pack(anchor=tk.W, pady=5)
    
    def create_wifi_tab(self):
        # Очищаем старые виджеты
        for widget in self.wifi_frame.winfo_children():
            widget.destroy()
            
        # SSID
        ttk.Label(self.wifi_frame, text=self.translations[self.language.get()]["wifi_ssid"]).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.wifi_frame, textvariable=self.wifi_ssid_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Пароль
        ttk.Label(self.wifi_frame, text=self.translations[self.language.get()]["wifi_password"]).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.wifi_frame, textvariable=self.wifi_password_var, width=30, show="*").grid(row=1, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Шифрование
        ttk.Label(self.wifi_frame, text=self.translations[self.language.get()]["wifi_encryption"]).grid(row=2, column=0, sticky=tk.W, pady=5)
        encryption_combo = ttk.Combobox(self.wifi_frame, textvariable=self.wifi_encryption_var, 
                                       values=["WPA", "WEP", "nopass"], state="readonly", width=27)
        encryption_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Скрытая сеть
        ttk.Checkbutton(self.wifi_frame, text=self.translations[self.language.get()]["wifi_hidden"], 
                       variable=self.wifi_hidden_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def create_vcard_tab(self):
        # Очищаем старые виджеты
        for widget in self.vcard_frame.winfo_children():
            widget.destroy()
            
        # Имя и фамилия
        ttk.Label(self.vcard_frame, text=self.translations[self.language.get()]["vcard_name"]).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.vcard_frame, textvariable=self.vcard_name_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Label(self.vcard_frame, text=self.translations[self.language.get()]["vcard_lastname"]).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.vcard_frame, textvariable=self.vcard_lastname_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Компания и должность
        ttk.Label(self.vcard_frame, text=self.translations[self.language.get()]["vcard_company"]).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.vcard_frame, textvariable=self.vcard_company_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Label(self.vcard_frame, text=self.translations[self.language.get()]["vcard_title"]).grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.vcard_frame, textvariable=self.vcard_title_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Телефон и email
        ttk.Label(self.vcard_frame, text=self.translations[self.language.get()]["vcard_phone"]).grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.vcard_frame, textvariable=self.vcard_phone_var, width=30).grid(row=4, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Label(self.vcard_frame, text=self.translations[self.language.get()]["vcard_email"]).grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.vcard_frame, textvariable=self.vcard_email_var, width=30).grid(row=5, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Веб-сайт и адрес
        ttk.Label(self.vcard_frame, text=self.translations[self.language.get()]["vcard_website"]).grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.vcard_frame, textvariable=self.vcard_website_var, width=30).grid(row=6, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Label(self.vcard_frame, text=self.translations[self.language.get()]["vcard_address"]).grid(row=7, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.vcard_frame, textvariable=self.vcard_address_var, width=30).grid(row=7, column=1, sticky=tk.W, pady=5, padx=(5, 0))
    
    def create_phone_tab(self):
        # Очищаем старые виджеты
        for widget in self.phone_frame.winfo_children():
            widget.destroy()
            
        ttk.Label(self.phone_frame, text=self.translations[self.language.get()]["phone_number"]).pack(anchor=tk.W, pady=5)
        ttk.Entry(self.phone_frame, textvariable=self.phone_var, width=30).pack(anchor=tk.W, pady=5)
        
        # Подсказка
        hint_text = "Введите номер телефона в международном формате" if self.language.get() == "ru" else "Enter phone number in international format"
        hint_label = ttk.Label(self.phone_frame, text=hint_text, 
                              font=("Arial", 9), foreground="gray")
        hint_label.pack(anchor=tk.W, pady=5)
    
    def create_email_tab(self):
        # Очищаем старые виджеты
        for widget in self.email_frame.winfo_children():
            widget.destroy()
            
        # Адрес email
        ttk.Label(self.email_frame, text=self.translations[self.language.get()]["email_address"]).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.email_frame, textvariable=self.email_address_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Тема
        ttk.Label(self.email_frame, text=self.translations[self.language.get()]["email_subject"]).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.email_frame, textvariable=self.email_subject_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Текст письма
        ttk.Label(self.email_frame, text=self.translations[self.language.get()]["email_body"]).grid(row=2, column=0, sticky=tk.NW, pady=5)
        self.email_body_text = tk.Text(self.email_frame, width=30, height=5)
        self.email_body_text.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
    
    def create_settings(self):
        # Очищаем старые виджеты
        for widget in self.settings_frame.winfo_children():
            widget.destroy()
            
        # Цвета
        colors_frame = ttk.Frame(self.settings_frame)
        colors_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(colors_frame, text=self.translations[self.language.get()]["qr_color"]).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        fill_color_btn = ttk.Button(colors_frame, text=self.translations[self.language.get()]["choose_color"], 
                                   command=self.choose_fill_color)
        fill_color_btn.grid(row=0, column=1, padx=(0, 20))
        
        self.fill_color_preview = tk.Label(colors_frame, bg=self.fill_color_var.get(), 
                                          width=5, height=1, relief="solid", bd=1)
        self.fill_color_preview.grid(row=0, column=2, padx=(0, 20))
        
        ttk.Label(colors_frame, text=self.translations[self.language.get()]["bg_color"]).grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        back_color_btn = ttk.Button(colors_frame, text=self.translations[self.language.get()]["choose_color"], 
                                   command=self.choose_back_color)
        back_color_btn.grid(row=0, column=4, padx=(0, 20))
        
        self.back_color_preview = tk.Label(colors_frame, bg=self.back_color_var.get(), 
                                          width=5, height=1, relief="solid", bd=1)
        self.back_color_preview.grid(row=0, column=5)
        
        # Логотип
        logo_frame = ttk.Frame(self.settings_frame)
        logo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(logo_frame, text=self.translations[self.language.get()]["logo"]).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Button(logo_frame, text=self.translations[self.language.get()]["load_logo"], 
                  command=self.load_logo).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(logo_frame, text=self.translations[self.language.get()]["remove_logo"], 
                  command=self.remove_logo).grid(row=0, column=2)
        
        # Параметры
        params_frame = ttk.Frame(self.settings_frame)
        params_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(params_frame, text=self.translations[self.language.get()]["module_size"]).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        box_size_spin = ttk.Spinbox(params_frame, from_=1, to=20, textvariable=self.box_size_var, width=5)
        box_size_spin.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(params_frame, text=self.translations[self.language.get()]["border"]).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        border_spin = ttk.Spinbox(params_frame, from_=1, to=10, textvariable=self.border_var, width=5)
        border_spin.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(params_frame, text=self.translations[self.language.get()]["version"]).grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        version_spin = ttk.Spinbox(params_frame, from_=1, to=40, textvariable=self.version_var, width=5)
        version_spin.grid(row=0, column=5)
    
    def choose_fill_color(self):
        color = colorchooser.askcolor(title=self.translations[self.language.get()]["choose_color"], 
                                     initialcolor=self.fill_color_var.get())
        if color[1]:
            self.fill_color_var.set(color[1])
            self.fill_color_preview.config(bg=color[1])
    
    def choose_back_color(self):
        color = colorchooser.askcolor(title=self.translations[self.language.get()]["choose_color"], 
                                     initialcolor=self.back_color_var.get())
        if color[1]:
            self.back_color_var.set(color[1])
            self.back_color_preview.config(bg=color[1])
    
    def load_logo(self):
        file_path = filedialog.askopenfilename(
            title=self.translations[self.language.get()]["load_logo"],
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.logo_path = file_path
            try:
                self.logo_image = Image.open(file_path)
                messagebox.showinfo("Успех", "Логотип загружен успешно!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить логотип: {str(e)}")
    
    def remove_logo(self):
        self.logo_path = None
        self.logo_image = None
        messagebox.showinfo("Успех", "Логотип удален!")
    
    def generate_qr(self):
        # Получаем данные в зависимости от активной вкладки
        current_tab = self.notebook.index(self.notebook.select())
        qr_data = ""
        
        if current_tab == 0:  # Текст
            qr_data = self.text_var.get().strip()
            if not qr_data:
                messagebox.showerror("Ошибка", "Введите текст или URL для генерации QR-кода!")
                return
        
        elif current_tab == 1:  # Wi-Fi
            ssid = self.wifi_ssid_var.get().strip()
            if not ssid:
                messagebox.showerror("Ошибка", "Введите имя сети Wi-Fi!")
                return
            
            password = self.wifi_password_var.get().strip()
            encryption = self.wifi_encryption_var.get()
            hidden = "H:true" if self.wifi_hidden_var.get() else "H:false"
            
            qr_data = f"WIFI:S:{ssid};T:{encryption};P:{password};{hidden};;"
        
        elif current_tab == 2:  # Визитка
            name = self.vcard_name_var.get().strip()
            lastname = self.vcard_lastname_var.get().strip()
            
            if not name and not lastname:
                messagebox.showerror("Ошибка", "Введите хотя бы имя или фамилию!")
                return
            
            # Формируем vCard
            qr_data = "BEGIN:VCARD\nVERSION:3.0\n"
            
            if name and lastname:
                qr_data += f"N:{lastname};{name};;;\n"
                qr_data += f"FN:{name} {lastname}\n"
            elif name:
                qr_data += f"FN:{name}\n"
            elif lastname:
                qr_data += f"FN:{lastname}\n"
            
            company = self.vcard_company_var.get().strip()
            if company:
                qr_data += f"ORG:{company}\n"
            
            title = self.vcard_title_var.get().strip()
            if title:
                qr_data += f"TITLE:{title}\n"
            
            phone = self.vcard_phone_var.get().strip()
            if phone:
                qr_data += f"TEL:{phone}\n"
            
            email = self.vcard_email_var.get().strip()
            if email:
                qr_data += f"EMAIL:{email}\n"
            
            website = self.vcard_website_var.get().strip()
            if website:
                qr_data += f"URL:{website}\n"
            
            address = self.vcard_address_var.get().strip()
            if address:
                qr_data += f"ADR:;;{address};;;\n"
            
            qr_data += "END:VCARD"
        
        elif current_tab == 3:  # Телефон
            phone = self.phone_var.get().strip()
            if not phone:
                messagebox.showerror("Ошибка", "Введите номер телефона!")
                return
            
            qr_data = f"tel:{phone}"
        
        elif current_tab == 4:  # Email
            email = self.email_address_var.get().strip()
            if not email:
                messagebox.showerror("Ошибка", "Введите email адрес!")
                return
            
            subject = self.email_subject_var.get().strip()
            body = self.email_body_text.get("1.0", tk.END).strip()
            
            qr_data = f"mailto:{email}"
            
            if subject or body:
                qr_data += "?"
                
                params = []
                if subject:
                    params.append(f"subject={subject}")
                if body:
                    params.append(f"body={body}")
                
                qr_data += "&".join(params)
        
        try:
            # Создание QR-кода
            qr = qrcode.QRCode(
                version=self.version_var.get(),
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=self.box_size_var.get(),
                border=self.border_var.get(),
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Создание изображения QR-кода
            qr_image = qr.make_image(
                fill_color=self.fill_color_var.get(),
                back_color=self.back_color_var.get()
            ).convert('RGB')
            
            # Добавление логотипа, если он есть
            if self.logo_image:
                # Изменение размера логотипа
                logo_size = min(qr_image.size) // 4
                logo_resized = self.logo_image.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Позиционирование логотипа в центре
                pos = ((qr_image.size[0] - logo_resized.size[0]) // 2,
                       (qr_image.size[1] - logo_resized.size[1]) // 2)
                
                # Вставка логотипа
                qr_image.paste(logo_resized, pos, logo_resized.convert('RGBA') if logo_resized.mode == 'RGBA' else None)
            
            # Сохранение изображения для отображения
            self.qr_image = qr_image
            
            # Отображение QR-кода в интерфейсе
            display_size = 300
            qr_display = qr_image.resize((display_size, display_size), Image.Resampling.LANCZOS)
            qr_photo = ImageTk.PhotoImage(qr_display)
            
            self.preview_label.config(image=qr_photo, text="")
            self.preview_label.image = qr_photo  # Сохраняем ссылку, чтобы избежать сборки мусора
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать QR-код: {str(e)}")
    
    def save_qr(self):
        if self.qr_image is None:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте QR-код!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title=self.translations[self.language.get()]["save_btn"],
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                self.qr_image.save(file_path)
                messagebox.showinfo("Успех", f"QR-код сохранен как {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить QR-код: {str(e)}")
    
    def change_language(self):
        lang = self.language.get()
        translations = self.translations[lang]
        
        # Обновляем заголовок окна
        self.root.title(translations['title'])
        
        # Обновляем заголовок
        self.title_label.config(text=translations['title'])
        
        # Обновляем вкладки
        self.notebook.tab(0, text=translations['tab_text'])
        self.notebook.tab(1, text=translations['tab_wifi'])
        self.notebook.tab(2, text=translations['tab_vcard'])
        self.notebook.tab(3, text=translations['tab_phone'])
        self.notebook.tab(4, text=translations['tab_email'])
        
        # Обновляем кнопки
        self.generate_btn.config(text=translations['generate_btn'])
        self.save_btn.config(text=translations['save_btn'])
        
        # Обновляем настройки
        self.settings_frame.config(text=translations['settings'])
        
        # Обновляем предпросмотр
        self.preview_frame.config(text=translations['preview'])
        if self.qr_image is None:
            self.preview_label.config(text=translations['preview_text'])
        
        # Пересоздаем меню
        self.create_menu()
        
        # Пересоздаем все вкладки с новыми переводами
        self.create_text_tab()
        self.create_wifi_tab()
        self.create_vcard_tab()
        self.create_phone_tab()
        self.create_email_tab()
        self.create_settings()
    
    def show_about(self):
        lang = self.language.get()
        about_window = tk.Toplevel(self.root)
        about_window.title(self.translations[lang]["about_title"])
        about_window.geometry("500x300")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Создаем фрейм для содержимого
        content_frame = ttk.Frame(about_window, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(content_frame, text=self.translations[lang]["about_title"], 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 15))
        
        # Текст о программе
        about_text = tk.Text(content_frame, wrap=tk.WORD, width=50, height=10, 
                            font=("Arial", 10), relief=tk.FLAT, bg=about_window.cget('bg'))
        about_text.insert(tk.END, self.translations[lang]["about_text"])
        about_text.config(state=tk.DISABLED)
        about_text.pack(fill=tk.BOTH, expand=True)
        
        # Кнопка OK
        ttk.Button(content_frame, text="OK", command=about_window.destroy).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()