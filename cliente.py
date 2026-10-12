import requests

URL = "http://127.0.0.1:5000"


def registrar():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    try:
        r = requests.post(
            f"{URL}/registro",
            json={"usuario": usuario, "contraseña": contraseña},
        )
        print(r.status_code, r.json())
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor. ¿Está corriendo servidor.py?")


def login():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    try:
        r = requests.post(
            f"{URL}/login",
            json={"usuario": usuario, "contraseña": contraseña},
        )
        print(r.status_code, r.json())
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor. ¿Está corriendo servidor.py?")


def ver_tareas():
    try:
        r = requests.get(f"{URL}/tareas")
        print(r.status_code)
        print(r.text)
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor. ¿Está corriendo servidor.py?")


def menu():
    while True:
        print("\n--- Sistema de Gestión de Tareas ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver tareas")
        print("4. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            print("Chau")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()
