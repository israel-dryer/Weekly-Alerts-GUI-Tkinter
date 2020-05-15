"""
    Alerts Program GUI. This program is meant to serve as a template for a program that you can use
    to initiate alerts of some kind. For example, sending emails.

    Author: Israel Dryer
    Modified: 2020-05-15
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Style, Progressbar
from PIL import Image, ImageTk

# function to convert rgb to hex values
rgb2hex = lambda r, g, b: f"#{r:02x}{g:02x}{b:02x}"

# application colors
BTN_BG = rgb2hex(217, 217, 217)
BTN_FG = rgb2hex(255, 255, 255)
HEADER_FG = rgb2hex(255, 255, 255)
HEADER_BG = rgb2hex(80, 45, 129)
BAR_COLOR = rgb2hex(0, 167, 181)
TROUGH_COLOR = rgb2hex(217, 217, 217)

class Alert:
    """GUI for Alerts program"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title('Weekly Alerts')
        self.root.iconbitmap('images/icon.ico')
        
        # weight columns
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=48)
        self.root.grid_columnconfigure(3, weight=50)     

        # weight rows
        self.root.grid_rowconfigure(0, weight=20)
        self.root.grid_rowconfigure(1, weight=70)
        self.root.grid_rowconfigure(2, weight=10)
        
        # create objects
        self.title = tk.Label(self.root, text='Weekly Alerts', font=('Arial Black', 40), 
            background=HEADER_BG, foreground=HEADER_FG, anchor=tk.CENTER)

        self.monday_img = ImageTk.PhotoImage(file='images/monday.png')
        self.monday_btn = tk.Button(self.root, image=self.monday_img, relief=tk.FLAT,
            background=BTN_BG, command=self.monday_alerts)

        self.friday_img = ImageTk.PhotoImage(file='images/friday.png')
        self.friday_btn = tk.Button(self.root, image=self.friday_img, relief=tk.FLAT,
            background=BTN_BG, command=self.friday_alerts)

        self.send_img = ImageTk.PhotoImage(file='images/send.png')
        self.send_btn = tk.Button(self.root, image=self.send_img, relief=tk.FLAT, command=self.send_alerts)

        self.delete_img = ImageTk.PhotoImage(file='images/delete.png')
        self.delete_btn = tk.Button(self.root, image=self.delete_img, relief=tk.FLAT, command=self.delete_alerts)

        self.pg_style = Style()
        self.pg_style.theme_use('alt')
        self.pg_style.configure('myProgress.Horizontal.TProgressbar', background=BAR_COLOR, 
            troughcolor=TROUGH_COLOR, troughrelief=tk.FLAT)
        self.progress_val = tk.DoubleVar()
        self.progress_bar = Progressbar(self.root, variable=self.progress_val, maximum=100,
            style='myProgress.Horizontal.TProgressbar')

        copyright_text = "© 2020 Your Company Name Here"
        self.copyright = tk.Label(self.root, text=copyright_text, font=('Arial', 12))

        # arrange objects
        self.title.grid(row=0, column=0, columnspan=4, sticky=tk.EW)
        self.monday_btn.grid(row=1, column=0, columnspan=3, padx=(10, 5), pady=10)    
        self.friday_btn.grid(row=1, column=3, padx=(5, 10), pady=10)
        self.send_btn.grid(row=2, column=0, sticky=tk.W, padx=(10, 5), pady=(0, 10))
        self.delete_btn.grid(row=2, column=1, sticky=tk.W, padx=(5, 5), pady=(0, 10))
        self.progress_bar.grid(row=2, column=2, sticky=tk.NSEW, padx=(5, 5), pady=(0, 10))
        self.copyright.grid(row=2, column=3, sticky=tk.EW, padx=(5, 10), pady=(0, 10))
        self.root.eval('tk::PlaceWindow . center')
        self.root.deiconify()


    def monday_alerts(self):
        """Create Monday alert"""
        # open source data file
        filename = filedialog.askopenfilename()
        if filename:
            confirm = messagebox.askokcancel(title="Continue", message="Continue with file?\n " + filename)
            if confirm:
                # test process progress update.
                self.increment_progress()
            else:
                messagebox.showinfo(
                    title='Monday Alert Cancelled',
                    message='Process has been cancelled by user. Please click the "Monday" button again to retry.')
        else:
            messagebox.showinfo(
                title='Monday Alert Cancelled',
                message='Process has been cancelled by user. Please click the "Monday" button again to retry.')


    def friday_alerts(self):
        """Create Friday alert"""
        # open source data file
        filename = filedialog.askopenfilename()
        if filename:
            confirm = messagebox.askokcancel(title="Continue", message="Continue with file?\n " + filename)
            if confirm:
                # test process progress update.
                self.increment_progress()
            else:
                messagebox.showinfo(
                    title='Friday Alert Cancelled',
                    message='Process has been cancelled by user. Please click the "Friday" button again to retry.')
        else:
            messagebox.showinfo(
                title='Friday Alert Cancelled',
                message='Process has been cancelled by user. Please click the "Friday" button again to retry.')

    def send_alerts(self):
        """Send all alerts created"""
        # check for alerts to send
        alert_count = self.progress_val.get()
        if not alert_count > 0:
            messagebox.showerror(title="Send Error", message=(
                "There are no alerts to send. Please create alerts by clicking on the Friday" + 
                " or Monday buttons before trying to send."))
            return
        # confirm that the user really wants to proceed
        confirm = messagebox.askyesno(title="Confirm Send", message="Are you sure you want to send all alerts?")
        if confirm:
            self.decrement_progress()
        else:
            messagebox.showinfo(
                title='Send Alert Cancelled',
                message='Process has been cancelled by user. Please click the "Send" button again to retry.')

    def delete_alerts(self):
        """Delete all created alerts"""
        # check for alerts to send
        alert_count = self.progress_val.get()
        if not alert_count > 0:
            messagebox.showerror(title="Delete Error", message=(
                "There are no alerts to delete. Please create alerts by clicking on the Friday" + 
                " or Monday buttons before trying to delete."))
            return
        # confirm that the user really wants to proceed
        confirm = messagebox.askyesno(
            title="Confirm Delete",
            message="IMPORTANT!!!\n\nProceed with Delete?? This process cannot be reversed!!")
        if confirm:
            self.decrement_progress()
        else:
            messagebox.showinfo(
                title='Delete Alert Cancelled',
                message='Process has been cancelled by user. Please click the "Delete" button again to retry.')

    def increment_progress(self, ):
        """Update progress bar value"""
        # get current value of pb
        pb_val = self.progress_val.get()
        # reset to 0 for new process
        if pb_val == 100:
            pb_val = 0
        # increment for new process
        self.progress_val.set(pb_val+1)
        # schedule again if not complete, else shutdown process
        if not self.progress_val.get() == 100:
            self.root.after(100, self.increment_progress)
        else:
            messagebox.showinfo(title="Complete", message="The process has completed.")

    def decrement_progress(self, ):
        """Update progress bar value"""
        # get current value of pb
        pb_val = self.progress_val.get()
        # reset to 100 for new process
        if pb_val == 0:
            pb_val = 100
        # increment for new process
        self.progress_val.set(pb_val-1)
        # schedule again if not complete, else shutdown process
        if not self.progress_val.get() == 0:
            self.root.after(100, self.decrement_progress)
        else:
            messagebox.showinfo(title="Complete", message="The process has completed.")

if __name__ == '__main__':

    alert = Alert()
    alert.root.mainloop()

