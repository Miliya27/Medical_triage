"""
Unit Test for BLE Sensor & Vitals Module
"""

import asyncio
from backend.app.sensors.ble_vitals import BLEVitalsScanner

def test_ble_sensor_scanner():
    scanner = BLEVitalsScanner()
    
    # Test device discovery
    devices = asyncio.run(scanner.scan_devices(timeout=1.0))
    assert len(devices) > 0, "BLE scanner should discover devices or return simulated sensors"
    print("Discovered BLE Devices:", devices)
    
    # Test reading live vitals
    vitals = scanner.read_live_vitals()
    assert "heart_rate" in vitals
    assert "spo2" in vitals
    assert "sensor_battery" in vitals
    print("Live BLE Vitals Sample:", vitals)
    print("✅ BLE Sensor test passed!")

if __name__ == "__main__":
    test_ble_sensor_scanner()
