# GUI for Machine Learning Application

The GUI is made with Python and PyQt5/Qt Designer.

## About the GUI

The GUI primarily contains two independent ML applications merged together:
- Hand gesture recognizer
- Activity tracker and analyzer

The ML side of the application utilizes the Mediapipe API to ensure lightweight application.

## Dependencies

This project is actually not intended to be used as a shared application. However, if you want to give it a try, you can setup your own Firebase project.
You will also need to install the dependencies listed below using `pip install`.
- `Pyrebase4`
- `firebase_admin`
- `mediapipe`
- `opencv-python`
- `pyqt5`
- `matplotlib`

## What's Inside

### Login and Signup Page
The authentication is done using Google Firebase, so we can focus on the application logic and styling.

![login](https://github.com/vincadrn/pyqt5-gui/assets/42486755/45e80f9c-54ee-4ac5-897f-cf567d21e190)
![signup](https://github.com/vincadrn/pyqt5-gui/assets/42486755/97ad4e5a-9978-4e69-a5a0-724be13a5343)

### Home Page
This is the home page of the GUI after logging in.

![home_profile](https://github.com/vincadrn/pyqt5-gui/assets/42486755/9e60c429-5a2b-4add-8646-2e7de8e84431)

### Hand Gesture Recognition
Hand gestures can be trained and then be recognized. The recognition is based on the matrix distance of every points in the hand.

![hand_train](https://github.com/vincadrn/pyqt5-gui/assets/42486755/45c495bc-0246-4319-87d0-0c9977ddaec2)
![hand_recog](https://github.com/vincadrn/pyqt5-gui/assets/42486755/f72fb5e6-317d-47a0-b9d0-26d8c3c077e6)

## Activity Tracker
Activity tracker is intended to detect activities that are caught inside the region of intereset (RoI). The simple statistics is provided in the app beside the camera feed and the user obtains the graph that summarize the activities.

![activity](https://github.com/vincadrn/pyqt5-gui/assets/42486755/29a23b2b-ebe6-4de7-ae2b-7b7bf26d0f59)
![activity_graph](https://github.com/vincadrn/pyqt5-gui/assets/42486755/ac592bde-6a52-4b5f-8d4f-2dd8dda70bcc)


## Acknowledgments

The GUI is made possible by collaboration with @wiryanatasunardi and Evelio, outside of Github.
