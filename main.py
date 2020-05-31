"""
This script allow to create simple text editor application.
This software was made in Python 3 on Windows 10.

Package used:
    Tkinter

Use:
    python main.py: ButtonFonctionality, MainApplication

    ButtonFonctionality (class): ButtonFonctionality is a class containing functionality for buttons.
    MainApplication (class): MainApplication is class to create tkinter widgets and configure the window.
"""

__author__ = ("Manitas Bahri")
__version__ = "1.0.0"
__date__ = "2020/01"

try:
    import os
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import colorchooser, filedialog, messagebox, font, scrolledtext

except ImportError as e_import:
    messagebox.showerror("Import Error", "The process could not import the necessary libraries.\nError: %s" % e_import)


class ButtonFonctionality:
    """
    ButtonFonctionality is a class containing functionality for buttons.

    Args:
        master (tkinter.Tk): This the main windows of the application.
        sheet (tkinter.Text): This the main text sheet of an application where the user writes.
    """

    def __init__(self, master, text_sheet):
        self.master = master
        self.text_sheet = text_sheet

        # These are the main variables for saving and opening a document.
        self.pathfile = ""
        self.content_to_save = None
        self.saved = False

        #Variables used to change the font style.
        self.family_font = "Courier New"
        self.value_size = 12
        self.style_bold = "normal"
        self.style_slant = "roman"
        self.is_underlined = False
        self.font_color = "black"

        self.font_update()

    def new_file(self, event=None):
        """This method is used to create new file."""
        new_file = False

        # Check if the current file is saved before creating another file.
        if not new_file:
            new_file = self.message_box_save(new_file, self.new_file)

        if new_file:
            self.text_sheet.delete("1.0", "end")
            self.content_to_sav = ""
            self.saved = False
            self.pathfile = ""

    def open_file(self, event=None):
        """This method is used to open an existing file."""
        open_file = False

        # Check if the current file is saved before opening another file.
        if not open_file:
            open_file = self.message_box_save(open_file, self.open_file)

        if open_file:
            try:
                self.pathfile = filedialog.askopenfilename(filetypes=[("txt files", ".txt"), ("all files", ".*")])
                if self.pathfile:
                    self.text_sheet.delete("1.0", "end")
                    file_opened = open(self.pathfile, "r")
                    self.text_sheet.insert("1.0", file_opened.read())
                    file_opened.close()
                    self.content_to_save = self.text_sheet.get("1.0", "end-1c")
                    self.is_saved()

            except FileNotFoundError as fnf_error:
                messagebox.showerror("File Not Found Error", "The proccess was failed. \
                The file or directory is requested doesn't exist.\nError: %s" % fnf_error)

            except OSError as os_error:
                messagebox.showerror("OS Error", "The proccess was failed.\nError: %s" % os_error)

            except Exception as e:
                messagebox.showerror("Error", "The proccess was failed.\nError: %s" % e)

    def save_file(self, event=None):
        """This method is used to save file."""
        try:
            # Check if the file has been already save with pathfile.
            if self.pathfile != "":
                self.content_to_save = self.text_sheet.get("1.0", "end-1c")
                file_saved = open(self.pathfile, "w", encoding="utf-8")
                file_saved.write(self.content_to_save)
                file_saved.close()
                self.is_saved()
            # If the file hasn't been saved: go to the save_as method to create save pathfile.
            else:
                self.save_as()

        except OSError as os_error:
            messagebox.showerror("OS Error", "The proccess was failed.\nError: %s" % os_error)

        except Exception as e:
            messagebox.showerror("Error", "The proccess was failed.\nError: %s" % e)

    def save_as(self, event=None):
        """This method is used to save as... the file."""
        try:
            self.pathfile = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("txt files", ".txt"), ("all files", ".*")])
            if self.pathfile:
                self.save_file()

        except OSError as os_error:
            messagebox.showerror("OS Error", "The proccess was failed.\nError: %s" % os_error)

        except Exception as e:
            messagebox.showerror("Error", "The proccess was failed.\nError: %s" % e)

    def client_exit(self):
        """Check if the text is saved and exit the application."""
        exit = False
        if not exit:
            exit = self.message_box_save(exit, self.client_exit)
        if exit:
            self.master.destroy()        

    def message_box_save(self, continue_process=False, go_to_method=None):
        """
        This method is used to create a message box about saving text. 
        If the text has not been saved so we ask the user if he wants to save the text or not 
        before to continuing the current operation (like opening a document or creating new file).

        Args:
            continue_process (boolean): Variable used to check if the current operation can be continued.
            go_to_method (method) : Once the file is saved, go to method to continue the current process (like opening file or quitting app)

        Return:
            continue_process: Return False if the user canceled the current action or True to continue current action.
        """
        self.is_saved()
        if len(self.text_sheet.get("1.0", "end-1c")) and not self.saved:
            ask_save = messagebox.askyesnocancel("Mind Note", "Would you want to save before to continue ?")
            if ask_save:
                self.save_file()
                continue_process = True
                go_to_method

            elif ask_save == False:
                continue_process = True

            else:
                continue_process = False
        
        else:
            continue_process = True
        
        return continue_process

    def is_saved(self, event=None):
        """Check if the text has been saved. If the text hasn't been saved add * to title."""
        file_name = os.path.basename(self.pathfile)
        if file_name == "":
            file_name = "untitled"

        if self.content_to_save != self.text_sheet.get("1.0", "end-1c"):
            self.saved = False
            self.master.title("%s : Mind Note*" % file_name)
        else:
            self.saved = True
            self.master.title("%s : Mind Note" % file_name)

    def get_color(self):
        """
        This method is used to open color palette and set the font color.
        """
        color = colorchooser.askcolor()   
        self.font_color = color[1]
        self.font_update()

    def font_bold(self, event=None):
        """To set the font bold / normal."""
        if self.style_bold == "normal":
            self.style_bold = "bold"

        elif self.style_bold == "bold":
            self.style_bold = "normal"

        # Updates the font style.
        self.font_update()

    def font_slant(self, event=None):
        """To set the font italic / normal."""
        if self.style_slant == "roman":
            self.style_slant = "italic"

        elif self.style_slant == "italic":
            self.style_slant = "roman"

        # Updates the font style.
        self.font_update()

    def font_underline(self, event=None):
        """To underlined the font."""
        if not self.is_underlined:
            self.is_underlined = True

        else:
            self.is_underlined = False

        # Updates the font style.
        self.font_update()

    def font(self, event, value_font):
        """
        This method is used to change the font family.

        Arg:
            value_font = Get the name of the font.
        """
        self.family_font = value_font.get()
        self.font_update()

    def font_size(self, event, value_size):
        """
        This method is used to change the size family.

        Arg:
            value_size = Get the size of the font.
        """        
        try:
            self.value_size = value_size.get()

        except tk._tkinter.TclError:
            value_size.set(10)
            self.value_size = 10

        if (self.value_size == 0) or (self.value_size > 100):
            value_size.set(10)
            self.value_size = 10
        
        self.font_update()

    def font_update(self, reset=False, btn_size=None, btn_font=None):
        """
        Use this method to update or reset the font style.
        - Style: Font, Size, Weight, Slant, Underline
        - Color: Font Color

        Arg:
            reset (bool): If true reset the style font.
            btn_size, btn_font (tkk.Combobox): To change the current value of combobox.
        """
        if reset:
            btn_font.current(1)
            self.family_font = "Courier New"
            btn_size.current(4)
            self.value_size = 12
            self.style_bold = "normal"
            self.style_slant = "roman"
            self.is_underlined = False
            self.font_color = "black"
            reset = False

        self.text_sheet.config(font=font.Font(family=self.family_font,
                                         size=self.value_size,
                                         weight=self.style_bold,
                                         slant=self.style_slant,
                                         underline=self.is_underlined), fg=self.font_color)


class MainApplication(ButtonFonctionality):
    """
    MainApplication is class to create tkinter widgets and configure the window.

    Arg:
        windows (tkinter.Tk): This the main windows of the application.
    """
    def __init__(self, window):
        self.window = window
        self.configure_gui()
        self.create_widget()

        super().__init__(window, self.text_sheet)

    def configure_gui(self):
        """This method allows to configure the main parameters to the window."""
        try:
            self.window.iconbitmap("icon.ico")

        except tk.TclError:
            pass

        self.window.title("Mind Note")
        self.window.geometry("420x590")
        self.window.minsize(width=420, height=200)
        self.window.protocol("WM_DELETE_WINDOW", lambda: super(MainApplication, self).client_exit())

        # Bind shortcuts.
        self.window.bind("<Control-n>", super().new_file)
        self.window.bind("<Control-o>", super().open_file)
        self.window.bind("<Control-Shift-S>", super().save_as)
        self.window.bind("<Control-s>", super().save_file)
        self.window.bind("<Control-b>", super().font_bold)
        self.window.bind("<Control-i>", super().font_slant)
        self.window.bind("<Control-u>", super().font_underline)

        # Check if the text has been modified and saved.
        self.window.bind("<Key>", super().is_saved)

    def create_widget(self):
        """
        This method creates the body of the 'Mind Note' application and adds
        functionality to the buttons provided by the ButtonFunctionality class.
        """

        # Creates the main navigation bar widgets.
        self.navbar = tk.Menu(self.window)
        self.window.config(menu=self.navbar)

        self.file_menu = tk.Menu(self.navbar, tearoff=0)
        self.navbar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=super().new_file)
        self.file_menu.add_command(label="Open", command=super().open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save As...", command=super().save_as)
        self.file_menu.add_command(label="Save", command=super().save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=super().client_exit)

        self.edit_menu = tk.Menu(self.navbar, tearoff=0)
        self.navbar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Reset the style font", 
                                   command=lambda: super(MainApplication, self).font_update(reset=True, btn_size=self.font_size, btn_font=self.font_family))

        # Creates the toolbar and adds the font style buttons.
        self.frame_tool = tk.LabelFrame(self.window, text="Toolbar :", font="Helvetica 9 bold underline")
        self.frame_tool.pack(side="top", fill="x", padx=10, pady=10)

        # Label frame for font style buttons.
        self.frame_font = tk.LabelFrame(self.frame_tool, text="Font Format :")
        self.frame_font.grid(row=0, column=0, ipadx=5, ipady=5, padx=10, pady=10)

        # Combobox for size font.
        tk.Label(self.frame_font, text="Font Size :").grid(row=0, column=0)
        self.options_size = [8, 9, 10, 11, 12, 13, 14, 16, 18, 22]
        self.value_size = tk.IntVar()
        self.font_size = ttk.Combobox(self.frame_font, textvariable=self.value_size, values=self.options_size, width=15)
        self.font_size.current(4)
        self.font_size.bind("<<ComboboxSelected>>", lambda event, value_size=self.value_size: super(MainApplication, self).font_size(event, value_size))
        self.font_size.bind("<Return>", lambda event, value_size=self.value_size: super(MainApplication, self).font_size(event, value_size))
        self.font_size.grid(row=0, column=1)

        # Combobox for font.
        tk.Label(self.frame_font, text="Font :").grid(row=1, column=0)
        self.options_font = ["Arial", "Courier New", "Comic Sans MS", "Fixedsys", "MS Sans Serif", "MS Serif", "System", "Times New Roman", "Verdana", "Symbol"]
        self.value_font = tk.StringVar()
        self.font_family = ttk.Combobox(self.frame_font, textvariable=self.value_font, values=self.options_font, width=15, state="readonly")
        self.font_family.current(1)
        self.font_family.bind("<<ComboboxSelected>>", lambda event, value_font=self.value_font: super(MainApplication, self).font(event, value_font))
        self.font_family.grid(row=1, column=1)

        # Label, Frame and Button for style font.
        tk.Label(self.frame_font, text="Font Style :").grid(row=0, column=2, padx=2)
        self.frame_btn_style = tk.Frame(self.frame_font)
        self.frame_btn_style.grid(row=0, column=3)
        tk.Button(self.frame_btn_style, text="B", width=3, font="Helvetica 9 bold", command=super().font_bold).grid(row=0, column=3, padx=2)
        tk.Button(self.frame_btn_style, text="I", width=3, font="Helvetica 9 italic", command=super().font_slant).grid(row=0, column=4, padx=2)
        tk.Button(self.frame_btn_style, text="U", width=3, font="Helvetica 9 underline", command=super().font_underline).grid(row=0, column=5, padx=2, pady=1)

        # Button for font color.
        tk.Label(self.frame_font, text="Font Color :").grid(row=1, column=2, padx=2)
        self.btn_color = tk.Button(self.frame_font, text="color", width=5, font="Helvetica 9 bold", command=super().get_color)
        self.btn_color.grid(row=1, column=3, sticky=tk.W+tk.E)

        # Creates the main text sheet.
        self.frame_sheet = tk.Frame(self.window)
        self.frame_sheet.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.text_sheet = tk.scrolledtext.ScrolledText(self.frame_sheet)
        self.text_sheet.pack(expand=True, fill=tk.BOTH)
try:
    if __name__ == "__main__":
        root = tk.Tk()
        MainApplication(root)
        root.mainloop()
except Exception as e:
    messagebox.showerror("Error", "The proccess was failed.\nError: %s" % e)
