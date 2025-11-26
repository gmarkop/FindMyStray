# FindMyStray (Korydallos)

A bilingual (English/Greek) mobile application for tracking and reporting stray animals in Korydallos, Greece. The app allows users to report lost pets, found strays, and view real-time locations of all reports on an interactive map.

## Features

- **Report Lost Pets**: Submit information about your lost pet with description and location
- **Report Found Strays**: Document stray animals you've encountered
- **GPS Location Detection**: Automatically capture your current location using device GPS
- **Photo Capture**: Take photos with your camera or choose from gallery to include with reports
- **Contact Information**: Add phone number or email for people to reach you
- **Pet Status Tracking**: Track status of pets (Lost, Found, or Reunited)
- **Search & Filter**: Search reports by keywords and filter by status (Lost/Found)
- **Live Map View**: Interactive map showing all active pet/stray reports with color-coded markers
- **Bilingual Interface**: Seamlessly switch between English and Greek languages
- **Cloud Database**: All reports are stored in Firebase Realtime Database for real-time synchronization
- **Location-Based**: Automatic geocoding around Korydallos area (37.9838°N, 23.6500°E)

## Screenshots

The app features three main screens:
- **Home Screen**: Main menu with options to report pets or view the map
- **Map Screen**: Interactive map displaying all active reports with markers
- **Report Screen**: Form to submit pet details (type, description)

## Requirements

- Python 3.7+
- KivyMD (Material Design components for Kivy)
- Kivy framework
- kivy-garden.mapview (for map functionality)
- Plyer (for GPS, camera, and file chooser functionality)
- Buildozer (for building Android APK)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/gmarkop/FindMyStray.git
cd FindMyStray
```

2. Install dependencies:
```bash
pip install kivymd
pip install kivy-garden.mapview
pip install kivy
pip install plyer
```

3. For building Android APK:
```bash
pip install buildozer
```

4. Configure Firebase:
   - Create a Firebase Realtime Database
   - Update the `FIREBASE_URL` in `main.py` (line 19) with your Firebase database URL

## Configuration

### Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Realtime Database
4. Copy your database URL (format: `https://your-project.firebasedatabase.app/`)
5. Update line 19 in `main.py`:
```python
FIREBASE_URL = "https://your-project.firebasedatabase.app/"
```

### Customizing Location

The default location is set to Korydallos, Greece. To change the default location:
- Update `MapScreen` coordinates (lines 111-113)
- Update `ReportScreen` random location generation (lines 211-212)

## Usage

Run the application:
```bash
python main.py
```

### User Guide

1. **Reporting a Pet**:
   - Tap "I LOST MY PET" or "I FOUND A STRAY" on the home screen
   - Enter the pet type (e.g., Dog, Cat)
   - Provide a detailed description
   - **NEW**: Add your contact information (phone/email)
   - **NEW**: Tap "GET MY LOCATION" to use GPS for accurate location
   - **NEW**: Tap "CAPTURE PHOTO" to take a photo or "CHOOSE FROM GALLERY" to select one
   - Submit the report

2. **Viewing Reports**:
   - Tap "VIEW LIVE MAP" on the home screen
   - **NEW**: Use the search bar to find specific pets (e.g., "Dog", "Black cat")
   - **NEW**: Tap the filter icon to show only Lost or Found pets
   - Browse map markers to see reported pets (color-coded by status)
   - Tap markers to view pet details including contact information
   - Use the refresh button to update the map

3. **Language Toggle**:
   - Tap the web icon in the top-right corner to switch languages

4. **Building for Android**:
   - See [BUILD.md](BUILD.md) for detailed instructions on creating an APK

## Project Structure

```
FindMyStray/
├── main.py                 # Main application file
├── buildozer.spec          # Android build configuration
├── BUILD.md                # APK build instructions
└── README.md               # This file
```

## Technologies Used

- **Kivy**: Cross-platform Python framework for developing multitouch applications
- **KivyMD**: Material Design components for Kivy
- **Firebase Realtime Database**: Cloud-hosted NoSQL database for real-time data storage
- **kivy-garden.mapview**: Map widget with marker support
- **Plyer**: Platform-independent API for accessing hardware features (GPS, Camera)
- **Buildozer**: Tool for packaging Kivy apps for Android

## Data Structure

Reports are stored in Firebase with the following structure:
```json
{
  "reports": {
    "unique_id": {
      "type": "Dog",
      "description": "Black Kokoni",
      "contact": "6912345678",
      "lat": 37.9838,
      "lon": 23.6500,
      "date": "26/11/2025 14:30",
      "status": "lost",
      "photo": "base64_encoded_image_data"
    }
  }
}
```

### Field Descriptions:
- **type**: Type of animal (Dog, Cat, etc.)
- **description**: Detailed description of the pet
- **contact**: Phone number or email for contact
- **lat/lon**: GPS coordinates of the report
- **date**: Timestamp when report was created
- **status**: Current status (lost, found, or reunited)
- **photo**: Base64-encoded image data (optional)

## Language Support

The application supports two languages:
- English (en)
- Greek (gr)

Default language: Greek

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Recent Enhancements (v1.0.0)

✅ **Implemented Features:**
- GPS-based automatic location detection
- Photo capture and upload functionality
- Contact information for pet owners
- Pet status tracking (lost/found/reunited)
- Search and filter functionality
- Color-coded map markers by status

## Future Enhancements

Potential features for future versions:
- User authentication and user profiles
- Push notifications for nearby reports
- In-app messaging between users
- Pet breed database with auto-suggestions
- Multi-language support beyond English/Greek
- Social media sharing of reports
- Report history and analytics
- Offline mode with sync when online

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## Acknowledgments

- Built with KivyMD for Material Design UI components
- Location services for Korydallos, Greece
- Firebase for real-time database functionality
