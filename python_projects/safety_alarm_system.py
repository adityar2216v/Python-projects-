import datetime
import time

class Sensor:
    def __init__(self, sensor_id, sensor_type, location):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type  # e.g., "smoke", "motion", "temperature", "door/window"
        self.location = location
        self.is_active = True
        self.last_triggered = None

    def activate(self):
        self.is_active = True
        print(f"Sensor {self.sensor_id} ({self.sensor_type}) at {self.location} activated.")

    def deactivate(self):
        self.is_active = False
        print(f"Sensor {self.sensor_id} ({self.sensor_type}) at {self.location} deactivated.")

    def trigger(self):
        if self.is_active:
            self.last_triggered = datetime.datetime.now()
            print(f"Sensor {self.sensor_id} ({self.sensor_type}) at {self.location} triggered at {self.last_triggered.strftime('%Y-%m-%d %H:%M:%S')}.")
            return True
        else:
            print(f"Sensor {self.sensor_id} is inactive and cannot be triggered.")
            return False

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        last_trigger_info = f", Last Triggered: {self.last_triggered.strftime('%H:%M:%S')}" if self.last_triggered else ""
        return (f"Sensor ID: {self.sensor_id}, Type: {self.sensor_type.capitalize()}, "
                f"Location: {self.location}, Status: {status}{last_trigger_info}")

class Alarm:
    def __init__(self, alarm_id, alarm_type, sound_file="default_alarm.wav"):
        self.alarm_id = alarm_id
        self.alarm_type = alarm_type  # e.g., "fire", "intrusion", "temperature_alert"
        self.sound_file = sound_file
        self.is_sounding = False
        self.triggered_by_sensors = []

    def sound_alarm(self, sensor_triggered):
        if not self.is_sounding:
            self.is_sounding = True
            self.triggered_by_sensors.append(sensor_triggered)
            print(f"!!! ALARM {self.alarm_id} ({self.alarm_type.upper()}) SOUNDING !!! Triggered by {sensor_triggered.sensor_type} sensor at {sensor_triggered.location}.")
            # In a real system, this would play a sound file
            # import winsound
            # winsound.PlaySound(self.sound_file, winsound.SND_ASYNC)
        else:
            print(f"Alarm {self.alarm_id} is already sounding.")

    def silence_alarm(self):
        if self.is_sounding:
            self.is_sounding = False
            self.triggered_by_sensors = [] # Clear triggered sensors after silencing
            print(f"Alarm {self.alarm_id} ({self.alarm_type}) silenced.")
        else:
            print(f"Alarm {self.alarm_id} is not sounding.")

    def __str__(self):
        status = "Sounding" if self.is_sounding else "Silent"
        return f"Alarm ID: {self.alarm_id}, Type: {self.alarm_type.capitalize()}, Status: {status}"

class SafetyAlarmSystem:
    def __init__(self, system_name="Home Safety System"):
        self.system_name = system_name
        self.sensors = {}
        self.alarms = {}
        self.event_log = []

    def add_sensor(self, sensor):
        if sensor.sensor_id not in self.sensors:
            self.sensors[sensor.sensor_id] = sensor
            print(f"Sensor {sensor.sensor_id} added to {self.system_name}.")
        else:
            print(f"Sensor {sensor.sensor_id} already exists.")

    def add_alarm(self, alarm):
        if alarm.alarm_id not in self.alarms:
            self.alarms[alarm.alarm_id] = alarm
            print(f"Alarm {alarm.alarm_id} added to {self.system_name}.")
        else:
            print(f"Alarm {alarm.alarm_id} already exists.")

    def get_sensor(self, sensor_id):
        return self.sensors.get(sensor_id)

    def get_alarm(self, alarm_id):
        return self.alarms.get(alarm_id)

    def process_sensor_trigger(self, sensor_id):
        sensor = self.get_sensor(sensor_id)
        if sensor and sensor.trigger():
            event_time = datetime.datetime.now()
            log_entry = {
                "timestamp": event_time,
                "type": "sensor_trigger",
                "sensor_id": sensor.sensor_id,
                "sensor_type": sensor.sensor_type,
                "location": sensor.location
            }
            self.event_log.append(log_entry)
            print(f"Logged event: Sensor {sensor.sensor_id} triggered.")

            # Logic to link sensor triggers to alarms
            if sensor.sensor_type == "smoke":
                fire_alarm = self.get_alarm("A001") # Assuming A001 is fire alarm
                if fire_alarm:
                    fire_alarm.sound_alarm(sensor)
                    self.event_log.append({"timestamp": datetime.datetime.now(), "type": "alarm_sounded", "alarm_id": fire_alarm.alarm_id})
            elif sensor.sensor_type == "motion" or sensor.sensor_type == "door/window":
                intrusion_alarm = self.get_alarm("A002") # Assuming A002 is intrusion alarm
                if intrusion_alarm:
                    intrusion_alarm.sound_alarm(sensor)
                    self.event_log.append({"timestamp": datetime.datetime.now(), "type": "alarm_sounded", "alarm_id": intrusion_alarm.alarm_id})
            # Add more conditions for other sensor types and alarms
        elif not sensor:
            print(f"Sensor {sensor_id} not found.")

    def silence_all_alarms(self):
        for alarm in self.alarms.values():
            alarm.silence_alarm()
        self.event_log.append({"timestamp": datetime.datetime.now(), "type": "all_alarms_silenced"})

    def get_event_log(self):
        return self.event_log

    def __str__(self):
        return (f"Safety Alarm System: {self.system_name} | "
                f"Sensors: {len(self.sensors)} | "
                f"Alarms: {len(self.alarms)}")

# Example Usage:
if __name__ == "__main__":
    system = SafetyAlarmSystem("Smart Home Security")
    print(system)

    # Add sensors
    smoke_sensor = Sensor("S001", "smoke", "Kitchen")
    motion_sensor = Sensor("S002", "motion", "Living Room")
    door_sensor = Sensor("S003", "door/window", "Front Door")
    temp_sensor = Sensor("S004", "temperature", "Bedroom")

    system.add_sensor(smoke_sensor)
    system.add_sensor(motion_sensor)
    system.add_sensor(door_sensor)
    system.add_sensor(temp_sensor)

    # Add alarms
    fire_alarm = Alarm("A001", "fire")
    intrusion_alarm = Alarm("A002", "intrusion")
    system.add_alarm(fire_alarm)
    system.add_alarm(intrusion_alarm)

    print("\n--- Initial Sensor Status ---")
    print(smoke_sensor)
    print(motion_sensor)

    # Deactivate a sensor
    motion_sensor.deactivate()
    print("\n--- Motion Sensor after deactivation ---")
    print(motion_sensor)

    # Trigger sensors
    print("\n--- Triggering Sensors ---")
    system.process_sensor_trigger("S001") # Smoke sensor in Kitchen
    time.sleep(1) # Simulate time passing
    system.process_sensor_trigger("S002") # Inactive motion sensor
    time.sleep(1)
    system.process_sensor_trigger("S003") # Door sensor

    print("\n--- Alarm Status ---")
    print(fire_alarm)
    print(intrusion_alarm)

    # Silence alarms
    print("\n--- Silencing All Alarms ---")
    system.silence_all_alarms()
    print(fire_alarm)
    print(intrusion_alarm)

    # View event log
    print("\n--- Event Log ---")
    for event in system.get_event_log():
        print(f"[{event['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}] Type: {event['type']}, Details: {event}")