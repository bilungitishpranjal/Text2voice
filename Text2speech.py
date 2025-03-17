from tkinter import *
from tkinter import filedialog
from PIL import Image as PILImage
import pyttsx3
import pytesseract
import speech_recognition as sr
import cv2

# Initialize main window
root = Tk()
root.title("OCR App")
root.geometry("400x400")
root.config(bg="Black")

# Variable to store extracted text
extracted_text = ""

label_text = StringVar()
label_text.set("Welcome to OCR App")

label = Label(root, textvariable=label_text, font=("Arial", 12))
label.pack(pady=10)

# Function to upload and extract text
def upload():
    global extracted_text
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if file_path:
        extracted_text = extract_text(file_path)
        label_text.set("Text Extracted")

# Function to extract text from image
def extract_text(image_path):
    img = PILImage.open(image_path)
    return pytesseract.image_to_string(img)

# Function to speak extracted text
def speak_text():
    global extracted_text
    if extracted_text:
        engine = pyttsx3.init()
        engine.say(extracted_text)
        engine.runAndWait()
    else:
        label_text.set("No text extracted!")

# Function to open camera
def open_camera():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

# Function for voice command
def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        label_text.set("Listening...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            process_command(command)
        except sr.UnknownValueError:
            label_text.set("Could not understand, try again.")
        except sr.RequestError as e:
            label_text.set(f"Error: {e}")

# Function to process commands
def process_command(command):
    if command == "start":
        speak_text()
    elif command == "upload":
        upload()
    elif command == "camera":
        open_camera()
    else:
        label_text.set("Unknown Command.")

# Buttons
Button(root, text="📸 Open Camera", command=open_camera, font=("Arial", 12)).pack(pady=5)
Button(root, text="📂 Upload Image", command=upload, font=("Arial", 12)).pack(pady=5)
Button(root, text="🔊 Speak Extracted Text", command=speak_text, font=("Arial", 12)).pack(pady=5)
Button(root, text="🎤 Voice Command", command=listen_for_commands, font=("Arial", 12)).pack(pady=5)
Button(root, text="Exit", command=root.quit, font=("Arial", 12)).pack(pady=5)

root.mainloop()
