import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
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
top.geometry('1000x700')
top.title('Nhận dạng biển báo giao thông')

# Đặt hình nền
bg_image = Image.open("background.jpg")  # Thay "background.jpg" bằng đường dẫn ảnh của bạn
bg_image = bg_image.resize((1000, 700), Image.LANCZOS)  # Điều chỉnh kích thước cho phù hợp
bg_photo = ImageTk.PhotoImage(bg_image)

# Label hình nền
background_label = tk.Label(top, image=bg_photo)
background_label.place(relwidth=1, relheight=1)  # Phủ đầy toàn bộ cửa sổ

# Thiết lập font chữ
large_font = ('Arial', 20, 'bold')
button_font = ('Arial', 12, 'bold')

# Tiêu đề ứng dụng
heading = tk.Label(top, text="Nhận dạng biển báo giao thông", font=large_font, bg='#ffffff', fg='#364156', wraplength=500)
heading.place(relx=0.5, y=30, anchor='n')  # Căn giữa theo chiều ngang

# Nơi chứa hình ảnh biển báo
sign_image = tk.Label(top, bg='#ffffff')
sign_image.place(x=100, y=100)  # Điều chỉnh vị trí

# Khu vực hiển thị kết quả
label = tk.Label(top, bg='#ffffff', font=large_font, wraplength=400, fg='#011638')
label.place(x=550, y=250)  # Điều chỉnh vị trí

# Khung chứa các nút
button_frame = tk.Frame(top, bg='#072541')
button_frame.place(x=850, y=100)  # Điều chỉnh vị trí

# Nút tải ảnh lên
upload_frame = tk.Frame(button_frame, bg='#f0f0f0')  # Tạo frame cho nút "Tải ảnh lên"
upload_frame.pack(side='top', pady=(0, 10))  # Điều chỉnh khoảng cách bên dưới nút "Tải ảnh lên"

upload = tk.Button(upload_frame, text="Tải ảnh lên", command=lambda: upload_image(), padx=20, pady=10, bg='#28A745', fg='white', font=button_font)
upload.pack()

# Nút Nhận dạng sẽ hiển thị ngay bên dưới sau khi tải ảnh
def show_classify_button(file_path):
    # Xóa các nút "Nhận dạng" cũ
    for widget in button_frame.winfo_children():
        if isinstance(widget, tk.Frame) and widget != upload_frame:
            widget.pack_forget()
    
    # Thêm frame và nút "Nhận dạng"
    classify_frame = tk.Frame(button_frame, bg='#f0f0f0')  # Tạo frame cho nút "Nhận dạng"
    classify_frame.pack(side='top')  # Đặt bên dưới nút "Tải ảnh lên" mà không gây khoảng cách với nền

    classify_b = tk.Button(classify_frame, text="Nhận dạng", command=lambda: classify(file_path), padx=20, pady=10, bg='#FF5733', fg='white', font=button_font)
    classify_b.pack()

# Hàm tải ảnh
def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        uploaded = Image.open(file_path)
        display_image = uploaded.resize((400, 400), Image.LANCZOS)
        im = ImageTk.PhotoImage(display_image)
        sign_image.configure(image=im)
        sign_image.image = im  # Giữ tham chiếu để tránh bị xóa
        label.configure(text='')
        show_classify_button(file_path)

# Hàm phân loại biển báo
def classify(file_path):
    image = Image.open(file_path)
    image = image.resize((30, 30))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    
    # Dự đoán biển báo
    pred_probabilities = model.predict(image)[0]
    pred = pred_probabilities.argmax(axis=-1)
    sign = classes.get(pred + 1, "Unknown")
    label.configure(text=sign)

# Bắt đầu vòng lặp GUI
top.mainloop()
