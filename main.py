from __future__ import annotations

from parking_system import ParkingSystem
import argparse
from datetime import datetime
from pathlib import Path
from tkinter import END, StringVar, Tk, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from parking_system import ParkingSystem


def parse_datetime(text: str) -> datetime:
    return datetime.strptime(text, "%Y-%m-%d %H:%M")


def format_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M")


def get_desktop_path() -> Path:
    home = Path.home()
    candidates = [home / "Desktop", home / "Escritorio", home / "desktop"]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    desktop_path = home / "Desktop"
    desktop_path.mkdir(parents=True, exist_ok=True)
    return desktop_path


class ParkingApp(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sistema de estacionamiento")
        self.geometry("760x520")
        self.resizable(False, False)
        self.parking = ParkingSystem(
            capacity=40,
            hourly_rate=1000,
            storage_path=Path(__file__).with_name("parking_state.json"),
        )
        self._build_ui()
        self.notebook.select(0)
        self.refresh_dashboard()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.plate_var = StringVar()
        self.vehicle_type_var = StringVar(value="auto")
        self.datetime_var = StringVar(value=format_datetime(datetime.now()))
        self.capacity_var = StringVar(value=str(self.parking.capacity))
        self.auto_rate_var = StringVar(value=str(self.parking.rates_by_vehicle_type.get("auto", self.parking.hourly_rate)))
        self.moto_rate_var = StringVar(value=str(self.parking.rates_by_vehicle_type.get("moto", self.parking.hourly_rate)))
        self.pickup_rate_var = StringVar(value=str(self.parking.rates_by_vehicle_type.get("pickup", self.parking.hourly_rate)))

        notebook = ttk.Notebook(self)
        notebook.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.notebook = notebook

        entry_frame = ttk.Frame(notebook)
        entry_frame.columnconfigure(1, weight=1)
        ttk.Label(entry_frame, text="Pantalla de ingreso de vehículos").grid(row=0, column=0, columnspan=2, padx=5, pady=8, sticky="w")
        ttk.Label(entry_frame, text="Patente:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(entry_frame, textvariable=self.plate_var, width=25).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(entry_frame, text="Tipo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(entry_frame, textvariable=self.vehicle_type_var, values=["auto", "moto", "pickup"], state="readonly", width=20).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(entry_frame, text="Fecha y hora:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(entry_frame, textvariable=self.datetime_var, width=25).grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(entry_frame, text="Registrar ingreso", command=self.register_entry).grid(row=4, column=1, padx=5, pady=10, sticky="w")
        entry_frame.grid_columnconfigure(1, weight=1)
        notebook.add(entry_frame, text="Ingreso")

        exit_frame = ttk.Frame(notebook)
        exit_frame.columnconfigure(1, weight=1)
        ttk.Label(exit_frame, text="Pantalla de egreso de vehículos").grid(row=0, column=0, columnspan=2, padx=5, pady=8, sticky="w")
        ttk.Label(exit_frame, text="Patente:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(exit_frame, textvariable=self.plate_var, width=25).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(exit_frame, text="Fecha y hora:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(exit_frame, textvariable=self.datetime_var, width=25).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(exit_frame, text="Registrar egreso", command=self.register_exit).grid(row=3, column=1, padx=5, pady=10, sticky="w")
        notebook.add(exit_frame, text="Egreso")

        dashboard_frame = ttk.Frame(notebook)
        dashboard_frame.columnconfigure(0, weight=1)
        dashboard_frame.rowconfigure(0, weight=1)
        self.dashboard_text = ScrolledText(dashboard_frame, wrap="word", height=18)
        self.dashboard_text.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        ttk.Button(dashboard_frame, text="Imprimir documento de estadísticas", command=self.export_statistics_report).grid(row=1, column=0, padx=8, pady=(0, 8), sticky="w")
        notebook.add(dashboard_frame, text="Estado")

        config_frame = ttk.Frame(notebook)
        config_frame.columnconfigure(1, weight=1)
        ttk.Label(config_frame, text="Configuración del estacionamiento").grid(row=0, column=0, columnspan=2, padx=5, pady=8, sticky="w")

        ttk.Label(config_frame, text="Capacidad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(config_frame, textvariable=self.capacity_var, width=20).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(config_frame, text="Auto:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(config_frame, textvariable=self.auto_rate_var, width=20).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(config_frame, text="Moto:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(config_frame, textvariable=self.moto_rate_var, width=20).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(config_frame, text="PickUp:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(config_frame, textvariable=self.pickup_rate_var, width=20).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(config_frame, text="Guardar configuración", command=self.apply_config).grid(row=5, column=0, padx=5, pady=10, sticky="w")
        ttk.Button(config_frame, text="Limpiar registro", command=self.clear_vehicle_registry).grid(row=6, column=0, padx=5, pady=5, sticky="w")
        notebook.add(config_frame, text="Configuración")

        self.rowconfigure(1, weight=1)

    def apply_config(self) -> None:
        try:
            capacity = int(self.capacity_var.get())
            auto_rate = float(self.auto_rate_var.get())
            moto_rate = float(self.moto_rate_var.get())
            pickup_rate = float(self.pickup_rate_var.get())
        except ValueError:
            messagebox.showerror("Error", "La capacidad debe ser un número entero y los precios deben ser válidos.")
            return

        self.parking.capacity = min(capacity, 40)
        self.parking.rates_by_vehicle_type = {
            "auto": auto_rate,
            "moto": moto_rate,
            "pickup": pickup_rate,
        }
        self.parking._refresh_available_spots()
        self.parking.save_state()
        self.refresh_dashboard()
        messagebox.showinfo("Listo", "Configuración guardada.")

    def clear_vehicle_registry(self) -> None:
        if messagebox.askyesno("Limpiar registro", "¿Desea eliminar todos los vehículos actuales del sistema?"):
            self.parking.clear_vehicles()
            self.refresh_dashboard()
            messagebox.showinfo("Listo", "Registro de vehículos limpiado.")

    def register_entry(self) -> None:
        plate = self.plate_var.get().strip().upper()
        vehicle_type = self.vehicle_type_var.get().strip().lower()
        try:
            entry_time = parse_datetime(self.datetime_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD HH:MM")
            return

        if not plate:
            messagebox.showwarning("Aviso", "Debe ingresar una patente.")
            return

        success = self.parking.enter_vehicle(plate, vehicle_type, entry_time)
        if success:
            self.plate_var.set("")
            self.datetime_var.set(format_datetime(datetime.now()))
            self.refresh_dashboard()
            messagebox.showinfo("Ingreso", f"Vehículo {plate} registrado correctamente.")
        else:
            messagebox.showwarning("Aviso", "No se pudo registrar el ingreso. Revise capacidad o patente duplicada.")

    def register_exit(self) -> None:
        plate = self.plate_var.get().strip().upper()
        try:
            exit_time = parse_datetime(self.datetime_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD HH:MM")
            return

        if not plate:
            messagebox.showwarning("Aviso", "Debe ingresar una patente.")
            return

        ticket = self.parking.exit_vehicle(plate, exit_time)
        if ticket is None:
            messagebox.showwarning("Aviso", "No existe un vehículo con esa patente dentro del estacionamiento.")
        else:
            self.plate_var.set("")
            self.datetime_var.set(format_datetime(datetime.now()))
            self.refresh_dashboard()
            messagebox.showinfo("Egreso", f"Egreso registrado. Monto: ${ticket['amount_paid']}")

    def export_statistics_report(self) -> None:
        stats = self.parking.get_statistics()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        desktop_path = get_desktop_path()
        report_path = desktop_path / f"estadisticas_estacionamiento_{timestamp}.txt"

        vehicle_type_totals: dict[str, int] = {}
        for record in self.parking.history:
            vehicle_type = record.get("vehicle_type", "desconocido")
            vehicle_type_totals[vehicle_type] = vehicle_type_totals.get(vehicle_type, 0) + int(record.get("amount_paid", 0))

        content = [
            "RESUMEN DEL ESTACIONAMIENTO",
            "=" * 30,
            f"Cantidad de vehículos: {stats['vehicles_attended']}",
            "",
            "Tiempo promedio por tipo de vehículo:",
        ]

        if self.parking.history:
            for vehicle_type in sorted({record.get("vehicle_type", "desconocido") for record in self.parking.history}):
                type_records = [record for record in self.parking.history if record.get("vehicle_type") == vehicle_type]
                average_minutes = sum(record.get("stay_minutes", 0) for record in type_records) / len(type_records)
                content.append(f"- {vehicle_type}: {average_minutes:.1f} min")
        else:
            content.append("- Ninguno")

        content.extend(["", "Total recaudado por tipo de vehículo:"])
        if vehicle_type_totals:
            for vehicle_type, total in sorted(vehicle_type_totals.items()):
                content.append(f"- {vehicle_type}: ${total}")
        else:
            content.append("- Ninguno")

        total_general = sum(vehicle_type_totals.values())
        content.extend(["", f"Total general: ${total_general}"])

        report_path.write_text("\n".join(content), encoding="utf-8")
        messagebox.showinfo("Documento creado", f"Se generó el reporte en: {report_path}")

    def refresh_dashboard(self) -> None:
        stats = self.parking.get_statistics()
        self.dashboard_text.delete("1.0", END)
        self.dashboard_text.insert(
            END,
            "Estado actual\n"
            f"- Espacios ocupados: {stats['current_occupied_spaces']}\n"
            f"- Espacios disponibles: {self.parking.available_spaces}\n"
            f"- Tasa de ocupación: {stats['occupancy_rate']:.2%}\n"
            f"- Vehículos atendidos: {stats['vehicles_attended']}\n"
            f"- Tiempo promedio de permanencia: {stats['average_stay_minutes']:.1f} min\n"
            f"- Tipos de vehículos atendidos: {stats['vehicle_type_counts']}\n\n"
            "Mapa del estacionamiento:\n"
        )
        for line in self.parking.get_parking_map():
            self.dashboard_text.insert(END, f"{line}\n")
        self.dashboard_text.insert(END, "\nVehículos dentro del estacionamiento:\n")
        if self.parking.vehicles:
            for plate, data in self.parking.vehicles.items():
                self.dashboard_text.insert(
                    END,
                    f"- {plate}: {data['type']} | puesto {data['spot']} | ingreso {format_datetime(data['entry_time'])}\n",
                )
        else:
            self.dashboard_text.insert(END, "- Ninguno\n")


def run_cli() -> None:
    capacity = min(int(input("Ingrese la capacidad del estacionamiento: ")), 40)
    parking = ParkingSystem(
        capacity=capacity,
        hourly_rate=0,
        storage_path=Path(__file__).with_name("parking_state.json"),
    )

    while True:
        print("\n--- MENU ---")
        print("1. Ingresar vehiculo")
        print("2. Egresar vehiculo")
        print("3. Ver estadisticas")
        print("4. Salir")

        option = input("Seleccione una opcion: ")

        if option == "1":
            plate = input("Ingrese la patente: ").strip().upper()
            vehicle_type = input("Ingrese el tipo de vehiculo (auto/moto/pickup): ").strip().lower()
            entry_time = parse_datetime(input("Ingrese la hora de ingreso (YYYY-MM-DD HH:MM): "))
            success = parking.enter_vehicle(plate, vehicle_type, entry_time)
            if success:
                spot = parking.vehicles[plate]["spot"]
                print(f"Vehiculo ingresado correctamente. Puesto asignado: {spot}")
            else:
                print("No se pudo ingresar el vehiculo. Verifique capacidad o patente.")

        elif option == "2":
            plate = input("Ingrese la patente: ").strip().upper()
            exit_time = parse_datetime(input("Ingrese la hora de egreso (YYYY-MM-DD HH:MM): "))
            ticket = parking.exit_vehicle(plate, exit_time)
            if ticket is None:
                print("No existe un vehiculo con esa patente dentro del estacionamiento.")
            else:
                print("Egreso registrado.")
                print(ticket)

        elif option == "3":
            stats = parking.get_statistics()
            print("Estadisticas:")
            print(stats)
            print("\nMapa del estacionamiento:")
            for line in parking.get_parking_map():
                print(line)

        elif option == "4":
            print("Saliendo del sistema...")
            break

        else:
            print("Opcion invalida.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sistema de estacionamiento")
    parser.add_argument("--cli", action="store_true", help="Ejecutar la versión por consola")
    parser.add_argument("--gui", action="store_true", help="Ejecutar la versión gráfica")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        app = ParkingApp()
        app.mainloop()


if __name__ == "__main__":
    main()
