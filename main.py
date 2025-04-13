
from functions.utils import read_csv, send_mail, generate_qr, sha256, get_email_body, encrypt
import firebase_admin
from firebase_admin import credentials, firestore
from config import (
  FIREBASE_CREDENTIALS_PATH,
  CSV_FILE_PATH,
  CSV_COLUMNS,
  SECRET_KEY,
  EMAIL_FROM,
  EMAIL_SUBJECT,
  RED, GREEN, YELLOW, RESET
)



cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()

if not SECRET_KEY or len(SECRET_KEY.encode("utf-8")) != 32:
    raise ValueError("La clave secreta debe tener exactamente 32 bytes")


def main():
  users = read_csv(CSV_FILE_PATH, CSV_COLUMNS)
  
  if users is None:
    print("No se pudo leer el archivo CSV.")
    return
  
  for name, surname, email, phone, dni in users:
    dni = dni.lower()
    
    print(f"{YELLOW}{f" Usuario: {name} {surname} | Email: {email} | Móvil: {phone} | DNI: {dni}".center(70, "-")}{RESET}")
    
    if name != "Daniel":
      continue
      
    try:
      qr_data = sha256(dni + SECRET_KEY)
      
      doc_ref = db.collection("users").document(qr_data)
      doc_ref.set({
        "dni": encrypt(dni, SECRET_KEY),
        "email": email,
        "name": f"{name} {surname}",
        "phone": phone,
        "used": False
      })
      
      qr_code = generate_qr(qr_data)
      body = get_email_body(name)
      
      send_mail(EMAIL_FROM, email, EMAIL_SUBJECT, body, qr_code)
      print(f"\t{GREEN}Email sent successfully{RESET}")

    except Exception as e:
      print(f"\t{RED}Error sending email: {e}{RESET}")
      
    print("\n")

  
if __name__ == "__main__":
  main()