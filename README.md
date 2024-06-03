# PDQ Connect Prometheus Exporter

## Overview

This project is a Prometheus exporter that collects and exposes metrics from the PDQ Connect API. It fetches device data and provides several metrics with detailed labels to facilitate monitoring and alerting.

## Features

- Fetches detailed device information from the PDQ Connect API.
- Exposes metrics in Prometheus format.
- Provides granular metrics for various aspects of the devices, including basic information, disk details, driver details, Active Directory information, and custom fields.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/brngates98/PDQ-Connect-Prometheus-Exporter/tree/main
    cd PDQ-Connect-Prometheus-Exporter
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set your PDQ Connect API key in the script by replacing `redacted` with your actual API key.

4. Run the exporter:

    ```bash
    python pdq_exporter.py
    ```

## Metrics

| Metric Name            | Description                         | Labels                                                                                                                       | Label Values Example                                                                                                                      | Metric Values  |
|------------------------|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| `pdq_device_count`     | Total number of devices managed by PDQ Connect | None                                                                                                                         | None                                                                                                                                      | Total count of devices (e.g., 50)  |
| `pdq_device_info`      | Basic information about the device  | `hostname`, `architecture`, `id`, `insertedAt`, `lastUser`, `model`, `name`, `osVersion`, `publicIpAddress`, `serialNumber`, `servicePack` | `hostname="example-hostname"`, `architecture="64-bit"`, `id="device123"`, `insertedAt="2024-01-01T00:00:00.000000Z"`, `lastUser="user1"`, `model="model123"`, `name="Device Name"`, `osVersion="10.0.12345"`, `publicIpAddress="192.0.2.1"`, `serialNumber="SN123456"`, `servicePack="SP1"` | 1               |
| `pdq_disk_info`        | Information about the device disks  | `hostname`, `disk_id`, `model`, `mediaType`, `totalSpaceKb`                                                                  | `hostname="example-hostname"`, `disk_id="disk1"`, `model="Disk Model"`, `mediaType="SSD"`, `totalSpaceKb="500000"`                        | 1               |
| `pdq_driver_info`      | Information about the device drivers | `hostname`, `driver_id`, `name`, `version`, `provider`                                                                       | `hostname="example-hostname"`, `driver_id="driver1"`, `name="Driver Name"`, `version="1.0.0"`, `provider="Provider Name"`                  | 1               |
| `pdq_ad_info`          | Active Directory information about the device | `hostname`, `deviceName`                                                                                                     | `hostname="example-hostname"`, `deviceName="AD Device Name"`                                                                              | 1               |
| `pdq_custom_fields_info` | Custom fields information about the device | `hostname`, `field_name`, `field_value`                                                                                       | `hostname="example-hostname"`, `field_name="Custom Field 1"`, `field_value="Custom Value 1"`                                              | 1               |

## Usage

The exporter runs a web server on port `8000` and exposes the metrics at the `/metrics` endpoint. You can configure Prometheus to scrape these metrics by adding the following job to your Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'pdq_exporter'
    static_configs:
      - targets: ['localhost:8000']
