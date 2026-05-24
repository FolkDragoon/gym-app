import qrcode
import os

QR_DIR = "assets/qr_codes"
os.makedirs(QR_DIR, exist_ok=True)

def generate_qr(qr_value: str, member_name: str):
    img = qrcode.make(qr_value)
    path = f"{QR_DIR}/{member_name}_{qr_value[:8]}.png"
    img.save(path)
    return path