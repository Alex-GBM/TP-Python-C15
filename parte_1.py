from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class ParkingSystem:
    def __init__(
        self,
        capacity: int,
        hourly_rate: float,
        storage_path: Optional[str | Path] = None,
        rates_by_vehicle_type: Optional[Dict[str, float]] = None,
    ) -> None:
        self.capacity = min(int(capacity), 40)
        self.hourly_rate = hourly_rate
        self.storage_path = Path(storage_path) if storage_path is not None else None
        self.rates_by_vehicle_type = {
            key.lower(): float(value) for key, value in (rates_by_vehicle_type or {}).items()
        }
        self.occupied_spaces = 0
        self.vehicles: Dict[str, Dict[str, Any]] = {}
        self.available_spots: list[int] = []
        self.history: list[dict] = []
        self.total_stay_minutes = 0
        self.vehicles_attended = 0
        self.vehicle_type_counts: Dict[str, int] = {}
        self._refresh_available_spots()
        if self.storage_path is not None:
            self.load_state()

    @property
    def available_spaces(self) -> int:
        return self.capacity - self.occupied_spaces

    def _refresh_available_spots(self) -> None:
        occupied_spots = {int(vehicle.get("spot", 0)) for vehicle in self.vehicles.values() if vehicle.get("spot")}
        self.available_spots = [spot for spot in range(1, self.capacity + 1) if spot not in occupied_spots]

    def enter_vehicle(self, plate: str, vehicle_type: str, entry_time: datetime) -> bool:
        if self.available_spaces <= 0:
            return False
        if plate in self.vehicles:
            return False

        normalized_type = vehicle_type.strip().lower() or "auto"
        spot = self.available_spots.pop(0)
        self.vehicles[plate] = {
            "type": normalized_type,
            "entry_time": entry_time,
            "spot": spot,
        }
        self.occupied_spaces += 1
        self.save_state()
        return True

    def exit_vehicle(self, plate: str, exit_time: datetime) -> Optional[Dict[str, Any]]:
        vehicle = self.vehicles.pop(plate, None)
        if vehicle is None:
            return None

        entry_time = vehicle["entry_time"]
        stay_minutes = max(int((exit_time - entry_time).total_seconds() // 60), 0)
        amount_paid = self._calculate_amount(stay_minutes, vehicle["type"])

        self.occupied_spaces -= 1
        self.available_spots.append(vehicle["spot"])
        self.available_spots.sort()
        self.total_stay_minutes += stay_minutes
        self.vehicles_attended += 1
        self.vehicle_type_counts[vehicle["type"]] = self.vehicle_type_counts.get(vehicle["type"], 0) + 1

        record = {
            "plate": plate,
            "vehicle_type": vehicle["type"],
            "entry_time": entry_time,
            "exit_time": exit_time,
            "stay_minutes": stay_minutes,
            "amount_paid": amount_paid,
        }
        self.history.append(record)
        self.save_state()
        return record

    def _calculate_amount(self, stay_minutes: int, vehicle_type: str) -> int:
        rate = self.rates_by_vehicle_type.get(vehicle_type.lower())
        if rate is None:
            rate = self.hourly_rate
        hours = max(1, (stay_minutes + 59) // 60)
        return int(hours * rate)

    def get_statistics(self) -> Dict[str, Any]:
        average_stay_minutes = (
            self.total_stay_minutes / self.vehicles_attended if self.vehicles_attended else 0.0
        )
        occupancy_rate = self.occupied_spaces / self.capacity if self.capacity else 0.0
        return {
            "vehicles_attended": self.vehicles_attended,
            "occupancy_rate": occupancy_rate,
            "average_stay_minutes": average_stay_minutes,
            "vehicle_type_counts": dict(self.vehicle_type_counts),
            "current_occupied_spaces": self.occupied_spaces,
        }

