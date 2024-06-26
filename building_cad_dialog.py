# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BuildingCadDialog
                                 A QGIS plugin
 This plugin can generate point features based on reference points and angles
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-01-12
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Kalundborg Kommune
        email                : andj@kalundborg.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import math

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPen, QBrush, QIcon
from PyQt5.QtCore import QVariant, Qt
from qgis.core import QgsProject, QgsMapLayerType, QgsWkbTypes, QgsFeature, QgsGeometry, QgsPointXY, QgsVectorLayer, QgsPointLocator, QgsField
from qgis.gui import QgsMapTool, QgsMapToolEmitPoint, QgsVertexMarker, QgsSnapIndicator, QgsRubberBand

# This loads the .ui file so that PyQt can populate the plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'building_cad_dialog_base.ui'))


class BuildingCadDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super(BuildingCadDialog, self).__init__(parent)
        self.setupUi(self)

        # Set the dialog window icon
        icon_path = ':/plugins/terrain_analysis/icon.png'  # Resource path to the icon
        self.setWindowIcon(QIcon(icon_path))
        
        # Setting the position of the dialog to not be in the middle of the screen
        self.move(100, 100)
        
        # Store the iface object for later use
        self.iface = iface

        # Create a custom map tool for emitting points
        self.emitPointTool = CustomEmitPointTool(self.iface.mapCanvas(), self)
        
        # Create a custom map tool for emitting points
        self.endEmitPointTool = EndCustomEmitPointTool(self.iface.mapCanvas(), self)

        # Connect the button click event to the custom map tool activation
        self.reference_start.clicked.connect(self.activateEmitPointTool)
        
        # Connect the button click event to the custom map tool activation
        self.reference_end.clicked.connect(self.activateEndEmitPointTool)
        
        # Connect the button click event to the custom map tool activation
        self.start_point_pb.clicked.connect(self.placeTemporaryDot)

        # Connect the button click event to clear_angle method
        self.clear_angel_pb.clicked.connect(self.clear_angle)

        # Connect the button box signals to custom slots
        self.button_box.accepted.connect(self.onButtonBoxAccepted)
        self.button_box.rejected.connect(self.onButtonBoxRejected)

        # Initialize variables to store the start and end points
        self.reference_x = None
        self.reference_y = None
        self.end_reference_x = None  # Initialize to None
        self.end_reference_y = None  # Initialize to None

        # Initialize the angle variable
        self.angle = None

        # Initialize snapping configuration
        self.snappingUtils = self.iface.mapCanvas().snappingUtils()
        self.snapIndicator = QgsSnapIndicator(self.iface.mapCanvas())
        self.snapping_enabled = True  

        # Activate snapping
        self.toggleSnapping()
        
        # Initialize the rubber band for line drawing, with line geometry
        self.rubberBand = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.LineGeometry)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(2)
        
        self.originalSnappingConfig = None
        self.saveUserSnappingSettings()

    def saveUserSnappingSettings(self):
        self.originalSnappingConfig = self.iface.mapCanvas().snappingUtils().config()

    def restoreUserSnappingSettings(self):
        self.iface.mapCanvas().snappingUtils().setConfig(self.originalSnappingConfig)

    def clear_angle(self):
        # Clear the angle variable
        self.angle = None
        self.reference_x = None
        self.reference_y = None
        self.end_reference_x = None  # Initialize to None
        self.end_reference_y = None  # Initialize to None

        # Clear the rubber band
        if self.rubberBand:
            self.rubberBand.reset(QgsWkbTypes.LineGeometry)  # Reset the rubber band

        # Show a message box to inform the user
        QMessageBox.information(self, "Angle Cleared", "Angle has been cleared.", QMessageBox.Ok)

    def calculate_angle(self):
        if self.reference_x is not None and self.reference_y is not None and \
                self.end_reference_x is not None and self.end_reference_y is not None:

            # Calculate the angle between start_feature and end_feature
            angle = math.atan2(self.end_reference_y - self.reference_y, self.end_reference_x - self.reference_x)
            angle_degrees = math.degrees(angle)

            # Store the angle as a class variable
            self.angle = angle_degrees

            # Print the angle to the console
            print(f"Angle between start_feature and end_feature: {self.angle} degrees")
        
    def activateEmitPointTool(self):
        # Check if the start reference point is already set and angle is not cleared
        if self.reference_x is not None and self.reference_y is not None and self.angle is not None:
            self.showErrorDialog("Start reference point has already been set. Please clear the angle first.")
            return
            
        # Minimize the dialog when the button is clicked
        self.showMinimized()

        # Deactivate snapping for the previous tool (if any)
        if hasattr(self, 'activeMapTool'):
            self.activeMapTool.deactivateSnapping()

        # Activate the custom emit point tool when the button is clicked
        self.emitPointTool.activateSnapping(self.snapping_enabled)
        self.emitPointTool.activate()
        self.iface.mapCanvas().setMapTool(self.emitPointTool)
        self.activeMapTool = self.emitPointTool

    def activateEndEmitPointTool(self):
        # Check if the end reference point is already set and angle is not cleared
        if self.end_reference_x is not None and self.end_reference_y is not None and self.angle is not None:
            self.showErrorDialog("End reference point has already been set. Please clear the angle first.")
            return
            
        # Minimize the dialog when the button is clicked
        self.showMinimized()

        # Deactivate snapping for the previous tool (if any)
        if hasattr(self, 'activeMapTool'):
            self.activeMapTool.deactivateSnapping()

        # Activate the custom emit point tool when the button is clicked
        self.endEmitPointTool.activateSnapping(self.snapping_enabled)
        self.endEmitPointTool.activate()
        self.iface.mapCanvas().setMapTool(self.endEmitPointTool)
        self.activeMapTool = self.endEmitPointTool

    def toggleSnapping(self):
        # Toggle snapping status
        self.snapping_enabled = not self.snapping_enabled
        self.snappingUtils.toggleEnabled()
        self.snappingUtils.setConfig(self.snappingUtils.config())  
        self.snapIndicator.setVisible(self.snapping_enabled)
            
    def handleEmitPoint(self, snapped_point, exact_point, button):
        # Choose which point(s) to use based on your requirements
        if snapped_point is not None:
            ref_x = snapped_point.x()
            ref_y = snapped_point.y()
            # Do something with snapped_point
        else:
            ref_x = exact_point.x()
            ref_y = exact_point.y()
            # Do something with exact_point

        # Do something common with the coordinates
        self.reference_x = ref_x
        self.reference_y = ref_y
        print(f"Reference Point: X={ref_x}, Y={ref_y}")

        # Restore the dialog to normal state
        self.showNormal()
        
        # Update the rubber band
        self.updateRubberBand()

    def handleEndEmitPoint(self, end_snapped_point, end_exact_point, button):
        # Choose which point(s) to use based on your requirements
        if end_snapped_point is not None:
            end_ref_x = end_snapped_point.x()
            end_ref_y = end_snapped_point.y()
            # Do something with end_snapped_point
        else:
            end_ref_x = end_exact_point.x()
            end_ref_y = end_exact_point.y()
            # Do something with end_exact_point

        # Do something common with the coordinates
        self.end_reference_x = end_ref_x
        self.end_reference_y = end_ref_y
        print(f"Reference Point: X={end_ref_x}, Y={end_ref_y}")

        # Restore the dialog to normal state
        self.showNormal()
        
        # Update the rubber band
        self.updateRubberBand()

    def updateRubberBand(self):
        self.rubberBand.reset(QgsWkbTypes.LineGeometry)  # Ensure geometry type is LineGeometry
        if self.reference_x is not None and self.reference_y is not None and \
           self.end_reference_x is not None and self.end_reference_y is not None:
            # Add points to the rubber band
            start_point = QgsPointXY(self.reference_x, self.reference_y)
            end_point = QgsPointXY(self.end_reference_x, self.end_reference_y)
            self.rubberBand.addPoint(start_point, False)  # False to not update canvas yet
            self.rubberBand.addPoint(end_point, True)  # True to update canvas now
        else:
            # If any point is missing, the rubber band is already reset above
            pass

    def placeTemporaryDot(self):
        # Check if required variables are set
        if (
            self.reference_x is None
            or self.reference_y is None
            or self.end_reference_x is None
            or self.end_reference_y is None
        ):
            error_message = "Please set both start and end reference points before placing a dot."
            self.showErrorDialog(error_message)
            return

        # Check if start_distance_edit has a valid input
        start_distance_text = self.start_distance_edit.text()
        if not start_distance_text or not start_distance_text.isdigit():
            error_message = "Please enter a valid distance."
            self.showErrorDialog(error_message)
            return

        # Convert the input distance to a float
        distance = float(start_distance_text)

        # Calculate the final coordinates of the start point
        start_point_x = self.reference_x
        start_point_y = self.reference_y

        # Calculate the angle (if not already calculated)
        if self.angle is None:
            self.calculate_angle()

        # Calculate the new dot coordinates using the distance and angle
        new_dot_x = start_point_x + distance * math.cos(math.radians(self.angle))
        new_dot_y = start_point_y + distance * math.sin(math.radians(self.angle))

        # Create a point geometry for the new dot
        new_dot_geometry = QgsGeometry.fromPointXY(QgsPointXY(new_dot_x, new_dot_y))

        # Create a temporary memory layer if it does not exist
        layer_name = "dot_layer"
        if not QgsProject.instance().mapLayersByName(layer_name):
            dot_layer = QgsVectorLayer("Point?crs=EPSG:25832", layer_name, "memory")
            QgsProject.instance().addMapLayer(dot_layer)

        # Get the temporary dot layer
        dot_layer = QgsProject.instance().mapLayersByName(layer_name)[0]

        # Create a feature with the point geometry
        new_dot_feature = QgsFeature()
        new_dot_feature.setGeometry(new_dot_geometry)

        # Add the "point" field to the feature
        dot_layer.startEditing()
        dot_layer.dataProvider().addAttributes([QgsField("point", QVariant.String)])
        dot_layer.updateFields()

        # Set the "point" attribute value
        new_dot_feature.setAttributes(["new_dot"])

        # Add the feature to the dot layer
        dot_layer.addFeature(new_dot_feature)
        dot_layer.commitChanges()

        # Refresh the canvas to reflect the changes
        self.iface.mapCanvas().refresh()

        # Print a message to indicate the new dot placement
        print(f"Placed a new dot at: X={new_dot_x}, Y={new_dot_y}")

        # Check if distance_direction has a valid input
        distance_direction_text = self.distance_direction.text()
        if not distance_direction_text or not distance_direction_text.replace(".", "").replace("-", "").isdigit():
            print("Please enter a valid distance direction.")
            return

        # Convert the input distance direction to a float
        distance_direction = float(distance_direction_text)

        # Calculate the angle adjustment based on the input
        angle_adjustment = 90 if distance_direction < 0 else -90

        # Calculate the final angle by considering both the distance and direction
        adjusted_angle = self.angle + angle_adjustment

        # Calculate the new dot coordinates using the adjusted angle
        building_point_x = new_dot_x + abs(distance_direction) * math.cos(math.radians(adjusted_angle))
        building_point_y = new_dot_y + abs(distance_direction) * math.sin(math.radians(adjusted_angle))

        # Create a point geometry for the building point
        building_point_geometry = QgsGeometry.fromPointXY(QgsPointXY(building_point_x, building_point_y))

        # Create a temporary memory layer if it does not exist
        building_layer_name = "building_point_layer"
        if not QgsProject.instance().mapLayersByName(building_layer_name):
            building_layer = QgsVectorLayer("Point?crs=EPSG:25832", building_layer_name, "memory")
            QgsProject.instance().addMapLayer(building_layer)

        # Get the temporary building point layer
        building_layer = QgsProject.instance().mapLayersByName(building_layer_name)[0]

        # Create a feature with the point geometry
        building_point_feature = QgsFeature()
        building_point_feature.setGeometry(building_point_geometry)

        # Add the "point" field to the feature
        building_layer.startEditing()
        building_layer.dataProvider().addAttributes([QgsField("point", QVariant.String)])
        building_layer.updateFields()

        # Set the "point" attribute value
        building_point_feature.setAttributes(["1"])

        # Add the feature to the building point layer
        building_layer.addFeature(building_point_feature)
        building_layer.commitChanges()

        # Refresh the canvas to reflect the changes
        self.iface.mapCanvas().refresh()

        # Print a message to indicate the building point placement
        print(f"Placed a building point at: X={building_point_x}, Y={building_point_y}")

    def showErrorDialog(self, error_message):
        # Create a QMessageBox for showing an error message
        error_dialog = QtWidgets.QMessageBox(self)
        error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(error_message)
        error_dialog.exec_()

    def onButtonBoxAccepted(self):
        # This slot is called when the "OK" button is clicked
        self.clearVariables()

        # Close the dialog
        self.accept()

    def onButtonBoxRejected(self):
        # This slot is called when the "Cancel" button is clicked
        self.clearVariables()

        # Close the dialog
        self.reject()

    def clearVariables(self):
        # Clear the variables
        self.reference_x = None
        self.reference_y = None
        self.end_reference_x = None
        self.end_reference_y = None
        self.angle = None
        
        # Clear the rubber band
        self.rubberBand.reset()
        
        # Deactivate the CustomEmitPointTool and EndCustomEmitPointTool if they are the active map tool
        if self.iface.mapCanvas().mapTool() == self.emitPointTool:
            self.emitPointTool.deactivate()
        elif self.iface.mapCanvas().mapTool() == self.endEmitPointTool:
            self.endEmitPointTool.deactivate()
        
        # Activate the selection tool
        self.iface.actionSelect().trigger()

class CustomEmitPointTool(QgsMapToolEmitPoint):
    def __init__(self, canvas, parent):
        super(CustomEmitPointTool, self).__init__(canvas)
        self.parent = parent
        self.snapIndicator = QgsSnapIndicator(canvas)
        self.snapped_point = None
        self.exact_point = None
        
    def activate(self):
        super(CustomEmitPointTool, self).activate()
        # Retrieve the current snapping configuration
        snapping_config = self.parent.snappingUtils.config()
        # Enable snapping
        snapping_config.setEnabled(True)
        # Apply the modified configuration
        self.parent.snappingUtils.setConfig(snapping_config)
        self.parent.snapIndicator.setVisible(True)

    def activateSnapping(self, enable_snapping):
        # Activate or deactivate snapping for this tool
        self.parent.snappingUtils.toggleEnabled()
        self.parent.snapIndicator.setVisible(enable_snapping)

    def canvasMoveEvent(self, event):
        snapMatch = self.parent.snappingUtils.snapToMap(event.pos())
        self.snapIndicator.setMatch(snapMatch)

        # Update the snapped_point variable
        if snapMatch.isValid():
            self.snapped_point = snapMatch.point()
        # Always update the exact_point variable
        self.exact_point = self.toMapCoordinates(event.pos())

    def canvasReleaseEvent(self, event):
        # Call the base class method to emit the point
        super(CustomEmitPointTool, self).canvasReleaseEvent(event)

        # Handle the emitted points in the parent dialog
        self.parent.handleEmitPoint(self.snapped_point, self.exact_point, event.button())

    def activateSnapping(self, enable_snapping):
        # Activate or deactivate snapping for this tool
        self.parent.snappingUtils.toggleEnabled()
        self.parent.snapIndicator.setVisible(enable_snapping)

    def deactivateSnapping(self):
        # Deactivate snapping for this tool
        self.parent.snappingUtils.toggleEnabled()
        self.parent.snapIndicator.setVisible(False)

    def deactivate(self):
        super(CustomEmitPointTool, self).deactivate()
    

class EndCustomEmitPointTool(QgsMapToolEmitPoint):
    def __init__(self, canvas, parent):
        super(EndCustomEmitPointTool, self).__init__(canvas)
        self.parent = parent
        self.snapIndicator = QgsSnapIndicator(canvas)
        self.end_snapped_point = None
        self.end_exact_point = None
        
    def activate(self):
        super(EndCustomEmitPointTool, self).activate()
        # The same changes as in CustomEmitPointTool
        snapping_config = self.parent.snappingUtils.config()
        snapping_config.setEnabled(True)
        self.parent.snappingUtils.setConfig(snapping_config)
        self.parent.snapIndicator.setVisible(True)

    def activateSnapping(self, enable_snapping):
        # Activate or deactivate snapping for this tool
        self.parent.snappingUtils.toggleEnabled()
        self.parent.snapIndicator.setVisible(enable_snapping)

    def canvasMoveEvent(self, event):
        snapMatch = self.parent.snappingUtils.snapToMap(event.pos())
        self.snapIndicator.setMatch(snapMatch)

        # Update the end_snapped_point variable
        if snapMatch.isValid():
            self.end_snapped_point = snapMatch.point()
        # Always update the end_exact_point variable
        self.end_exact_point = self.toMapCoordinates(event.pos())

    def canvasReleaseEvent(self, event):
        # Call the base class method to emit the point
        super(EndCustomEmitPointTool, self).canvasReleaseEvent(event)

        # Handle the emitted points in the parent dialog
        self.parent.handleEndEmitPoint(self.end_snapped_point, self.end_exact_point, event.button())

    def activateSnapping(self, enable_snapping):
        # Activate or deactivate snapping for this tool
        self.parent.snappingUtils.toggleEnabled()
        self.parent.snapIndicator.setVisible(enable_snapping)

    def deactivateSnapping(self):
        # Deactivate snapping for this tool
        self.parent.snappingUtils.toggleEnabled()
        self.parent.snapIndicator.setVisible(False)

    def deactivate(self):
        super(EndCustomEmitPointTool, self).deactivate()
