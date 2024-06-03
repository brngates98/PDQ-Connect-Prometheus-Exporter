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
| `pdq_device_info`      | Basic information about the device  | `hostname`, `architecture`, `id`, `insertedAt`, `lastUser`, `model`, `name`, `osVersion`, `publicIpAddress`, `serialNumber`, `servicePack` | `hostname="TMG-PF2KWRXY.bearsden.local"`, `architecture="64-bit"`, `id="dvc_1bced782734040a581d"`, `insertedAt="2024-01-01T00:00:00.000000Z"`, `lastUser="someuser"`, `model="8884664217"`, `name="LAB01"`, `osVersion="10.0.17328"`, `publicIpAddress="451E:6414:DEC9:2428:7154:D717:8D0F:7D2C"`, `serialNumber="56701fc8-de8f-4ccb-9a4d-3b97676d04d2"`, `servicePack="wav"` | 1               |
| `pdq_disk_info`        | Information about the device disks  | `hostname`, `disk_id`, `model`, `mediaType`, `totalSpaceKb`                                                                  | `hostname="TMG-PF2KWRXY.bearsden.local"`, `disk_id="disk1"`, `model="Samsung SSD"`, `mediaType="SSD"`, `totalSpaceKb="500000"`              | 1               |
| `pdq_driver_info`      | Information about the device drivers | `hostname`, `driver_id`, `name`, `version`, `provider`                                                                       | `hostname="TMG-PF2KWRXY.bearsden.local"`, `driver_id="driver1"`, `name="Intel Network Driver"`, `version="1.0.0"`, `provider="Intel"`       | 1               |
| `pdq_ad_info`          | Active Directory information about the device | `hostname`, `deviceName`                                                                                                     | `hostname="TMG-PF2KWRXY.bearsden.local"`, `deviceName="AD Device 1"`                                                                      | 1               |
| `pdq_custom_fields_info` | Custom fields information about the device | `hostname`, `field_name`, `field_value`                                                                                       | `hostname="TMG-PF2KWRXY.bearsden.local"`, `field_name="Custom Field 1"`, `field_value="Custom Value 1"`                                    | 1               |

## Usage

The exporter runs a web server on port `8000` and exposes the metrics at the `/metrics` endpoint. You can configure Prometheus to scrape these metrics by adding the following job to your Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'pdq_exporter'
    static_configs:
      - targets: ['localhost:8000']
