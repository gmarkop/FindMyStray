import json
import random
import base64
from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.utils import platform

# GPS functionality
try:
    from plyer import gps
    GPS_AVAILABLE = True
except ImportError:
    GPS_AVAILABLE = False
    print("Warning: GPS not available (plyer not installed)")

# Camera functionality
try:
    from plyer import camera
    from plyer import filechooser
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    print("Warning: Camera not available (plyer not installed)")

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
    'help_type':  {'en': 'e.g., Dog', 'gr': 'π.χ. Σκύλος'},
    'hint_desc':  {'en': 'Description', 'gr': 'Περιγραφή'},
    'help_desc':  {'en': 'e.g., Black Kokoni', 'gr': 'π.χ. Μαύρο Κοκόνι'},
    'hint_contact': {'en': 'Contact Info (Phone/Email)', 'gr': 'Στοιχεία Επικοινωνίας (Τηλ/Email)'},
    'help_contact': {'en': 'e.g., 6912345678', 'gr': 'π.χ. 6912345678'},
    'btn_photo':  {'en': 'CAPTURE PHOTO', 'gr': 'ΦΩΤΟΓΡΑΦΙΑ'},
    'btn_gallery': {'en': 'CHOOSE FROM GALLERY', 'gr': 'ΕΠΙΛΟΓΗ ΑΠΟ ΣΥΛΛΟΓΗ'},
    'btn_gps':    {'en': 'GET MY LOCATION', 'gr': 'ΤΟΠΟΘΕΣΙΑ ΜΟΥ'},
    'btn_sub':    {'en': 'SUBMIT REPORT', 'gr': 'ΥΠΟΒΟΛΗ'},
    'alert_tit':  {'en': 'Report Sent', 'gr': 'Εστάλη'},
    'alert_txt':  {'en': 'Saved to Cloud Database!', 'gr': 'Αποθηκεύτηκε στη βάση δεδομένων!'},
    'btn_ok':     {'en': 'OK', 'gr': 'ΕΝΤΑΞΕΙ'},
    'status_lost': {'en': 'Lost', 'gr': 'Χαμένο'},
    'status_found': {'en': 'Found', 'gr': 'Βρέθηκε'},
    'status_reunited': {'en': 'Reunited', 'gr': 'Επανενώθηκε'},
    'lbl_status': {'en': 'Status:', 'gr': 'Κατάσταση:'},
    'lbl_location': {'en': 'Location acquired!', 'gr': 'Τοποθεσία ενημερώθηκε!'},
    'lbl_photo': {'en': 'Photo selected!', 'gr': 'Φωτογραφία επιλέχθηκε!'},
    'search_hint': {'en': 'Search (Dog, Cat, etc.)', 'gr': 'Αναζήτηση (Σκύλος, Γάτα κλπ.)'},
    'filter_all': {'en': 'All', 'gr': 'Όλα'},
    'filter_lost': {'en': 'Lost Only', 'gr': 'Μόνο Χαμένα'},
    'filter_found': {'en': 'Found Only', 'gr': 'Μόνο Βρεθέντα'},
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
                    root.set_report_type('lost')
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
                    root.set_report_type('found')
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
            right_action_items: [["refresh", lambda x: root.load_reports()], ["filter", lambda x: root.show_filter_dialog()]]

        MDBoxLayout:
            orientation: 'vertical'

            MDTextField:
                id: search_field
                hint_text: app.txt_search_hint
                mode: "rectangle"
                size_hint_x: 1
                padding: "10dp"
                on_text: root.filter_reports(self.text)

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
                spacing: "15dp"
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

                MDTextField:
                    id: contact_info
                    hint_text: app.txt_hint_contact
                    helper_text: app.txt_help_contact
                    mode: "rectangle"

                MDLabel:
                    id: location_label
                    text: ""
                    halign: "center"
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: "30dp"

                MDFillRoundFlatButton:
                    text: app.txt_btn_gps
                    size_hint_x: 1
                    md_bg_color: 0.2, 0.6, 0.8, 1
                    icon: "crosshairs-gps"
                    on_release: root.request_gps_location()

                MDLabel:
                    id: photo_label
                    text: ""
                    halign: "center"
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: "30dp"

                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "10dp"
                    size_hint_y: None
                    height: "50dp"

                    MDFillRoundFlatButton:
                        text: app.txt_btn_photo
                        size_hint_x: 0.5
                        md_bg_color: 0.4, 0.2, 0.8, 1
                        icon: "camera"
                        on_release: root.capture_photo()

                    MDFillRoundFlatButton:
                        text: app.txt_btn_gallery
                        size_hint_x: 0.5
                        md_bg_color: 0.6, 0.2, 0.6, 1
                        icon: "image"
                        on_release: root.choose_photo()

                MDFillRoundFlatButton:
                    text: app.txt_btn_sub
                    size_hint_x: 1
                    md_bg_color: 0, 0.5, 1, 1
                    on_release: root.submit_report()
'''

class HomeScreen(Screen):
    def set_report_type(self, report_type):
        """Set whether this is a 'lost' or 'found' report"""
        app = MDApp.get_running_app()
        app.current_report_type = report_type

class MapScreen(Screen):
    all_reports = {}
    current_filter = 'all'

    def on_enter(self):
        self.load_reports()

    def load_reports(self):
        print("Fetching data from Firebase...")
        self.ids.mapview.clear_widgets()
        req = UrlRequest(
            f"{FIREBASE_URL}reports.json",
            on_success=self.on_request_success,
            on_failure=self.on_request_error,
            on_error=self.on_request_error
        )

    def on_request_success(self, req, result):
        if result:
            print(f"Found {len(result)} reports!")
            self.all_reports = result
            self.display_filtered_reports()
        else:
            print("No reports found.")

    def on_request_error(self, req, error):
        print(f"Error fetching: {error}")

    def display_filtered_reports(self):
        """Display reports based on current filter and search"""
        self.ids.mapview.clear_widgets()
        search_text = self.ids.search_field.text.lower()

        for key, report_data in self.all_reports.items():
            # Apply status filter
            if self.current_filter != 'all':
                report_status = report_data.get('status', 'lost')
                if report_status != self.current_filter:
                    continue

            # Apply search filter
            if search_text:
                searchable_text = f"{report_data.get('type', '')} {report_data.get('description', '')}".lower()
                if search_text not in searchable_text:
                    continue

            self.add_pin(report_data, key)

    def filter_reports(self, search_text):
        """Filter reports based on search text"""
        self.display_filtered_reports()

    def show_filter_dialog(self):
        """Show dialog to filter by status"""
        app = MDApp.get_running_app()

        if not hasattr(self, 'filter_dialog'):
            self.filter_dialog = MDDialog(
                title="Filter Reports",
                type="simple",
                items=[
                    FilterItem(text=app.txt_filter_all, filter_type='all', map_screen=self),
                    FilterItem(text=app.txt_filter_lost, filter_type='lost', map_screen=self),
                    FilterItem(text=app.txt_filter_found, filter_type='found', map_screen=self),
                ],
            )
        self.filter_dialog.open()

    def apply_filter(self, filter_type):
        """Apply status filter"""
        self.current_filter = filter_type
        self.display_filtered_reports()
        if hasattr(self, 'filter_dialog'):
            self.filter_dialog.dismiss()

    def add_pin(self, report_data, key):
        marker = MapMarkerPopup(lat=report_data['lat'], lon=report_data['lon'])

        # Determine marker color based on status
        status = report_data.get('status', 'lost')
        if status == 'lost':
            bg_color = (1, 0.9, 0.9, 1)  # Light red
        elif status == 'found':
            bg_color = (0.9, 1, 0.9, 1)  # Light green
        else:  # reunited
            bg_color = (0.9, 0.9, 1, 1)  # Light blue

        bubble = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            size_hint=(None, None),
            size=("250dp", "150dp"),
            md_bg_color=bg_color
        )

        label_type = MDLabel(text=f"Type: {report_data['type']}", theme_text_color="Primary")
        label_desc = MDLabel(text=report_data['description'], theme_text_color="Secondary", font_style="Caption")
        label_status = MDLabel(text=f"Status: {report_data.get('status', 'lost')}", theme_text_color="Secondary", font_style="Caption")

        bubble.add_widget(label_type)
        bubble.add_widget(label_desc)
        bubble.add_widget(label_status)

        if report_data.get('contact'):
            label_contact = MDLabel(text=f"Contact: {report_data['contact']}", theme_text_color="Primary", font_style="Caption")
            bubble.add_widget(label_contact)

        marker.add_widget(bubble)
        self.ids.mapview.add_marker(marker)

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

class FilterItem(MDBoxLayout):
    text = StringProperty()
    filter_type = StringProperty()
    map_screen = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = "48dp"

        btn = MDFlatButton(
            text=self.text,
            on_release=lambda x: self.map_screen.apply_filter(self.filter_type)
        )
        self.add_widget(btn)

class ReportScreen(Screen):
    current_lat = None
    current_lon = None
    photo_path = None

    def on_enter(self):
        """Reset fields when entering screen"""
        self.current_lat = None
        self.current_lon = None
        self.photo_path = None
        self.ids.location_label.text = ""
        self.ids.photo_label.text = ""

    def request_gps_location(self):
        """Request GPS location from device"""
        app = MDApp.get_running_app()

        if not GPS_AVAILABLE:
            print("GPS not available on this device")
            self.ids.location_label.text = "GPS not available - using default location"
            self.current_lat = 37.9838
            self.current_lon = 23.6500
            return

        try:
            gps.configure(on_location=self.on_gps_location, on_status=self.on_gps_status)
            gps.start(minTime=1000, minDistance=1)
            self.ids.location_label.text = "Getting location..."
        except Exception as e:
            print(f"GPS Error: {e}")
            self.ids.location_label.text = "GPS error - using default location"
            self.current_lat = 37.9838
            self.current_lon = 23.6500

    def on_gps_location(self, **kwargs):
        """Callback when GPS location is obtained"""
        app = MDApp.get_running_app()
        self.current_lat = kwargs.get('lat')
        self.current_lon = kwargs.get('lon')
        self.ids.location_label.text = app.txt_lbl_location
        print(f"GPS Location: {self.current_lat}, {self.current_lon}")
        gps.stop()

    def on_gps_status(self, stype, status):
        """Callback for GPS status updates"""
        print(f"GPS Status: {stype} - {status}")

    def capture_photo(self):
        """Capture photo using device camera"""
        app = MDApp.get_running_app()

        if not CAMERA_AVAILABLE:
            print("Camera not available on this device")
            self.ids.photo_label.text = "Camera not available"
            return

        try:
            camera.take_picture(
                filename='/tmp/findmystray_photo.jpg',
                on_complete=self.on_photo_captured
            )
        except Exception as e:
            print(f"Camera Error: {e}")
            self.ids.photo_label.text = "Camera error"

    def choose_photo(self):
        """Choose photo from gallery"""
        app = MDApp.get_running_app()

        if not CAMERA_AVAILABLE:
            print("File chooser not available")
            self.ids.photo_label.text = "Gallery not available"
            return

        try:
            filechooser.open_file(
                on_selection=self.on_photo_selected,
                filters=["*.jpg", "*.jpeg", "*.png"]
            )
        except Exception as e:
            print(f"File chooser Error: {e}")
            self.ids.photo_label.text = "Gallery error"

    def on_photo_captured(self, filepath):
        """Callback when photo is captured"""
        app = MDApp.get_running_app()
        self.photo_path = filepath
        self.ids.photo_label.text = app.txt_lbl_photo
        print(f"Photo captured: {filepath}")

    def on_photo_selected(self, selection):
        """Callback when photo is selected from gallery"""
        app = MDApp.get_running_app()
        if selection:
            self.photo_path = selection[0]
            self.ids.photo_label.text = app.txt_lbl_photo
            print(f"Photo selected: {self.photo_path}")

    def submit_report(self):
        app = MDApp.get_running_app()
        pet_type = self.ids.pet_type.text
        description = self.ids.description.text
        contact_info = self.ids.contact_info.text

        if not pet_type or not description:
            return

        # Use GPS location if available, otherwise use random location
        if self.current_lat and self.current_lon:
            report_lat = self.current_lat
            report_lon = self.current_lon
        else:
            report_lat = 37.9838 + random.uniform(-0.005, 0.005)
            report_lon = 23.6500 + random.uniform(-0.005, 0.005)

        # Get current timestamp
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Get report type (lost or found)
        report_status = getattr(app, 'current_report_type', 'lost')

        report_data = {
            "type": pet_type,
            "description": description,
            "contact": contact_info if contact_info else "Not provided",
            "lat": report_lat,
            "lon": report_lon,
            "date": current_time,
            "status": report_status
        }

        # Add photo if available (convert to base64 for Firebase)
        if self.photo_path:
            try:
                with open(self.photo_path, 'rb') as f:
                    photo_data = base64.b64encode(f.read()).decode('utf-8')
                    report_data['photo'] = photo_data[:10000]  # Limit size
            except Exception as e:
                print(f"Error encoding photo: {e}")

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
        self.ids.contact_info.text = ""
        self.ids.location_label.text = ""
        self.ids.photo_label.text = ""
        self.current_lat = None
        self.current_lon = None
        self.photo_path = None

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
    txt_hint_contact = StringProperty()
    txt_help_contact = StringProperty()
    txt_btn_photo = StringProperty()
    txt_btn_gallery = StringProperty()
    txt_btn_gps = StringProperty()
    txt_btn_sub = StringProperty()
    txt_alert_tit = StringProperty()
    txt_alert_txt = StringProperty()
    txt_btn_ok = StringProperty()
    txt_lbl_location = StringProperty()
    txt_lbl_photo = StringProperty()
    txt_search_hint = StringProperty()
    txt_filter_all = StringProperty()
    txt_filter_lost = StringProperty()
    txt_filter_found = StringProperty()

    current_report_type = 'lost'

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
        self.txt_hint_contact = TRANS['hint_contact'][self.current_lang]
        self.txt_help_contact = TRANS['help_contact'][self.current_lang]
        self.txt_btn_photo = TRANS['btn_photo'][self.current_lang]
        self.txt_btn_gallery = TRANS['btn_gallery'][self.current_lang]
        self.txt_btn_gps = TRANS['btn_gps'][self.current_lang]
        self.txt_btn_sub = TRANS['btn_sub'][self.current_lang]
        self.txt_alert_tit = TRANS['alert_tit'][self.current_lang]
        self.txt_alert_txt = TRANS['alert_txt'][self.current_lang]
        self.txt_btn_ok = TRANS['btn_ok'][self.current_lang]
        self.txt_lbl_location = TRANS['lbl_location'][self.current_lang]
        self.txt_lbl_photo = TRANS['lbl_photo'][self.current_lang]
        self.txt_search_hint = TRANS['search_hint'][self.current_lang]
        self.txt_filter_all = TRANS['filter_all'][self.current_lang]
        self.txt_filter_lost = TRANS['filter_lost'][self.current_lang]
        self.txt_filter_found = TRANS['filter_found'][self.current_lang]

if __name__ == '__main__':
    FindMyStrayApp().run()
