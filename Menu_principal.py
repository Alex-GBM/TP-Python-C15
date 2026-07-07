if __name__ == "__main__":
    from datetime import datetime, timedelta

    # Inicializamos el sistema con capacidad de 40 lugares
    parking = ParkingSystem(capacity=40, hourly_rate=1500, storage_path="estacionamiento.json")
    
    while True:
        print("\n" + "="*35)
        print("   SISTEMA DE ESTACIONAMIENTO (40)")
        print("="*35)
        print(f" Lugares libres: {parking.available_spaces} / {parking.capacity}")
        print("-"*35)
        print("1. Ingresar vehículo")
        print("2. Registrar salida de vehículo (Manual)")
        print("3. Ver mapa del estacionamiento")
        print("4. Ver estadísticas de hoy")
        print("5. Salir")
        print("="*35)
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            patente = input("Ingrese la patente: ").strip().upper()
            
            # Menú de selección de tipo de vehículo para estandarizar el texto
            print("\n--- Tipo de Vehículo ---")
            print("1. Auto")
            print("2. Moto")
            print("3. PickUp")
            tipo_opcion = input("Seleccione el tipo (1-3): ").strip()
            
            # Mapeamos el número ingresado a la palabra correspondiente
            if tipo_opcion == "1":
                tipo = "Auto"
            elif tipo_opcion == "2":
                tipo = "Moto"
            elif tipo_opcion == "3":
                tipo = "PickUp"
            else:
                print("⚠️ Opción inválida. Se registrará como 'Auto' por defecto.")
                tipo = "Auto"
            
            print("\n¿Tipo de estadía?")
            print("1. Tiempo indefinido (Registra hora de entrada actual)")
            print("2. Tiempo definido (Establece cantidad de horas)")
            tipo_estadia = input("Seleccione (1 o 2): ").strip()
            
            hora_ingreso = datetime.now()
            
            if tipo_estadia == "2":
                try:
                    horas = int(input("¿Cuántas horas se va a quedar?: ").strip())
                    if horas <= 0:
                        print("⚠️ Cantidad de horas inválida. Se asignará tiempo indefinido.")
                    else:
                        # Simulamos el ingreso restando las horas para el cálculo interno
                        hora_ingreso = datetime.now() - timedelta(hours=horas)
                        print(f"⏱️ Modo definido: Se configuraron {horas} horas de estadía.")
                except ValueError:
                    print("⚠️ Entrada inválida. Se asignará tiempo indefinido.")

            exito = parking.enter_vehicle(patente, tipo, hora_ingreso)
            if exito:
                # Mostramos la hora exacta en la que el sistema registró el ingreso
                print(f"✅ Vehículo {patente} ingresado a las {hora_ingreso.strftime('%H:%M:%S')}.")
            else:
                print("❌ No se pudo ingresar (Estacionamiento lleno o patente ya registrada).")
                
        elif opcion == "2":
            patente = input("Ingrese la patente del vehículo que sale: ").strip().upper()
            
            # Verificamos primero si el auto realmente existe en el sistema
            if patente not in parking.vehicles:
                print("❌ La patente ingresada no se encuentra en el sistema.")
            else:
                print(f"Vehículo encontrado. Ingresó a las: {parking.vehicles[patente]['entry_time'].strftime('%H:%M:%S')}")
                print("\n--- Registrar Hora de Salida ---")
                try:
                    hora_salida_input = int(input("Ingrese la HORA de salida (0-23): ").strip())
                    minutos_salida_input = int(input("Ingrese los MINUTOS de salida (0-59): ").strip())
                    
                    # Tomamos la fecha de hoy pero le sobreescribimos la hora y minutos que ingresaste
                    ahora = datetime.now()
                    hora_salida = ahora.replace(hour=hora_salida_input, minute=minutos_salida_input, second=0, microsecond=0)
                    
                    # Si la hora de salida ingresada es menor a la de entrada, asumimos que es del día siguiente
                    if hora_salida < parking.vehicles[patente]['entry_time']:
                        hora_salida += timedelta(days=1)

                    # Procesamos la salida con tu hora manual
                    ticket = parking.exit_vehicle(patente, hora_salida)
                    
                    if ticket:
                        print("\n" + "-"*30)
                        print("       TICKET DE SALIDA")
                        print("-"*30)
                        print(f"Patente:     {ticket['plate']}")
                        print(f"Tipo:        {ticket['vehicle_type'].upper()}")
                        print(f"Entrada:     {ticket['entry_time'].strftime('%H:%M')}")
                        print(f"Salida:      {ticket['exit_time'].strftime('%H:%M')}")
                        print(f"Estadía:     {ticket['stay_minutes']} minutos")
                        print(f"Total cobrado: ${ticket['amount_paid']}")
                        print("-"*30)
                except ValueError:
                    print("❌ Error: Debes ingresar números válidos para la hora y los minutos.")
                
        elif opcion == "3":
            print("\n--- MAPA DE OCUPACIÓN ---")
            mapa = parking.get_parking_map()
            for fila in mapa:
                print(fila)
                
        elif opcion == "4":
            stats = parking.get_statistics()
            print("\n--- ESTADÍSTICAS DEL DÍA ---")
            print(f"Vehículos atendidos:      {stats['vehicles_attended']}")
            print(f"Tasa de ocupación actual: {stats['occupancy_rate'] * 100:.1f}%")
            print(f"Tiempo promedio de estadía: {stats['average_stay_minutes']:.1f} min")
            print("Cantidad por tipo:")
            for t, cant in stats['vehicle_type_counts'].items():
                print(f"  - {t.upper()}: {cant}")
                
        elif opcion == "5":
            print("💾 Estado guardado. Saliendo del sistema... ¡Hasta luego!")
            break
        else:
            print("⚠️ Opción inválida. Intente de nuevo.")

    
