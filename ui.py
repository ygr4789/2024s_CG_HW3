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

        # prompt
        with imgui.begin_child("Prompt", border=True, height=30):
            imgui.text(self.log_text)
            
        imgui.end()

        imgui.end_frame()
