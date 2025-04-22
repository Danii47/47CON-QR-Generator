from config import EMAIL_USER, EMAIL_APP_PASSWORD, BANNER_IMAGE_PATH
import qrcode
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import csv
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

def read_csv(csv_file, column_names):
  with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    try:
      column = [[row[column_name] for column_name in column_names] for row in reader]

    except Exception as e:
      print(f"Column name not found in CSV file. {e}")
      return None

  return column

def send_mail(from_email, to_email, subject, body, img_bytes):
  message = MIMEMultipart("related")
  message["From"] = from_email
  message["To"] = to_email
  message["Subject"] = subject
  msg_alternative = MIMEMultipart("alternative")
  msg_alternative.attach(MIMEText(body, "html"))
  message.attach(msg_alternative)
  
  
  qr_image = MIMEImage(img_bytes, _subtype="png")
  qr_image.add_header("Content-Disposition", "attachment", filename="ENTRADA_47CON.png")
  message.attach(qr_image)

  # Imagen incrustada: el banner (se busca y se incrusta aquí)
  try:
      with open(BANNER_IMAGE_PATH, "rb") as f:
          banner_data = f.read()
          banner = MIMEImage(banner_data)
          banner.add_header("Content-ID", "<banner>")
          banner.add_header("Content-Disposition", "inline", filename="BANNER_SUGUS.png")
          message.attach(banner)
  except FileNotFoundError as e:
      print("Banner image file not found: ", e)
  
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
  server.sendmail(from_email, to_email, message.as_string())
  server.quit()
  
  
def generate_qr(data):
  qr = qrcode.QRCode(
      error_correction=qrcode.constants.ERROR_CORRECT_L,  # nivel de corrección de errores
      box_size=10,  # tamaño de cada "cuadradito"
      border=3,  # borde blanco alrededor del QR
  )

  qr.add_data(data)
  qr.make(fit=True)

  img = qr.make_image(fill_color="black", back_color="white")

  buffer = BytesIO()
  img.save(buffer, format="PNG")
  buffer.seek(0)
  
  return buffer.read()

def sha256(data):
  hash_object = hashlib.sha256(data.encode())
  hash_hex = hash_object.hexdigest()
  return hash_hex

def get_email_body(user_name):
  return f"""
    <html>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">
      </head>
      <body style="color: black; font-family: 'Trebuchet MS', sans-serif; font-size: 1.3rem">
        <div style="text-align: center;">
          <img src="cid:banner" style="width: 100%; max-width: 600px; height: auto;" alt="Banner SUGUS">
        </div>
        <h1 style="font-size: 5vw">Tu entrada para la 47CON</h1>
        <p>Hola, {user_name}, aquí tienes tu entrada para el evento. Deberá ser mostrada para realizar el acceso.</p>
        <p>
          <h3>Detalles del evento:</h3>
          <b>Fechas y horario:</b>
          <ul>
            <li>25 de abril, 2025: 08:30h - 20:30h</li>
            <li>26 de abril, 2025: 10:00h - 15:00h</li>
          </ul>
          <b>Ubicación:</b> <a href="https://maps.app.goo.gl/YsyVtZ4maHd4ck5V9">Escuela de Ingeniería Informática de la Universidad de Valladolid</a>
          <br>
          <i>Puedes consultar el resto de informacion como el horario y las ponencias en nuestra página: <a href="https://sugusuva.es/47CON" target="_blank">SUGUS</a></i>
        </p>
      </body>
    </html>
  """

def pad(s):
  pad_len = 16 - len(s) % 16
  return s + chr(pad_len) * pad_len

def encrypt(data, key):
  iv = get_random_bytes(16)
  cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)
  padded_data = pad(data)
  encrypted_bytes = cipher.encrypt(padded_data.encode("utf-8"))
  return base64.b64encode(iv + encrypted_bytes).decode("utf-8")

def capitalize_all(texto):
    return ' '.join(palabra.capitalize() for palabra in texto.split())