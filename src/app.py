import customtkinter as ctk
from tkinter import filedialog
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# =========================
# LOAD MODEL
# =========================
model = tf.keras.models.load_model(
    "D:/leaf-disease-detection/src/leaf_disease_model.h5",
    compile=False
)

# =========================
# CLASSES
# =========================
classes = [
    "Apple Scab","Apple Black Rot","Apple Cedar Rust","Apple Healthy",
    "Blueberry Healthy","Cherry Healthy","Cherry Powdery Mildew",
    "Corn Cercospora","Corn Rust","Corn Healthy","Corn Blight",
    "Grape Black Rot","Grape Esca","Grape Healthy","Grape Leaf Blight",
    "Orange Greening","Peach Bacterial Spot","Peach Healthy",
    "Pepper Bacterial Spot","Pepper Healthy","Potato Early Blight",
    "Potato Healthy","Potato Late Blight","Raspberry Healthy",
    "Soybean Healthy","Squash Powdery Mildew","Strawberry Healthy",
    "Strawberry Leaf Scorch","Tomato Bacterial Spot",
    "Tomato Early Blight","Tomato Healthy","Tomato Late Blight",
    "Tomato Leaf Mold","Tomato Septoria","Tomato Spider Mites",
    "Tomato Target Spot","Tomato Mosaic Virus","Tomato Yellow Leaf Curl"
]

# =========================
# TREATMENTS
# =========================
treatments = {
    "Apple Scab" : "Apply fungicides like captan; remove fallen infected leaves to prevent spread.",
    "Apple Black Rot": "Prune infected branches and use copper-based fungicides.",
    "Apple Cedar Rust" : "Use fungicides and remove nearby cedar/juniper hosts.",
    "Apple Healthy":"No treatment required.maintain proper care and monitoring.",
    "default": "Maintain good plant care and hygiene.",
    "Blueberry Healthy":"No treatment needed; ensure proper irrigation and soil pH.",
    "Cherry Healthy":"No treatment required; maintain good orchard hygiene.",
    "Cherry Powdery Mildew":"Apply sulfur fungicide and improve air circulation.",
    "Corn Cercospora (Leaf Spot)":"Use resistant varieties and apply fungicides if severe.",
    "Corn Rust":"Apply fungicides and grow resistant hybrids.",
    "Corn Healthy":"No treatment required; follow balanced fertilization.",
    "Corn Blight":"Remove infected debris and use fungicide sprays.",
    "Grape Black Rot":"Remove infected parts and apply fungicides regularly.",
    "Grape Esca (Black Measles)":"Prune infected wood and avoid water stress.",
    "Grape Healthy":"No treatment needed; maintain vineyard hygiene.",
    "Grape Leaf Blight":"Use fungicides and ensure proper spacing for airflow.",
    "Orange Greening (Huanglongbing)":"Control psyllid insects and remove infected trees.",
    "Peach Bacterial Spot":"Use copper sprays and resistant varieties.",
    "Peach Healthy":"No treatment required; regular monitoring is enough.",
    "Pepper Bacterial Spot":"Use disease-free seeds and apply copper fungicides.",
    "Pepper Healthy":"No treatment needed; maintain proper watering.",
    "Potato Early Blight":"Apply fungicides and rotate crops regularly.",
    "Potato Healthy":"No treatment required; maintain soil health.",
    "Potato Late Blight":"Use resistant varieties and apply fungicides immediately.",
    "Raspberry Healthy":"No treatment needed; ensure proper pruning.",
    "Strawberry Healthy":"No treatment required; maintain clean beds.",
    "Strawberry Leaf Scorch":"Remove infected leaves and apply fungicides.",
    "Soybean Healthy":"No treatment needed; maintain proper irrigation.",
    "Squash Powdery Mildew":"Apply sulfur fungicides and reduce humidity.",
    "Tomato Bacterial Spot":"Use copper sprays and avoid overhead watering.",
    "Tomato Early Blight":"Remove infected leaves and apply fungicide.",
    "Tomato Healthy":"No treatment required; maintain proper spacing.",
    "Tomato Late Blight":"Apply fungicides and remove infected plants quickly.",
    "Tomato Leaf Mold":"Improve ventilation and reduce humidity.",
    "Tomato Septoria":"Remove lower infected leaves and apply fungicide.",
    "Tomato Spider Mites":"Spray neem oil or insecticidal soap.",
    "Tomato Target Spot":"Apply fungicides and avoid leaf wetness.",
    "Tomato Mosaic Virus":"Remove infected plants and disinfect tools.",
    "Tomato Yellow Leaf Curl":"Control whiteflies and remove infected plants."
}

# =========================
# PREPROCESS
# =========================
def preprocess(img):
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# =========================
# LEAF DETECTION
# =========================
def is_leaf_present(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([25, 40, 40])
    upper = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    ratio = np.sum(mask > 0) / (img.shape[0]*img.shape[1])
    return ratio > 0.05

# =========================
# PREDICTION
# =========================
def predict_image(img):
    try:
        original = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        if not is_leaf_present(original):
            result_label.configure(text="No leaf detected ❌", text_color="red")
    
            # 🔥 CLEAR OLD DATA
            confidence_label.configure(text="")
            status_label.configure(text="")
            treatment_label.configure(text="")
    
            return


        processed = preprocess(original)
        preds = model.predict(processed)

        idx = np.argmax(preds)
        confidence = float(np.max(preds))
        predicted_class = classes[idx] if idx < len(classes) else "Unknown"

        # Fix index error
        if idx >= len(classes):
            result_label.configure(text="Model error ❌")
            return

        # Status
        if "healthy" in predicted_class.lower():
            status = "Healthy"
            color = "lightgreen"
        else:
            status = "Diseased"
            color = "red"

        # Treatment
        treatment = treatments.get(predicted_class, treatments["default"])

        # UI Update
        result_label.configure(text=predicted_class, text_color="white")
        confidence_label.configure(text=f"{confidence*100:.2f}% Confidence")
        status_label.configure(text=status, text_color=color)
        treatment_label.configure(text=f"💊 {treatment}")

    except Exception as e:
        print("Error:", e)
        result_label.configure(text="Error ❌", text_color="red")

        confidence_label.configure(text="")
        status_label.configure(text="")
        treatment_label.configure(text="")
# =========================
# IMAGE DISPLAY
# =========================
def display_image(img):
    img = cv2.resize(img, (250, 250))
    img = Image.fromarray(img)
    img = ctk.CTkImage(light_image=img, size=(250, 250))
    image_label.configure(image=img, text="")
    image_label.image = img

# =========================
# UPLOAD
# =========================
def upload_image():
    path = filedialog.askopenfilename()
    if path:
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        display_image(img)
        predict_image(img)

# =========================
# CAMERA
# =========================
camera_on = False

def start_camera():
    global camera_on, cap
    camera_on = True
    cap = cv2.VideoCapture(0)
    update_camera()

def stop_camera():
    global camera_on
    camera_on = False
    cap.release()

def update_camera():
    if camera_on:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            display_image(frame)
            current_frame[0] = frame
        app.after(10, update_camera)

def capture_image():
    stop_camera()
    img = current_frame[0]
    if img is not None:
        predict_image(img)

current_frame = [None]

# =========================
# UI SETUP
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("900x700")
app.title("🌿 AI Plant Detector")

# =========================
# BACKGROUND
# =========================
bg = ctk.CTkImage(
    light_image=Image.open("D:/leaf-disease-detection/bg.jpg"),
    size=(900,700)
)

bg_label = ctk.CTkLabel(app, image=bg, text="")
bg_label.image = bg
bg_label.place(x=0,y=0,relwidth=1,relheight=1)

# =========================
# MAIN PANEL
# =========================
frame = ctk.CTkFrame(
    app,
    fg_color="#0f3d1c",
    width=700,
    height=600
)

frame.place(relx=0.5, rely=0.5, anchor="center")


# =========================
# TITLE
# =========================
title = ctk.CTkLabel(frame, text="🌿 Plant Disease Detector",
                     font=("Arial",28,"bold"), text_color="white")
title.pack(pady=15)

# =========================
# IMAGE
# =========================
image_label = ctk.CTkLabel(frame, text="Upload Image",
                          width=250,height=250, fg_color="#2e7d32")
image_label.pack(pady=10)

# =========================
# BUTTONS
# =========================
btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame,text="📁 Upload",command=upload_image).grid(row=0,column=0,padx=10)
ctk.CTkButton(btn_frame,text="📷 Camera",command=start_camera).grid(row=0,column=1,padx=10)
ctk.CTkButton(btn_frame,text="📸 Capture",command=capture_image).grid(row=0,column=2,padx=10)
ctk.CTkButton(btn_frame,text="❌ Stop",command=stop_camera).grid(row=0,column=3,padx=10)

# =========================
# RESULTS
# =========================
result_label = ctk.CTkLabel(frame,text="Prediction",
                            font=("Arial",20,"bold"),text_color="white")
result_label.pack(pady=5)

confidence_label = ctk.CTkLabel(frame,text="")
confidence_label.pack()

status_label = ctk.CTkLabel(frame,text="",font=("Arial",18))
status_label.pack(pady=5)

treatment_label = ctk.CTkLabel(frame,text="",wraplength=500)
treatment_label.pack(pady=10)

# =========================
app.mainloop()
