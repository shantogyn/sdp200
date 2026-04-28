# main.py
# eita puro application er entry point
# ekhane splash screen theke main dashboard e transition kora hocche
#ui file  namme : diet.py,component.py,dashboard.py,disease_info.py,first_aid.py,disease_prediction.py,medicine_reminder.py,lab_analyzer.py,login.py,reminder.py,singup.py
#services file name: auth_service.py,deit_service.py,disease_service.py,lab_service.py,reminder_service.py,user_service.py
from tkinter import *
# from ui.splash import SplashScreen
from ui.login import LoginScreen
from ui.singup import SignupScreen
from ui.dashboard import Dashboard
from services.auth_service import AuthService
from services.user_service import UserService

class Swastha:
    def __init__(self, root):
        self.root = root
        self.auth_service = AuthService()
        self.user_service = UserService()
        self.show_splash()

    # def show_splash(self):
    #     SplashScreen(self.root, self.show_login)

    def show_login(self):
        LoginScreen(self.root, self.auth_service, self.user_service, self.show_dashboard, self.show_signup)

    def show_signup(self):
        SignupScreen(self.root, self.auth_service, self.user_service, self.show_login)

    def show_dashboard(self):
        Dashboard(self.root)

if __name__ == "__main__":
    root = Tk()
    root.title("Swastha ")
    root.geometry("1200x800")
    root.minsize(800, 600)
    root.maxsize(1600, 1200)
    Swastha(root)
    root.mainloop()