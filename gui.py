import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy as np
from keras.models import load_model

# Load mô hình đã huấn luyện
model = load_model('my_model.h5')

# Từ điển gán nhãn các lớp biển báo
classes = {
    1: 'Speed limit (20km/h)', 2: 'Speed limit (30km/h)', 3: 'Speed limit (50km/h)',
    4: 'Speed limit (60km/h)', 5: 'Speed limit (70km/h)', 6: 'Speed limit (80km/h)',
    7: 'End of speed limit (80km/h)', 8: 'Speed limit (100km/h)', 9: 'Speed limit (120km/h)',
    10: 'No passing', 11: 'No passing veh over 3.5 tons', 12: 'Right-of-way at intersection',
    13: 'Priority road', 14: 'Yield', 15: 'Stop', 16: 'No vehicles', 
    17: 'Veh > 3.5 tons prohibited', 18: 'No entry', 19: 'General caution',
    20: 'Dangerous curve left', 21: 'Dangerous curve right', 22: 'Double curve', 
    23: 'Bumpy road', 24: 'Slippery road', 25: 'Road narrows on the right', 
    26: 'Road work', 27: 'Traffic signals', 28: 'Pedestrians', 29: 'Children crossing', 
    30: 'Bicycles crossing', 31: 'Beware of ice/snow', 32: 'Wild animals crossing', 
    33: 'End speed + passing limits', 34: 'Turn right ahead', 35: 'Turn left ahead', 
    36: 'Ahead only', 37: 'Go straight or right', 38: 'Go straight or left', 
    39: 'Keep right', 40: 'Keep left', 41: 'Roundabout mandatory', 42: 'End of no passing', 
    43: 'End no passing veh > 3.5 tons'
}

# Khởi tạo GUI
top = tk.Tk()
top.geometry('1000x700')  # Tăng kích thước giao diện
top.title('Nhận dạng biển báo giao thông')

# Đặt hình nền
background_image = Image.open("background.png")  # Đảm bảo bạn có hình ảnh nền "background.jpg"
background_image = background_image.resize((1000, 700), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

bg_label = Label(top, image=background_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Thiết lập font chữ
large_font = ('Arial', 20, 'bold')
medium_font = ('Arial', 15)
button_font = ('Arial', 12, 'bold')

# Tạo không gian hiển thị biển báo
label = Label(top, background='#ffffff', font=large_font, pady=20, wraplength=600)  # Tăng kích thước font và padding
label.pack(side=BOTTOM, expand=True)

# Nơi chứa hình ảnh biển báo
sign_image = Label(top)
sign_image.pack(side=BOTTOM, expand=True)

# Hàm phân loại biển báo
def classify(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((30, 30))  # Điều chỉnh kích thước ảnh về 30x30 pixel
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    
    # Dự đoán biển báo
    pred_probabilities = model.predict(image)[0]
    pred = pred_probabilities.argmax(axis=-1)
    sign = classes[pred + 1]
    label.configure(foreground='#011638', text=sign)

# Hiển thị nút "Nhận dạng"
def show_classify_button(file_path):
    classify_b = Button(top, text="Nhận dạng", command=lambda: classify(file_path), padx=20, pady=10)
    classify_b.configure(background='#FF5733', foreground='white', font=button_font, borderwidth=2)
    classify_b.place(relx=0.75, rely=0.55)

# Hàm tải ảnh
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass

# Nút upload hình ảnh
upload = Button(top, text="Tải ảnh lên", command=upload_image, padx=20, pady=10)
upload.configure(background='#28A745', foreground='white', font=button_font, borderwidth=2)
upload.pack(side=BOTTOM, pady=50)

# Tiêu đề ứng dụng
heading = Label(top, text="Nhận dạng biển báo giao thông", pady=20, font=large_font)
heading.configure(background='#ffffff', foreground='#364156')
heading.pack()

# Vòng lặp chính của ứng dụng
top.mainloop()
