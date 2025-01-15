import csv
from qgis.core import QgsWkbTypes
from qgis.utils import iface
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, QInputDialog, QLineEdit
from shapely.geometry import Polygon
import sys
import os

# Add the python/ directory to sys.path
plugin_path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(plugin_path, "python"))

from polygon_geohasher.polygon_geohasher import polygon_to_geohashes

class GeohashGeneratorPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        """Create the plugin GUI elements."""
        icon_path = os.path.join(plugin_path, 'icons', 'icon.png')  # Adjust path as needed
        if not os.path.exists(icon_path):
            print(f"Icon not found at {icon_path}")  # Debugging message
        self.action = QAction('Geohash Generator', self.iface.mainWindow())
        self.action.setIcon(QIcon(icon_path))
        self.action.triggered.connect(self.run)
        
        # Add the action to the QGIS toolbar
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        """Clean up the plugin when unloaded."""
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        """Main plugin execution."""

        # Step 1: Show dialog to select a layer
        layer = self.select_layer()
        if not layer:
            QMessageBox.critical(None, "Error", "No layer selected or invalid layer type.")
            return
        
        # Step 2: Show dialog to select geohash precision
        precision, ok = self.get_geohash_precision()
        if not ok or precision is None:
            QMessageBox.critical(None, "Error", "Invalid geohash precision.")
            return
        
        # Step 3: Check if the layer geometry type is polygon
        if layer.geometryType() != QgsWkbTypes.PolygonGeometry:
            QMessageBox.critical(None, "Error", "Layer must contain polygon or multipolygon geometries.")
            return

        # Step 4: Prompt for CSV file path
        file_path, ok = self.get_csv_file_path()
        if not ok or file_path is None:
            QMessageBox.critical(None, "Error", "Invalid file path.")
            return

        # Step 5: Process features and generate geohashes
        features_data = []
        for feature in layer.getFeatures():
            geometry = feature.geometry()

            # Check if geometry is a polygon or multipolygon
            if geometry.isMultipart():
                # Convert MultiPolygon to Polygon (flatten)
                polygons = [part for part in geometry.asMultiPolygon()]
            else:
                polygons = [geometry.asPolygon()]

            for polygon in polygons:
                # Convert list of QgsPointXY to a list of (x, y) tuples
                polygon_coords = []
                for ring in polygon:
                    for point in ring:
                        polygon_coords.append((point.x(), point.y()))  # Ensure it's a QgsPointXY

                # Convert list of coordinates to a Shapely Polygon
                shapely_polygon = Polygon(polygon_coords)

                # Generate geohashes
                try:
                    geohashes = polygon_to_geohashes(shapely_polygon, precision)  # Use selected precision
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Failed to generate geohashes: {e}")
                    return

                # Add features' attributes and geohashes to the data list
                for geohash in geohashes:
                    feature_data = list(feature.attributes()) + [geohash]
                    features_data.append(feature_data)

        # Step 6: Write data to CSV
        self.write_to_csv(file_path, features_data)

        QMessageBox.information(None, "Success", "Geohashes generated and saved to CSV.")

    def select_layer(self):
        """Allow the user to select a layer from the active layers."""
        layer = iface.activeLayer()
        if not layer:
            QMessageBox.critical(None, "Error", "No active layer found. Please select a valid layer.")
            return None
        return layer

    def get_geohash_precision(self):
        """Allow the user to input the geohash precision."""
        # Show input dialog for geohash precision
        precision, ok = QInputDialog.getInt(None, "Geohash Precision", 
                                             "Enter geohash precision (between 1 and 12):", 
                                             7, 1, 12, 1)
        return precision, ok

    def get_csv_file_path(self):
        """Prompt the user to provide the file path for saving the CSV."""
        # Use QInputDialog to let the user input the file path (no echo mode needed)
        file_path, ok = QInputDialog.getText(None, "Save CSV", 
                                            "Enter the file path for the CSV:", 
                                            QLineEdit.Normal, "/path/to/save.csv")
        return file_path, ok

    def write_to_csv(self, file_path, data):
        """Write the data to a CSV file."""
        try:
            # Write the headers (fields from the layer and geohash)
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if data:
                    headers = [field.name() for field in iface.activeLayer().fields()] + ['geohash']
                    writer.writerow(headers)  # Write header row
                    writer.writerows(data)  # Write the feature data
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to write CSV: {e}")
