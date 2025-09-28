# Filed Map Area Project

This project contains scripts that gives example how to copy offline map areas in ArcGIS Portal. (workaround for the fastforward solution that is not working with the error "token required")

## Setup

Configure your environment variables:
   - Copy `config.py.example` to `config.py`
   - Edit `config.env` with your actual values:
     ```
     USERNAME=your_username@domain.com
     PASSWORD=your_password
     SOURCE=your_source_map_area_id
     TARGET=your_target_map_area_id
     ```

## Usage

### CpFMAreaImprove.py
Accepts configuration from config.py file and using it to get token of the owner of the filed mapo area and the source and targer id for the map to copy the feild-map-areas.

```bash
python CpFMAreaImprove.py
```

## Configuration

The `config.py` file contains:
- `USERNAME`: Your GIS portal username
- `PASSWORD`: Your GIS portal password  
- `SOURCE`: Source map area ID to copy from
- `TARGET`: Target map area ID to copy to

## Security Note

Never commit the `config.py` file to version control as it contains sensitive credentials. The `config.py.example` file serves as a template for other developers.
