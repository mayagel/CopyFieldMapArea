# Filed Map Area Project

This project contains scripts for managing offline map areas in ArcGIS Portal.

## Setup

Configure your environment variables:
   - Copy `config.env.example` to `config.env`
   - Edit `config.env` with your actual values:
     ```
     USERNAME=your_username@domain.com
     PASSWORD=your_password
     SOURCE=your_source_map_area_id
     TARGET=your_target_map_area_id
     ```

## Usage

### CpFMAreaImprove.py
Improved version that accepts configuration via environment variables instead of command line arguments.

```bash
python CpFMAreaImprove.py
```

## Configuration

The `config.env` file contains:
- `USERNAME`: Your GIS portal username
- `PASSWORD`: Your GIS portal password  
- `SOURCE`: Source map area ID to copy from
- `TARGET`: Target map area ID to copy to

## Security Note

Never commit the `config.env` file to version control as it contains sensitive credentials. The `config.env.example` file serves as a template for other developers.
