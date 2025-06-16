import datetime

class Device:
    def __init__(self, device_id, name, power_consumption_rate, is_on=False):
        self.device_id = device_id
        self.name = name
        self.power_consumption_rate = power_consumption_rate  # in Watts
        self.is_on = is_on
        self.usage_history = []  # Stores (start_time, end_time, duration_minutes, energy_consumed_kWh)

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            self.start_time = datetime.datetime.now()
            print(f"Device '{self.name}' ({self.device_id}) turned ON at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}.")
        else:
            print(f"Device '{self.name}' ({self.device_id}) is already ON.")

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            end_time = datetime.datetime.now()
            duration_seconds = (end_time - self.start_time).total_seconds()
            duration_minutes = duration_seconds / 60
            energy_consumed_kWh = (self.power_consumption_rate * duration_seconds) / (1000 * 3600) # Wh to kWh
            self.usage_history.append((self.start_time, end_time, duration_minutes, energy_consumed_kWh))
            print(f"Device '{self.name}' ({self.device_id}) turned OFF at {end_time.strftime('%Y-%m-%d %H:%M:%S')}. Used {energy_consumed_kWh:.4f} kWh.")
        else:
            print(f"Device '{self.name}' ({self.device_id}) is already OFF.")

    def get_current_consumption(self):
        return self.power_consumption_rate if self.is_on else 0

    def get_total_energy_consumed(self):
        return sum(item[3] for item in self.usage_history)

    def __str__(self):
        status = "ON" if self.is_on else "OFF"
        return (f"Device ID: {self.device_id}, Name: {self.name}, "
                f"Power Rate: {self.power_consumption_rate}W, Status: {status}")

class SmartMeter:
    def __init__(self, meter_id, unit_cost_per_kWh):
        self.meter_id = meter_id
        self.unit_cost_per_kWh = unit_cost_per_kWh
        self.connected_devices = {}
        self.readings = [] # Stores (timestamp, total_consumption_kWh, cost)

    def add_device(self, device):
        if device.device_id not in self.connected_devices:
            self.connected_devices[device.device_id] = device
            print(f"Device '{device.name}' connected to Smart Meter {self.meter_id}.")
        else:
            print(f"Device '{device.name}' is already connected.")

    def remove_device(self, device_id):
        if device_id in self.connected_devices:
            device = self.connected_devices.pop(device_id)
            print(f"Device '{device.name}' disconnected from Smart Meter {self.meter_id}.")
        else:
            print(f"Device {device_id} not found.")

    def get_total_current_power_draw(self):
        return sum(device.get_current_consumption() for device in self.connected_devices.values())

    def take_reading(self):
        total_energy_consumed_all_devices = sum(device.get_total_energy_consumed() for device in self.connected_devices.values())
        cost = total_energy_consumed_all_devices * self.unit_cost_per_kWh
        timestamp = datetime.datetime.now()
        self.readings.append((timestamp, total_energy_consumed_all_devices, cost))
        print(f"Reading taken at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}: Total Energy: {total_energy_consumed_all_devices:.4f} kWh, Estimated Cost: ${cost:.2f}")
        return total_energy_consumed_all_devices, cost

    def get_cost_estimate(self):
        total_energy_consumed_all_devices = sum(device.get_total_energy_consumed() for device in self.connected_devices.values())
        return total_energy_consumed_all_devices * self.unit_cost_per_kWh

    def __str__(self):
        return (f"Smart Meter ID: {self.meter_id}, Cost per kWh: ${self.unit_cost_per_kWh:.2f}, "
                f"Connected Devices: {len(self.connected_devices)}")

class ElectricityManagementSystem:
    def __init__(self):
        self.meters = {}
        self.all_devices = {}

    def add_meter(self, meter):
        if meter.meter_id not in self.meters:
            self.meters[meter.meter_id] = meter
            print(f"Smart Meter {meter.meter_id} added to the system.")
        else:
            print(f"Smart Meter {meter.meter_id} already exists.")

    def add_device_to_system(self, device):
        if device.device_id not in self.all_devices:
            self.all_devices[device.device_id] = device
            print(f"Device '{device.name}' added to the overall system.")
        else:
            print(f"Device '{device.name}' already exists in the system.")

    def connect_device_to_meter(self, device_id, meter_id):
        device = self.all_devices.get(device_id)
        meter = self.meters.get(meter_id)
        if device and meter:
            meter.add_device(device)
        else:
            print("Error: Device or Meter not found.")

    def get_meter(self, meter_id):
        return self.meters.get(meter_id)

    def get_device(self, device_id):
        return self.all_devices.get(device_id)

    def get_system_total_current_power_draw(self):
        return sum(meter.get_total_current_power_draw() for meter in self.meters.values())

    def get_system_total_estimated_cost(self):
        return sum(meter.get_cost_estimate() for meter in self.meters.values())

# Example Usage:
if __name__ == "__main__":
    system = ElectricityManagementSystem()

    # Create Smart Meter
    meter1 = SmartMeter("SM001", 0.15) # $0.15 per kWh
    meter2 = SmartMeter("SM002", 0.18) # $0.18 per kWh
    system.add_meter(meter1)
    system.add_meter(meter2)

    # Create Devices
    tv = Device("DEV001", "Living Room TV", 150) # 150 Watts
    fridge = Device("DEV002", "Kitchen Fridge", 100) # 100 Watts
    ac = Device("DEV003", "Bedroom AC", 1500) # 1500 Watts
    lamp = Device("DEV004", "Desk Lamp", 60) # 60 Watts

    system.add_device_to_system(tv)
    system.add_device_to_system(fridge)
    system.add_device_to_system(ac)
    system.add_device_to_system(lamp)

    # Connect devices to meters
    system.connect_device_to_meter("DEV001", "SM001")
    system.connect_device_to_meter("DEV002", "SM001")
    system.connect_device_to_meter("DEV003", "SM002")
    system.connect_device_to_meter("DEV004", "SM001")

    print("\n--- Device Operations ---")
    tv.turn_on()
    fridge.turn_on()
    ac.turn_on()
    lamp.turn_on()

    # Simulate some time passing
    import time
    time.sleep(2) # Simulate 2 seconds of usage

    tv.turn_off()
    time.sleep(1) # Simulate 1 second of usage for others
    fridge.turn_off()
    ac.turn_off()
    lamp.turn_off()

    print("\n--- Meter Readings and Costs ---")
    meter1.take_reading()
    meter2.take_reading()

    print(f"\nTotal current power draw across all meters: {system.get_system_total_current_power_draw()} Watts")
    print(f"Total estimated cost across all meters: ${system.get_system_total_estimated_cost():.2f}")

    print("\n--- Device Usage History ---")
    for device_id, device in system.all_devices.items():
        print(f"\n{device.name} ({device.device_id}) Total Energy Consumed: {device.get_total_energy_consumed():.4f} kWh")
        for usage in device.usage_history:
            print(f"  - Start: {usage[0].strftime('%H:%M:%S')}, End: {usage[1].strftime('%H:%M:%S')}, Duration: {usage[2]:.2f} min, Energy: {usage[3]:.4f} kWh")

    print("\n--- Smart Meter Readings History ---")
    for meter_id, meter in system.meters.items():
        print(f"\nMeter {meter.meter_id} Readings:")
        for reading in meter.readings:
            print(f"  - At: {reading[0].strftime('%H:%M:%S')}, Total kWh: {reading[1]:.4f}, Cost: ${reading[2]:.2f}")