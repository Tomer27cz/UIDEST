import tkinter
from PIL import Image
from tkinter import ttk
from tkinter import filedialog

from tkhtmlview import HTMLScrolledText
import customtkinter
from os import mkdir
from time import time
import subprocess

from Features.Image.ImageScramble import new_scramble_algorithm
from Features.Image.ImageSteganography import Steganography, Steganography3, Steganography4, Steganography5, Steganography6, Steganography7, Steganography8
from Features.Image.Text.TextSteganography import TextSteganographyLayeredDynamic, TextSteganography, TextSteganographyLayered, TextSteganographyLayeredDynamicTransparent
from Features.Image.Text.TextToImage import TextToImageDynamic
from Features.tkinter.ToolTip import CreateToolTip

from Assets.lang_list import lang_dict, lang_dict_inv

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk, tkinter.Tk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Universal Image Decode Encode and Steganography Tool")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0) # NOQA
        self.grid_rowconfigure((0, 1, 2), weight=1) # NOQA

        # configure paths
        self.exif_tool_path = 'Features/Executable/exiftool.exe'
        self.yt_dlp_path = 'Features/Executable/yt-dlp.exe'
        self.steganography_explanation = "Assets/html/SteganographyExplanation.html"
        self.markdown = 'Assets/html/README.html'
        self.about_html_text = open(self.markdown, 'r').read()

        # configure misc
        self.initial_browser_dir = 'Desktop'
        self.title_open = "Select image file"

        # lists
        self.filetypes = (("image files", "*.png *.jpg *.jpeg *.gif *.webp *.ico *.tiff *.bmp *.im *.msp *.pcx *.ppm *.sgi *.xbm *.dds *.dib *.eps *.spi"), ("all files", "*.*"))
        self.output_type_list = ["BMP", "DDS", "DIB", "EPS", "GIF", "ICO", "IM", "JPEG", "JPG", "PCX", "PNG", "PPM", "SGI", "SPIDER", "TGA", "TIFF", "WebP"]
        self.output_type_list_lossless = ["BMP", "GIF", "PNG", "TIFF", "WebP", "ICO", "PCX", "SGI", "TGA"]
        self.resolutions_list = ["144p", "240p (SD)", "360p (SD)", "480p (SD/DVD)", "720p (HD)", "1080p (Full HD)", "1440p (QHD/2k)", "2160p (UHD/4k)", "4320p (8k)", "best"]
        self.resolutions_list_values = [(256, 144), (426, 240), (640, 360), (854, 480), (1280, 720), (1920, 1080), (2560, 1440), (3840, 2160), (7680, 4320)]
        # self.yt_ext = ['mp4', 'webm', 'mkv', 'mov', 'flv']
        # self.yt_ext_audio = ['mp3', 'ogg', 'opus', 'webm', 'm4a', 'aac', 'flac', 'wav']

        self.yt_codec = ['vp9', 'av01', 'avc1', 'best']
        self.yt_codec_audio = ['opus', 'mp4a', 'best']

        # self.yt_ext = ['avi', 'flv', 'gif', 'mkv', 'mov', 'mp4', 'webm', 'aac', 'aiff', 'alac', 'flac', 'm4a', 'mka', 'mp3', 'ogg', 'opus', 'vorbis', 'wav']
        self.yt_ext = ['avi', 'mkv', 'mp4', 'webm', 'mka']
        self.yt_ext_audio = ['aac', 'alac', 'flac', 'm4a', 'mp3', 'ogg', 'opus', 'vorbis', 'wav']

        self.sub_ext_list = ['vtt', 'ttml', 'srv3', 'srv2', 'srv1', 'json3']
        self.sub_lang_list = list(lang_dict.values())

        self.text_encryption_list = ["None", "AES", "RSA"]

        # icons
        self.folder_button_icon = customtkinter.CTkImage(light_image=Image.open("Assets/icons/folder-open-light.png"), dark_image=Image.open("Assets/icons/folder-open-dark.png"))
        self.info_marker_icon = customtkinter.CTkImage(light_image=Image.open("Assets/icons/info-mark-light.png"), dark_image=Image.open("Assets/icons/info-mark-dark.png"))
        self.copy_icon = customtkinter.CTkImage(light_image=Image.open('Assets/icons/copy-dark.png'), dark_image=Image.open('Assets/icons/copy-dark.png'))

        # create variables

        self.button_spacing = 5
        self.spacing = 5
        self.st_spacing = 3
        self.tab_spacing = 2
        #-----------------------------------------------
        self.sc_seed_loop_var = tkinter.IntVar(value=0)
        self.sc_size_loop_var = tkinter.IntVar(value=0)
        self.sc_action_type_var = tkinter.StringVar(value="Encode")
        self.sc_output_type_var = tkinter.StringVar(value="PNG")
        self.sc_ent1_var = tkinter.StringVar(value="")
        self.sc_ent2_var = tkinter.StringVar(value="")
        self.sc_output_name_var = tkinter.StringVar(value="")
        self.sc_output_folder_var = tkinter.StringVar(value="")
        #-----------------------------------------------
        self.st_type_var = tkinter.StringVar(value="Steganography x2")
        self.st_output_type_var = tkinter.StringVar(value="PNG")
        self.st_action_type_var = tkinter.StringVar(value="Merge")
        self.st_ent1_var = tkinter.StringVar(value="")
        self.st_ent2_var = tkinter.StringVar(value="")
        self.st_ent3_var = tkinter.StringVar(value="")
        self.st_ent4_var = tkinter.StringVar(value="")
        self.st_ent5_var = tkinter.StringVar(value="")
        self.st_ent6_var = tkinter.StringVar(value="")
        self.st_ent7_var = tkinter.StringVar(value="")
        self.st_ent8_var = tkinter.StringVar(value="")
        self.st_ent_folder_var = tkinter.StringVar(value="")
        self.st_output_name_var = tkinter.StringVar(value="")
        self.st_output_folder_var = tkinter.StringVar(value="")
        #-----------------------------------------------
        self.stt_type_var = tkinter.StringVar(value="Layered8")
        self.stt_output_type_var = tkinter.StringVar(value="PNG")
        self.stt_action_type_var = tkinter.StringVar(value="Encode")
        self.stt_encoding_type_var = tkinter.StringVar(value="ASCII")
        self.stt_text_output_checkbox_var = tkinter.IntVar(value=0)
        self.stt_text_input_checkbox_var = tkinter.IntVar(value=0)
        self.stt_ent1_var = tkinter.StringVar(value="")
        self.stt_ent2_var = tkinter.StringVar(value="")
        self.stt_ent4_var = tkinter.StringVar(value="")
        self.stt_output_name_var = tkinter.StringVar(value="")
        #-----------------------------------------------
        self.tti_text_input_checkbox_var = tkinter.IntVar(value=0)
        self.tti_text_output_checkbox_var = tkinter.IntVar(value=0)
        self.tti_output_type_var = tkinter.StringVar(value="PNG")
        self.tti_action_type_var = tkinter.StringVar(value="Encode")
        self.tti_color_var = tkinter.StringVar(value="RGB")
        self.tti_ent1_var = tkinter.StringVar(value="")
        self.tti_ent2_var = tkinter.StringVar(value="")
        self.tti_ent3_var = tkinter.StringVar(value="")
        self.tti_output_name_var = tkinter.StringVar(value="")
        #-----------------------------------------------
        self.iet_output_type_var = tkinter.StringVar(value="PNG")
        self.iet_ent1_var = tkinter.StringVar(value="")
        #-----------------------------------------------
        self.mi_ent1_var = tkinter.StringVar(value="")
        #-----------------------------------------------
        self.yt_resolution_var = tkinter.StringVar(value="best")
        self.yt_playlist_var = tkinter.IntVar(value=0)
        self.yt_ent1_var = tkinter.StringVar(value="")
        self.yt_ent2_var = tkinter.StringVar(value="")
        self.yt_ent3_var = tkinter.StringVar(value="")
        self.yt_ent4_var = tkinter.StringVar(value="")
        self.yt_sub_lang_var = tkinter.StringVar(value="English")
        self.yt_sub_ext_var = tkinter.StringVar(value="vtt")
        self.yt_sub_auto_var = tkinter.IntVar(value=1)
        self.yt_video_ext_var = tkinter.StringVar(value="mp4")
        self.yt_audio_ext_var = tkinter.StringVar(value="mp3")
        self.yt_video_codec_var = tkinter.StringVar(value="best")
        self.yt_audio_codec_var = tkinter.StringVar(value="best")
        self.yt_checkbox_video_var = tkinter.IntVar(value=1)
        self.yt_checkbox_audio_var = tkinter.IntVar(value=1)
        self.yt_checkbox3_var = tkinter.IntVar(value=0)
        self.yt_checkbox4_var = tkinter.IntVar(value=0)
        self.yt_checkbox5_var = tkinter.IntVar(value=0)
        # -----------------------------------------------
        self.te_dropdown1_var = tkinter.StringVar(value="uft8")
        self.te_dropdown2_var = tkinter.StringVar(value="utf8")


        # create sidebar

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="UIDEST 2.1", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Image Scrambler", command=self.sidebar_button_event_frame_0)
        self.sidebar_button_1.grid(row=1, column=0, padx=10, pady=self.button_spacing)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Image - Image\nSteganography", command=self.sidebar_button_event_frame_1)
        self.sidebar_button_2.grid(row=2, column=0, padx=10, pady=self.button_spacing)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Image - Text\nSteganography", command=self.sidebar_button_event_frame_2)
        self.sidebar_button_3.grid(row=3, column=0, padx=10, pady=self.button_spacing)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Text - Image\nGenerator", command=self.sidebar_button_event_frame_3)
        self.sidebar_button_4.grid(row=4, column=0, padx=10, pady=self.button_spacing)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Transform Image\nExtension", command=self.sidebar_button_event_frame_4)
        self.sidebar_button_5.grid(row=5, column=0, padx=10, pady=self.button_spacing)
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text="Get Metadata", command=self.sidebar_button_event_frame_5)
        self.sidebar_button_6.grid(row=6, column=0, padx=10, pady=self.button_spacing)
        self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, text="YT Downloader", command=self.sidebar_button_event_frame_6)
        self.sidebar_button_7.grid(row=7, column=0, padx=10, pady=self.button_spacing)
        self.sidebar_button_8 = customtkinter.CTkButton(self.sidebar_frame, text="Text Encryption", command=self.sidebar_button_event_frame_7)
        self.sidebar_button_8.grid(row=8, column=0, padx=10, pady=self.button_spacing)


        self.sidebar_button_about = customtkinter.CTkButton(self.sidebar_frame, text="About", command=self.sidebar_button_event_frame_about)
        self.sidebar_button_about.grid(row=13, column=0, padx=10, pady=0)
        # self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        # self.appearance_mode_label.grid(row=14, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=15, column=0, padx=10, pady=(10, 10))

        # create notebook

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TNotebook", background="#ffffff", borderwidth=0, padding=0)
        self.style.layout('Tabless.TNotebook.Tab', [])  # turn off tabs

        self.my_notebook = ttk.Notebook(self, style="Tabless.TNotebook")
        self.my_notebook.grid(row=0, column=1, rowspan=4, sticky="nsew")

        # create frames

        # ----------------------------------------------- About --------------------------------------------------------

        self.frame69 = customtkinter.CTkFrame(self.my_notebook, width=140, corner_radius=0)
        self.frame69.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # label
        # self.about_logo_label = customtkinter.CTkLabel(self.frame69, text="About", font=customtkinter.CTkFont(size=30, weight="bold"))
        # self.about_logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        # text
        # self.about_text = customtkinter.CTkLabel(self.frame69, width=100, height=100, font=customtkinter.CTkFont(size=12))
        # self.about_text.grid(row=1, column=0, padx=10, pady=20)

        # html
        self.about_html = HTMLScrolledText(self.frame69, html=self.about_html_text)
        self.about_html.grid(row=0, column=0, padx=0, pady=00, sticky="ws")

        #-------------------------------------------- Image Scrambler --------------------------------------------------


        self.frame0 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame0.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame0.grid_rowconfigure(9, weight=1)
        self.frame0.grid_columnconfigure(2, weight=1)

        # label
        self.sc_logo_label = customtkinter.CTkLabel(self.frame0, text="Image Scrambler", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sc_logo_label.grid(row=0, column=0, padx=10, pady=(20, 10), columnspan=3, sticky="w")

        # input/output entry
        self.sc_ent1 = customtkinter.CTkEntry(self.frame0, placeholder_text="Input image path here", width=100, textvariable=self.sc_ent1_var)
        self.sc_ent1.grid(row=1, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")
        self.sc_ent2 = customtkinter.CTkEntry(self.frame0, placeholder_text="Output folder path here", width=100, textvariable=self.sc_ent2_var)
        self.sc_ent2.grid(row=2, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")

        # input/output button
        self.sc_sidebar_button_1 = customtkinter.CTkButton(self.frame0, command=self.sc_open_image, image=self.folder_button_icon, text="Open Image")
        self.sc_sidebar_button_1.grid(row=1, column=0, padx=10, pady=self.spacing)
        self.sc_sidebar_button_2 = customtkinter.CTkButton(self.frame0, command=self.sc_open_folder, image=self.folder_button_icon, text="Open folder")
        self.sc_sidebar_button_2.grid(row=2, column=0, padx=10, pady=self.spacing)

        # loop checkboxes
        self.sc_loop_checkbox1 = customtkinter.CTkCheckBox(self.frame0, text="Seed", command=self.sc_seed_loop_checkbox_event, variable=self.sc_seed_loop_var, onvalue=1, offvalue=0)
        self.sc_loop_checkbox1.grid(row=4, column=0, padx=15, pady=10, sticky="wn")
        self.sc_loop_checkbox2 = customtkinter.CTkCheckBox(self.frame0, text="Size", command=self.sc_size_loop_checkbox_event, variable=self.sc_size_loop_var, onvalue=1, offvalue=0)
        self.sc_loop_checkbox2.grid(row=4, column=0, padx=(90, 0), pady=10, sticky="w", columnspan=2)

        # seed and size entry fields
        self.sc_from_seed_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="Seed", width=60)
        self.sc_from_seed_ent.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.sc_from_size_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="Size", width=60)
        self.sc_from_size_ent.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.sc_to_seed_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="", width=60, state="disabled", border_width=0)
        self.sc_to_seed_ent.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.sc_to_size_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="", width=60, state="disabled", border_width=0)
        self.sc_to_size_ent.grid(row=6, column=0, padx=10, pady=5, sticky="e")

        # filename and folder name entry fields
        self.sc_output_name_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="Output filename", width=100, textvariable=self.sc_output_name_var)
        self.sc_output_name_ent.grid(row=7, column=0, padx=10, pady=10, columnspan=1, sticky="ew")
        self.sc_output_folder_ent = customtkinter.CTkEntry(self.frame0, placeholder_text="", width=100, border_width=0, state="disabled", textvariable=self.sc_output_folder_var)
        self.sc_output_folder_ent.grid(row=8, column=0, padx=10, pady=10, columnspan=1, sticky="ew")

        # drop down menus
        self.sc_output_type_dropdown = customtkinter.CTkOptionMenu(self.frame0, values=self.output_type_list, variable=self.sc_output_type_var)
        self.sc_output_type_dropdown.grid(row=12, column=0, padx=10, pady=(10, 10))
        self.sc_action_type_dropdown = customtkinter.CTkOptionMenu(self.frame0, values=["Encode", "Decode"], variable=self.sc_action_type_var)
        self.sc_action_type_dropdown.grid(row=13, column=0, padx=10, pady=(10, 20))

        # console
        self.sc_console = customtkinter.CTkTextbox(self.frame0, width=100, height=300, font=customtkinter.CTkFont(size=15, family="Consolas"))
        self.sc_console.grid(row=4, column=2, columnspan=3, rowspan=8, sticky="ewsn", padx=10, pady=10)

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

        #start button
        self.sc_start_button = customtkinter.CTkButton(self.frame0, command=self.sc_start_button_event, text="Run Image Scrambler")
        self.sc_start_button.grid(row=12, column=2, padx=10, pady=10, ipady=5, columnspan=3, rowspan=2, sticky="we")


        #---------------------------------------- IM - IM Steganography ------------------------------------------------


        self.frame1 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame1.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame1.grid_rowconfigure(10, weight=1)
        self.frame1.grid_columnconfigure(3, weight=1)

        # logo
        self.st_logo_label = customtkinter.CTkLabel(self.frame1, text="Image - Image Steganography", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.st_logo_label.grid(row=0, column=0, padx=10, pady=(20, 10), columnspan=3, sticky="w")

        # image entries
        self.st_ent1 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100, textvariable=self.st_ent1_var)
        self.st_ent2 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100, textvariable=self.st_ent2_var)
        self.st_ent3 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100, textvariable=self.st_ent3_var)
        self.st_ent4 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100, textvariable=self.st_ent4_var)
        self.st_ent5 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100, textvariable=self.st_ent5_var)
        self.st_ent6 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100, textvariable=self.st_ent6_var)
        self.st_ent7 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100, textvariable=self.st_ent7_var)
        self.st_ent8 = customtkinter.CTkEntry(self.frame1, placeholder_text="Input image path here", width=100, textvariable=self.st_ent8_var)
        self.st_ent1.grid(row=1, column=1, padx=10, pady=self.st_spacing, columnspan=7, sticky="ew")
        self.st_ent2.grid(row=2, column=1, padx=10, pady=self.st_spacing, columnspan=7, sticky="ew")
        self.st_ent3.grid(row=3, column=1, padx=10, pady=self.st_spacing, columnspan=7, sticky="ew")
        self.st_ent4.grid(row=4, column=1, padx=10, pady=self.st_spacing, columnspan=7, sticky="ew")
        self.st_ent5.grid(row=5, column=1, padx=10, pady=self.st_spacing, columnspan=7, sticky="ew")
        self.st_ent6.grid(row=6, column=1, padx=10, pady=self.st_spacing, columnspan=7, sticky="ew")
        self.st_ent7.grid(row=7, column=1, padx=10, pady=self.st_spacing, columnspan=7, sticky="ew")
        self.st_ent8.grid(row=8, column=1, padx=10, pady=self.st_spacing, columnspan=7, sticky="ew")

        # folder entry
        self.st_ent_folder = customtkinter.CTkEntry(self.frame1, placeholder_text="Output folder path here", width=100, textvariable=self.st_ent_folder_var)
        self.st_ent_folder.grid(row=9, column=1, padx=10, pady=23, columnspan=7, sticky="ew")

        # image buttons
        self.st_sidebar_button_1 = customtkinter.CTkButton(self.frame1, command=self.st_open_image1, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_2 = customtkinter.CTkButton(self.frame1, command=self.st_open_image2, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_3 = customtkinter.CTkButton(self.frame1, command=self.st_open_image3, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_4 = customtkinter.CTkButton(self.frame1, command=self.st_open_image4, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_5 = customtkinter.CTkButton(self.frame1, command=self.st_open_image5, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_6 = customtkinter.CTkButton(self.frame1, command=self.st_open_image6, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_7 = customtkinter.CTkButton(self.frame1, command=self.st_open_image7, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_8 = customtkinter.CTkButton(self.frame1, command=self.st_open_image8, image=self.folder_button_icon, text="Open Image")
        self.st_sidebar_button_1.grid(row=1, column=0, padx=10, pady=self.st_spacing)
        self.st_sidebar_button_2.grid(row=2, column=0, padx=10, pady=self.st_spacing)
        self.st_sidebar_button_3.grid(row=3, column=0, padx=10, pady=self.st_spacing)
        self.st_sidebar_button_4.grid(row=4, column=0, padx=10, pady=self.st_spacing)
        self.st_sidebar_button_5.grid(row=5, column=0, padx=10, pady=self.st_spacing)
        self.st_sidebar_button_6.grid(row=6, column=0, padx=10, pady=self.st_spacing)
        self.st_sidebar_button_7.grid(row=7, column=0, padx=10, pady=self.st_spacing)
        self.st_sidebar_button_8.grid(row=8, column=0, padx=10, pady=self.st_spacing)

        # folder button
        self.st_sidebar_button_folder = customtkinter.CTkButton(self.frame1, command=self.st_open_folder, image=self.folder_button_icon, text="Open folder")
        self.st_sidebar_button_folder.grid(row=9, column=0, padx=10, pady=23)

        # console
        self.st_console = customtkinter.CTkTextbox(self.frame1, width=100, height=20, font=customtkinter.CTkFont(size=15, family="Consolas"))
        self.st_console.grid(row=10, column=0, columnspan=9, rowspan=1, sticky="ewsn", padx=10)

        # drop down menus
        self.st_output_type_dropdown = customtkinter.CTkOptionMenu(self.frame1, values=self.output_type_list, variable=self.st_output_type_var)
        self.st_output_type_dropdown.grid(row=11, column=0, padx=10, pady=(10, 10))
        self.st_type_dropdown = customtkinter.CTkOptionMenu(self.frame1, values=["Steganography x2", "Steganography x3", "Steganography x4", "Steganography x5", "Steganography x6", "Steganography x7", "Steganography x8"], variable=self.st_type_var, command=self.st_type_dropdown_event)
        self.st_type_dropdown.grid(row=12, column=0, padx=10, pady=10)
        self.st_action_type_dropdown = customtkinter.CTkOptionMenu(self.frame1, values=["Merge", "Unmerge"], variable=self.st_action_type_var, command=self.st_type_dropdown_event)
        self.st_action_type_dropdown.grid(row=13, column=0, padx=10, pady=10)

        # file name and folder entries
        self.st_output_name_ent = customtkinter.CTkEntry(self.frame1, placeholder_text="Output filename", textvariable=self.st_output_name_var)
        self.st_output_name_ent.grid(row=11, column=2, padx=10, pady=10, columnspan=1, sticky="ew")
        self.st_folder_checkbox = customtkinter.CTkCheckBox(self.frame1, text="", command=self.st_folder_checkbox_event, onvalue=True, offvalue=False)
        self.st_folder_checkbox.grid(row=11, column=4, padx=(0, 100), pady=0, sticky="w", columnspan=2)
        self.st_output_folder_ent = customtkinter.CTkEntry(self.frame1, placeholder_text="Output folder name", textvariable=self.st_output_folder_var)
        self.st_output_folder_ent.grid(row=11, column=5, padx=10, pady=10, columnspan=1, sticky="ew")

        # info markers
        self.stt_explanation = customtkinter.CTkButton(self.frame1, text="Show Explanation", command=self.st_explanation_event)
        self.stt_explanation.grid(row=0, column=3, padx=10, pady=10, sticky="w")

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
        self.st_start_button.grid(row=12, column=2, padx=10, pady=10, ipady=5, columnspan=5, rowspan=2, sticky="we")


        # ------------------------------------ Text - IM Steganography -------------------------------------------------

        self.frame2 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame2.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame2.grid_rowconfigure(5, weight=1)
        self.frame2.grid_columnconfigure(2, weight=1)

        # logo
        self.stt_logo_label = customtkinter.CTkLabel(self.frame2, text="Image - Text Steganography", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.stt_logo_label.grid(row=0, column=0, padx=10, pady=(20, 10), columnspan=3, sticky="w")

        # entries
        self.stt_ent1 = customtkinter.CTkEntry(self.frame2, placeholder_text="Input image path here", width=100, textvariable=self.stt_ent1_var)
        self.stt_ent1.grid(row=1, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")
        self.stt_ent2 = customtkinter.CTkEntry(self.frame2, placeholder_text="Output folder path here", width=100, textvariable=self.stt_ent2_var)
        self.stt_ent2.grid(row=3, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")
        self.stt_ent4 = customtkinter.CTkEntry(self.frame2, placeholder_text="Input text file path here", width=100, textvariable=self.stt_ent4_var)
        self.stt_ent4.grid(row=2, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")

        # buttons
        self.stt_sidebar_button_1 = customtkinter.CTkButton(self.frame2, command=self.stt_open_image, image=self.folder_button_icon, text="Open Image")
        self.stt_sidebar_button_1.grid(row=1, column=0, padx=10, pady=self.spacing)
        self.stt_sidebar_button_2 = customtkinter.CTkButton(self.frame2, command=self.stt_open_folder, image=self.folder_button_icon, text="Open folder")
        self.stt_sidebar_button_2.grid(row=3, column=0, padx=10, pady=self.spacing)
        self.stt_sidebar_button_4 = customtkinter.CTkButton(self.frame2, command=self.stt_open_text, image=self.folder_button_icon, text="Open text file")
        self.stt_sidebar_button_4.grid(row=2, column=0, padx=10, pady=self.spacing)

        # text entry
        self.stt_ent3 = customtkinter.CTkTextbox(self.frame2, width=100)
        self.stt_ent3.grid(row=4, column=1, padx=10, pady=10, columnspan=3, rowspan=3, sticky="ewsn")

        # console
        self.stt_console = customtkinter.CTkTextbox(self.frame2, width=100, height=20, font=customtkinter.CTkFont(size=15, family="Consolas"))
        self.stt_console.grid(row=9, column=2, columnspan=3, rowspan=2, sticky="wens", padx=10, pady=10)

        # file name entry
        self.stt_output_name_ent = customtkinter.CTkEntry(self.frame2, placeholder_text="Output filename", width=100, textvariable=self.stt_output_name_var)
        self.stt_output_name_ent.grid(row=8, column=0, padx=10, pady=10, columnspan=1, sticky="ew")
        self.stt_text_output_checkbox = customtkinter.CTkCheckBox(self.frame2, text="Output text to file", variable=self.stt_text_output_checkbox_var, state="disabled", command=self.stt_text_output_checkbox_event)
        self.stt_text_output_checkbox.grid(row=7, column=0, padx=10, pady=0, columnspan=1, sticky="w")
        self.stt_text_input_checkbox = customtkinter.CTkCheckBox(self.frame2, text="Input text from file", variable=self.stt_text_input_checkbox_var, command=self.stt_text_input_checkbox_event)
        self.stt_text_input_checkbox.grid(row=6, column=0, padx=10, pady=5, columnspan=1, sticky="w")

        # drop down menus
        self.stt_output_type_dropdown = customtkinter.CTkOptionMenu(self.frame2, values=self.output_type_list_lossless, variable=self.stt_output_type_var)
        self.stt_output_type_dropdown.grid(row=9, column=0, padx=10, pady=10)
        self.stt_type_dropdown = customtkinter.CTkOptionMenu(self.frame2, values=["Layered8", "Sequential8", "LayeredDynamic", "LayeredDynamic\nTransparent"], variable=self.stt_type_var, command=self.stt_type_dropdown_event)
        self.stt_type_dropdown.grid(row=10, column=0, padx=10, pady=10)
        self.stt_action_type_dropdown = customtkinter.CTkOptionMenu(self.frame2, values=["Encode", "Decode"], variable=self.stt_action_type_var, command=self.stt_action_type_dropdown_event)
        self.stt_action_type_dropdown.grid(row=11, column=0, padx=10, pady=10)
        self.stt_encoding_type_dropdown = customtkinter.CTkOptionMenu(self.frame2, values=["ASCII", "UNICODE"], variable=self.stt_encoding_type_var, command=self.stt_encoding_type_dropdown_event)
        self.stt_encoding_type_dropdown.grid(row=4, column=0, padx=10, pady=10)

        # info marker
        self.stt_info_marker_1 = customtkinter.CTkLabel(self.frame2, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.stt_info_marker_1.grid(row=9, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.stt_info_marker_2 = customtkinter.CTkLabel(self.frame2, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.stt_info_marker_2.grid(row=10, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.stt_info_marker_3 = customtkinter.CTkLabel(self.frame2, text="", image=self.info_marker_icon, width=30, height=20, bg_color="#1F6AA5")
        self.stt_info_marker_3.grid(row=11, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        CreateToolTip(self.stt_info_marker_1, "The output type is the file type of the output image.\nOnly Lossless image formats are supported for this program\n(others may not work because of compression of the data)\n\nDefault: 'PNG' - Lossless encoding for better quality when decoding.", height=90, width=400)
        CreateToolTip(self.stt_info_marker_2, "This is the folder you want to save the output to")
        CreateToolTip(self.stt_info_marker_3, "This is the type of output you want to get\n\nLayered - The program will encode the text into the image\nand save the output image in the output folder\n\nSequential - The program will encode the text into the image\nand save the output image in the output folder\n\nLayeredDynamic - The program will encode the text into the image\nand save the output image in the output folder")
        CreateToolTip(self.stt_output_name_ent, "Default: 'output' - The name of the output file\n\nNote: The file extension will be added automatically\nbased on the output type", height=75, width=300)
        CreateToolTip(self.stt_text_output_checkbox, "If checked, the program will output the text to a text file\nin the output folder with the output filename(UTF-8 encoding)\n\nDefault: 'False'", height=75, width=360)

        # start button
        self.stt_start_button = customtkinter.CTkButton(self.frame2, command=self.stt_start_button_event, text="Run Text Steganographer")
        self.stt_start_button.grid(row=11, column=2, padx=10, pady=10, ipady=5, columnspan=3, rowspan=2, sticky="we")


        # ------------------------------------ Text - IM Generator -----------------------------------------------------

        self.frame3 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame3.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame3.grid_rowconfigure(5, weight=1)
        self.frame3.grid_columnconfigure(2, weight=1)

        # logo
        self.tti_logo_label = customtkinter.CTkLabel(self.frame3, text="Text to Image Generator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.tti_logo_label.grid(row=0, column=0, padx=10, pady=(20, 10), columnspan=3, sticky="w")

        # entries
        self.tti_ent1 = customtkinter.CTkEntry(self.frame3, placeholder_text="Input text file path here", width=100, textvariable=self.tti_ent1_var)
        self.tti_ent1.grid(row=2, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")
        self.tti_ent2 = customtkinter.CTkEntry(self.frame3, placeholder_text="Input Image path here", width=100, textvariable=self.tti_ent2_var)
        self.tti_ent2.grid(row=3, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")
        self.tti_ent3 = customtkinter.CTkEntry(self.frame3, placeholder_text="Output folder path here", width=100, textvariable=self.tti_ent3_var)
        self.tti_ent3.grid(row=4, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")

        # buttons
        self.tti_sidebar_button_1 = customtkinter.CTkButton(self.frame3, command=self.tti_open_text, image=self.folder_button_icon, text="Open text file")
        self.tti_sidebar_button_1.grid(row=2, column=0, padx=10, pady=self.spacing)
        self.tti_sidebar_button_2 = customtkinter.CTkButton(self.frame3, command=self.tti_open_image, image=self.folder_button_icon, text="Open image")
        self.tti_sidebar_button_2.grid(row=3, column=0, padx=10, pady=self.spacing)
        self.tti_sidebar_button_3 = customtkinter.CTkButton(self.frame3, command=self.tti_open_folder, image=self.folder_button_icon, text="Open folder")
        self.tti_sidebar_button_3.grid(row=4, column=0, padx=10, pady=self.spacing)

        # text entry
        self.tti_ent4 = customtkinter.CTkTextbox(self.frame3, width=100)
        self.tti_ent4.grid(row=5, column=1, padx=10, pady=10, columnspan=3, rowspan=4, sticky="ewsn")

        # console
        self.tti_console = customtkinter.CTkTextbox(self.frame3, width=100, height=20, font=customtkinter.CTkFont(size=15, family="Consolas"))
        self.tti_console.grid(row=9, column=2, columnspan=3, rowspan=2, sticky="wens", padx=10, pady=10)

        # file name entry
        self.tti_output_name_ent = customtkinter.CTkEntry(self.frame3, placeholder_text="Output filename", width=100, textvariable=self.tti_output_name_var)
        self.tti_output_name_ent.grid(row=8, column=0, padx=10, pady=10, columnspan=1, sticky="ew")
        self.tti_text_output_checkbox = customtkinter.CTkCheckBox(self.frame3, text="Output text to file", variable=self.tti_text_output_checkbox_var, state="disabled", command=self.tti_text_output_checkbox_event)
        self.tti_text_output_checkbox.grid(row=7, column=0, padx=10, pady=0, columnspan=1, sticky="w")
        self.tti_text_input_checkbox = customtkinter.CTkCheckBox(self.frame3, text="Input text from file", variable=self.tti_text_input_checkbox_var, command=self.tti_text_input_checkbox_event)
        self.tti_text_input_checkbox.grid(row=6, column=0, padx=10, pady=5, columnspan=1, sticky="w")

        # drop down menus
        self.tti_output_type_dropdown = customtkinter.CTkOptionMenu(self.frame3, values=self.output_type_list_lossless, variable=self.tti_output_type_var)
        self.tti_output_type_dropdown.grid(row=9, column=0, padx=10, pady=10)
        self.tti_color_dropdown = customtkinter.CTkOptionMenu(self.frame3, values=["RGB", "RGBA", "Mono"], variable=self.tti_color_var)
        self.tti_color_dropdown.grid(row=10, column=0, padx=10, pady=10, columnspan=1, sticky="w")
        self.tti_action_type_dropdown = customtkinter.CTkOptionMenu(self.frame3, values=["Encode", "Decode"],variable=self.tti_action_type_var,command=self.tti_action_type_dropdown_event)
        self.tti_action_type_dropdown.grid(row=11, column=0, padx=10, pady=10)

        # info marker
        self.tti_info_marker_1 = customtkinter.CTkLabel(self.frame3, text="", image=self.info_marker_icon, width=30,height=20, bg_color="#1F6AA5")
        self.tti_info_marker_1.grid(row=9, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.tti_info_marker_2 = customtkinter.CTkLabel(self.frame3, text="", image=self.info_marker_icon, width=30,height=20, bg_color="#1F6AA5")
        self.tti_info_marker_2.grid(row=10, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        self.tti_info_marker_3 = customtkinter.CTkLabel(self.frame3, text="", image=self.info_marker_icon, width=30,height=20, bg_color="#1F6AA5")
        self.tti_info_marker_3.grid(row=11, column=1, padx=0, pady=0, ipadx=2, ipady=5)
        CreateToolTip(self.tti_info_marker_1,"The output type is the file type of the output image.\nOnly Lossless image formats are supported for this program\n(others may not work because of compression of the data)\n\nDefault: 'PNG' - Lossless encoding for better quality when decoding.",height=90, width=400)
        CreateToolTip(self.tti_info_marker_2,"This determines the color mode of the output image.\n\nDefault: 'RGB' - 3 channels of color\n'RGBA' - 4 channels of color\n'Mono' - 1 channel of color",height=90, width=310)
        CreateToolTip(self.tti_info_marker_3,"This is the type of output you want to get\n\nLayered - The program will encode the text into the image\nand save the output image in the output folder\n\nSequential - The program will encode the text into the image\nand save the output image in the output folder\n\nLayeredDynamic - The program will encode the text into the image\nand save the output image in the output folder")
        CreateToolTip(self.tti_output_name_ent,"Default: 'output' - The name of the output file\n\nNote: The file extension will be added automatically\nbased on the output type",height=75, width=300)
        CreateToolTip(self.tti_text_output_checkbox,"If checked, the program will output the text to a text file\nin the output folder with the output filename(UTF-8 encoding)\n\nDefault: 'False'",height=75, width=360)

        # start button
        self.tti_start_button = customtkinter.CTkButton(self.frame3, command=self.tti_start_button_event, text="Run Text Steganographer")
        self.tti_start_button.grid(row=11, column=2, padx=10, pady=10, ipady=5, columnspan=3, rowspan=2, sticky="we")

        # ------------------------------------ IM Extension Transform --------------------------------------------------

        self.frame4 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        # self.frame4.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame4.grid_rowconfigure(4, weight=1)
        self.frame4.grid_columnconfigure(0, weight=1)

        # logo
        self.iet_logo_label = customtkinter.CTkLabel(self.frame4, text="Image Extension Transform", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.iet_logo_label.grid(row=1, column=0, padx=10, pady=(20, 10), columnspan=3, sticky="w")

        # entries
        self.iet_ent1 = customtkinter.CTkEntry(self.frame4, placeholder_text="Input Image file path here", width=100, textvariable=self.iet_ent1_var)
        self.iet_ent1.grid(row=2, column=0, padx=10, pady=self.spacing, ipady=10  ,columnspan=3, sticky="ew")

        # buttons
        self.iet_sidebar_button_1 = customtkinter.CTkButton(self.frame4, command=self.iet_open_image, image=self.folder_button_icon, text="Open image", font=customtkinter.CTkFont(size=20))
        self.iet_sidebar_button_1.grid(row=3, column=0, padx=10, pady=30, ipady=15 ,columnspan=3, sticky="ew")

        # drop down menus
        self.iet_output_type_dropdown = customtkinter.CTkOptionMenu(self.frame4, values=self.output_type_list, variable=self.iet_output_type_var, height=50, width=400, font=customtkinter.CTkFont(size=17))
        self.iet_output_type_dropdown.grid(row=4, column=0, padx=10, pady=10)

        # console
        self.iet_console = customtkinter.CTkTextbox(self.frame4, width=100, height=10, state="disabled", font=customtkinter.CTkFont(size=15, family="Consolas"))
        self.iet_console.grid(row=5, column=0, padx=10, pady=10, ipady=10, columnspan=3, sticky="ew")

        # start button
        self.iet_start_button = customtkinter.CTkButton(self.frame4, command=self.iet_start_button_event, text="Transform", font=customtkinter.CTkFont(size=20))
        self.iet_start_button.grid(row=6, column=0, padx=10, pady=50, ipady=10, columnspan=3, rowspan=2, sticky="we")

        # --------------------------------------- Metadata Info --------------------------------------------------------

        self.frame5 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame5.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame5.grid_rowconfigure(4, weight=1)
        self.frame5.grid_columnconfigure(1, weight=1)

        # logo
        self.mi_logo_label = customtkinter.CTkLabel(self.frame5, text="Get Metadata", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.mi_logo_label.grid(row=1, column=0, padx=10, pady=(20, 10), columnspan=3, sticky="w")

        # entries
        self.mi_ent1 = customtkinter.CTkEntry(self.frame5, placeholder_text="File path", width=100, textvariable=self.mi_ent1_var)
        self.mi_ent1.grid(row=2, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")

        # buttons
        self.mi_sidebar_button_1 = customtkinter.CTkButton(self.frame5, command=self.mi_open_image, image=self.folder_button_icon, text="Open file")
        self.mi_sidebar_button_1.grid(row=2, column=0, padx=10, pady=5)

        # console
        self.mi_console = customtkinter.CTkTextbox(self.frame5, width=100, height=10, state="disabled", font=customtkinter.CTkFont(size=15, family="Consolas"))
        self.mi_console.grid(row=4, column=0, padx=10, pady=10, ipady=10, columnspan=3, sticky="ewns")

        # --------------------------------------- Youtube Downloader ---------------------------------------------------

        self.frame6 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame6.grid(row=0, column=1, rowspan=4, sticky="snew")
        self.frame6.grid_rowconfigure(9, weight=1)
        self.frame6.grid_columnconfigure(1, weight=1)

        # logo
        self.yt_logo_label = customtkinter.CTkLabel(self.frame6, text="Youtube Downloader",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.yt_logo_label.grid(row=1, column=0, padx=10, pady=(20, 10), columnspan=3, sticky="w")

        # entries
        self.yt_ent1 = customtkinter.CTkEntry(self.frame6, placeholder_text="Youtube link", width=100, font=customtkinter.CTkFont(size=15), textvariable=self.yt_ent1_var)
        self.yt_ent1.grid(row=2, column=0, padx=10, pady=self.spacing, ipady=5, columnspan=3 ,sticky="ew")
        self.yt_ent2 = customtkinter.CTkEntry(self.frame6, placeholder_text="Folder path", width=100, textvariable=self.yt_ent2_var)
        self.yt_ent2.grid(row=3, column=1, padx=10, pady=self.spacing, columnspan=3, sticky="ew")

        # buttons
        self.yt_sidebar_button_2 = customtkinter.CTkButton(self.frame6, command=self.yt_open_folder, image=self.folder_button_icon, text="Open folder")
        self.yt_sidebar_button_2.grid(row=3, column=0, padx=10, pady=(5, 0))
        self.yt_copy_button = customtkinter.CTkButton(self.frame6, image=self.copy_icon, width=10, command=self.to_clipboard)
        self.yt_copy_button.grid(row=4, column=0, padx=10, pady=(0, 5), sticky='w', ipadx=2)

        # console
        self.yt_command_console = customtkinter.CTkTextbox(self.frame6, width=100, height=10, state="disabled", font=customtkinter.CTkFont(size=15, family="Consolas"))
        self.yt_command_console.grid(row=4, column=0, padx=(45, 10), pady=(0, 5), columnspan=3, sticky='we')
        self.yt_console = customtkinter.CTkTextbox(self.frame6, width=100, height=10, font=customtkinter.CTkFont(size=10, family="Consolas"))
        #self.yt_console = customtkinter.CTkLabel(self.frame6, width=100, height=10, font=customtkinter.CTkFont(size=10), anchor="nw", justify="left", text="")
        self.yt_console.grid(row=5, column=1, columnspan=3, rowspan=6, sticky="ewsn", padx=10)

        # tab view
        self.yt_tab_view = customtkinter.CTkTabview(self.frame6, width=100, height=10)
        self.yt_tab_view.grid(row=5, column=0, padx=10, pady=(0, 10), columnspan=1, rowspan=15 , sticky="ewns")
        self.yt_av = self.yt_tab_view.add("AudioVideo")
        self.yt_sub = self.yt_tab_view.add("Subtitles")

        # audio video tab
        self.yt_sidebar_button_3 = customtkinter.CTkButton(self.yt_av, command=self.yt_get_res_event, text="Get Resolutions")
        self.yt_sidebar_button_3.grid(row=0, column=0, padx=10, pady=5)

        self.yt_checkbox_video = customtkinter.CTkCheckBox(self.yt_av, text="Video", variable=self.yt_checkbox_video_var, command=self.yt_toggle_video, width=60)
        self.yt_checkbox_video.grid(row=1, column=0, padx=10, pady=(self.tab_spacing, 10), sticky="w")
        self.yt_checkbox_audio = customtkinter.CTkCheckBox(self.yt_av, text="Audio", variable=self.yt_checkbox_audio_var, command=self.yt_toggle_audio, width=60)
        self.yt_checkbox_audio.grid(row=1, column=0, padx=10, pady=(self.tab_spacing, 10), sticky="e")

        self.yt_dropdown1 = customtkinter.CTkOptionMenu(self.yt_av, values=self.resolutions_list, variable=self.yt_resolution_var, command=self.yt_update_event)
        self.yt_dropdown1.grid(row=2, column=0, padx=10, pady=self.tab_spacing)
        self.yt_dropdown5 = customtkinter.CTkOptionMenu(self.yt_av, values=self.yt_ext, variable=self.yt_video_ext_var, command=self.yt_update_event)
        self.yt_dropdown5.grid(row=3, column=0, padx=10, pady=self.tab_spacing)
        self.yt_dropdown6 = customtkinter.CTkOptionMenu(self.yt_av, values=self.yt_codec, variable=self.yt_video_codec_var, command=self.yt_update_event)
        self.yt_dropdown6.grid(row=4, column=0, padx=10, pady=self.tab_spacing)
        self.yt_dropdown7 = customtkinter.CTkOptionMenu(self.yt_av, values=self.yt_ext_audio, variable=self.yt_audio_ext_var, command=self.yt_update_event)
        self.yt_dropdown7.grid(row=6, column=0, padx=10, pady=self.tab_spacing)
        self.yt_dropdown8 = customtkinter.CTkOptionMenu(self.yt_av, values=self.yt_codec_audio, variable=self.yt_audio_codec_var, command=self.yt_update_event)
        self.yt_dropdown8.grid(row=7, column=0, padx=10, pady=self.tab_spacing)

        self.yt_ent3 = customtkinter.CTkEntry(self.yt_av, placeholder_text="Format code", width=10, textvariable=self.yt_ent3_var)
        self.yt_ent3.grid(row=8, column=0, padx=10, pady=self.spacing, sticky="ew")

        self.yt_checkbox1 = customtkinter.CTkCheckBox(self.yt_av, text="Download playlist", variable=self.yt_playlist_var, command=self.yt_update_event)
        self.yt_checkbox1.grid(row=9, column=0, padx=10, pady=self.spacing, sticky="w")
        self.yt_checkbox3 = customtkinter.CTkCheckBox(self.yt_av, variable=self.yt_checkbox3_var, text='', width=10, command=self.yt_update_event)
        self.yt_checkbox3.grid(row=5, column=0, padx=10, pady=self.spacing, sticky="w")
        self.yt_checkbox4 = customtkinter.CTkCheckBox(self.yt_av, variable=self.yt_checkbox4_var, text='', width=10, command=self.yt_update_event)
        self.yt_checkbox4.grid(row=5, column=0, padx=(65,0), pady=self.spacing, sticky="w")
        self.yt_checkbox5 = customtkinter.CTkCheckBox(self.yt_av, variable=self.yt_checkbox5_var, text='', width=10, command=self.yt_update_event)
        self.yt_checkbox5.grid(row=5, column=0, padx=(120, 0), pady=self.spacing, sticky="w")

        CreateToolTip(self.yt_checkbox3, "Embed metadata in video file", width=180, height=20)
        CreateToolTip(self.yt_checkbox4, "Embed default subtitles in video file", width=220, height=20)
        CreateToolTip(self.yt_checkbox5, "Embed thumbnail in video file", width=180, height=20)


        # subtitles tab
        self.yt_sidebar_button_4 = customtkinter.CTkButton(self.yt_sub, command=self.yt_get_sub_event, text="Get Subtitles")
        self.yt_sidebar_button_4.grid(row=0, column=0, padx=10, pady=5)

        self.yt_dropdown3 = customtkinter.CTkOptionMenu(self.yt_sub, values=self.sub_lang_list, variable=self.yt_sub_lang_var)
        self.yt_dropdown3.grid(row=1, column=0, padx=10, pady=5)
        self.yt_dropdown4 = customtkinter.CTkOptionMenu(self.yt_sub, values=self.sub_ext_list, variable=self.yt_sub_ext_var)
        self.yt_dropdown4.grid(row=2, column=0, padx=10, pady=5)

        self.yt_ent4 = customtkinter.CTkEntry(self.yt_sub, placeholder_text="Language code", width=10, textvariable=self.yt_ent4_var)
        self.yt_ent4.grid(row=3, column=0, padx=10, pady=self.spacing, sticky="ew")

        self.yt_checkbox2 = customtkinter.CTkCheckBox(self.yt_sub, text="Automatic subtitles", variable=self.yt_sub_auto_var)
        self.yt_checkbox2.grid(row=4, column=0, padx=10, pady=self.spacing, sticky="w")

        # start button
        self.yt_start_button = customtkinter.CTkButton(self.frame6, command=self.yt_start_button_event, text="Download", font=customtkinter.CTkFont(size=15))
        self.yt_start_button.grid(row=10, column=1, padx=10, pady=10, ipady=10, columnspan=3, sticky="we")
        # self.yt_sub_start_button = customtkinter.CTkButton(self.frame6, command=self.yt_sub_start_button_event, text="Download Subtitles", font=customtkinter.CTkFont(size=15))
        # self.yt_sub_start_button.grid(row=16, column=0, padx=10, pady=10, ipady=10, sticky="we")


        # # just for testing --- delte after
        # self.yt_ent1_var.set("https://www.youtube.com/watch?v=QH2-TGUlwu4")
        # self.yt_ent2_var.set("C:/Users/Tomer27cz/Desktop/Files/CODING/Python Projects/Image Editors/downloads")
        # self.yt_checkbox_audio_var.set(0)

        #-------------------------------------------------- Text Encryptor ---------------------------------------------

        self.frame7 = customtkinter.CTkFrame(self, fg_color=("#ebebeb", "#242424"))
        self.frame7.grid(row=0, column=1, rowspan=4, sticky="snew")
        # self.frame7.grid_rowconfigure(5, weight=1)
        self.frame7.grid_columnconfigure(2, weight=1)

        self.te_dropdown1 = customtkinter.CTkOptionMenu(self.frame7, values=self.text_encryption_list, variable=self.te_dropdown1_var)
        self.te_dropdown1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.te_dropdown2 = customtkinter.CTkOptionMenu(self.frame7, values=self.text_encryption_list, variable=self.te_dropdown2_var)
        self.te_dropdown2.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.te_console = customtkinter.CTkTextbox(self.frame7, width=50, height=20, font=customtkinter.CTkFont(size=10, family="Consolas"))
        self.te_console.grid(row=0, column=1, padx=10, pady=10, columnspan=3, sticky="nsew")
        self.te_console2 = customtkinter.CTkTextbox(self.frame7, width=50, height=20, font=customtkinter.CTkFont(size=10, family="Consolas"))
        self.te_console2.grid(row=5, column=1, padx=10, pady=10, columnspan=3, sticky="nsew")

        # add frames to notebook

        self.my_notebook.add(self.frame0, text="Tab 1")
        self.my_notebook.add(self.frame1, text="Tab 2")
        self.my_notebook.add(self.frame2, text="Tab 3")
        self.my_notebook.add(self.frame3, text="Tab 4")
        self.my_notebook.add(self.frame4, text="Tab 5")
        self.my_notebook.add(self.frame5, text="Tab 6")
        self.my_notebook.add(self.frame6, text="Tab 7")
        self.my_notebook.add(self.frame7, text="Tab 8")

        self.my_notebook.add(self.frame69, text="Tab 69", )

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
        self.stt_text_input_checkbox_event()
        # ------------------------------------ Text - IM Generator -----------------------------------------------------
        self.tti_console.configure(state="disabled")
        self.tti_text_input_checkbox_event()
        self.tti_action_type_dropdown_event('Encode')
        #------------------------------------------ Other --------------------------------------------------------------
        self.appearance_mode_optionemenu.set("System")
        self.my_notebook.select(6)


    # ------------------------------------ FUNCTIONS -------------------------------------------------------------------


    def change_appearance_mode_event(self, new_appearance_mode: str): # NOQA
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Sidebar functions ------------------------------------------------------------------------------------------------

    def sidebar_button_event_frame_0(self): self.my_notebook.select(self.frame0)
    def sidebar_button_event_frame_1(self): self.my_notebook.select(self.frame1)
    def sidebar_button_event_frame_2(self): self.my_notebook.select(self.frame2)
    def sidebar_button_event_frame_3(self): self.my_notebook.select(self.frame3)
    def sidebar_button_event_frame_4(self): self.my_notebook.select(self.frame4)
    def sidebar_button_event_frame_5(self): self.my_notebook.select(self.frame5)
    def sidebar_button_event_frame_6(self): self.my_notebook.select(self.frame6)
    def sidebar_button_event_frame_7(self): self.my_notebook.select(self.frame7)

    def sidebar_button_event_frame_about(self): self.my_notebook.select(self.frame69)

    # Image Scrambler functions ----------------------------------------------------------------------------------------

    def sc_open_folder(self):
        self.sc_ent2.delete(0, "end")
        self.sc_ent2_var.set(filedialog.askdirectory(initialdir=self.initial_browser_dir, title="Select output folder"))
    def sc_open_image(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        with Image.open(filename) as image:
            text = f"Image size: {image.size}\nImage mode: {image.mode}\nImage format: {image.format}\nPossible sizes: {_calc_size(image.size[0], image.size[1])}"
        CreateToolTip(self.sc_ent1, text, height=100, width=200)
        self.sc_ent1.delete(0, "end")
        self.sc_ent1_var.set(filename)

        CreateToolTip(self.sc_ent1, )

    def sc_seed_loop_checkbox_event(self):
        self.sc_to_seed_ent.configure(state="normal" if self.sc_loop_checkbox1.get() else "disabled",
                                   placeholder_text="To" if self.sc_loop_checkbox1.get() else "",
                                   border_width=2 if self.sc_loop_checkbox1.get() else 0)
        self.sc_from_seed_ent.configure(placeholder_text="From" if self.sc_loop_checkbox1.get() else "Seed")
        self.sc_output_folder_ent.configure(
            state="normal" if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else "disabled",
            border_width=2 if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else 0,
            placeholder_text="Output Folder Name" if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else "")
    def sc_size_loop_checkbox_event(self):
        self.sc_to_size_ent.configure(state="normal" if self.sc_loop_checkbox2.get() else "disabled",
                                   placeholder_text="To" if self.sc_loop_checkbox2.get() else "",
                                   border_width=2 if self.sc_loop_checkbox1.get() else 0)
        self.sc_from_size_ent.configure(placeholder_text="From" if self.sc_loop_checkbox1.get() else "Size")
        self.sc_output_folder_ent.configure(
            state="normal" if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else "disabled",
            border_width=2 if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else 0,
            placeholder_text="Output Folder Name" if self.sc_loop_checkbox2.get() or self.sc_loop_checkbox1.get() else "")

    def sc_start_button_event(self):
        seed = self.sc_from_seed_ent.get()
        size = self.sc_from_size_ent.get()
        image_path = self.sc_ent1_var.get()
        folder_path = self.sc_ent2_var.get()
        action_type = self.sc_action_type_var.get()
        output_type = self.sc_output_type_var.get()
        seed_loop = self.sc_loop_checkbox1.get()
        size_loop = self.sc_loop_checkbox2.get()
        seed_to = self.sc_to_seed_ent.get()
        size_to = self.sc_to_size_ent.get()
        file_name = self.sc_output_name_var.get()
        folder_name = self.sc_output_folder_var.get()

        if not image_path or not folder_path:
            self.print_to_sc_console("Please select an image and a folder.", error=True)
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
            folder_path, message = make_folder(folder_path + folder_name)
            self.print_to_sc_console(message)
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
                self.print_to_sc_console("Please enter a valid size. (Integer)", error=True)
                return

            # configure start button
            self.sc_start_button.configure(state="disabled")
            self.sc_start_button.configure(text="Working...")

            # print info to console
            self.print_to_sc_console("-" * 72 + "START" + "-" * 73)
            self.print_to_sc_console(f"Seed: {seed} | Size: {size} | Action: {action_type} | Output: {output_type} | Output filename: {file_name}_({seed}_{size}) |Image: {image_path.split('/')[-1]}")
            self.print_to_sc_console(f"Seed loop: False | Size loop: False")
            self.print_to_sc_console("Folder: " + folder_path + "\n")

            # start
            try:
                operation_type = 1 if action_type == 'Encode' else 0
                new_scramble_algorithm(operation_type=operation_type, output_type=output_type, image_path=image_path, folder_path=folder_path, output_name=f"{file_name}_({seed}_{size})", seed=seed, size=size)
            except Exception as e:
                self.print_to_sc_console(f"Error: {e}") # print output to console

            # configure start button
            self.sc_start_button.configure(state="normal")
            self.sc_start_button.configure(text="Run Image Scramble")

        else:
            if seed_loop:
                if seed == "" or seed_to == "":
                    return self.print_to_sc_console("Please enter a valid seed range.", error=True)
                try:
                    seed = int(seed)
                    seed_to = int(seed_to)
                except ValueError:
                    self.print_to_sc_console("Please enter a valid seed range. (Integer)", error=True)
                    return

                if seed > seed_to: return self.print_to_sc_console("Please enter a valid seed range. (From < To)", error=True)

                seed_range = list(range(seed, seed_to+1))
            else:
                if seed == "": seed = 0
                seed_range = [seed]

            if size_loop:
                if size == "" or size_to == "":
                    return self.print_to_sc_console("Please enter a valid size range.", error=True)
                try:
                    size = int(size)
                    size_to = int(size_to)
                except ValueError:
                    self.print_to_sc_console("Please enter a valid size range. (Integer)", error=True)
                    return

                if size > size_to: return self.print_to_sc_console("Please enter a valid size range. (From < To)", error=True)

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
        self.st_ent1_var.set(filename)
        CreateToolTip(self.st_ent1, filename=filename)
    def st_open_image2(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent2.delete(0, "end")
        self.st_ent2_var.set(filename)
        CreateToolTip(self.st_ent2, filename=filename)
    def st_open_image3(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent3.delete(0, "end")
        self.st_ent3_var.set(filename)
        CreateToolTip(self.st_ent3, filename=filename)
    def st_open_image4(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent4.delete(0, "end")
        self.st_ent4_var.set(filename)
        CreateToolTip(self.st_ent4, filename=filename)
    def st_open_image5(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent5.delete(0, "end")
        self.st_ent5_var.set(filename)
        CreateToolTip(self.st_ent5, filename=filename)
    def st_open_image6(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent6.delete(0, "end")
        self.st_ent6_var.set(filename)
        CreateToolTip(self.st_ent6, filename=filename)
    def st_open_image7(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent7.delete(0, "end")
        self.st_ent7_var.set(filename)
        CreateToolTip(self.st_ent7, filename=filename)
    def st_open_image8(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.st_ent8.delete(0, "end")
        self.st_ent8_var.set(filename)
        CreateToolTip(self.st_ent8, filename=filename)

    def st_open_folder(self):
        self.st_ent_folder.delete(0, "end")
        self.st_ent_folder_var.set(filedialog.askdirectory(initialdir=self.initial_browser_dir, title=self.title_open))

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
        with open(self.steganography_explanation, "r") as f:
            html_label = HTMLScrolledText(window, html=f.read(), )
        html_label.pack(fill="both", expand=True)
        html_label.fit_height()

    def st_start_button_event(self):
        ent1 = self.st_ent1_var.get()
        ent2 = self.st_ent2_var.get()
        ent3 = self.st_ent3_var.get()
        ent4 = self.st_ent4_var.get()
        ent5 = self.st_ent5_var.get()
        ent6 = self.st_ent6_var.get()
        ent7 = self.st_ent7_var.get()
        ent8 = self.st_ent8_var.get()
        ent_folder = self.st_ent_folder_var.get()

        output_type_dropdown = self.st_output_type_dropdown.get() # "PNG" or "JPG"
        type_dropdown = self.st_type_dropdown.get() # steganography type
        action_type_dropdown = self.st_action_type_dropdown.get() # "Merge" or "Unmerge"
        folder_checkbox = self.st_folder_checkbox.get() # 0 or 1
        output_folder_ent = self.st_output_folder_var.get() # output folder
        output_name_ent = self.st_output_name_var.get() # output name

        image = ""
        images = []

        if output_name_ent == "": output_name_ent = "output"

        if folder_checkbox == 1 and output_folder_ent == "": output_folder_ent = "SteganographyOutput"

        if not ent_folder: return self.print_to_st_console("Please select an output folder", error=True)

        if ent_folder[-1] != "/" or ent_folder[-1] != "\\":
            if "\\" in ent_folder: ent_folder += "\\"
            else: ent_folder += "/"

        # Get path

        path = f"{ent_folder}{output_name_ent}.{output_type_dropdown.lower()}"

        if folder_checkbox == 1:
            output_folder_path, message = make_folder(ent_folder + output_folder_ent)
            self.print_to_st_console(message)
            path = f"{output_folder_path}/{output_name_ent}.{output_type_dropdown.lower()}"


        # Warning message

        if action_type_dropdown == "Unmerge":
            if not ent1:
                return self.print_to_st_console("Image 1 must be filled in", error=True)

        if action_type_dropdown == "Merge":
            if type_dropdown == "Steganography x2" and (not ent1 or not ent2):
                return self.print_to_st_console("Image 1 and 2 must be filled in", error=True)
            elif type_dropdown == "Steganography x3" and (not ent1 or not ent2 or not ent3):
                return self.print_to_st_console("Image 1, 2 and 3 must be filled in", error=True)
            elif type_dropdown == "Steganography x4" and (not ent1 or not ent2 or not ent3 or not ent4):
                return self.print_to_st_console("Image 1, 2, 3 and 4 must be filled in", error=True)
            elif type_dropdown == "Steganography x5" and (not ent1 or not ent2 or not ent3 or not ent4 or not ent5):
                return self.print_to_st_console("Image 1, 2, 3, 4 and 5 must be filled in", error=True)
            elif type_dropdown == "Steganography x6" and (not ent1 or not ent2 or not ent3 or not ent4 or not ent5 or not ent6):
                return self.print_to_st_console("Image 1, 2, 3, 4, 5 and 6 must be filled in", error=True)
            elif type_dropdown == "Steganography x7" and (not ent1 or not ent2 or not ent3 or not ent4 or not ent5 or not ent6 or not ent7):
                return self.print_to_st_console("Image 1, 2, 3, 4, 5, 6 and 7 must be filled in", error=True)
            elif type_dropdown == "Steganography x8" and (not ent1 or not ent2 or not ent3 or not ent4 or not ent5 or not ent6 or not ent7 or not ent8):
                return self.print_to_st_console("Image 1, 2, 3, 4, 5, 6, 7 and 8 must be filled in", error=True)

        # Merge / Unmerge

        if action_type_dropdown == "Merge":
            im_list = []
            if type_dropdown == "Steganography x2":
                for i in range(2): im_list.append(Image.open(ent1 if i == 0 else ent2))
                try: image = Steganography().merge(im_list)
                except Exception as e: return self.print_to_st_console(f"Error: {e}", error=True)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x3":
                for i in range(3): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3))
                try: image = Steganography3().merge(im_list)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x4":
                for i in range(4): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4))
                try: image = Steganography4().merge(im_list)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x5":
                for i in range(5): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4 if i == 3 else ent5))
                try: image = Steganography5().merge(im_list)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x6":
                for i in range(6): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4 if i == 3 else ent5 if i == 4 else ent6))
                try: image = Steganography6().merge(im_list)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x7":
                for i in range(7): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4 if i == 3 else ent5 if i == 4 else ent6 if i == 5 else ent7))
                try: image = Steganography7().merge(im_list)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
                for im in im_list: im.close()
            elif type_dropdown == "Steganography x8":
                for i in range(8): im_list.append(Image.open(ent1 if i == 0 else ent2 if i == 1 else ent3 if i == 2 else ent4 if i == 3 else ent5 if i == 4 else ent6 if i == 5 else ent7 if i == 6 else ent8))
                try: image = Steganography8().merge(im_list)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
                for im in im_list: im.close()

            for im in im_list:
                im.close()

        if action_type_dropdown == "Unmerge":
            im = Image.open(ent1)
            if type_dropdown == "Steganography x2":
                try: images = Steganography().unmerge(im)
                except Exception as e: return self.print_to_st_console(f"Error: {e}", error=True)
            elif type_dropdown == "Steganography x3":
                try: images = Steganography3().unmerge(im)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
            elif type_dropdown == "Steganography x4":
                try: images = Steganography4().unmerge(im)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
            elif type_dropdown == "Steganography x5":
                try: images = Steganography5().unmerge(im)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
            elif type_dropdown == "Steganography x6":
                try: images = Steganography6().unmerge(im)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
            elif type_dropdown == "Steganography x7":
                try: images = Steganography7().unmerge(im)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
            elif type_dropdown == "Steganography x8":
                try: images = Steganography8().unmerge(im)
                except Exception as e:return self.print_to_st_console(f"Error: {e}", error=True)
            im.close()

        # Save image

        if action_type_dropdown == "Merge":
            try: image.save(f"{path}.{output_type_dropdown.lower()}")
            except Exception as e: return self.print_to_st_console(f"Error saving image: {e}", error=True)
        else:
            for i, im in enumerate(images):
                try: im.save(f"{path}_{i + 1}.{output_type_dropdown.lower()}")
                except Exception as e: return self.print_to_st_console(f"Error saving image: {e}", error=True)

        self.print_to_st_console(f"Saved to: '{path}'")


    # Text Steganography Functions -------------------------------------------------------------------------------------

    def stt_open_folder(self):
        self.stt_ent2.delete(0, "end")
        self.stt_ent2_var.set(filedialog.askdirectory(initialdir=self.initial_browser_dir, title="Select output folder"))
    def stt_open_image(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.stt_ent1.delete(0, "end")
        self.stt_ent1_var.set(filename)
        CreateToolTip(self.stt_ent1, filename=filename)
    def stt_open_text(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title="Select text file", filetypes=[("text files", ["*.txt"])])
        self.stt_ent4.delete(0, "end")
        self.stt_ent4_var.set(filename)

    def stt_action_type_dropdown_event(self, new_action_type: str):
        if new_action_type == "Encode":
            # ent2
            self.stt_ent2.configure(state="normal", border_width=2)
            self.stt_sidebar_button_2.configure(state="normal")
            # output type dropdown
            if self.stt_type_dropdown.get() == "LayeredDynamicTransparent":
                self.stt_output_type_dropdown.configure(state="disabled")
            else:
                self.stt_output_type_dropdown.configure(state="normal")
            # output text checkbox
            self.stt_text_output_checkbox.configure(state="disabled")
            self.stt_text_output_checkbox.deselect()
            self.stt_text_output_checkbox_event()
            # output name ent
            self.stt_output_name_ent.configure(state="normal", border_width=2)
            # output text checkbox
            self.stt_text_input_checkbox.configure(state="normal")
            self.stt_text_input_checkbox_event()

        if new_action_type == "Decode":
            # ent2
            self.stt_ent2.configure(state="disabled", border_width=0)
            self.stt_sidebar_button_2.configure(state="disabled")
            # output type dropdown
            self.stt_output_type_dropdown.configure(state="disabled")
            # output text checkbox
            self.stt_text_output_checkbox.configure(state="normal")
            self.stt_text_output_checkbox_event()
            # output name ent
            self.stt_output_name_ent.configure(state="disabled", border_width=0)
            # input text checkbox
            self.stt_text_input_checkbox.configure(state="disabled")
            self.stt_text_input_checkbox.deselect()
            self.stt_text_input_checkbox_event()
    def stt_encoding_type_dropdown_event(self, new_type: str):
        if new_type == "UNICODE":
            self.stt_type_dropdown.configure(values=["LayeredDynamic", "LayeredDynamic\nTransparent"])
            self.stt_type_dropdown.set("LayeredDynamic")
        if new_type == "ASCII":
            self.stt_type_dropdown.configure(state="normal", values=["Layered8", "Sequential8", "LayeredDynamic", "LayeredDynamic\nTransparent"])
    def stt_type_dropdown_event(self, new_type: str):
        if new_type == "LayeredDynamic\nTransparent":
            self.stt_output_type_dropdown.set("PNG")
            self.stt_output_type_dropdown.configure(state="disabled")
        else:
            self.stt_output_type_dropdown.configure(state="normal")

    def stt_text_output_checkbox_event(self):
        if self.stt_text_output_checkbox.get():
            self.stt_output_name_ent.configure(state="normal", border_width=2)
            self.stt_output_type_dropdown.set("TXT")
        else:
            self.stt_output_name_ent.configure(state="disabled", border_width=0)
            self.stt_output_type_dropdown.set("PNG")
    def stt_text_input_checkbox_event(self):
        if self.stt_text_input_checkbox.get():
            self.stt_ent4.configure(state="normal", border_width=2)
            self.stt_sidebar_button_4.configure(state="normal")
        else:
            self.stt_ent4.configure(state="disabled", border_width=0)
            self.stt_sidebar_button_4.configure(state="disabled")

    def stt_start_button_event(self):
        start_time = time()
        ent1 = self.stt_ent1_var.get()
        ent2 = self.stt_ent2_var.get()
        ent3 = self.stt_ent3.get(index1="0.0", index2="end")
        ent4 = self.stt_ent4_var.get()
        output_text_to_file = self.stt_text_output_checkbox.get()
        input_text_from_file = self.stt_text_input_checkbox.get()
        output_name = self.stt_output_name_var.get()
        st_type = self.stt_type_dropdown.get() # Steganography Type: Layered, Sequential, etc.
        encoding_type = self.stt_encoding_type_dropdown.get() # Encoding Type: UNICODE, ASCII
        action_type_dropdown = self.stt_action_type_dropdown.get() # Action Type: Encode, Decode
        output_type_dropdown = self.stt_output_type_dropdown.get() # Output Type: PNG, GIF, etc. (Only for encoding - only lossless formats)

        # Render start button as disabled
        self.stt_start_button.configure(state="disabled", text="Running...")
        self.update_idletasks()
        self.update()

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
        if input_text_from_file:
            try:
                with open(ent4, "r") as f: ent3 = f.read()
            except Exception as e: return self.print_to_stt_console(f"Error opening text file: {e}", error=True)

        # start
        if action_type_dropdown == "Encode":
            if not ent3: return self.print_to_stt_console("Please enter text.", error=True)
            if ent3.isascii() == False and encoding_type == "ASCII": return self.print_to_stt_console("Text contains non-ASCII characters.\n\nSwitch to UNICODE", error=True)

            if st_type == "Layered8":
                if encoding_type == "UNICODE":
                    return self.print_to_stt_console("UNICODE encoding is not supported for Layered. Please select LayeredDynamic or LayeredDynamicTransparent", error=True)
                if encoding_type == "ASCII":
                    try:
                        image, layers = TextSteganographyLayered().encode(image=im, text=ent3)
                        image.save(path)
                        self.print_to_stt_console(f"Layered8 | Bits: 8 | Layers: {layers} | Characters: {len(ent3)} | Type: {encoding_type} | Action: {action_type_dropdown} | Time: {round(time()-start_time, 2)} sec\n\nSaved to: '{path}'")
                    except ValueError as e: return self.print_to_stt_console(e, error=True)

            if st_type == "Sequential8":
                if encoding_type == "UNICODE":
                    return self.print_to_stt_console("UNICODE encoding is not supported for Sequential. Please select LayeredDynamic or LayeredDynamicTransparent", error=True)
                if encoding_type == "ASCII":
                    try:
                        image, layers = TextSteganography().encode(image=im, text=ent3)
                        image.save(path)
                        self.print_to_stt_console(f"Sequential8 | Bits: 8 | Layers: {layers} | Characters: {len(ent3)} | Type: {encoding_type} | Action: {action_type_dropdown} | Time: {round(time()-start_time, 2)} sec\n\nSaved to: '{path}'")
                    except ValueError as e: return self.print_to_stt_console(e, error=True)

            if st_type == "LayeredDynamic":
                try:
                    image, bits, layers = TextSteganographyLayeredDynamic().encode(image=im, text=ent3)
                    image.save(path)
                    self.print_to_stt_console(f"LayeredDynamic | Bits: {bits} | Layers: {layers} | Characters: {len(ent3)} | Type: {encoding_type} | Action: {action_type_dropdown} | Time: {round(time()-start_time, 2)} sec\n\nSaved to: '{path}'")
                except ValueError as e: return self.print_to_stt_console(e, error=True)

            if st_type == "LayeredDynamic\nTransparent":
                if im.format != "PNG": return self.print_to_stt_console("LayeredDynamicTransparent only supports PNG images. Please select a PNG image.", error=True)
                try:
                    image, bits, layers = TextSteganographyLayeredDynamicTransparent().encode(image=im, text=ent3)
                    image.save(path)
                    self.print_to_stt_console(f"LayeredDynamicTransparent | Bits: {bits} | Layers: {layers} | Characters: {len(ent3)} | Type: {encoding_type} | Action: {action_type_dropdown} | Time: {round(time()-start_time, 2)} sec\n\nSaved to: '{path}'")
                except ValueError as e: return self.print_to_stt_console(e, error=True)

        if action_type_dropdown == "Decode":
            if st_type == "Layered8":
                try:
                    text = TextSteganographyLayered().decode(image=im)
                    self.print_to_stt_textbox(text, output_to)
                    self.print_to_stt_console(f"Layered8 | Bits: 8 | Characters: {len(text)} | Type: {encoding_type} | Action: {action_type_dropdown} | Time: {round(time()-start_time, 2)} sec\n\nOutput in: {output_to}")
                except ValueError as e: return self.print_to_stt_console(e, error=True)

            if st_type == "Sequential8":
                try:
                    text = TextSteganography().decode(image=im, layer=1)
                    self.print_to_stt_textbox(text, output_to)
                    self.print_to_stt_console(f"Sequential8 | Bits: 8 | Characters: {len(text)} | Type: {encoding_type} | Action: {action_type_dropdown} | Time: {round(time()-start_time, 2)} sec\n\nOutput in: {output_to}")
                except ValueError as e: return self.print_to_stt_console(e, error=True)

            if st_type == "LayeredDynamic":
                try:
                    text, bits = TextSteganographyLayeredDynamic().decode(image=im)
                    self.print_to_stt_textbox(text, output_to)
                    self.print_to_stt_console(f"LayeredDynamic | Bits: {bits} | Characters: {len(text)} | Type: {'ASCII' if text.isascii() else 'UNICODE'} | Action: {action_type_dropdown} | Time: {round(time()-start_time, 2)} sec\n\nOutput in: {output_to}")
                except ValueError as e: return self.print_to_stt_console(e, error=True)

            if st_type == "LayeredDynamic\nTransparent":
                if im.format != "PNG": return self.print_to_stt_console("LayeredDynamicTransparent only supports PNG images. Please select a PNG image.", error=True)
                try:
                    text, bits = TextSteganographyLayeredDynamicTransparent().decode(image=im)
                    self.print_to_stt_textbox(text, output_to)
                    self.print_to_stt_console(f"LayeredDynamicTransparent | Bits: {bits} | Characters: {len(text)} | Type: {'ASCII' if text.isascii() else 'UNICODE'} | Action: {action_type_dropdown} | Time: {round(time()-start_time, 2)} sec\n\nOutput in: {output_to}")
                except ValueError as e: return self.print_to_stt_console(e, error=True)

    # Text To Image Generator ------------------------------------------------------------------------------------------

    def tti_open_folder(self):
        self.tti_ent3.delete(0, "end")
        self.tti_ent3_var.set(filedialog.askdirectory(initialdir=self.initial_browser_dir, title="Select output folder"))
    def tti_open_image(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.tti_ent2.delete(0, "end")
        self.tti_ent2_var.set(filename)
    def tti_open_text(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title="Select text file", filetypes=[("text files", ["*.txt"])])
        self.tti_ent1.delete(0, "end")
        self.tti_ent1_var.set(filename)

    def tti_action_type_dropdown_event(self, new_action_type: str):
        if new_action_type == "Encode":
            # ent3
            self.tti_ent3.configure(state="normal", border_width=2)
            self.tti_sidebar_button_3.configure(state="normal")
            # ent2
            self.tti_ent2.configure(state="disabled", border_width=0)
            self.tti_sidebar_button_2.configure(state="disabled")
            # output type dropdown
            self.tti_output_type_dropdown.configure(state="normal")
            # output text checkbox
            self.tti_text_output_checkbox.configure(state="disabled")
            self.tti_text_output_checkbox.deselect()
            self.tti_text_output_checkbox_event()
            # output name ent
            self.tti_output_name_ent.configure(state="normal", border_width=2)
            # output text checkbox
            self.tti_text_input_checkbox.configure(state="normal")
            self.tti_text_input_checkbox_event()

        if new_action_type == "Decode":
            # ent3
            self.tti_ent3.configure(state="disabled", border_width=0)
            self.tti_sidebar_button_3.configure(state="disabled")
            # ent2
            self.tti_ent2.configure(state="normal", border_width=2)
            self.tti_sidebar_button_2.configure(state="normal")
            # output type dropdown
            self.tti_output_type_dropdown.configure(state="disabled")
            # output text checkbox
            self.tti_text_output_checkbox.configure(state="normal")
            self.tti_text_output_checkbox_event()
            # output name ent
            self.tti_output_name_ent.configure(state="disabled", border_width=0)
            # input text checkbox
            self.tti_text_input_checkbox.configure(state="disabled")
            self.tti_text_input_checkbox.deselect()
            self.tti_text_input_checkbox_event()

    def tti_text_output_checkbox_event(self):
        if self.tti_text_output_checkbox.get():
            self.tti_ent3.configure(state="normal", border_width=2)
            self.tti_sidebar_button_3.configure(state="normal")
            self.tti_output_name_ent.configure(state="normal", border_width=2)
            self.tti_output_type_dropdown.set("TXT")
        else:
            if self.tti_action_type_dropdown.get() != "Encode":
                self.tti_ent3.configure(state="disabled", border_width=0)
                self.tti_sidebar_button_3.configure(state="disabled")
            self.tti_output_name_ent.configure(state="disabled", border_width=0)
            self.tti_output_type_dropdown.set("PNG")
    def tti_text_input_checkbox_event(self):
        if self.tti_text_input_checkbox.get():
            self.tti_ent1.configure(state="normal", border_width=2)
            self.tti_sidebar_button_1.configure(state="normal")
        else:
            self.tti_ent1.configure(state="disabled", border_width=0)
            self.tti_sidebar_button_1.configure(state="disabled")

    def tti_start_button_event(self):
        start_time = time()
        ent1 = self.tti_ent1_var.get()
        ent2 = self.tti_ent2_var.get()
        ent3 = self.tti_ent3_var.get()
        ent4 = self.tti_ent4.get(index1="0.0", index2="end")

        output_text_to_file = self.tti_text_output_checkbox.get()
        input_text_from_file = self.tti_text_input_checkbox.get()

        output_name = self.tti_output_name_var.get()
        action_type_dropdown = self.tti_action_type_dropdown.get()  # Action Type: Encode, Decode
        output_type_dropdown = self.tti_output_type_dropdown.get()  # Output Type: PNG, GIF, etc. (Only for encoding - only lossless formats)
        color = self.tti_color_dropdown.get()  # Color: RGB, etc.

        # Render start button as disabled
        self.tti_start_button.configure(state="disabled", text="Running...")
        self.update_idletasks()
        self.update()

        # folder/file path
        if action_type_dropdown == "Encode" or output_text_to_file:
            if not ent3: return self.print_to_tti_console("Output folder not specified", error=True)
            if ent3[-1] != "/" or ent3[-1] != "\\":
                if "\\" in ent3:ent3 += "\\"
                else:ent3 += "/"
        if not output_name: output_name = "TextToImageOutput"
        path = f"{ent3}{output_name}.{output_type_dropdown.lower()}"
        if output_text_to_file: output_to = f"{ent3}{output_name}.txt"
        else: output_to = "TextBox"

        # text
        if input_text_from_file:
            try:
                with open(ent1, "r") as f: ent4 = f.read()
            except Exception as e: return self.print_to_tti_console(f"Error opening text file: {e}", error=True)

        if action_type_dropdown == "Encode":
            output_to = path
            if not ent4: return self.print_to_tti_console("No text to encode", error=True)
            if color == "RGB":
                try: result_image, bits = TextToImageDynamic().encode(ent4, mode="RGB")
                except Exception as e: return self.print_to_tti_console(f"Error encoding text: {e}", error=True)
                try: result_image.save(path)
                except Exception as e: return self.print_to_tti_console(f"Error saving image: {e}", error=True)
                self.print_to_tti_console(f"TextToImageDynamic | Bits: {bits} | Mode: {color} | Characters: {len(ent4)} | Action: {action_type_dropdown} | Time: {round(time() - start_time, 2)} sec\n\nOutput in: {output_to}")

            if color == "RGBA":
                try: result_image, bits = TextToImageDynamic().encode(ent4, mode="RGBA")
                except Exception as e: return self.print_to_tti_console(f"Error encoding text: {e}", error=True)
                try: result_image.save(path)
                except Exception as e: return self.print_to_tti_console(f"Error saving image: {e}", error=True)
                self.print_to_tti_console(f"TextToImageDynamic | Bits: {bits} | Mode: {color} | Characters: {len(ent4)} | Action: {action_type_dropdown} | Time: {round(time() - start_time, 2)} sec\n\nOutput in: {output_to}")

            if color == "Mono":
                try: result_image, bits = TextToImageDynamic().encode(ent4, mode="L")
                except Exception as e: return self.print_to_tti_console(f"Error encoding text: {e}", error=True)
                try: result_image.save(path)
                except Exception as e: return self.print_to_tti_console(f"Error saving image: {e}", error=True)
                self.print_to_tti_console(f"TextToImageDynamic | Bits: {bits} | Mode: {color} | Characters: {len(ent4)} | Action: {action_type_dropdown} | Time: {round(time() - start_time, 2)} sec\n\nOutput in: {output_to}")


        if action_type_dropdown == "Decode":
            if not ent2: return self.print_to_tti_console("Please select an image.", error=True)
            try:image = Image.open(ent2)
            except Exception as e: return self.print_to_tti_console(f"Error opening image: {e}", error=True)
            if color == "RGB":
                try:
                    text, bits = TextToImageDynamic().decode(image, mode="RGB")
                    self.print_to_tti_textbox(text, output_to)
                    self.print_to_tti_console(f"TextToImageDynamic | Bits: {bits} | Mode: {color} | Characters: {len(text)} | Action: {action_type_dropdown} | Time: {round(time() - start_time, 2)} sec\n\nOutput in: {output_to}")
                except Exception as e: return self.print_to_tti_console(f"Error decoding text: {e}", error=True)
            if color == "RGBA":
                try:
                    text, bits = TextToImageDynamic().decode(image, mode="RGBA")
                    self.print_to_tti_textbox(text, output_to)
                    self.print_to_tti_console(f"TextToImageDynamic | Bits: {bits} | Mode: {color} | Characters: {len(text)} | Action: {action_type_dropdown} | Time: {round(time() - start_time, 2)} sec\n\nOutput in: {output_to}")
                except Exception as e: return self.print_to_tti_console(f"Error decoding text: {e}", error=True)
            if color == "Mono":
                try:
                    text, bits = TextToImageDynamic().decode(image, mode="L")
                    self.print_to_tti_textbox(text, output_to)
                    self.print_to_tti_console(f"TextToImageDynamic | Bits: {bits} | Mode: {color} | Characters: {len(text)} | Action: {action_type_dropdown} | Time: {round(time() - start_time, 2)} sec\n\nOutput in: {output_to}")
                except Exception as e: return self.print_to_tti_console(f"Error decoding text: {e}", error=True)

    # Image Extension Transform ----------------------------------------------------------------------------------------

    def iet_open_image(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open, filetypes=self.filetypes)
        self.iet_ent1.delete(0, "end")
        self.iet_ent1_var.set(filename)

    def iet_start_button_event(self):
        ent1 = self.iet_ent1_var.get()
        if not ent1: return self.print_to_iet_console("Please select an image.", error=True)
        ext = self.iet_output_type_var.get()
        try: image = Image.open(ent1)
        except Exception as e: return self.print_to_iet_console(f"Error opening image: {e}", error=True)
        title = image.filename.split("/")[-1].split(".")[0] # NOQA
        filename = filedialog.asksaveasfilename(initialdir=self.initial_browser_dir, defaultextension=ext.lower(), filetypes=self.filetypes, initialfile=title)
        try: image.save(filename)
        except Exception as e: return self.print_to_iet_console(f"Error saving image: {e}", error=True)
        self.print_to_iet_console(f"Output in: {filename}")

    # Metadata Info ----------------------------------------------------------------------------------------------------

    def mi_open_image(self):
        filename = filedialog.askopenfilename(initialdir=self.initial_browser_dir, title=self.title_open)
        self.mi_ent1.delete(0, "end")
        self.mi_ent1_var.set(filename)
        self.update_idletasks()
        self.update()
        self.mi_get_metadata_event()

    def mi_get_metadata_event(self):
        path = self.mi_ent1_var.get()
        if not path: return self.print_to_mi_console("Please select a file.", error=True)

        self.print_to_mi_console("Getting metadata info...\n")

        for ch in path:
            print(f"{ch} - {ord(ch)}")

        command = f'{self.exif_tool_path} "{path}"'

        try:
            for line in execute(command):
                if line != "\n" and line != '\n\n':
                    self.print_to_mi_console(line, clear=False)
        except Exception as e: return self.print_to_mi_console(f"Error getting metadata: {e}", error=True)

    # Youtube downloader -----------------------------------------------------------------------------------------------

    def yt_open_folder(self):
        folder = filedialog.askdirectory(initialdir=self.initial_browser_dir, title=self.title_open)
        self.yt_ent2.delete(0, "end")
        self.yt_ent2_var.set(folder)
        self.yt_update_event()

    def yt_get_res_event(self):
        ent1 = self.yt_ent1_var.get()
        playlist = self.yt_playlist_var.get()

        if not ent1: return self.print_to_yt_console("Please enter a URL.", error=True)

        self.print_to_yt_console("Getting video info...\n")
        self.update_idletasks()
        self.update()

        command = f"{self.yt_dlp_path} -F {'--yes-playlist ' if playlist else '--no-playlist '}{ent1}"

        try:
            for line in execute(command):
                self.print_to_yt_console(line, error=False, clear=False)
        except Exception as e: return self.print_to_yt_console(f"Error getting video info: {e}", error=True, clear=False)
    def yt_get_sub_event(self):
        ent1 = self.yt_ent1_var.get()
        playlist = self.yt_playlist_var.get()

        if not ent1: return self.print_to_yt_console("Please enter a URL.", error=True)

        self.print_to_yt_console("Getting video info...\n")
        self.update_idletasks()
        self.update()

        command = f"{self.yt_dlp_path} --list-subs {'--yes-playlist ' if playlist else '--no-playlist '}{ent1}"

        try:
            for line in execute(command):
                self.print_to_yt_console(line, error=False, clear=False)
        except Exception as e:return self.print_to_yt_console(f"Error getting video info: {e}", error=True, clear=False)

    def yt_toggle_video(self):
        self.yt_dropdown1.configure(state="normal" if self.yt_checkbox_video.get() else "disabled")
        self.yt_dropdown5.configure(state="normal" if self.yt_checkbox_video.get() else "disabled")
        self.yt_dropdown6.configure(state="normal" if self.yt_checkbox_video.get() else "disabled")
        self.yt_update_event()

    def yt_toggle_audio(self):
        self.yt_dropdown7.configure(state="normal" if self.yt_checkbox_audio.get() else "disabled")
        self.yt_dropdown8.configure(state="normal" if self.yt_checkbox_audio.get() else "disabled")
        self.yt_update_event()

    def yt_start_button_event(self):
        tab = self.yt_tab_view.get()
        if tab == "AudioVideo":
            self.yt_av_event()
        elif tab == "Subtitles":
            self.yt_sub_event()

    def yt_update_event(self):
        command = self.yt_av_event(download=False)
        print(command)
        self.print_to_yt_command_textbox('yt-dlp' + command[30:])

    def yt_av_event(self, download=True):
        ent1 = self.yt_ent1_var.get()
        ent2 = self.yt_ent2_var.get()
        ent3 = self.yt_ent3_var.get()
        resolution = self.yt_resolution_var.get()
        playlist = self.yt_playlist_var.get()
        ch_video = self.yt_checkbox_video.get()
        ch_audio = self.yt_checkbox_audio.get()
        v_ext = self.yt_video_ext_var.get()
        a_ext = self.yt_audio_ext_var.get()
        v_codec = self.yt_video_codec_var.get()
        a_codec = self.yt_audio_codec_var.get()
        ch_meta = self.yt_checkbox3_var.get()
        ch_sub = self.yt_checkbox4_var.get()
        ch_thumb = self.yt_checkbox5_var.get()

        if ch_video and ch_audio: av = 'video'
        elif ch_video and not ch_audio: av = 'video_only'
        elif not ch_video and ch_audio: av = 'audio'
        else: return self.print_to_yt_console("Please select at least one option.", error=True)

        v_codec = v_codec if v_codec != "best" else ''
        a_codec = a_codec if a_codec != "best" else ''

        res = self.resolutions_list_values[self.resolutions_list.index(resolution)][1] if resolution != "best" else ''

        if not ent1: return self.print_to_yt_console("Please enter a URL.", error=True)
        if not ent2: return self.print_to_yt_console("Please select a folder.", error=True)

        if ent2[-1] != "/" or ent2[-1] != "\\":
            if "\\" in ent2: ent2 += "\\"
            else: ent2 += "/"

        if download:
            self.yt_start_button.configure(state="disabled", text="Downloading...")
            self.print_to_yt_console('', clear=True)
            self.update_idletasks()
            self.update()

        if playlist: name = f"%(playlist)s/{av}-%(id)s (%(height)sp)-%(playlist_index)s.%(ext)s"
        else: name = f"{av}-%(id)s (%(height)sp).%(ext)s"

        dash_s = '-S "' + \
                 (f"res:{res}" if res else '')+ \
                 (',' if res and ch_video and v_codec else '') + \
                 (f"vcodec:{v_codec}" if ch_video and v_codec else '') + \
                 (',' if ch_video and v_codec and ch_audio and a_codec else '') + \
                 (f"acodec:{a_codec}" if ch_audio and a_codec else '') +\
                 '"'
        dash_s = dash_s+' ' if dash_s != '-S ""' else ''

        embed = ('--embed-subs' if ch_sub else '') + \
                (' ' if ch_sub and ch_thumb or ch_meta else '') + \
                ('--embed-thumbnail' if ch_thumb else '') + \
                (' ' if ch_thumb and ch_meta else '') + \
                ('--embed-metadata' if ch_meta else '')
        embed = embed+' ' if embed != '' else ''

        if ent3: command = f"{self.yt_dlp_path} -f \"{ent3}\" {'--yes-playlist ' if playlist else '--no-playlist '}--ignore-config -o \"{ent2+name}\" {ent1}"
        else:
            if av == "audio":
                command = f"{self.yt_dlp_path} {dash_s}-f ba --extract-audio --audio-format {a_ext} {'--yes-playlist ' if playlist else '--no-playlist '}-o \"{ent2 + name}\" {ent1}"
            elif av == "video_only":
                command = f"{self.yt_dlp_path} {dash_s}{embed}-f bv --remux-video {v_ext} {embed}{'--yes-playlist ' if playlist else '--no-playlist '}-o \"{ent2 + name}\" {ent1}"
            elif av == 'video':
                command = f"{self.yt_dlp_path} {dash_s}{embed}--remux-video {v_ext} {'--yes-playlist ' if playlist else '--no-playlist '}-o \"{ent2 + name}\" {ent1}"
            else: return self.print_to_yt_console("Error: Invalid AV option.", error=True)

        # url: https://www.youtube.com/watch?v=QH2-TGUlwu4
        if not download:
            return command

        if download:
            try:
                for line in execute(command):
                    self.print_to_yt_console(line, error=False, clear=False)
            except Exception as e: return self.print_to_yt_console(f"Error downloading: {e}", error=True, clear=False)

            self.yt_start_button.configure(state="normal", text="Download")
            self.update_idletasks()
            self.update()

    def yt_sub_event(self):
        ent1 = self.yt_ent1_var.get()
        ent2 = self.yt_ent2_var.get()
        ext = self.yt_sub_ext_var.get()
        lang = self.yt_sub_lang_var.get()
        playlist = self.yt_playlist_var.get()
        auto = self.yt_sub_auto_var.get()
        if not ent1: return self.print_to_yt_console("Please enter a URL.", error=True)
        if not ent2: return self.print_to_yt_console("Please select a folder.", error=True)

        if ent2[-1] != "/" or ent2[-1] != "\\":
            if "\\" in ent2: ent2 += "\\"
            else: ent2 += "/"

        self.yt_start_button.configure(state="disabled", text="Downloading...")
        self.print_to_yt_console('', clear=True)
        self.update_idletasks()
        self.update()

        if playlist: name = f"%(playlist)s/sub-%(id)s-%(playlist_index)s.%(ext)s"
        else: name = f"sub-%(id)s.%(ext)s"
        command = f"{self.yt_dlp_path} --skip-download {'--write-auto-subs ' if auto else ''}--write-sub --sub-lang \"{lang_dict_inv[lang]}\" {'--yes-playlist ' if playlist else '--no-playlist '}--sub-format \"{ext}\" -o \"{ent2+name}\" {ent1}"

        try:
            for path in execute(command):
                self.print_to_yt_console(path, error=False, clear=False)
        except Exception as e: return self.print_to_yt_console(f"Error downloading: {e}", error=True, clear=False)

        self.yt_start_button.configure(state="normal", text="Download")

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
    def print_to_st_console(self, text, error=False, clear=True):
        self.st_console.configure(state="normal")
        if clear: self.st_console.delete("1.0", "end")
        self.st_console.insert(customtkinter.END, text)
        self.st_console.configure(state="disabled")
        self.st_console.see("end")
        if error: self.st_console.configure(border_width=2, border_color="#1F6AA5")
        else: self.st_console.configure(border_width=0)
        self.update_idletasks()
        self.update()
    def print_to_stt_console(self, text, error=False, clear=True):
        self.stt_console.configure(state="normal")
        if clear: self.stt_console.delete("1.0", "end")
        self.stt_console.insert(customtkinter.END, text)
        self.stt_console.configure(state="disabled")
        self.stt_console.see("end")
        if error: self.stt_console.configure(border_width=2, border_color="#1F6AA5")
        else: self.stt_console.configure(border_width=0)
        self.stt_start_button.configure(state="normal", text="Run Text Steganographer")
        self.update_idletasks()
        self.update()
    def print_to_tti_console(self, text, error=False, clear=True):
        self.tti_console.configure(state="normal")
        if clear: self.tti_console.delete("1.0", "end")
        self.tti_console.insert(customtkinter.END, text)
        self.tti_console.configure(state="disabled")
        self.tti_console.see("end")
        if error: self.tti_console.configure(border_width=2, border_color="#1F6AA5")
        else: self.tti_console.configure(border_width=0)
        self.tti_start_button.configure(state="normal", text="Run Generator")
        self.update_idletasks()
        self.update()
    def print_to_iet_console(self, text, error=False, clear=True):
        self.iet_console.configure(state="normal")
        if clear: self.iet_console.delete("1.0", "end")
        self.iet_console.insert(customtkinter.END, text)
        self.iet_console.configure(state="disabled")
        self.iet_console.see("end")
        if error: self.iet_console.configure(border_width=2, border_color="#1F6AA5")
        else: self.iet_console.configure(border_width=0)
        self.update_idletasks()
        self.update()
    def print_to_mi_console(self, text, error=False, clear=True):
        self.mi_console.configure(state="normal")
        if clear: self.mi_console.delete("1.0", "end")
        self.mi_console.insert(customtkinter.END, text)
        self.mi_console.configure(state="disabled")
        self.mi_console.see("end")
        if error: self.mi_console.configure(border_width=2, border_color="#1F6AA5")
        else: self.mi_console.configure(border_width=0)
        self.update_idletasks()
        self.update()
    def print_to_yt_console(self, text, error=False, clear=True):
        if clear: self.yt_console.delete("1.0", "end")
        self.yt_console.insert(customtkinter.END, text)
        self.yt_console.see("end")
        if error:
            self.yt_console.configure(border_width=2, border_color="#1F6AA5")
            self.yt_start_button.configure(state="normal", text="Download")
            self.update_idletasks()
            self.update()
        else: self.yt_console.configure(border_width=0)
        self.update_idletasks()
        self.update()

    def print_to_stt_textbox(self, text, output_to, clear=True):
        if output_to == "TextBox":
            if clear: self.stt_ent3.delete("0.0", "end")
            self.stt_ent3.insert(customtkinter.END, text)
            self.update_idletasks()
            self.update()
        else:
            try:
                with open(output_to, "w", encoding="utf-8") as f: f.write(text)
            except Exception as e: return self.print_to_stt_console(f"Error writing to file: {e}", error=True)
    def print_to_tti_textbox(self, text, output_to, clear=True):
        if output_to == "TextBox":
            if clear: self.tti_ent4.delete("0.0", "end")
            self.tti_ent4.insert(customtkinter.END, text)
            self.update_idletasks()
            self.update()
        else:
            try:
                with open(output_to, "w", encoding="utf-8") as f: f.write(text)
            except Exception as e: return self.print_to_tti_console(f"Error writing to file: {e}", error=True)

    def print_to_yt_command_textbox(self, text):
        self.yt_command_console.configure(state='normal')
        self.yt_command_console.delete('0.0', customtkinter.END)
        self.yt_command_console.insert('0.0', text)
        self.yt_command_console.configure(state='disabled')

    def to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.yt_command_console.get('0.0', customtkinter.END))
        self.update()  # now it stays on the clipboard after the window is closed


# Static Functions -----------------------------------------------------------------------------------------------------

def make_folder(folder_path):
    # Example folder path: "C:/Users/Tomer27cz/Desktop/Files/CODING/Python Projects/AICode/Output"
    try:
        print("Making folder: " + folder_path)
        mkdir(folder_path)
        return folder_path, f"Making folder: {folder_path}"
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


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    error = popen.stderr.read()
    yield "\n"+error+"\n"
    popen.stdout.close()
    popen.stderr.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


# Main -----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
