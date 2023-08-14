# -*- coding: utf-8 -*-
import substance_painter 
import pathlib
import os
from PySide2 import QtWidgets


preset_path = "/Users/ymgmcmc/ymgmcmc/temp"
path = os.environ['SUBSTANCE_PAINTER_PLUGINS_PATH']
print(path)
SAMPLE_PRESET_PATH = os.path.join(path,"resources/liltoon.spexp")
print(SAMPLE_PRESET_PATH)
sample_plugin_widgets = []

def get_export_path()-> str:
    mesh_path = substance_painter.project.last_imported_mesh_path()
    mesh_name = pathlib.Path(mesh_path).stem
    export_path = pathlib.Path(preset_path, mesh_name)
    return str(export_path)

def get_export_config(export_path: str)-> dict:
    export_preset = substance_painter.resource.import_session_resource(SAMPLE_PRESET_PATH, substance_painter.resource.Usage.EXPORT)
    export_preset_url = export_preset.identifier().url()
    export_config = {
                    "exportPath":export_path,
                    "defaultExportPreset": export_preset_url,
                    "exportPresets":[ { "name" : "default", "maps" : [] } ],
                    "exportList":[],
                    "exportParameters":[{"parameters" : { "paddingAlgorithm": "infinite" }}],
                    "exportShaderParams":False
                    }
    export_list = export_config.get("exportList")
    for texture_set in substance_painter.textureset.all_texture_sets():
        export_list.append({"rootPath": texture_set.name()})
    return export_config

def export_textures():
    if not substance_painter.project.is_open():
        substance_painter.logging.log(
            substance_painter.logging.INFO,
            "samplePlugin",
            "Please open project or save project.")
        return
    export_path = get_export_path()
    export_config = get_export_config(export_path)
    export_result = substance_painter.export.export_project_textures(export_config)
    substance_painter.logging.log(
        substance_painter.logging.INFO,
        "samplePlugin",
        export_result.message)
    return  

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setWindowTitle("ymg_material")
        self.filepath = QtWidgets.QLabel("self")
        self.filepath.setText("empty")
        layout.addWidget(self.filepath)
        self.filebutton = QtWidgets.QPushButton("file")
        self.filebutton.clicked.connect(self.showDialog)
        layout.addWidget(self.filebutton)
        self.button = QtWidgets.QPushButton("export")
        self.button.clicked.connect(export_textures)
        layout.addWidget(self.button)
        self.setLayout(layout)
    
    def showDialog(self):
        options = QtWidgets.QFileDialog.Options()
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Folder", "", options=options)
        
        if folder_name:
            global preset_path 
            preset_path = folder_name
            self.filepath.setText(folder_name)
            print("Selected folder:", folder_name)

def start_plugin():
    global preset_path
    widget = Widget()
    substance_painter.ui.add_dock_widget(widget)
    sample_plugin_widgets.append(widget)

def close_plugin():
    for widget in sample_plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)
    sample_plugin_widgets.clear()

if __name__ == "__main__":
    start_plugin()