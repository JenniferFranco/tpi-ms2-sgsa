# SGSA - Sistema de Gestion de Solicitudes Academicas
# version 1 - hecho rapido para la demo, despues lo ordenamos
import json, os, datetime

DATA_FILE = os.environ.get("SGSA_DATA", "datos.json")
datos = None  # se carga al iniciar


def cargar():
    global datos
    try:
        f = open(DATA_FILE, "r", encoding="utf-8")
        datos = json.load(f)
        f.close()
    except:
        # si no existe el archivo arrancamos de cero
        datos = {"estudiantes": [], "responsables": [
            {"id": 1, "nombre": "Laura Gomez", "area": "Alumnado"},
            {"id": 2, "nombre": "Martin Ruiz", "area": "Secretaria Academica"},
            {"id": 3, "nombre": "Sofia Diaz", "area": "Bedelia"}],
            "solicitudes": [], "ultimo_id": 0}


def hoy():
    h = os.environ.get("SGSA_HOY")
    if h:
        return datetime.datetime.strptime(h, "%Y-%m-%d").date()
    return datetime.date.today()


class GestorSolicitudes:

    def registrar_estudiante(self):
        print("--- Registrar estudiante ---")
        legajo = input("Legajo: ").strip()
        # validar legajo
        if not legajo.isdigit() or len(legajo) < 4 or len(legajo) > 6:
            print("Error: legajo invalido (4 a 6 digitos)")
            return
        for e in datos["estudiantes"]:
            if e["legajo"] == legajo:
                print("Error: ya existe un estudiante con ese legajo")
                return
        n = input("Nombre: ").strip()
        a = input("Apellido: ").strip()
        if n == "" or a == "":
            print("Error: nombre y apellido son obligatorios")
            return
        em = input("Email: ").strip()
        if "@" not in em or "." not in em.split("@")[-1]:
            print("Error: email invalido")
            return
        datos["estudiantes"].append({"legajo": legajo, "nombre": n, "apellido": a, "email": em})
        f = open(DATA_FILE, "w", encoding="utf-8")
        json.dump(datos, f, indent=2, ensure_ascii=False)
        f.close()
        print("Estudiante registrado: " + a + ", " + n)

    def registrar_solicitud(self):
        print("--- Registrar solicitud ---")
        legajo = input("Legajo del estudiante: ").strip()
        # validar legajo (igual que arriba)
        if not legajo.isdigit() or len(legajo) < 4 or len(legajo) > 6:
            print("Error: legajo invalido (4 a 6 digitos)")
            return
        est = None
        for e in datos["estudiantes"]:
            if e["legajo"] == legajo:
                est = e
        if est == None:
            print("Error: el estudiante no existe")
            return
        print("Tipos: CERT=Certificado, EQUIV=Equivalencia, MESA=Mesa especial, RECL=Reclamo de nota")
        t = input("Tipo: ").strip().upper()
        if t != "CERT" and t != "EQUIV" and t != "MESA" and t != "RECL":
            print("Error: tipo invalido")
            return
        d = input("Descripcion: ").strip()
        if len(d) < 10:
            print("Error: la descripcion debe tener al menos 10 caracteres")
            return
        p = input("Prioridad (1=Alta, 2=Media, 3=Baja, Enter=automatica): ").strip()
        if p == "":
            # prioridad automatica segun tipo
            if t == "RECL":
                p = 1
            elif t == "MESA":
                p = 1
            elif t == "EQUIV":
                p = 2
            else:
                p = 3
        else:
            if p != "1" and p != "2" and p != "3":
                print("Error: prioridad invalida")
                return
            p = int(p)
        self.crear_solicitud(est["legajo"], est["nombre"], est["apellido"], est["email"], t, d, p, None, hoy().isoformat())

    def crear_solicitud(self, legajo, nombre, apellido, email, tipo, descripcion, prioridad, responsable, fecha):
        datos["ultimo_id"] = datos["ultimo_id"] + 1
        s = {"id": datos["ultimo_id"], "legajo": legajo, "tipo": tipo, "descripcion": descripcion,
             "prioridad": prioridad, "estado": "P", "responsable": responsable, "fecha": fecha}
        datos["solicitudes"].append(s)
        f = open(DATA_FILE, "w", encoding="utf-8")
        json.dump(datos, f, indent=2, ensure_ascii=False)
        f.close()
        # nombre y email no se usan pero los dejamos por si hay que mandar mail
        print("Solicitud #" + str(s["id"]) + " registrada para " + apellido + ", " + nombre)

    def cambiar_estado(self):
        print("--- Cambiar estado ---")
        try:
            id = int(input("Nro de solicitud: "))
        except:
            print("Error: numero invalido")
            return
        s = None
        for x in datos["solicitudes"]:
            if x["id"] == id:
                s = x
        if s == None:
            print("Error: la solicitud no existe")
            return
        print("Estados: P=Pendiente, EP=En proceso, R=Resuelta, X=Rechazada")
        nuevo = input("Nuevo estado: ").strip().upper()
        if nuevo != "P" and nuevo != "EP" and nuevo != "R" and nuevo != "X":
            print("Error: estado invalido")
            return
        flag = False
        if s["estado"] == "P":
            if nuevo == "EP" or nuevo == "X":
                flag = True
        elif s["estado"] == "EP":
            if nuevo == "R" or nuevo == "X":
                flag = True
        if flag == False:
            print("Error: transicion no permitida")
            return
        if nuevo == "EP" and s["responsable"] == None:
            print("Error: debe asignar un responsable antes")
            return
        s["estado"] = nuevo
        f = open(DATA_FILE, "w", encoding="utf-8")
        json.dump(datos, f, indent=2, ensure_ascii=False)
        f.close()
        if nuevo == "P":
            txt = "Pendiente"
        elif nuevo == "EP":
            txt = "En proceso"
        elif nuevo == "R":
            txt = "Resuelta"
        else:
            txt = "Rechazada"
        print("Solicitud #" + str(id) + " ahora esta " + txt)

    def asignar_responsable(self):
        print("--- Asignar responsable ---")
        try:
            id = int(input("Nro de solicitud: "))
        except:
            print("Error: numero invalido")
            return
        s = None
        for x in datos["solicitudes"]:
            if x["id"] == id:
                s = x
        if s == None:
            print("Error: la solicitud no existe")
            return
        if s["estado"] == "R" or s["estado"] == "X":
            print("Error: la solicitud ya esta cerrada")
            return
        for r in datos["responsables"]:
            print(str(r["id"]) + ") " + r["nombre"] + " - " + r["area"])
        try:
            rid = int(input("Responsable: "))
        except:
            print("Error: numero invalido")
            return
        resp = None
        for r in datos["responsables"]:
            if r["id"] == rid:
                resp = r
        if resp == None:
            print("Error: el responsable no existe")
            return
        s["responsable"] = rid
        # si estaba pendiente pasa a en proceso automaticamente
        if s["estado"] == "P":
            s["estado"] = "EP"
        f = open(DATA_FILE, "w", encoding="utf-8")
        json.dump(datos, f, indent=2, ensure_ascii=False)
        f.close()
        print("Solicitud #" + str(id) + " asignada a " + resp["nombre"])

    def buscar(self):
        print("--- Buscar / filtrar ---")
        print("Filtrar por: 1) Estado 2) Tipo 3) Legajo 4) Todas")
        op = input("Opcion: ").strip()
        res = []
        if op == "1":
            v = input("Estado (P/EP/R/X): ").strip().upper()
            for x in datos["solicitudes"]:
                if x["estado"] == v:
                    res.append(x)
        elif op == "2":
            v = input("Tipo (CERT/EQUIV/MESA/RECL): ").strip().upper()
            for x in datos["solicitudes"]:
                if x["tipo"] == v:
                    res.append(x)
        elif op == "3":
            v = input("Legajo: ").strip()
            if not v.isdigit() or len(v) < 4 or len(v) > 6:
                print("Error: legajo invalido (4 a 6 digitos)")
                return
            for x in datos["solicitudes"]:
                if x["legajo"] == v:
                    res.append(x)
        elif op == "4":
            res = datos["solicitudes"]
        else:
            print("Error: opcion invalida")
            return
        if len(res) == 0:
            print("No se encontraron solicitudes")
            return
        # ordenar por prioridad y despues por id
        res = sorted(res, key=lambda x: (x["prioridad"], x["id"]))
        for x in res:
            if x["estado"] == "P":
                e = "Pendiente"
            elif x["estado"] == "EP":
                e = "En proceso"
            elif x["estado"] == "R":
                e = "Resuelta"
            else:
                e = "Rechazada"
            if x["prioridad"] == 1:
                pr = "Alta"
            elif x["prioridad"] == 2:
                pr = "Media"
            else:
                pr = "Baja"
            rn = "-"
            for r in datos["responsables"]:
                if r["id"] == x["responsable"]:
                    rn = r["nombre"]
            print("#" + str(x["id"]) + " | " + x["tipo"] + " | " + e + " | Prioridad: " + pr + " | Legajo: " + x["legajo"] + " | Resp: " + rn)

    def reporte(self):
        print("--- Reporte basico ---")
        # leemos de nuevo el archivo por las dudas
        try:
            f = open(DATA_FILE, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
        except:
            d = datos
        sols = d["solicitudes"]
        print("Total de solicitudes: " + str(len(sols)))
        c1 = 0; c2 = 0; c3 = 0; c4 = 0
        for x in sols:
            if x["estado"] == "P":
                c1 = c1 + 1
            elif x["estado"] == "EP":
                c2 = c2 + 1
            elif x["estado"] == "R":
                c3 = c3 + 1
            elif x["estado"] == "X":
                c4 = c4 + 1
        print("Por estado -> Pendiente: " + str(c1) + " | En proceso: " + str(c2) + " | Resuelta: " + str(c3) + " | Rechazada: " + str(c4))
        t1 = 0; t2 = 0; t3 = 0; t4 = 0
        for x in sols:
            if x["tipo"] == "CERT":
                t1 += 1
            if x["tipo"] == "EQUIV":
                t2 += 1
            if x["tipo"] == "MESA":
                t3 += 1
            if x["tipo"] == "RECL":
                t4 += 1
        print("Por tipo -> CERT: " + str(t1) + " | EQUIV: " + str(t2) + " | MESA: " + str(t3) + " | RECL: " + str(t4))
        a = 0
        for x in sols:
            if x["prioridad"] == 1 and (x["estado"] == "P" or x["estado"] == "EP"):
                a += 1
        print("Abiertas con prioridad alta: " + str(a))
        venc = []
        for x in sols:
            if x["estado"] == "P":
                f2 = datetime.datetime.strptime(x["fecha"], "%Y-%m-%d").date()
                if (hoy() - f2).days > 3:
                    venc.append(x)
        print("Pendientes con mas de 3 dias sin atender: " + str(len(venc)))
        for x in venc:
            print("  #" + str(x["id"]) + " (" + x["tipo"] + ") desde " + x["fecha"])


def main():
    cargar()
    g = GestorSolicitudes()
    while True:
        print("")
        print("===== SGSA - Gestion de Solicitudes Academicas =====")
        print("1. Registrar estudiante")
        print("2. Registrar solicitud")
        print("3. Cambiar estado de solicitud")
        print("4. Asignar responsable")
        print("5. Buscar / filtrar solicitudes")
        print("6. Reporte basico")
        print("0. Salir")
        op = input("Opcion: ").strip()
        if op == "1":
            g.registrar_estudiante()
        elif op == "2":
            g.registrar_solicitud()
        elif op == "3":
            g.cambiar_estado()
        elif op == "4":
            g.asignar_responsable()
        elif op == "5":
            g.buscar()
        elif op == "6":
            g.reporte()
        elif op == "0":
            print("Hasta luego")
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    main()
