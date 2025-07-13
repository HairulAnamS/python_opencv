import cv2

# Muat model deteksi wajah dari OpenCV (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Buka kamera (0 = default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera tidak dapat dibuka")
    exit()

frame_width = int(cap.get(3))  # biasanya 640
frame_height = int(cap.get(4))  # biasanya 480

def map_range(value, left_min, left_max, right_min, right_max):
    # Fungsi seperti map() di Arduino
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return int(right_min + (value_scaled * right_span))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal mengambil frame")
        break

    # Ubah ke grayscale agar deteksi wajah lebih efektif
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Deteksi wajah
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Gambar kotak di wajah
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Hitung titik tengah
        center_x = x + w // 2
        center_y = y + h // 2

        # Konversi koordinat ke sudut servo
        servo_x = map_range(center_x, 0, frame_width, 0, 180)
        servo_y = map_range(center_y, 0, frame_height, 0, 180)

        # Gambar titik tengah (lingkaran kecil merah)
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

        # (Opsional) Tambahkan label koordinat
        cv2.putText(frame, f'({center_x}, {center_y})', (center_x + 10, center_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(frame, f"Servo: {servo_x}, {servo_y}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Tampilkan hasilnya
    cv2.imshow('Deteksi Wajah', frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan dan tutup
cap.release()
cv2.destroyAllWindows()
