import customtkinter
from PIL import Image

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info', filename=None, height=70, width=170, waittime=500):
        self.waittime = waittime
        self.wraplength = 180   #pixels
        self.widget = widget
        if filename:
            with Image.open(filename) as image:
                self.text = f"Image size: {image.size}\nImage mode: {image.mode}\nImage format: {image.format}"
        else:
            self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.height = height
        self.width = width
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = customtkinter.CTkToplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = customtkinter.CTkTextbox(self.tw, border_width=1, corner_radius=0, activate_scrollbars=False, width=self.width, height=self.height)
        label.insert("0.0", self.text)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
