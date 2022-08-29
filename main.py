from tkinter import *
from GUI.main_frame import Main_Frame
from GUI.Menu.MenuBar import MenuBar
from GUI.Login.login_form import LoginForm




class LoginTopLevel (Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("600x450")
        self.config(bg="#7bacc7")
        self.title('  AGENDA FÚ')
        self.iconphoto(True, PhotoImage(file="img.png"))
        self.attributes('-topmost', 'true')

        #disabling the X-closing button
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.disable_close_on_X)




    def disable_close_on_X(self):
            pass


if __name__ == "__main__":

    root = Tk()
    root.minsize(600, 450)
    root.maxsize(1350,900)
    root.title("    Agenda FÚ   ")

    main = Main_Frame(root)
    login_toplevel = LoginTopLevel()
    LoginForm(login_toplevel, root)
    root.config(menu=MenuBar(root, main), bg="#7bacc7")
    root.update_idletasks()
    root.mainloop()



