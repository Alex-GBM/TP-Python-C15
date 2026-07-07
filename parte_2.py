    def get_parking_map(self) -> list[str]:
        map_lines: list[str] = []
        for row in range(0, self.capacity, 10):
            line = []
            for spot in range(row + 1, min(row + 11, self.capacity + 1)):
                if any(vehicle.get("spot") == spot for vehicle in self.vehicles.values()):
                    line.append("[X]")
                else:
                    line.append(f"[{spot:02d}]")
            map_lines.append(" ".join(line))
        return map_lines

    def clear_vehicles(self) -> None:
        self.vehicles = {}
        self.occupied_spaces = 0
        self.available_spots = list(range(1, self.capacity + 1))
        self.history = []
        self.total_stay_minutes = 0
        self.vehicles_attended = 0
        self.vehicle_type_counts = {}
        self.save_state()

    def save_state(self) -> None:
        if self.storage_path is None:
            return

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "capacity": self.capacity,
            "hourly_rate": self.hourly_rate,
            "rates_by_vehicle_type": self.rates_by_vehicle_type,
            "occupied_spaces": self.occupied_spaces,
            "vehicles": {
                plate: {
                    "type": data["type"],
                    "entry_time": data["entry_time"].isoformat(),
                    "spot": data["spot"],
                }
                for plate, data in self.vehicles.items()
            },
            "history": [
                {
                    **record,
                    "entry_time": record["entry_time"].isoformat(),
                    "exit_time": record["exit_time"].isoformat(),
                }
                for record in self.history
            ],
            "total_stay_minutes": self.total_stay_minutes,
            "vehicles_attended": self.vehicles_attended,
            "vehicle_type_counts": self.vehicle_type_counts,
        }
        with self.storage_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)

    def load_state(self) -> bool:
        if self.storage_path is None or not self.storage_path.exists():
            return False

        try:
            with self.storage_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            return False

        self.capacity = int(data.get("capacity", self.capacity))
        self.hourly_rate = float(data.get("hourly_rate", self.hourly_rate))
        self.rates_by_vehicle_type = {
            str(key).lower(): float(value)
            for key, value in data.get("rates_by_vehicle_type", {}).items()
        }
        self.occupied_spaces = int(data.get("occupied_spaces", 0))
        self.vehicles = {
            plate: {
                "type": item.get("type", "auto"),
                "entry_time": datetime.fromisoformat(item["entry_time"]),
                "spot": int(item.get("spot", 0)),
            }
            for plate, item in data.get("vehicles", {}).items()
        }
        self.history = [
            {
                **record,
                "entry_time": datetime.fromisoformat(record["entry_time"]),
                "exit_time": datetime.fromisoformat(record["exit_time"]),
            }
            for record in data.get("history", [])
        ]
        self.total_stay_minutes = int(data.get("total_stay_minutes", 0))
        self.vehicles_attended = int(data.get("vehicles_attended", 0))
        self.vehicle_type_counts = {
            str(key): int(value) for key, value in data.get("vehicle_type_counts", {}).items()
        }
        self._refresh_available_spots()
        return True


