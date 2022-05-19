from fastmda.device_types.example_device import example_device

from fastapi.testclient import TestClient
from fastmda.main import app


def test_example_device():
    device_id = 1
    device_instance = example_device.Device(device_id, 'COM1')
    assert device_instance.device_id == device_id
    assert isinstance(device_instance.detectors, dict)
    device_instance.connect()


def test_get_device_types():
    with TestClient(app) as client:
        response = client.get('/devices/device_types')
        response_json = response.json()
        print(response_json)
        assert isinstance(response_json, dict)
