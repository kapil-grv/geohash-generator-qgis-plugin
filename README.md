# Geohash Generator Plugin for QGIS

This QGIS plugin generates geohashes for polygon features in a selected vector layer and optionally saves them to a CSV file. It uses the Shapely library to convert polygons to geohashes with a specified precision and processes the polygons from a selected layer.

## Features

- Select a vector layer containing polygon or multipolygon geometries.
- Specify the precision of the geohashes (between 1 and 12).
- Generate geohashes for the polygons in the selected layer.
- Export the geohashes to a new CSV file for further analysis.

## Requirements

- QGIS 3.x (tested with QGIS 3.40.2-Bratislava)
- Python 3.x (tested with Python 3.12.3)
- Required Python libraries:
  - `shapely` (for polygon to geohash conversion)
  - `polygon_geohasher` (for geohash generation)

## Installation

### Method 1:
1. Download the repository and zip the folder / Just use the zip already available in the repo
2. Open QGIS -> Plugins -> Manage and Install Plugins -> Install from ZIP -> Upload the zip and click on Install Plugin

### Method 2:
1. Clone or download the repository.
2. Install the necessary Python libraries. Run the following command:
   ```bash
   pip install shapely polygon_geohasher
   ```
3. Copy the plugin folder to your QGIS plugin directory. For example:
   - `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
4. Restart QGIS.

## Usage

1. Open QGIS and load a vector layer containing polygons.
2. Find and activate the "Geohash Generator" plugin from the toolbar.
3. Select the layer you want to process.
4. Choose the precision level for the geohash generation (between 1 and 12).
5. Optionally, specify a file path to save the results as a CSV file.
6. The plugin will generate geohashes and save them to a new CSV file.

### Example Workflow

1. **Select Layer**: Choose the layer containing polygon data (e.g., a shapefile of regions).
2. **Set Precision**: Enter the desired geohash precision (e.g., 7).
3. **Generate Geohashes**: The plugin will process the polygons and generate geohashes.
4. **Save to CSV**: You will be prompted to provide a file path to save the output as a CSV.

## Contributing

Feel free to fork the repository, submit issues, and contribute code. All contributions are welcome.

## License

This plugin is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This structure provides a concise overview of your plugin, its features, installation instructions, usage guidelines, and how to contribute. Make sure to update the README with any specific details related to your implementation or features. Let me know if you need further adjustments!