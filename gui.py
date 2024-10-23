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
    1: 'Giới hạn tốc độ (20km/h)', 2: 'Giới hạn tốc độ (30km/h)', 3: 'Giới hạn tốc độ (50km/h)',
    4: 'Giới hạn tốc độ (60km/h)', 5: 'Giới hạn tốc độ (70km/h)', 6: 'Giới hạn tốc độ (80km/h)',
    7: 'Kết thúc giới hạn tốc độ (80km/h)', 8: 'Giới hạn tốc độ (100km/h)', 9: 'Giới hạn tốc độ (120km/h)',
    10: 'Cấm vượt', 11: 'Cấm vượt với xe trên 3.5 tấn', 12: 'Quyền ưu tiên tại giao lộ',
    13: 'Đường ưu tiên', 14: 'Nhường đường', 15: 'Dừng lại', 16: 'Cấm xe',
    17: 'Cấm xe trên 3.5 tấn', 18: 'Cấm vào', 19: 'Chú ý chung',
    20: 'Khúc cua nguy hiểm bên trái', 21: 'Khúc cua nguy hiểm bên phải', 22: 'Hai khúc cua',
    23: 'Đường gồ ghề', 24: 'Đường trơn', 25: 'Đường hẹp bên phải',
    26: 'Công trình đường bộ', 27: 'Tín hiệu giao thông', 28: 'Người đi bộ',
    29: 'Trẻ em qua đường', 30: 'Người đi xe đạp qua đường', 31: 'Chú ý băng tuyết', 32: 'Động vật hoang dã qua đường',
    33: 'Kết thúc giới hạn tốc độ và cấm vượt', 34: 'Rẽ phải phía trước', 35: 'Rẽ trái phía trước',
    36: 'Chỉ được đi thẳng', 37: 'Đi thẳng hoặc rẽ phải', 38: 'Đi thẳng hoặc rẽ trái',
    39: 'Giữ bên phải', 40: 'Giữ bên trái', 41: 'Bắt buộc đi vòng', 42: 'Kết thúc cấm vượt',
    43: 'Kết thúc cấm vượt với xe trên 3.5 tấn'
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
