
from functions.utils import read_csv, send_mail, generate_qr, sha256, get_email_body, encrypt, capitalize_all
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
import requests


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
    name_and_surname = capitalize_all(f"{name} {surname}")
    email = email.lower()

    print(f"{YELLOW}Usuario: {name_and_surname} | Email: {email} | Móvil: {phone} | DNI: {dni}{RESET}")

    try:
      qr_data = sha256(dni + SECRET_KEY)
      encrypted_dni = encrypt(dni, SECRET_KEY)
      
      doc_ref = db.collection("users").document(qr_data)
      doc_ref.set({
        "dni": encrypted_dni,
        "email": email,
        "name": name_and_surname,
        "phone": phone,
        "used": False
      })
      
      print(f"\t{GREEN}Usuario añadido a Firebase{RESET}")
      
      # response = requests.post(
      #   "https://sugusuva.es/api/v1/participants",
      #   json={
      #     "dni": dni.upper(),
      #     "name": name.capitalize(),
      #     "surname": surname.capitalize(),
      #     "email": email,
      #     "telephone": phone,
      #     "prefix": "+34"
      #   },
      #   verify=False
      # )
      
      # if response.status_code != 200:
      #   raise Exception(f"\t{RED}Error al añadir el usuario a la BDD de SUGUS: {response.status_code}\n{response.text}{RESET}")
      
      # print(f"\t{GREEN}Usuario añadido a la BDD de SUGUS{RESET}")
      
      qr_code = generate_qr(qr_data)
      body = get_email_body(name)
      
      # send_mail(EMAIL_FROM, email, EMAIL_SUBJECT, body, qr_code)
      print(f"\t{GREEN}Email enviado correctamente{RESET}")

    except Exception as e:
      print(f"\t{RED}Error: {e}{RESET}")
      
    print("\n")

  
if __name__ == "__main__":
  main()