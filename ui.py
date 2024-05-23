import imgui
import imgui.core
from imgui.integrations.pyglet import PygletProgrammablePipelineRenderer

import tkinter as tk
from tkinter import filedialog

class UI:
    def __init__(self, window):
        imgui.create_context()
        self.impl = PygletProgrammablePipelineRenderer(window)
        imgui.new_frame()
        imgui.end_frame()

        # Window variables
        self.focused = False
        self.color = 0.5, 0.5, 0.5, 1.0
        self.grid_active = False
        self.grid_size = 100
        self.grid_unit = 1
        self.wireframe_active = False
        self.control_active = True
        self.filename = None
        self.command_queue = []
        self.log_text = ""
        
    def log(self, arg):
        self.log_text = str(arg)

    def render(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())
        imgui.new_frame()

        # root window
        imgui.begin("Controller")
        self.focused = imgui.is_window_focused(flags = imgui.FOCUS_CHILD_WINDOWS)
        
        # button (reset)
        if imgui.button("Reset"):
            self.command_queue.append("reset")
        imgui.same_line()
        imgui.text("Reset Control Points")

        # button (import)
        if imgui.button("Import"):
            root = tk.Tk()
            root.withdraw()
            filename = filedialog.askopenfilename(
                filetypes=(("object files", ".obj"),), title="Import obj file"
            )
            root.destroy()
            if len(filename) > 0:
                self.command_queue.append("import")
                self.filename = filename
        imgui.same_line()
        imgui.text("Load *.obj file")

        # color edit (color)
        changed, self.color = imgui.color_edit4("Color", *self.color)
        if changed:
            self.command_queue.append("update_color")

        # radio (wireframe onoff)
        if imgui.radio_button("Wireframe On/Off", self.wireframe_active):
            self.wireframe_active = not self.wireframe_active
            self.command_queue.append("update_visibility")
            
        # radio (control onoff)
        if imgui.radio_button("Control On/Off", self.control_active):
            self.control_active = not self.control_active
            self.command_queue.append("update_visibility")
            
        # collapse (grid options)
        expanded, _ = imgui.collapsing_header("Grid Options", None)
        if expanded:
            # radio (grid onoff)
            if imgui.radio_button("Grid On/Off", self.grid_active):
                self.grid_active = not self.grid_active
                self.command_queue.append("update_visibility")
                
            # slider int (grid size)
            changed, self.grid_size = imgui.slider_int(
                "Size", self.grid_size, min_value=1, max_value=100, format="%d"
            )
            if changed:
                self.command_queue.append("update_grid")
        
            # slider float (grid unit)
            changed, self.grid_unit = imgui.slider_float(
                "Unit", self.grid_unit, min_value=0.1, max_value=10.0, format="%.2f"
            )
            if changed:
                self.command_queue.append("update_grid")

        # prompt
        with imgui.begin_child("Prompt", border=True, height=30):
            imgui.text(self.log_text)
            
        imgui.end()

        imgui.end_frame()
