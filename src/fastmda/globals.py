from fastmda.schemas import DeviceInfo

device_info = {
    1: DeviceInfo(
        name="Some device",
        device_type='example_device',
        args={
            "com_port": "COM1"
        }
    )
}
device_dict = {}