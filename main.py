from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import psycopg2
from psycopg2 import Error

# Assuming you have a Database class defined in a separate file (DB.py)
from DB import Database

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a horizontal ScrollView
        scroll_view = ScrollView(size_hint=(1, 0.6), do_scroll_x=True, do_scroll_y=False)
        image_layout = GridLayout(cols=5, size_hint_x=None, height=200, spacing=10, padding=10)
        image_layout.bind(minimum_width=image_layout.setter('width'))

        # Add images to the GridLayout
        image_files = [r'images/image1.jpg', r'images/image2.jpg', r'images/image3.jpg', r'images/image4.jpg', r'images/image5.jpg']
        for img_file in image_files:
            try:
                image = Image(source=img_file, size_hint_y=None, height=200)
                image_layout.add_widget(image)
                print(f"Loaded image: {img_file}")
            except Exception as e:
                print(f"Failed to load image {img_file}: {e}")

        scroll_view.add_widget(image_layout)
        layout.add_widget(scroll_view)

        # Add buttons
        admin_button = Button(text='Admin Login', size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        admin_button.bind(on_press=self.go_to_admin_login)
        layout.add_widget(admin_button)

        customer_button = Button(text='Customer Login', size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        customer_button.bind(on_press=self.go_to_customer_login)
        layout.add_widget(customer_button)

        self.add_widget(layout)

    def go_to_admin_login(self, instance):
        self.manager.current = 'admin_login'

    def go_to_customer_login(self, instance):
        self.manager.current = 'customer_login'

class AdminLoginScreen(Screen):
    def __init__(self,db, **kwargs):
        super(AdminLoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.db = db
        self.username_input = TextInput(hint_text='Username', multiline=False)
        layout.add_widget(self.username_input)

        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        layout.add_widget(self.password_input)

        login_button = Button(text='Login', size_hint=(0.5, None), height=40)
        login_button.bind(on_press=self.check_credentials)
        layout.add_widget(login_button)

        back_button = Button(text='Back to Main', size_hint=(0.5, None), height=40)
        back_button.bind(on_press=self.go_back_to_main)
        layout.add_widget(back_button)

        self.message_label = Label(text='')
        layout.add_widget(self.message_label)

        # Customer list section
        self.customer_list_label = Label(text='Customers:', size_hint=(1, None), height=40)
        layout.add_widget(self.customer_list_label)

        self.customer_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.customer_list.bind(minimum_height=self.customer_list.setter('height'))
        layout.add_widget(self.customer_list)

        self.add_widget(layout)

    def check_credentials(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        # Example of checking credentials (replace with your logic)
        if username == 'admin' and password == '123':
            self.message_label.text = 'Login successful!'
            self.fetch_customers()
        else:
            self.message_label.text = 'Invalid username or password'

    def fetch_customers(self):
        try:
            # Replace with your actual database fetch logic
            db = Database('postgres', 'postgres', '1234')  # Replace with your actual database credentials
            db.connect()
            select_query = "SELECT name, mobile_number FROM customers"
            customers = self.db.fetch_all(select_query)
            db.close()

            self.customer_list.clear_widgets()
            for customer in customers:
                customer_label = Label(text=f"Name: {customer[0]}, Mobile: {customer[1]}", size_hint_y=None, height=40)
                self.customer_list.add_widget(customer_label)
        except Error as e:
            print(f"Error fetching customers: {e}")

    def go_back_to_main(self, instance):
        self.manager.current = 'main'

class CustomerLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(CustomerLoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        register_button = Button(text='Register', size_hint=(0.5, None), height=40)
        register_button.bind(on_press=self.go_to_registration)
        layout.add_widget(register_button)

        login_button = Button(text='Login', size_hint=(0.5, None), height=40)
        login_button.bind(on_press=self.go_to_customer_login)
        layout.add_widget(login_button)

        back_button = Button(text='Back to Main', size_hint=(0.5, None), height=40)
        back_button.bind(on_press=self.go_back_to_main)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_registration(self, instance):
        self.manager.current = 'customer_register'

    def go_to_customer_login(self, instance):
        # Logic for customer login goes here
        pass

    def go_back_to_main(self, instance):
        self.manager.current = 'main'

class CustomerRegisterScreen(Screen):
    def __init__(self,db, **kwargs):
        super(CustomerRegisterScreen, self).__init__(**kwargs)
        self.db = db
        layout = BoxLayout(orientation='vertical')

        self.name_input = TextInput(hint_text='Name', multiline=False)
        layout.add_widget(self.name_input)

        self.mobile_input = TextInput(hint_text='Mobile Number', multiline=False)
        layout.add_widget(self.mobile_input)

        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        layout.add_widget(self.password_input)

        self.confirm_password_input = TextInput(hint_text='Confirm Password', password=True, multiline=False)
        layout.add_widget(self.confirm_password_input)
        
        register_button = Button(text='Register', size_hint=(0.5, None), height=40)
        register_button.bind(on_press=self.register_customer)
        layout.add_widget(register_button)

        back_button = Button(text='Back to Main', size_hint=(0.5, None), height=40)
        back_button.bind(on_press=self.go_back_to_main)
        layout.add_widget(back_button)

        self.message_label = Label(text='')
        layout.add_widget(self.message_label)

        self.add_widget(layout)

    def register_customer(self, instance):
        name = self.name_input.text.strip()
        mobile_number = self.mobile_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()

        if not (name and mobile_number and password and confirm_password):
            self.message_label.text = 'Please fill in all fields'
            return
        
        if password != confirm_password:
            self.message_label.text = 'Passwords do not match'
            return
        
        try:
            insert_query = "INSERT INTO customers (name, mobile_number, password) VALUES (%s, %s, %s)"
            self.db.execute_query(insert_query, (name, mobile_number, password))
            self.message_label.text = 'Registration successful!'
        except Error as e:
            self.message_label.text = f'Error: {e}'

    def go_back_to_main(self, instance):
        self.manager.current = 'main'


class MilkOrderApp(App):
    def build(self):
        db = Database('postgres', 'postgres', '1234')
        db.connect()
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AdminLoginScreen(name='admin_login', db=db))
        sm.add_widget(CustomerLoginScreen(name='customer_login'))
        sm.add_widget(CustomerRegisterScreen(name='customer_register', db=db))
        return sm

if __name__ == '__main__':
    MilkOrderApp().run()
