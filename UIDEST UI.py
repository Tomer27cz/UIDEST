import tkinter
from PIL import Image
from tkinter import ttk
from tkinter import filedialog

from tkhtmlview import HTMLScrolledText
import customtkinter
import os

from Features.Image.ImageScramble import new_scramble_algorithm
from Features.Image.ImageSteganography import Steganography, Steganography3, Steganography4, Steganography5, Steganography6, Steganography7, Steganography8
from Features.Image.Text.TextSteganography import TextSteganographyLayeredDynamic, TextSteganography, TextSteganographyLayered, TextSteganographyLayeredDynamicTransparent
from Features.Image.Text.TextToImage import TextToImage
from Features.tkinter.ToolTip import CreateToolTip

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk, tkinter.Tk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Universal Image Decode and Encode Steganography Tool")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0) # NOQA
        self.grid_rowconfigure((0, 1, 2), weight=1) # NOQA

        # configure misc

        self.initial_browser_dir = 'Desktop'
        self.title_open = "Select image file"
        self.filetypes = (("image files", "*.png *.jpg *.gif *.webp *.ico *.tiff *.bmp *.im *.msp *.pcx *.ppm *.sgi *.xbm "
                                     "*.dds *.dib *.eps *.spi"), ("all files", "*.*"))
        self.output_type_list = ["BMP", "DDS", "DIB", "EPS", "GIF", "ICO", "IM", "JPEG", "PCX", "PNG", "PPM", "SGI",
             "SPIDER", "TGA", "TIFF", "WebP"]
        self.output_type_list_lossless = ["BMP", "GIF", "PNG", "TIFF", "WebP", "ICO", "PCX", "SGI", "TGA"]
        self.folder_button_icon = customtkinter.CTkImage(light_image=Image.open("Assets/folder-open-light.png"), dark_image=Image.open("Assets/folder-open-dark.png"))
        self.info_marker_icon = customtkinter.CTkImage(light_image=Image.open("Assets/info-mark-light.png"), dark_image=Image.open("Assets/info-mark-dark.png"))

        # create variables

        self.sc_seed_loop_var = tkinter.IntVar(value=0)
        self.sc_size_loop_var = tkinter.IntVar(value=0)
        self.sc_action_type_var = tkinter.StringVar(value="Encode")
        self.sc_output_type_var = tkinter.StringVar(value="PNG")
        #-----------------------------------------------
        self.st_type_var = tkinter.StringVar(value="Steganography x2")
        self.st_output_type_var = tkinter.StringVar(value="PNG")
        self.st_action_type_var = tkinter.StringVar(value="Merge")
        #-----------------------------------------------
        self.stt_type_var = tkinter.StringVar(value="Layered8")
        self.stt_output_type_var = tkinter.StringVar(value="PNG")
        self.stt_action_type_var = tkinter.StringVar(value="Encode")
        self.stt_encoding_type_var = tkinter.StringVar(value="ASCII")
        self.stt_text_output_checkbox_var = tkinter.IntVar(value=0)

        # create sidebar

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="UIDEST 1.0\nALPHA", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Image Scrambler", command=self.sidebar_button_event_frame_0)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Image - Image\nSteganography", command=self.sidebar_button_event_frame_1)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Image - Text\nSteganography", command=self.sidebar_button_event_frame_2)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["System", "Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        # self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        # self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
        #                                                        values=["80%", "90%", "100%", "110%", "120%"],
        #                                                        command=self.change_scaling_event)
        # self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create notebook

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TNotebook", background="#ffffff", borderwidth=0, padding=0)
        self.style.layout('Tabless.TNotebook.Tab', [])  # turn off tabs

        self.my_notebook = ttk.Notebook(self, style="Tabless.TNotebook")
        self.my_notebook.grid(row=0, column=1, rowspan=4, sticky="nsew")

        # create frames


        #--------------------------------------Image Scrambler----------------------------------------------------------


        self.frame0 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame0.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame0.grid_rowconfigure(9, weight=1)
        self.frame0.grid_columnconfigure(2, weight=1)

        # label
        self.sc_logo_label = customtkinter.CTkLabel(self.frame0, text="Image Scrambler", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sc_logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # input/output entry
        self.sc_ent1 = customtkinter.CTkEntry(self.frame0, placeholder_text="Input image path here", width=100)
        self.sc_ent1.grid(row=1, column=2, padx=20, pady=10, columnspan=3, sticky="ew")
        self.sc_ent2 = customtkinter.CTkEntry(self.frame0, placeholder_text="Output folder path here", width=100)
        self.sc_ent2.grid(row=2, column=2, padx=20, pady=10, columnspan=3, sticky="ew")

        # input/output button
        self.sc_sidebar_button_1 = customtkinter.CTkButton(self.frame0, command=self.sc_open_image, image=self.folder_button_icon, text="Open Image")
        self.sc_sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sc_sidebar_button_2 = customtkinter.CTkButton(self.frame0, command=self.sc_open_folder, image=self.folder_button_icon, text="Open folder")
        self.sc_sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # loop checkboxes
        self.sc_loop_label = customtkinter.CTkLabel(self.frame0, text="Loop mode:", anchor="w")
        self.sc_loop_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.sc_loop_checkbox1 = customtkinter.CTkCheckBox(self.frame0, text="Seed", command=self.sc_seed_loop_checkbox_event, variable=self.sc_seed_loop_var, onvalue=1, offvalue=0)
        self.sc_loop_checkbox1.grid(row=4, column=0, padx=35, pady=10, sticky="wn")
        self.sc_loop_checkbox2 = customtkinter.CTkCheckBox(self.frame0, text="Size", command=self.sc_size_loop_checkbox_event, variable=self.sc_size_loop_var, onvalue=1, offvalue=0)
        self.sc_loop_checkbox2.grid(row=4, column=0, padx=0, pady=10, sticky="en")

        # seed and size entry fields
        self.sc_from_seed_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="Seed", width=75)
        self.sc_from_seed_ent.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.sc_from_size_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="Size", width=75)
        self.sc_from_size_ent.grid(row=5, column=0, padx=20, pady=10, sticky="e")
        self.sc_to_seed_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="", width=75, state="disabled", border_width=0)
        self.sc_to_seed_ent.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        self.sc_to_size_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="", width=75, state="disabled", border_width=0)
        self.sc_to_size_ent.grid(row=6, column=0, padx=20, pady=5, sticky="e")

        # filename and folder name entry fields
        self.sc_output_name_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="Output filename", width=100)
        self.sc_output_name_ent.grid(row=7, column=0, padx=20, pady=10, columnspan=1, sticky="ew")
        self.sc_output_folder_name_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="", width=100, border_width=0, state="disabled")
        self.sc_output_folder_name_ent.grid(row=8, column=0, padx=20, pady=10, columnspan=1, sticky="ew")

        # drop down menus
        self.sc_output_type_dropdown = customtkinter.CTkOptionMenu(self.frame0, values=self.output_type_list, variable=self.sc_output_type_var)
        self.sc_output_type_dropdown.grid(row=12, column=0, padx=20, pady=(10, 10))
        self.sc_action_type_dropdown = customtkinter.CTkOptionMenu(self.frame0, values=["Encode", "Decode"], variable=self.sc_action_type_var)
        self.sc_action_type_dropdown.grid(row=13, column=0, padx=20, pady=(10, 20))

        # console
        self.sc_console = customtkinter.CTkTextbox(self.frame0, width=100, height=300)
        self.sc_console.grid(row=4, column=2, columnspan=3, rowspan=8, sticky="ewsn", padx=20)

        # info markers
        self.sc_info_marker_1 = customtkinter.CTkLabel(self.frame0, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.sc_info_marker_1.grid(row=4, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.sc_info_marker_2 = customtkinter.CTkLabel(self.frame0, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.sc_info_marker_2.grid(row=5, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.sc_info_marker_3 = customtkinter.CTkLabel(self.frame0, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.sc_info_marker_3.grid(row=7, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.sc_info_marker_4 = customtkinter.CTkLabel(self.frame0, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.sc_info_marker_4.grid(row=8, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.sc_info_marker_5 = customtkinter.CTkLabel(self.frame0, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.sc_info_marker_5.grid(row=12, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        CreateToolTip(self.sc_info_marker_1, "Check the box to enable the loop mode.\nThe program will loop through all the seeds and sizes in the ranges you specify.",height=50 ,width=460)
        CreateToolTip(self.sc_info_marker_2, f"The size of the image should be divisible by the size.\n\nFor example, if the image is 1920x1080, the size can be:\n{_calc_size(1920, 1080)}", height=75, width=350)
        CreateToolTip(self.sc_info_marker_3, "The output filename will be appended with the seed/size\nExample: 'output_(69_10).png' for seed 69 and size 10\n\nNote: The file extension will be added automatically\nbased on the output type", height=90, width=330)
        CreateToolTip(self.sc_info_marker_4, "The output folder will be created in output folder path,\nif the loop mode is enabled.\nDefault: 'Image Scrambler Output'", height=65, width=330)
        CreateToolTip(self.sc_info_marker_5, "The output type is the file type of the output image.\n\nDefault: 'PNG' - Lossless encoding for better quality when decoding.", height=65, width=400)

        # start button
        self.sc_start_button = customtkinter.CTkButton(self.frame0, command=self.sc_start_button_event, text="Run Image Scrambler")
        self.sc_start_button.grid(row=13, column=2, padx=20, pady=(10, 20), columnspan=3, sticky="we")


        #---------------------------------------- IM - IM Steganography-------------------------------------------------


        self.frame1 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame1.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame1.grid_rowconfigure(10, weight=1)
        self.frame1.grid_columnconfigure(3, weight=1)

        # variables
        self.spacing = 3

        # logo
        self.st_logo_label = customtkinter.CTkLabel(self.frame1, text="Image - Image Steganography", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.st_logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=3, sticky="w")

        # image entries
        self.st_ent1 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100)
        self.st_ent2 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100)
        self.st_ent3 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100)
        self.st_ent4 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100)
        self.st_ent5 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100)
        self.st_ent6 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100)
        self.st_ent7 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100)
        self.st_ent8 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100)
        self.st_ent1.grid(row=1, column=1, padx=20, pady=self.spacing, columnspan=7, sticky="ew")
        self.st_ent2.grid(row=2, column=1, padx=20, pady=self.spacing, columnspan=7, sticky="ew")
        self.st_ent3.grid(row=3, column=1, padx=20, pady=self.spacing, columnspan=7, sticky="ew")
        self.st_ent4.grid(row=4, column=1, padx=20, pady=self.spacing, columnspan=7, sticky="ew")
        self.st_ent5.grid(row=5, column=1, padx=20, pady=self.spacing, columnspan=7, sticky="ew")
        self.st_ent6.grid(row=6, column=1, padx=20, pady=self.spacing, columnspan=7, sticky="ew")
        self.st_ent7.grid(row=7, column=1, padx=20, pady=self.spacing, columnspan=7, sticky="ew")
        self.st_ent8.grid(row=8, column=1, padx=20, pady=self.spacing, columnspan=7, sticky="ew")

        # folder entry
        self.st_ent_folder = customtkinter.CTkEntry(self.frame1, placeholder_text="Output folder path here", width=100)
        self.st_ent_folder.grid(row=9, column=1, padx=20, pady=23, columnspan=7, sticky="ew")

        # image buttons
        self.st_sidebar_button_1 = customtkinter.CTkButton(self.frame1, command=self.st_open_image1, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_2 = customtkinter.CTkButton(self.frame1, command=self.st_open_image2, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_3 = customtkinter.CTkButton(self.frame1, command=self.st_open_image3, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_4 = customtkinter.CTkButton(self.frame1, command=self.st_open_image4, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_5 = customtkinter.CTkButton(self.frame1, command=self.st_open_image5, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_6 = customtkinter.CTkButton(self.frame1, command=self.st_open_image6, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_7 = customtkinter.CTkButton(self.frame1, command=self.st_open_image7, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_8 = customtkinter.CTkButton(self.frame1, command=self.st_open_image8, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_1.grid(row=1, column=0, padx=20, pady=self.spacing)
        self.st_sidebar_button_2.grid(row=2, column=0, padx=20, pady=self.spacing)
        self.st_sidebar_button_3.grid(row=3, column=0, padx=20, pady=self.spacing)
        self.st_sidebar_button_4.grid(row=4, column=0, padx=20, pady=self.spacing)
        self.st_sidebar_button_5.grid(row=5, column=0, padx=20, pady=self.spacing)
        self.st_sidebar_button_6.grid(row=6, column=0, padx=20, pady=self.spacing)
        self.st_sidebar_button_7.grid(row=7, column=0, padx=20, pady=self.spacing)
        self.st_sidebar_button_8.grid(row=8, column=0, padx=20, pady=self.spacing)

        # folder button
        self.st_sidebar_button_folder = customtkinter.CTkButton(self.frame1, command=self.st_open_folder, image=self.folder_button_icon, text="Open folder")
        self.st_sidebar_button_folder.grid(row=9, column=0, padx=20, pady=23)

        # console
        self.st_console = customtkinter.CTkTextbox(self.frame1, width=100, height=20)
        self.st_console.grid(row=10, column=0, columnspan=9, rowspan=1, sticky="ewsn", padx=20)

        # drop down menus
        self.st_output_type_dropdown = customtkinter.CTkOptionMenu(self.frame1, values=self.output_type_list, variable=self.st_output_type_var)
        self.st_output_type_dropdown.grid(row=11, column=0, padx=20, pady=(10, 10))
        self.st_type_dropdown = customtkinter.CTkOptionMenu(self.frame1, values=["Steganography x2", "Steganography x3", "Steganography x4", "Steganography x5", "Steganography x6", "Steganography x7", "Steganography x8"], variable=self.st_type_var, command=self.st_type_dropdown_event)
        self.st_type_dropdown.grid(row=12, column=0, padx=20, pady=10)
        self.st_action_type_dropdown = customtkinter.CTkOptionMenu(self.frame1, values=["Merge", "Unmerge"], variable=self.st_action_type_var, command=self.st_type_dropdown_event)
        self.st_action_type_dropdown.grid(row=13, column=0, padx=20, pady=10)

        # file name and folder entries
        self.st_output_name_ent = customtkinter.CTkEntry(self.frame1, placeholder_text="Output filename")
        self.st_output_name_ent.grid(row=11, column=2, padx=20, pady=10, columnspan=1, sticky="ew")
        self.st_folder_checkbox = customtkinter.CTkCheckBox(self.frame1, text="", command=self.st_folder_checkbox_event, onvalue=True, offvalue=False)
        self.st_folder_checkbox.grid(row=11, column=4, padx=(0, 100), pady=0, sticky="w", columnspan=2)
        self.st_output_folder_ent = customtkinter.CTkEntry(self.frame1, placeholder_text="Output folder name")
        self.st_output_folder_ent.grid(row=11, column=5, padx=20, pady=10, columnspan=1, sticky="ew")

        # info markers
        self.stt_explanation = customtkinter.CTkButton(self.frame1, text="Show Explanation", command=self.st_explanation_event)
        self.stt_explanation.grid(row=0, column=3, padx=20, pady=10, sticky="w")

        self.stt_info_marker_1 = customtkinter.CTkLabel(self.frame1, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.stt_info_marker_1.grid(row=11, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.stt_info_marker_2 = customtkinter.CTkLabel(self.frame1, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.stt_info_marker_2.grid(row=12, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.stt_info_marker_3 = customtkinter.CTkLabel(self.frame1, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.stt_info_marker_3.grid(row=13, column=1, padx=0, pady=0, ipadx=2, ipady=5)

        CreateToolTip(self.stt_info_marker_1, "The output type is the file type of the output image.\n\nDefault: 'PNG' - Lossless encoding for better quality when decoding.", height=65, width=400)
        CreateToolTip(self.stt_info_marker_2, "The type of steganography to use.\nBinary representation:\n'Steganography x2' - {0000} {0000}\nSteganography x3 - {0000} {00} {00}\nSteganography x4 - {00} {00} {00} {00}\nSteganography x5 - {00} {00} {00} {0} {0}\nSteganography x6 - {00} {00} {0} {0} {0} {0}\nSteganography x7 - {00} {0} {0} {0} {0} {0} {0}\nSteganography x8 - {0} {0} {0} {0} {0} {0} {0} {0}\n\nDefault: 'Steganography x2' for two images", height=180, width=300)
        CreateToolTip(self.stt_info_marker_3, "The program will merge the images into one image\nor unmerge the image into multiple images replacing\nthe blank spot from other images with black pixels\n\nFor Unmerging it is recommended to check the 'Output to new folder' box.", height=90, width=425)
        CreateToolTip(self.stt_explanation, "Show explanation of how steganography works", height=30, width=200)
        CreateToolTip(self.st_folder_checkbox, "Output the files to a new folder", height=30, width=200)
        CreateToolTip(self.st_output_name_ent, "Default: 'SteganographyOutput' - The name of the output file\n\nNote: The file extension will be added automatically\nbased on the output type", height=75, width=350)

        # start button
        self.st_start_button = customtkinter.CTkButton(self.frame1, command=self.st_start_button_event, text="Run Steganographer")
        self.st_start_button.grid(row=12, column=2, padx=20, pady=10, ipady=5, columnspan=5, rowspan=2, sticky="we")


        # ------------------------------------Text - IM Steganography --------------------------------------------------

        self.frame2 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame2.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame2.grid_rowconfigure(4, weight=1)
        self.frame2.grid_columnconfigure(2, weight=1)

        # logo
        self.stt_logo_label = customtkinter.CTkLabel(self.frame2, text="Image - Text Steganography", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.stt_logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=3, sticky="w")

        # entries
        self.stt_ent1 = customtkinter.CTkEntry(self.frame2, placeholder_text="Input image path here", width=100)
        self.stt_ent1.grid(row=1, column=1, padx=20, pady=self.spacing, columnspan=3, sticky="ew")
        self.stt_ent2 = customtkinter.CTkEntry(self.frame2, placeholder_text="Output folder path here", width=100)
        self.stt_ent2.grid(row=2, column=1, padx=20, pady=10, columnspan=3, sticky="ew")

        # buttons
        self.stt_sidebar_button_1 = customtkinter.CTkButton(self.frame2, command=self.stt_open_image, image=self.folder_button_icon, text="Open Image")
        self.stt_sidebar_button_1.grid(row=1, column=0, padx=20, pady=5)
        self.stt_sidebar_button_2 = customtkinter.CTkButton(self.frame2, command=self.stt_open_folder, image=self.folder_button_icon, text="Open folder")
        self.stt_sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # text entry
        self.stt_ent3 = customtkinter.CTkTextbox(self.frame2, width=100)
        self.stt_ent3.grid(row=3, column=1, padx=20, pady=10, columnspan=3, rowspan=3, sticky="ewsn")

        # console
        self.stt_console = customtkinter.CTkTextbox(self.frame2, width=100, height=20)
        self.stt_console.grid(row=8, column=2, columnspan=3, rowspan=2, sticky="wens", padx=20, pady=10)

        # file name entry
        self.stt_output_name_ent = customtkinter.CTkEntry(self.frame2, placeholder_text="Output filename", width=100)
        self.stt_output_name_ent.grid(row=7, column=0, padx=20, pady=10, columnspan=1, sticky="ew")
        self.stt_text_output_checkbox = customtkinter.CTkCheckBox(self.frame2, text="Output text to file", variable=self.stt_text_output_checkbox_var, state="disabled", command=self.stt_text_output_checkbox_event)
        self.stt_text_output_checkbox.grid(row=6, column=0, padx=20, pady=10, columnspan=1, sticky="w")

        # drop down menus
        self.stt_output_type_dropdown = customtkinter.CTkOptionMenu(self.frame2, values=self.output_type_list_lossless, variable=self.stt_output_type_var)
        self.stt_output_type_dropdown.grid(row=8, column=0, padx=20, pady=10)
        self.stt_type_dropdown = customtkinter.CTkOptionMenu(self.frame2, values=["Layered8", "Sequential8", "LayeredDynamic", "LayeredDynamicTransparent"], variable=self.stt_type_var, command=self.stt_type_dropdown_event)
        self.stt_type_dropdown.grid(row=9, column=0, padx=20, pady=10)
        self.stt_action_type_dropdown = customtkinter.CTkOptionMenu(self.frame2, values=["Encode", "Decode"], variable=self.stt_action_type_var, command=self.stt_action_type_dropdown_event)
        self.stt_action_type_dropdown.grid(row=10, column=0, padx=20, pady=10)
        self.stt_encoding_type_dropdown = customtkinter.CTkOptionMenu(self.frame2, values=["ASCII", "UNICODE"], variable=self.stt_encoding_type_var, command=self.stt_encoding_type_dropdown_event)
        self.stt_encoding_type_dropdown.grid(row=3, column=0, padx=20, pady=10)

        # info marker
        self.stt_info_marker_1 = customtkinter.CTkLabel(self.frame2, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.stt_info_marker_1.grid(row=8, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.stt_info_marker_2 = customtkinter.CTkLabel(self.frame2, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.stt_info_marker_2.grid(row=9, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.stt_info_marker_3 = customtkinter.CTkLabel(self.frame2, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.stt_info_marker_3.grid(row=10, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        CreateToolTip(self.stt_info_marker_1, "The output type is the file type of the output image.\nOnly Lossless image formats are supported for this program\n(others may not work because of compression of the data)\n\nDefault: 'PNG' - Lossless encoding for better quality when decoding.", height=90, width=400)
        CreateToolTip(self.stt_info_marker_2, "This is the folder you want to save the output to")
        CreateToolTip(self.stt_info_marker_3, "This is the type of output you want to get\n\nLayered - The program will encode the text into the image\nand save the output image in the output folder\n\nSequential - The program will encode the text into the image\nand save the output image in the output folder\n\nLayeredDynamic - The program will encode the text into the image\nand save the output image in the output folder")
        CreateToolTip(self.stt_output_name_ent, "Default: 'output' - The name of the output file\n\nNote: The file extension will be added automatically\nbased on the output type", height=75, width=300)
        CreateToolTip(self.stt_text_output_checkbox, "If checked, the program will output the text to a text file\nin the output folder with the output filename(UTF-8 encoding)\n\nDefault: 'False'", height=75, width=360)

        # start button
        self.stt_start_button = customtkinter.CTkButton(self.frame2, command=self.stt_start_button_event, text="Run Text Steganographer")
        self.stt_start_button.grid(row=10, column=2, padx=20, pady=10, ipady=5, columnspan=3, rowspan=2, sticky="we")


        #---------------------------------------------------------------------------------------------------------------

        # add frames to notebook

        self.my_notebook.add(self.frame0, text="Tab 1")
        self.my_notebook.add(self.frame1, text="Tab 2")
        self.my_notebook.add(self.frame2, text="Tab 3")

        # set default values
        #------------------------------------ Image Scrambler ----------------------------------------------------------
        self.sc_console.configure(state="disabled")
        #------------------------------------Image - Image Steganography -----------------------------------------------
        self.st_console.configure(state="disabled")
        self.st_type_dropdown.set("Steganography x2")
        self.st_type_dropdown_event("Steganography x2")
        self.st_folder_checkbox.deselect()
        self.st_folder_checkbox_event()
        #------------------------------------Text - IM Steganography ---------------------------------------------------
        self.stt_console.configure(state="disabled")
        self.stt_type_dropdown.set("LayeredDynamic")
        #------------------------------------------ Other --------------------------------------------------------------
        self.appearance_mode_optionemenu.set("System")
        self.my_notebook.select(2)


    # ------------------------------------ FUNCTIONS -------------------------------------------------------------------


    def change_appearance_mode_event(self, new_appearance_mode: str): # NOQA
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Sidebar functions ------------------------------------------------------------------------------------------------

    def sidebar_button_event_frame_0(self): self.my_notebook.select(0)
    def sidebar_button_event_frame_1(self): self.my_notebook.select(1)
    def sidebar_button_event_frame_2(self): self.my_notebook.select(2)

    # Image Scrambler functions ----------------------------------------------------------------------------------------

    def sc_open_folder(self):
        self.sc_ent2.delete(0, "end")
        self.sc_ent2.insert(0, filedialog.askdirectory(initialdir=self.initial_browser_dir, title="Select output folder"))

    def sc_open_image(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        with Image.open(filename) as image:
            text = f"Image size: {image.size}\nImage mode: {image.mode}\nImage format: {image.format}\nPossible sizes: {_calc_size(image.size[0], image.size[1])}"
        CreateToolTip(self.sc_ent1, text, height=100, width=200)
        self.sc_ent1.delete(0, "end")
        self.sc_ent1.insert(0, filename)

        CreateToolTip(self.sc_ent1, )

    def sc_seed_loop_checkbox_event(self):
        self.sc_to_seed_ent.configure(state="normal" if self.sc_loop_checkbox1.get() else "disabled",
                                   placeholder_text="To" if self.sc_loop_checkbox1.get() else "",
                                   border_width=2 if self.sc_loop_checkbox1.get() else 0)
        self.sc_from_seed_ent.configure(placeholder_text="From" if self.sc_loop_checkbox1.get() else "Seed")
        self.sc_output_folder_name_ent.configure(
            state="normal" if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else "disabled",
            border_width=2 if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else 0,
            placeholder_text="Output Folder Name" if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else "")

    def sc_size_loop_checkbox_event(self):
        self.sc_to_size_ent.configure(state="normal" if self.sc_loop_checkbox2.get() else "disabled",
                                   placeholder_text="To" if self.sc_loop_checkbox2.get() else "",
                                   border_width=2 if self.sc_loop_checkbox1.get() else 0)
        self.sc_from_size_ent.configure(placeholder_text="From" if self.sc_loop_checkbox1.get() else "Size")
        self.sc_output_folder_name_ent.configure(
            state="normal" if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else "disabled",
            border_width=2 if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else 0,
            placeholder_text="Output Folder Name" if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else "")

    def sc_start_button_event(self):
        seed = self.sc_from_seed_ent.get()
        size = self.sc_from_size_ent.get()
        image_path = self.sc_ent1.get()
        folder_path = self.sc_ent2.get()
        action_type = self.sc_action_type_var.get()
        output_type = self.sc_output_type_var.get()
        seed_loop = self.sc_loop_checkbox1.get()
        size_loop = self.sc_loop_checkbox2.get()
        seed_to = self.sc_to_seed_ent.get()
        size_to = self.sc_to_size_ent.get()
        file_name = self.sc_output_name_ent.get()
        folder_name = self.sc_output_folder_name_ent.get()

        if not image_path or not folder_path:
            self.print_to_sc_console("Please select an image and a folder.")
            return

        if file_name == "":
            file_name = "output"

        if folder_name == "":
            folder_name = "Image Scrambler Output"

        if folder_path[-1] != "/" or folder_path[-1] != "\\":
            if "\\" in folder_path:
                folder_path += "\\"
            else:
                folder_path += "/"

        if seed_loop or size_loop:
            folder_path = make_folder(folder_path + folder_name)
            if "\\" in folder_path:
                folder_path += "\\"
            else:
                folder_path += "/"

        if not seed_loop and not size_loop:

            if seed == "": seed = 0
            if size == "": size = 10

            try:
                size = int(size)
            except ValueError:
                self.print_to_sc_console("Please enter a valid size. (Integer)")
                return

            # configure start button
            self.sc_start_button.configure(state="disabled")
            self.sc_start_button.configure(text="Working...")

            # print info to console
            self.print_to_sc_console("-" * 72 + "START" + "-" * 73)
            self.print_to_sc_console(f"Seed: {seed} | Size: {size} | Action: {action_type} | Output: {output_type} | Output filename: {file_name}_({seed}_{size}) |Image: {image_path.split('/')[-1]}")
            self.print_to_sc_console(f"Seed loop: False | Size loop: False")
            self.print_to_sc_console("Folder: " + folder_path + "\n")

            # start thread
            output = new_scramble_algorithm(action_type, output_type, image_path, folder_path, f"{file_name}_({seed}_{size})", seed, size)
            self.print_to_sc_console(output) # print output to console

            # configure start button
            self.sc_start_button.configure(state="normal")
            self.sc_start_button.configure(text="Run Image Scramble")

        else:
            if seed_loop:
                if seed == "" or seed_to == "":
                    return self.print_to_sc_console("Please enter a valid seed range.")
                try:
                    seed = int(seed)
                    seed_to = int(seed_to)
                except ValueError:
                    self.print_to_sc_console("Please enter a valid seed range. (Integer)")
                    return

                if seed > seed_to: return self.print_to_sc_console("Please enter a valid seed range. (From < To)")

                seed_range = list(range(seed, seed_to+1))
            else:
                if seed == "": seed = 0
                seed_range = [seed]

            if size_loop:
                if size == "" or size_to == "":
                    return self.print_to_sc_console("Please enter a valid size range.")
                try:
                    size = int(size)
                    size_to = int(size_to)
                except ValueError:
                    self.print_to_sc_console("Please enter a valid size range. (Integer)")
                    return

                if size > size_to: return self.print_to_sc_console("Please enter a valid size range. (From < To)")

                size_range = list(range(size, size_to+1))
            else:
                if size == "": size = 10
                size_range = [size]

            # configure start button
            self.sc_start_button.configure(state="disabled")
            self.sc_start_button.configure(text="Working...")

            # print info to console
            self.print_to_sc_console("-" * 75 + "START" + "-" * 77)
            self.print_to_sc_console(f"Seed: {seed} | Size: {size} | Action: {action_type} | Output: {output_type} | Image: {image_path.split('/')[-1]}")
            if seed_loop and size_loop: self.print_to_sc_console(f"Seed loop: {seed} -> {seed_to} | Size loop: {size} -> {size_to}")
            elif seed_loop: self.print_to_sc_console(f"Seed loop: {seed} -> {seed_to} | Size loop: False")
            elif size_loop: self.print_to_sc_console(f"Seed loop: False | Size loop: {size} -> {size_to}")
            self.print_to_sc_console("Folder: " + folder_path + "\n")

            # start thread
            for size in size_range:
                for seed in seed_range:
                    self.print_to_sc_console(f"\nSeed: {seed} | Size: {size} | Iteration: {(size_range.index(size)+1)*(seed_range.index(seed)+1)}/{len(size_range)*len(seed_range)} | Filename: {file_name}_({seed}_{size})")
                    output = new_scramble_algorithm(action_type, output_type, image_path, folder_path, f"{file_name}_({seed}_{size})", seed, size)
                    self.print_to_sc_console(output)

            self.print_to_sc_console(f"\nIterations Finished. \nTotal iterations done: {len(size_range)*len(seed_range)}")

            # configure start button
            self.sc_start_button.configure(state="normal")
            self.sc_start_button.configure(text="Run Image Scramble")


    # Steganography functions ------------------------------------------------------------------------------------------

    def st_open_image1(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent1.delete(0, "end")
        self.st_ent1.insert(0, filename)
        CreateToolTip(self.st_ent1, filename=filename)
    def st_open_image2(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent2.delete(0, "end")
        self.st_ent2.insert(0, filename)
        CreateToolTip(self.st_ent2, filename=filename)
    def st_open_image3(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent3.delete(0, "end")
        self.st_ent3.insert(0, filename)
        CreateToolTip(self.st_ent3, filename=filename)
    def st_open_image4(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent4.delete(0, "end")
        self.st_ent4.insert(0, filename)
        CreateToolTip(self.st_ent4, filename=filename)
    def st_open_image5(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent5.delete(0, "end")
        self.st_ent5.insert(0, filename)
        CreateToolTip(self.st_ent5, filename=filename)
    def st_open_image6(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent6.delete(0, "end")
        self.st_ent6.insert(0, filename)
        CreateToolTip(self.st_ent6, filename=filename)
    def st_open_image7(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent7.delete(0, "end")
        self.st_ent7.insert(0, filename)
        CreateToolTip(self.st_ent7, filename=filename)
    def st_open_image8(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent8.delete(0, "end")
        self.st_ent8.insert(0, filename)
        CreateToolTip(self.st_ent8, filename=filename)

    def st_open_folder(self):
        self.st_ent_folder.delete(0, "end")
        self.st_ent_folder.insert(0, filedialog.askdirectory(initialdir=self.initial_browser_dir, title="Select output folder"))

    def st_type_dropdown_event(self, new_action_type: str):
        num = 1
        if new_action_type == "Unmerge":
            num = 1
            self.st_folder_checkbox.select()
        if self.st_action_type_dropdown.get() == "Merge":
            self.st_folder_checkbox.deselect()
            if self.st_type_dropdown.get() == "Steganography x2": num=2
            if self.st_type_dropdown.get() == "Steganography x3": num=3
            if self.st_type_dropdown.get() == "Steganography x4": num=4
            if self.st_type_dropdown.get() == "Steganography x8": num=8


        for i in range(num):
            exec(f"self.st_ent{i+1}.configure(state='normal', border_width=2)")
            exec(f"self.st_sidebar_button_{i+1}.configure(state='normal')")

        if num != 8:
            for i in range(8-num):
                exec(f"self.st_ent{8-i}.configure(state='disabled', border_width=0)")
                exec(f"self.st_sidebar_button_{8-i}.configure(state='disabled')")

    def st_folder_checkbox_event(self):
        if self.st_folder_checkbox.get() == 1: self.st_output_folder_ent.configure(state="normal", border_width=2)
        else: self.st_output_folder_ent.configure(state="disabled", border_width=0)

    def st_explanation_event(self):
        window = customtkinter.CTkToplevel(self)
        window.title("Steganography Explanation")
        window.geometry("1100x700")
        with open("Assets/SteganographyExplanation.html", "r") as f:
            html_label = HTMLScrolledText(window, html=f.read(), )
        html_label.pack(fill="both", expand=True)
        html_label.fit_height()

    def st_start_button_event(self):
        ent1 = self.st_ent1.get()
        ent2 = self.st_ent2.get()
        ent3 = self.st_ent3.get()
        ent4 = self.st_ent4.get()
        ent5 = self.st_ent5.get()
        ent6 = self.st_ent6.get()
        ent7 = self.st_ent7.get()
        ent8 = self.st_ent8.get()
        ent_folder = self.st_ent_folder.get()

        output_type_dropdown = self.st_output_type_dropdown.get() # "PNG" or "JPG"
        type_dropdown = self.st_type_dropdown.get() # steganography type
        action_type_dropdown = self.st_action_type_dropdown.get() # "Merge" or "Unmerge"
        folder_checkbox = self.st_folder_checkbox.get() # 0 or 1
        output_folder_ent = self.st_output_folder_ent.get() # output folder
        output_name_ent = self.st_output_name_ent.get() # output name

        image = ""
        images = []

        if output_name_ent == "": output_name_ent = "output"

        if folder_checkbox == 1 and output_folder_ent == "": output_folder_ent = "SteganographyOutput"

        if ent_folder[-1] != "/" or ent_folder[-1] != "\\":
            if "\\" in ent_folder: ent_folder += "\\"
            else: ent_folder += "/"

        # Get path

        path = f"{ent_folder}/{output_name_ent}"

        if folder_checkbox == 1:
            output_folder_path = make_folder(ent_folder + output_folder_ent)
            path = f"{output_folder_path}/{output_name_ent}"


        # Warning message

        if action_type_dropdown == "Unmerge":
            if not ent1:
                return self.print_to_st_console("Image 1 must be filled in")

        if action_type_dropdown == "Merge":
            if type_dropdown == "Steganography x2" and (not ent1 or not ent2):
                return self.print_to_st_console("Image 1 and 2 must be filled in")
            elif type_dropdown == "Steganography x3" and (not ent1 or not ent2 or not ent3):
                return self.print_to_st_console("Image 1, 2 and 3 must be filled in")
            elif type_dropdown == "Steganography x4" and (not ent1 or not ent2 or not ent3 or not ent4):
                return self.print_to_st_console("Image 1, 2, 3 and 4 must be filled in")
            elif type_dropdown == "Steganography x5" and (not ent1 or not ent2 or not ent3 or not ent4 or not ent5):
                return self.print_to_st_console("Image 1, 2, 3, 4 and 5 must be filled in")
            elif type_dropdown == "Steganography x6" and (not ent1 or not ent2 or not ent3 or not ent4 or not ent5 or not ent6):
                return self.print_to_st_console("Image 1, 2, 3, 4, 5 and 6 must be filled in")
            elif type_dropdown == "Steganography x7" and (not ent1 or not ent2 or not ent3 or not ent4 or not ent5 or not ent6 or not ent7):
                return self.print_to_st_console("Image 1, 2, 3, 4, 5, 6 and 7 must be filled in")
            elif type_dropdown == "Steganography x8" and (not ent1 or not ent2 or not ent3 or not ent4 or not ent5 or not ent6 or not ent7 or not ent8):
                return self.print_to_st_console("Image 1, 2, 3, 4, 5, 6, 7 and 8 must be filled in")

        # Merge / Unmerge

        if action_type_dropdown == "Merge":
            im_list = []
            if type_dropdown == "Steganography x2":
                for i in range(2): im_list.append(Image.open(ent1 if i == 0 else ent2))
                image = Steganography().merge(im_list)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x3":
                for i in range(3): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3))
                image = Steganography3().merge(im_list)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x4":
                for i in range(4): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4))
                image = Steganography4().merge(im_list)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x5":
                for i in range(5): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4 if i == 3 else ent5))
                image = Steganography5().merge(im_list)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x6":
                for i in range(6): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4 if i == 3 else ent5 if i == 4 else ent6))
                image = Steganography6().merge(im_list)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x7":
                for i in range(7): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4 if i == 3 else ent5 if i == 4 else ent6 if i == 5 else ent7))
                image = Steganography7().merge(im_list)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x8":
                for i in range(8): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4 if i == 3 else ent5 if i == 4 else ent6 if i == 5 else ent7 if i == 6 else ent8))
                image = Steganography8().merge(im_list)
                for im in im_list: im.close()

            for im in im_list:
                im.close()

        if action_type_dropdown == "Unmerge":
            im = Image.open(ent1)
            if type_dropdown == "Steganography x2":
                images = Steganography().unmerge(im)
            elif type_dropdown == "Steganography x3":
                images = Steganography3().unmerge(im)
            elif type_dropdown == "Steganography x4":
                images = Steganography4().unmerge(im)
            elif type_dropdown == "Steganography x5":
                images = Steganography5().unmerge(im)
            elif type_dropdown == "Steganography x6":
                images = Steganography6().unmerge(im)
            elif type_dropdown == "Steganography x7":
                images = Steganography7().unmerge(im)
            elif type_dropdown == "Steganography x8":
                images = Steganography8().unmerge(im)
            im.close()

        # Save image

        if action_type_dropdown == "Merge":
            image.save(f"{path}.{output_type_dropdown.lower()}")
        else:
            for i, im in enumerate(images):
                im.save(f"{path}_{i + 1}.{output_type_dropdown.lower()}")

        self.print_to_st_console(f"Saved to: '{path}'")


    # Text Steganography Functions -------------------------------------------------------------------------------------

    def stt_open_folder(self):
        self.stt_ent2.delete(0, "end")
        self.stt_ent2.insert(0, filedialog.askdirectory(initialdir=self.initial_browser_dir, title="Select output folder"))

    def stt_open_image(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.stt_ent1.delete(0, "end")
        self.stt_ent1.insert(0, filename)
        CreateToolTip(self.stt_ent1, filename=filename)

    def stt_action_type_dropdown_event(self, new_action_type: str):
        if new_action_type == "Encode":
            self.stt_ent2.configure(state="normal", border_width=2)
            self.stt_sidebar_button_2.configure(state="normal")
            if self.stt_type_dropdown.get() == "LayeredDynamicTransparent":
                self.stt_output_type_dropdown.configure(state="disabled")
            else:
                self.stt_output_type_dropdown.configure(state="normal")
            self.stt_text_output_checkbox.configure(state="disabled")
            self.stt_text_output_checkbox.deselect()
            self.stt_text_output_checkbox_event()
            self.stt_output_name_ent.configure(state="normal", border_width=2)

        if new_action_type == "Decode":
            self.stt_ent2.configure(state="disabled", border_width=0)
            self.stt_sidebar_button_2.configure(state="disabled")
            self.stt_output_type_dropdown.configure(state="disabled")
            self.stt_text_output_checkbox.configure(state="normal")
            self.stt_text_output_checkbox_event()
            self.stt_output_name_ent.configure(state="disabled", border_width=0)

    def stt_encoding_type_dropdown_event(self, new_type: str):
        if new_type == "UNICODE":
            self.stt_type_dropdown.set("LayeredDynamic")
            self.stt_type_dropdown.configure(state="disabled")
        if new_type == "ASCII":
            self.stt_type_dropdown.configure(state="normal")

    def stt_text_output_checkbox_event(self):
        if self.stt_text_output_checkbox.get():
            self.stt_output_name_ent.configure(state="normal", border_width=2)
            self.stt_output_type_dropdown.set("TXT")
        else:
            self.stt_output_name_ent.configure(state="disabled", border_width=0)
            self.stt_output_type_dropdown.set("PNG")

    def stt_type_dropdown_event(self, new_type: str):
        if new_type == "LayeredDynamicTransparent":
            self.stt_output_type_dropdown.set("PNG")
            self.stt_output_type_dropdown.configure(state="disabled")
        else:
            self.stt_output_type_dropdown.configure(state="normal")


    def stt_start_button_event(self):
        ent1 = self.stt_ent1.get()
        ent2 = self.stt_ent2.get()
        ent3 = self.stt_ent3.get(index1="0.0", index2="end")
        output_text_to_file = self.stt_text_output_checkbox.get()
        output_name = self.stt_output_name_ent.get()
        st_type = self.stt_type_dropdown.get() # Steganography Type: Layered, Sequential, etc.
        encoding_type = self.stt_encoding_type_dropdown.get() # Encoding Type: UNICODE, ASCII
        action_type_dropdown = self.stt_action_type_dropdown.get() # Action Type: Encode, Decode
        output_type_dropdown = self.stt_output_type_dropdown.get() # Output Type: PNG, GIF, etc. (Only for encoding - only lossless formats)

        # folder/file path
        if action_type_dropdown == "Encode" or output_text_to_file:
            if not ent2: return self.print_to_stt_console("Output folder not specified", error=True)
            if ent2[-1] != "/" or ent2[-1] != "\\":
                if "\\" in ent2: ent2 += "\\"
                else: ent2 += "/"
        if not output_name: output_name = "TextSteganographyOutput"
        path = f"{ent2}{output_name}.{output_type_dropdown.lower()}"
        if output_text_to_file: output_to = f"{ent2}{output_name}.txt"
        else: output_to = "TextBox"

        # image
        if not ent1: return self.print_to_stt_console("Please select an image.", error=True)
        try: im = Image.open(ent1)
        except Exception as e: return self.print_to_stt_console(f"Error opening image: {e}", error=True)

        # text
        if ent3.isascii() == False and encoding_type == "ASCII": return self.print_to_stt_console("Text contains non-ASCII characters.\n\nSwitch to LayeredDynamic and UNICODE", error=True)

        # start
        if action_type_dropdown == "Encode":
            if not ent3: return self.print_to_stt_console("Please enter text.", error=True)

            if st_type == "Layered8":
                if encoding_type == "UNICODE":
                    return self.print_to_stt_console("UNICODE encoding is not supported for Layered. Please select LayeredDynamic", error=True)
                if encoding_type == "ASCII":
                    try:
                        image, layers = TextSteganographyLayered().encode(image=im, text=ent3)
                        image.save(path)
                        self.print_to_stt_console(f"Layered8 | Bits: 8 | Layers: {layers} | Characters: {len(ent3)} | Type: {encoding_type} | Action: {action_type_dropdown}\n\nSaved to: '{path}'")
                    except ValueError as e: return self.print_to_stt_console(e)

            if st_type == "Sequential8":
                if encoding_type == "UNICODE":
                    return self.print_to_stt_console("UNICODE encoding is not supported for Sequential. Please select LayeredDynamic", error=True)
                if encoding_type == "ASCII":
                    try:
                        image, layers = TextSteganography().encode(image=im, text=ent3)
                        image.save(path)
                        self.print_to_stt_console(f"Sequential8 | Bits: 8 | Layers: {layers} | Characters: {len(ent3)} | Type: {encoding_type} | Action: {action_type_dropdown}\n\nSaved to: '{path}'")
                    except ValueError as e: return self.print_to_stt_console(e)

            if st_type == "LayeredDynamic":
                try:
                    image, bits, layers = TextSteganographyLayeredDynamic().encode(image=im, text=ent3)
                    image.save(path)
                    self.print_to_stt_console(f"LayeredDynamic | Bits: {bits} | Layers: {layers} | Characters: {len(ent3)} | Type: {encoding_type} | Action: {action_type_dropdown}\n\nSaved to: '{path}'")
                except ValueError as e: return self.print_to_stt_console(e)

        if action_type_dropdown == "Decode":
            if st_type == "Layered8":
                try:
                    text = TextSteganographyLayered().decode(image=im)
                    self.print_to_stt_textbox(text, output_to)
                    self.print_to_stt_console(f"Layered8 | Bits: 8 | Characters: {len(text)} | Type: {encoding_type} | Action: {action_type_dropdown}\n\nOutput in: {output_to}")
                except ValueError as e: return self.print_to_stt_console(e)

            if st_type == "Sequential8":
                try:
                    text = TextSteganography().decode(image=im, layer=1)
                    self.print_to_stt_textbox(text, output_to)
                    self.print_to_stt_console(f"Sequential8 | Bits: 8 | Characters: {len(text)} | Type: {encoding_type} | Action: {action_type_dropdown}\n\nOutput in: {output_to}")
                except ValueError as e: return self.print_to_stt_console(e)

            if st_type == "LayeredDynamic":
                try:
                    text, bits = TextSteganographyLayeredDynamic().decode(image=im)
                    self.print_to_stt_textbox(text, output_to)
                    self.print_to_stt_console(f"LayeredDynamic | Bits: {bits} | Characters: {len(text)} | Type: {'ASCII' if text.isascii() else 'UNICODE'} | Action: {action_type_dropdown}\n\nOutput in: {output_to}")
                except ValueError as e: return self.print_to_stt_console(e)

            if st_type == "LayeredDynamicTransparent":
                try:
                    text, bits = TextSteganographyLayeredDynamicTransparent().decode(image=im)
                    self.print_to_stt_textbox(text, output_to)
                    self.print_to_stt_console(f"LayeredDynamicTransparent | Bits: {bits} | Characters: {len(text)} | Type: {'ASCII' if text.isascii() else 'UNICODE'} | Action: {action_type_dropdown}\n\nOutput in: {output_to}")
                except ValueError as e: return self.print_to_stt_console(e)



    # Console Functions ------------------------------------------------------------------------------------------------

    def print_to_sc_console(self, text, error=False):
        self.sc_console.configure(state="normal")
        self.sc_console.insert(customtkinter.END, text + "\n")
        self.sc_console.configure(state="disabled")
        self.sc_console.see("end")
        if error: self.sc_console.configure(border_width=2, border_color="#1F6AA5")
        else: self.sc_console.configure(border_width=0)
        self.update_idletasks()
        self.update()

    def print_to_st_console(self, text, error=False):
        self.st_console.configure(state="normal")
        self.st_console.delete("1.0", "end")
        self.st_console.insert(customtkinter.END, text)
        self.st_console.configure(state="disabled")
        if error: self.st_console.configure(border_width=2, border_color="#1F6AA5")
        else: self.st_console.configure(border_width=0)
        self.update_idletasks()
        self.update()

    def print_to_stt_console(self, text, error=False):
        self.stt_console.configure(state="normal")
        self.stt_console.delete("1.0", "end")
        self.stt_console.insert(customtkinter.END, text)
        self.stt_console.configure(state="disabled")
        if error: self.stt_console.configure(border_width=2, border_color="#1F6AA5")
        else: self.stt_console.configure(border_width=0)
        self.update_idletasks()
        self.update()

    def print_to_stt_textbox(self, text, output_to):
        if output_to == "TextBox":
            self.stt_ent3.delete("0.0", "end")
            self.stt_ent3.insert(customtkinter.END, text)
            self.update_idletasks()
            self.update()
        else:
            with open(output_to, "w", encoding="utf-8") as f:
                f.write(text)




# Static Functions -----------------------------------------------------------------------------------------------------

def make_folder(folder_path):
    # Example folder path: "C:/Users/Tomer27cz/Desktop/Files/CODING/Python Projects/AICode/Output"
    try:
        print("Making folder: " + folder_path)
        os.mkdir(folder_path)
        return folder_path
    except FileExistsError:
        print("Folder already exists: " + folder_path)
        if folder_path[-1] == ")":
            number = folder_path.split("(")[-1].split(")")[0]
            print("Folder number: " + number)
            print(folder_path[:-3] + f"({int(number) + 1})")
            return make_folder(folder_path[:-3] + f"({int(number) + 1})")
        else:
            print(folder_path + "(1)")
            return make_folder(folder_path + " (1)")


def _calc_size(width, height):
    """Calculate all the sizes for the image."""
    possible_sizes = []
    for n in range(1, max(width, height) + 1):
        if width % n == 0 and height % n == 0:
            possible_sizes.append(n)
    return possible_sizes



# Main -----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()