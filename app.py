import time
import requests
from prometheus_client import start_http_server, Gauge

# Constants
API_KEY = 'redacted'  # Replace with your actual API key
BASE_URL = 'https://app.pdq.com/v1/api'

# Prometheus metrics definitions
device_count = Gauge('pdq_device_count', 'Total number of devices managed by PDQ Connect')
device_info = Gauge('pdq_device_info', 'Basic information about the device', [
    'hostname', 'architecture', 'id', 'insertedAt', 'lastUser',
    'model', 'name', 'osVersion', 'publicIpAddress', 'serialNumber', 'servicePack'
])
disk_info = Gauge('pdq_disk_info', 'Information about the device disks', [
    'hostname', 'disk_id', 'model', 'mediaType', 'totalSpaceKb'
])
driver_info = Gauge('pdq_driver_info', 'Information about the device drivers', [
    'hostname', 'driver_id', 'name', 'version', 'provider'
])
ad_info = Gauge('pdq_ad_info', 'Active Directory information about the device', [
    'hostname', 'deviceName'
])
custom_fields_info = Gauge('pdq_custom_fields_info', 'Custom fields information about the device', [
    'hostname', 'field_name', 'field_value'
])

# Function to get devices from PDQ Connect API
def get_devices():
    url = f'{BASE_URL}/devices'
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "accept": "application/json"
    }
    params = {
        "includes": "disks,drivers,features,networking,processors,updates,software,activeDirectory,activeDirectoryGroups,customFields",
        "pageSize": 100,
        "page": 1,
        "sort": "insertedAt"
    }
    print(f"Fetching devices from {url} with params {params}")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad status codes
    print("Devices fetched successfully")
    return response.json()

# Function to collect and update Prometheus metrics for devices
def collect_device_metrics(devices):
    device_count.set(len(devices['data']))
    print(f"Updating metrics for {len(devices['data'])} devices")
    for device in devices['data']:
        hostname = device.get('hostname', 'unknown')
        architecture = device.get('architecture', 'unknown')
        device_id = device.get('id', 'unknown')
        inserted_at = device.get('insertedAt', 'unknown')
        last_user = device.get('lastUser', 'unknown')
        model = device.get('model', 'unknown')
        name = device.get('name', 'unknown')
        os_version = device.get('osVersion', 'unknown')
        public_ip_address = device.get('publicIpAddress', 'unknown')
        serial_number = device.get('serialNumber', 'unknown')
        service_pack = device.get('servicePack', 'unknown')

        # Update device info metric
        device_info.labels(
            hostname=hostname,
            architecture=architecture,
            id=device_id,
            insertedAt=inserted_at,
            lastUser=last_user,
            model=model,
            name=name,
            osVersion=os_version,
            publicIpAddress=public_ip_address,
            serialNumber=serial_number,
            servicePack=service_pack
        ).set(1)

        # Update disk info metrics
        for disk in device.get('disks', []):
            disk_info.labels(
                hostname=hostname,
                disk_id=disk.get('id', 'unknown'),
                model=disk.get('model', 'unknown'),
                mediaType=disk.get('mediaType', 'unknown'),
                totalSpaceKb=disk.get('totalSpaceKb', 0)
            ).set(1)

        # Update driver info metrics
        for driver in device.get('drivers', []):
            driver_info.labels(
                hostname=hostname,
                driver_id=driver.get('id', 'unknown'),
                name=driver.get('name', 'unknown'),
                version=driver.get('version', 'unknown'),
                provider=driver.get('provider', 'unknown')
            ).set(1)

        # Update Active Directory info metric
        active_directory = device.get('activeDirectory', {})
        if active_directory:
            ad_info.labels(
                hostname=hostname,
                deviceName=active_directory.get('deviceName', 'unknown')
            ).set(1)

        # Update custom fields metrics
        for field in device.get('customFields', []):
            custom_fields_info.labels(
                hostname=hostname,
                field_name=field.get('name', 'unknown'),
                field_value=field.get('value', 'unknown')
            ).set(1)

        print(f"Metrics updated for device: {hostname}")

if __name__ == '__main__':
    print("Starting Prometheus exporter")
    # Start up the server to expose the metrics.
    start_http_server(8000)
    print("Prometheus exporter started on port 8000")
    # Continuously collect metrics every 60 seconds.
    while True:
        try:
            print("Collecting metrics...")
            devices = get_devices()
            collect_device_metrics(devices)
            print("Metrics collected successfully")
        except Exception as e:
            print(f"Error collecting metrics: {e}")
        time.sleep(60)
