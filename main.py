import json
import random
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivy.network.urlrequest import UrlRequest # <--- The native Kivy tool
from kivy.clock import Clock

# =========================================================
# CONFIGURATION
# =========================================================
# PASTE YOUR FIREBASE URL HERE
FIREBASE_URL = "https://findmystray-gr-default-rtdb.europe-west1.firebasedatabase.app/"

# =========================================================
# LANGUAGE DICTIONARY
# =========================================================
TRANS = {
    'title_home': {'en': 'FindMyStray (Korydallos)', 'gr': 'Βρες το Αδέσποτο (Κορυδαλλός)'},
    'btn_lost':   {'en': 'I LOST MY PET', 'gr': 'ΕΧΑΣΑ ΤΟ ΖΩΟ ΜΟΥ'},
    'btn_found':  {'en': 'I FOUND A STRAY', 'gr': 'ΒΡΗΚΑ ΑΔΕΣΠΟΤΟ'},
    'btn_map':    {'en': 'VIEW LIVE MAP', 'gr': 'ΔΕΣ ΤΟ ΧΑΡΤΗ'},
    'title_map':  {'en': 'Active Alerts', 'gr': 'Ενεργές Ειδοποιήσεις'},
    'title_rep':  {'en': 'Report a Pet', 'gr': 'Αναφορά Ζώου'},
    'lbl_enter':  {'en': 'Enter Pet Details', 'gr': 'Στοιχεία Ζώου'},
    'hint_type':  {'en': 'Dog or Cat?', 'gr': 'Σκύλος ή Γάτα;'},
    'help_type':  {'en': 'e.g., Dog (Skylos)', 'gr': 'π.χ. Σκύλος'},
    'hint_desc':  {'en': 'Description', 'gr': 'Περιγραφή'},
    'help_desc':  {'en': 'e.g., Black Kokoni', 'gr': 'π.χ. Μαύρο Κοκόνι'},
    'btn_photo':  {'en': 'UPLOAD PHOTO', 'gr': 'ΦΩΤΟΓΡΑΦΙΑ'},
    'btn_sub':    {'en': 'SUBMIT REPORT', 'gr': 'ΥΠΟΒΟΛΗ'},
    'alert_tit':  {'en': 'Report Sent', 'gr': 'Εστάλη'},
    'alert_txt':  {'en': 'Saved to Cloud Database!', 'gr': 'Αποθηκεύτηκε στη βάση δεδομένων!'},
    'btn_ok':     {'en': 'OK', 'gr': 'ΕΝΤΑΞΕΙ'}
}

KV = '''
ScreenManager:
    HomeScreen:
    MapScreen:
    ReportScreen:

<HomeScreen>:
    name: 'home'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1
        
        MDTopAppBar:
            title: app.txt_title_home
            elevation: 4
            right_action_items: [["web", lambda x: app.toggle_lang()]]

        MDBoxLayout:
            orientation: 'vertical'
            spacing: "20dp"
            padding: "20dp"
            adaptive_height: True
            pos_hint: {"center_x": .5, "center_y": .5}

            MDFillRoundFlatIconButton:
                icon: "alert-circle-outline"
                text: app.txt_btn_lost
                font_size: "20sp"
                md_bg_color: 0.8, 0, 0, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 1
                height: "80dp"
                on_release: 
                    root.manager.current = 'report'
                    root.manager.transition.direction = 'left'

            MDFillRoundFlatIconButton:
                icon: "camera"
                text: app.txt_btn_found
                font_size: "20sp"
                md_bg_color: 0, 0.6, 0, 1
                size_hint_x: 1
                height: "80dp"
                on_release:
                    root.manager.current = 'report'
                    root.manager.transition.direction = 'left'

            MDFillRoundFlatIconButton:
                icon: "map-marker"
                text: app.txt_btn_map
                font_size: "18sp"
                size_hint_x: 1
                on_release: 
                    root.manager.current = 'map'
                    root.manager.transition.direction = 'left'

<MapScreen>:
    name: 'map'
    BoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: app.txt_title_map
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["refresh", lambda x: root.load_reports()]]

        MapView:
            id: mapview
            lat: 37.9838
            lon: 23.6500
            zoom: 14
            double_tap_zoom: True

<ReportScreen>:
    name: 'report'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1

        MDTopAppBar:
            title: app.txt_title_rep
            left_action_items: [["arrow-left", lambda x: root.go_back()]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "20dp"
                adaptive_height: True

                MDLabel:
                    text: app.txt_lbl_enter
                    font_style: "H5"
                    halign: "center"

                MDTextField:
                    id: pet_type
                    hint_text: app.txt_hint_type
                    helper_text: app.txt_help_type
                    mode: "rectangle"

                MDTextField:
                    id: description
                    hint_text: app.txt_hint_desc
                    helper_text: app.txt_help_desc
                    mode: "rectangle"
                    multiline: True

                MDFillRoundFlatButton:
                    text: app.txt_btn_sub
                    size_hint_x: 1
                    md_bg_color: 0, 0.5, 1, 1
                    on_release: root.submit_report()
'''

class HomeScreen(Screen):
    pass

class MapScreen(Screen):
    def on_enter(self):
        self.load_reports()

    def load_reports(self):
        print("Fetching data from Firebase...")
        # Using Kivy UrlRequest instead of requests
        req = UrlRequest(
            f"{FIREBASE_URL}reports.json",
            on_success=self.on_request_success,
            on_failure=self.on_request_error,
            on_error=self.on_request_error
        )

    def on_request_success(self, req, result):
        # 'result' is the dictionary from Firebase
        if result:
            print(f"Found {len(result)} reports!")
            # We must use MainThread to update UI from a network call
            for key, value in result.items():
                self.add_pin(value)
        else:
            print("No reports found.")

    def on_request_error(self, req, error):
        print(f"Error fetching: {error}")

    def add_pin(self, report_data):
        marker = MapMarkerPopup(lat=report_data['lat'], lon=report_data['lon'])
        bubble = MDBoxLayout(orientation="vertical", padding="10dp", size_hint=(None, None), size=("200dp", "100dp"), md_bg_color=(1,1,1,1))
        label_type = MDLabel(text=f"Type: {report_data['type']}", theme_text_color="Primary")
        label_desc = MDLabel(text=report_data['description'], theme_text_color="Secondary", font_style="Caption")
        bubble.add_widget(label_type)
        bubble.add_widget(label_desc)
        marker.add_widget(bubble)
        self.ids.mapview.add_marker(marker)

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

class ReportScreen(Screen):
    def submit_report(self):
        app = MDApp.get_running_app()
        pet_type = self.ids.pet_type.text
        description = self.ids.description.text
        
        if not pet_type or not description:
            return

        rand_lat = 37.9838 + random.uniform(-0.005, 0.005)
        rand_lon = 23.6500 + random.uniform(-0.005, 0.005)

        report_data = {
            "type": pet_type,
            "description": description,
            "lat": rand_lat,
            "lon": rand_lon,
            "date": "23/11/2025" 
        }

        # Send data using UrlRequest
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        req = UrlRequest(
            f"{FIREBASE_URL}reports.json",
            req_body=json.dumps(report_data),
            req_headers=headers,
            on_success=self.on_post_success,
            on_failure=self.on_post_error,
            on_error=self.on_post_error
        )

    def on_post_success(self, req, result):
        app = MDApp.get_running_app()
        self.dialog = MDDialog(
            title=app.txt_alert_tit,
            text=app.txt_alert_txt,
            buttons=[MDFlatButton(text=app.txt_btn_ok, on_release=self.close_dialog)],
        )
        self.dialog.open()
        self.ids.pet_type.text = ""
        self.ids.description.text = ""

    def on_post_error(self, req, error):
        print(f"Error posting: {error}")

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.manager.current = 'home'

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

class FindMyStrayApp(MDApp):
    # StringProperties definitions
    txt_title_home = StringProperty()
    txt_btn_lost = StringProperty()
    txt_btn_found = StringProperty()
    txt_btn_map = StringProperty()
    txt_title_map = StringProperty()
    txt_title_rep = StringProperty()
    txt_lbl_enter = StringProperty()
    txt_hint_type = StringProperty()
    txt_help_type = StringProperty()
    txt_hint_desc = StringProperty()
    txt_help_desc = StringProperty()
    txt_btn_photo = StringProperty()
    txt_btn_sub = StringProperty()
    txt_alert_tit = StringProperty()
    txt_alert_txt = StringProperty()
    txt_btn_ok = StringProperty()

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.current_lang = 'gr'
        self.update_text()
        return Builder.load_string(KV)

    def toggle_lang(self):
        if self.current_lang == 'en':
            self.current_lang = 'gr'
        else:
            self.current_lang = 'en'
        self.update_text()

    def update_text(self):
        self.txt_title_home = TRANS['title_home'][self.current_lang]
        self.txt_btn_lost = TRANS['btn_lost'][self.current_lang]
        self.txt_btn_found = TRANS['btn_found'][self.current_lang]
        self.txt_btn_map = TRANS['btn_map'][self.current_lang]
        self.txt_title_map = TRANS['title_map'][self.current_lang]
        self.txt_title_rep = TRANS['title_rep'][self.current_lang]
        self.txt_lbl_enter = TRANS['lbl_enter'][self.current_lang]
        self.txt_hint_type = TRANS['hint_type'][self.current_lang]
        self.txt_help_type = TRANS['help_type'][self.current_lang]
        self.txt_hint_desc = TRANS['hint_desc'][self.current_lang]
        self.txt_help_desc = TRANS['help_desc'][self.current_lang]
        self.txt_btn_photo = TRANS['btn_photo'][self.current_lang]
        self.txt_btn_sub = TRANS['btn_sub'][self.current_lang]
        self.txt_alert_tit = TRANS['alert_tit'][self.current_lang]
        self.txt_alert_txt = TRANS['alert_txt'][self.current_lang]
        self.txt_btn_ok = TRANS['btn_ok'][self.current_lang]

if __name__ == '__main__':
    FindMyStrayApp().run()