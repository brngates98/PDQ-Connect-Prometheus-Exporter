import time
import requests
from prometheus_client import start_http_server, Gauge

# Constants
API_KEY = 'redacted'  # Replace with your actual API key
BASE_URL = 'https://app.pdq.com/v1/api'

# Prometheus metrics definition
pdq_devices = Gauge('pdq_devices', 'Information about devices managed by PDQ Connect', [
    'hostname', 'architecture', 'id', 'insertedAt', 'lastUser',
    'model', 'name', 'osVersion', 'publicIpAddress', 'serialNumber',
    'servicePack', 'activeDirectory', 'customFields', 'disks', 'drivers'
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

# Function to format custom fields into a string
def format_custom_fields(custom_fields):
    return ', '.join(f"{field.get('name', 'unknown')}={field.get('value', 'unknown')}" for field in custom_fields if field)

# Function to format disks into a string
def format_disks(disks):
    return '; '.join(f"Disk {disk.get('id', 'unknown')}: {disk.get('model', 'unknown')}, {disk.get('mediaType', 'unknown')}, {disk.get('totalSpaceKb', 'unknown')} KB" for disk in disks if disk)

# Function to format drivers into a string
def format_drivers(drivers):
    return '; '.join(f"Driver {driver.get('id', 'unknown')}: {driver.get('name', 'unknown')}, {driver.get('version', 'unknown')}, {driver.get('provider', 'unknown')}" for driver in drivers if driver)

# Function to collect and update Prometheus metrics for devices
def collect_device_metrics(devices):
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

        active_directory = device.get('activeDirectory', {}).get('deviceName', 'unknown') if device.get('activeDirectory') else 'unknown'
        custom_fields = format_custom_fields(device.get('customFields', [])) if device.get('customFields') else 'unknown'
        disks = format_disks(device.get('disks', [])) if device.get('disks') else 'unknown'
        drivers = format_drivers(device.get('drivers', [])) if device.get('drivers') else 'unknown'

        pdq_devices.labels(
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
            servicePack=service_pack,
            activeDirectory=active_directory,
            customFields=custom_fields,
            disks=disks,
            drivers=drivers
        ).set(1)  # Using 1 as the value to indicate the presence of the device

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
