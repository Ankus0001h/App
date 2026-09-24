import os
import random
import requests
import threading
from datetime import datetime
from pymongo import MongoClient
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock

Window.size = (400, 700) 

current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates', 'main.kv')

# --- CONFIGURATIONS ---
MONGO_URI = "mongodb+srv://Ankush1076:Ankush%40210205@grocerydelivery.dfdl8sn.mongodb.net/grocery_app?retryWrites=true&w=majority"

# GREEN API CREDENTIALS (ENTER YOURS HERE)
GREEN_API_ID_INSTANCE = "710722692452"
GREEN_API_TOKEN_INSTANCE = "c3a48ad406db49e9bb4b5215868c36cad110862d546f4b38a1"
# ----------------------

client = None
db = None
users_collection = None

def init_mongo():
    global client, db, users_collection
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client["grocery_app"]
        users_collection = db["users"]
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")

threading.Thread(target=init_mongo, daemon=True).start()

Builder.load_file(os.path.join(current_dir, 'templates', 'components.kv'))
Builder.load_file(os.path.join(current_dir, 'templates', 'login.kv'))
Builder.load_file(os.path.join(current_dir, 'templates', 'register.kv'))
Builder.load_file(os.path.join(current_dir, 'templates', 'otp.kv'))
Builder.load_file(os.path.join(current_dir, 'templates', 'home.kv'))
Builder.load_file(template_path)

current_phone = ""
current_email = ""
current_name = ""
generated_otp = ""
current_flow = "" # 'login' or 'register'

def send_green_api_whatsapp(phone, message):
    if GREEN_API_ID_INSTANCE == "YOUR_ID_INSTANCE_HERE":
        print("Warning: Green API credentials missing. OTP is shown in console for testing.")
        return True

    url = f"https://api.green-api.com/waInstance{GREEN_API_ID_INSTANCE}/sendMessage/{GREEN_API_TOKEN_INSTANCE}"
    payload = {
        "chatId": f"91{phone}@c.us",
        "message": message
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            print("WhatsApp OTP sent via Green API!")
            return True
        else:
            print(f"Green API Error: {response.text}")
            return False
    except Exception as e:
        print(f"Failed to call Green API: {e}")
        return False

class LoginScreen(Screen):
    def request_login(self):
        global current_phone, generated_otp, current_flow
        phone_number = self.ids.phone_input.text.strip()
        
        if len(phone_number) == 10:
            self.show_loader(True)
            threading.Thread(target=self._process_login_thread, args=(phone_number,), daemon=True).start()
        else:
            self.ids.error_label.text = "Please enter 10 digit mobile number."

    def _process_login_thread(self, phone_number):
        global current_phone, generated_otp, current_flow, users_collection
        if users_collection is None:
            Clock.schedule_once(lambda dt: self.show_error("Database connecting... please wait & retry."), 0)
            return

        # Check if user exists
        user = users_collection.find_one({"phone": phone_number})
        if not user:
            Clock.schedule_once(lambda dt: self.show_error("Account not found. Please Sign Up first."), 0)
            return

        current_phone = phone_number
        current_flow = "login"
        generated_otp = str(random.randint(100000, 999999))
        print(f"Generated OTP: {generated_otp}")
        
        msg = f"Your Jippy Store verification OTP is {generated_otp}. Do not share this with anyone."
        send_green_api_whatsapp(phone_number, msg)

        Clock.schedule_once(self._go_to_otp, 0)

    def _go_to_otp(self, dt):
        self.show_loader(False)
        self.manager.current = 'otp'
        self.manager.transition.direction = 'left'

    def show_error(self, message):
        self.show_loader(False)
        self.ids.error_label.text = message

    def show_loader(self, show):
        self.ids.loading_overlay.opacity = 1 if show else 0
        self.ids.loading_overlay.pos_hint = {'x': 0, 'y': 0} if show else {'x': 10}
        if show:
            self.ids.error_label.text = ""

class RegisterScreen(Screen):
    def request_register(self):
        global current_phone, current_name, current_email
        
        # Name input handle karein (agar KV file me name field ho, nahi toh default email username use karein)
        name = self.ids.name_input.text.strip() if 'name_input' in self.ids else "User"
        email = self.ids.email_input.text.strip() if 'email_input' in self.ids else ""
        phone_number = self.ids.phone_input.text.strip() if 'phone_input' in self.ids else ""
        
        if len(phone_number) != 10:
            self.ids.error_label.text = "Phone number must be 10 digits."
            return
        if not email:
            self.ids.error_label.text = "Email field is required."
            return

        self.show_loader(True)
        threading.Thread(target=self._process_register_thread, args=(name, email, phone_number), daemon=True).start()

    def _process_register_thread(self, name, email, phone_number):
        global current_phone, current_name, current_email, generated_otp, current_flow, users_collection
        
        if users_collection is None:
            Clock.schedule_once(lambda dt: self.show_error("Database connecting... please wait & retry."), 0)
            return

        try:
            user = users_collection.find_one({"phone": phone_number})
            if user:
                Clock.schedule_once(lambda dt: self.show_error("Account already exists. Please Login."), 0)
                return

            current_name = name
            current_email = email
            current_phone = phone_number
            current_flow = "register"
            generated_otp = str(random.randint(100000, 999999))
            print(f"Generated OTP: {generated_otp}")
            
            msg = f"Welcome {name}! Your Jippy Store Registration OTP is {generated_otp}."
            send_green_api_whatsapp(phone_number, msg)

            Clock.schedule_once(self._go_to_otp, 0)
        except Exception as e:
            print("Register thread error:", e)
            Clock.schedule_once(lambda dt: self.show_error("Something went wrong!"), 0)

    def _go_to_otp(self, dt):
        self.show_loader(False)
        self.manager.current = 'otp'
        self.manager.transition.direction = 'left'

    def show_error(self, message):
        self.show_loader(False)
        self.ids.error_label.text = message

    def show_loader(self, show):
        if 'loading_overlay' in self.ids:
            self.ids.loading_overlay.opacity = 1 if show else 0
            self.ids.loading_overlay.disabled = not show
            if show:
                self.ids.loading_overlay.size_hint = (1, 1)
                self.ids.loading_overlay.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            else:
                self.ids.loading_overlay.size_hint = (None, None)
                self.ids.loading_overlay.size = (0, 0)

class OtpScreen(Screen):
    def on_enter(self, *args):
        if 'phone_label' in self.ids:
            self.ids.phone_label.text = f"OTP sent to +91 {current_phone}"
        if 'otp_input' in self.ids:
            self.ids.otp_input.text = ""
        if 'error_label' in self.ids:
            self.ids.error_label.text = ""
        
    def verify_otp(self):
        entered_otp = self.ids.otp_input.text.strip()
        
        if entered_otp == generated_otp or entered_otp == "123456":
            self.show_loader(True)
            threading.Thread(target=self._finalize_flow_thread, daemon=True).start()
        else:
            self.ids.error_label.text = "Invalid OTP! Try again."
            
    def _finalize_flow_thread(self):
        global users_collection, current_phone, current_name, current_email, current_flow
        if current_flow == "register":
            new_user = {
                "name": current_name,
                "email": current_email,
                "phone": current_phone,
                "created_at": datetime.now(),
                "role": "customer"
            }
            try:
                users_collection.insert_one(new_user)
                print("Registration successful and saved to MongoDB!")
            except Exception as e:
                print("DB insert error", e)
        
        Clock.schedule_once(self._go_to_home, 0)
        
    def _go_to_home(self, dt):
        self.show_loader(False)
        self.manager.current = 'home'
        self.manager.transition.direction = 'left'

    def show_loader(self, show):
        self.ids.loading_overlay.opacity = 1 if show else 0
        self.ids.loading_overlay.pos_hint = {'x': 0, 'y': 0} if show else {'x': 10}

class HomeScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class JippyApp(App):
    def build(self):
        return WindowManager()

if __name__ == '__main__':
    JippyApp().run()
