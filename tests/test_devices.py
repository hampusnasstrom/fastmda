from fastmda.exceptions import FastMDAConnectFailed
from fastmda.devices import example_device


def test_example_device():
    device_instance = example_device.Device('COM1')
    print(device_instance.id)
    print(device_instance.get_detectors())
    try:
        device_instance.connect()
    except FastMDAConnectFailed as e:
        print(e)


def main():
    test_example_device()


if __name__ == "__main__":
    main()
