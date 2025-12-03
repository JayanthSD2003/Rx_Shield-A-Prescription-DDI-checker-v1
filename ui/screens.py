from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from core.auth_manager import login, register
from core.database import save_analysis, get_recent_analysis
from core.gemini_client import perform_ocr, check_ddi
from core.tts_manager import play_welcome_message
from core.exporter import create_markdown, create_word
import threading
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.app import App
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

class LoginScreen(Screen):
    def do_login(self, username, password):
        success, message = login(username, password)
        if success:
            # Store username in App state
            app = App.get_running_app()
            app.username = username
            
            self.manager.current = 'home'
        else:
            self.show_popup("Login Failed", message)

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

    def exit_app(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Do you want to exit?"))
        
        buttons = BoxLayout(spacing=10, size_hint_y=None, height=40)
        btn_yes = Button(text="Yes", on_press=lambda x: App.get_running_app().stop())
        btn_no = Button(text="No", on_press=lambda x: self.popup.dismiss())
        
        buttons.add_widget(btn_yes)
        buttons.add_widget(btn_no)
        content.add_widget(buttons)
        
        self.popup = Popup(title="Exit Confirmation", content=content, size_hint=(None, None), size=(300, 150))
        self.popup.open()

class RegisterScreen(Screen):
    def do_register(self, username, password):
        success, message = register(username, password)
        if success:
            self.show_popup("Success", message)
            self.manager.current = 'login'
        else:
            self.show_popup("Registration Failed", message)

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

class HomeScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        
        # Update Welcome Message
        if hasattr(app, 'username'):
            self.ids.welcome_label.text = f"Welcome, {app.username}!"
            
            # Play welcome message only once
            if not getattr(app, 'welcome_played', False):
                play_welcome_message(app.username)
                app.welcome_played = True

            # Load Recent Analysis from DB
            recent = get_recent_analysis(app.username)
            if recent:
                image_path, result_text = recent
                
                # Ensure image path is absolute and exists
                if image_path and os.path.exists(image_path):
                    self.ids.recent_image.source = image_path
                    
                    # Store in app state for export/viewing
                    app.recent_image = image_path
                    app.recent_text = result_text
                    
                    # Truncate text for preview
                    preview_text = result_text[:100] + "..." if len(result_text) > 100 else result_text
                    self.ids.recent_text.text = preview_text
                    
                    # Show filename
                    filename = os.path.basename(image_path)
                    self.ids.recent_filename.text = f"File: {filename}"
                else:
                     # Handle missing file case
                    self.ids.recent_image.source = ''
                    self.ids.recent_text.text = "Recent file not found."
                    self.ids.recent_filename.text = ''
            else:
                self.ids.recent_image.source = ''
                self.ids.recent_text.text = "No recent analysis found."
                self.ids.recent_filename.text = ''

    def logout(self):
        app = App.get_running_app()
        if hasattr(app, 'username'):
            del app.username
        if hasattr(app, 'welcome_played'):
            del app.welcome_played
        # Clear recent analysis on logout
        if hasattr(app, 'recent_image'): del app.recent_image
        if hasattr(app, 'recent_text'): del app.recent_text
        
        self.manager.current = 'login'

class WelcomeScreen(Screen):
    def set_user(self, username):
        self.ids.welcome_label.text = f"Welcome, {username}!"
        play_welcome_message(username)

class DashboardScreen(Screen):
    def on_enter(self):
        # Clear selection when entering dashboard
        self.ids.filechooser.selection = []

    def analyze_image(self, selection):
        if not selection:
            return
        
        image_path = selection[0]
        self.manager.current = 'results'
        self.manager.get_screen('results').process_image(image_path)

from kivy.clock import mainthread

class ResultsScreen(Screen):
    def reset_and_back(self):
        self.ids.results_label.text = "Processing..."
        self.manager.current = 'dashboard'

    def go_home(self):
        self.ids.results_label.text = "Processing..."
        self.ids.result_image.source = ''
        self.manager.current = 'home'

    def export_result(self, format_type):
        app = App.get_running_app()
        if not hasattr(app, 'recent_text') or not app.recent_text:
            self.show_popup("Error", "No analysis to export.")
            return

        text = app.recent_text
        image_path = getattr(app, 'recent_image', None)
        
        # Ensure reports directory exists
        reports_dir = os.path.join(os.getcwd(), 'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"Report_{timestamp}"
        
        # Initialize Tkinter root (hidden)
        root = tk.Tk()
        root.withdraw()
        
        if format_type == 'markdown':
            file_path = filedialog.asksaveasfilename(
                initialdir=reports_dir,
                initialfile=f"{default_filename}.md",
                title="Save Analysis Report",
                filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
            )
            if file_path:
                success = create_markdown(text, image_path, file_path)
                msg = f"Exported to {os.path.basename(file_path)}" if success else "Export failed"
            else:
                return # User cancelled

        elif format_type == 'word':
            file_path = filedialog.asksaveasfilename(
                initialdir=reports_dir,
                initialfile=f"{default_filename}.docx",
                title="Save Analysis Report",
                filetypes=[("Word Documents", "*.docx"), ("All files", "*.*")]
            )
            if file_path:
                success = create_word(text, image_path, file_path)
                msg = f"Exported to {os.path.basename(file_path)}" if success else "Export failed"
            else:
                return # User cancelled
        else:
            msg = "Unknown format"
            
        root.destroy()
        self.show_popup("Export", msg)

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

    @mainthread
    def update_ui(self, final_text, image_path):
        self.ids.results_label.text = final_text
        if image_path and os.path.exists(image_path):
            self.ids.result_image.source = image_path
            self.ids.result_image.reload() # Force reload

    def process_image(self, image_path):
        self.ids.results_label.text = "Processing image... Please wait."
        self.ids.result_image.source = '' # Clear previous image
        
        def _process():
            # Combined Analysis (OCR + DDI)
            from core.gemini_client import analyze_prescription
            final_text = analyze_prescription(image_path)
            
            # Update UI on main thread
            self.update_ui(final_text, image_path if "Error" not in final_text else None)
            
            # Save to App state and DB
            if "Error" not in final_text:
                from kivy.app import App
                app = App.get_running_app()
                app.recent_image = image_path
                app.recent_text = final_text
                
                # Save to DB
                if hasattr(app, 'username'):
                    save_analysis(app.username, image_path, final_text)

        threading.Thread(target=_process).start()
