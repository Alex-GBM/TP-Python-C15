def Menu_principal():
    continuar = True
    while continuar:
        print(
            "Bienvenido a nuestro sistema de gestion de estacionamiento. por favor seleccione alguna de las siguientes opciones:\n"
            "1. Ingreso o egreso de vehiculos\n"
            "2. Calculo de tiempo de permanencia de los vehiculos\n"
            "3. Control de los espacios de estacionamiento disponibles\n"
            "4. Calculo de importes a pagar\n"
            "0. Cerrar el programa\n"
        )
        eleccion = int(input("Ingrese la opcion segun el numero asignado:"))
        if eleccion == "1":
            ingreso_egreso()
        elif eleccion == "2":
            tiempo_permanencia()
        elif eleccion == "3":
            espacios_disponibles()
        elif eleccion == "4":
            calculo_importes()
        elif eleccion == "0":
            print("Gracias por utilizar nuestro sistema de gestion de estacionamiento")  
            continuar = False
        else:
            print("Opcion invalida. Por favor seleccione una opcion del 0 al 4.")


Menu_principal()

    