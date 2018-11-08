# -*- coding: utf-8 -*-
"""Home Automation Control Panel.

Authors:
    Yvan Satyawan <y_satyawan@hotmail.com>

A full screen application for Raspberry Pi meant to interact with Home
Assistant to control to provide an on screen GUI designed for a 3.5" screen.
"""

import tkinter as tk    # Import Tkinter

from tkinter import font as tkfont

import time # Import time for timing click durations


class HACP(tk.Tk):
    """ Main class that represents the app and extends tkinter.Tk.

        This is the main class of the control panel. It holds all the
        different functions that are used to control the house outside of
        the communication functions, which are handled by its own class.
    """
    def __init__(self, *args, **kwargs):
        # initialize tk itself
        tk.Tk.__init__(self, *args, **kwargs)

        # set self properties
        self.geometry("480x320")
        self.current_screen = []
        self.title("Home Automation Control Panel")

        # house states
        # TODO change this to query the actual state first
        self.lights_master_state = False
        self.heating_master_state = False

        # Using a stacked frame system with one main frame to contain the
        # others. Sourced from https://stackoverflow.com/questions/7546050/
        # switch-between-two-frames-in-tkinter#
        container = tk.Frame(self, bg='#303030')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # List of all frames to be used, i.e. rooms
        frame_list = {Home,
                      Living,
                      Bed,
                      Entrance,
                      Hallway,
                      Kitchen}

        self.frames = {}

        for F in frame_list:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")
        self.current_screen = "Home"

    def show_frame(self, page_name):
        """ Shows the desired frame by putting it on top.

        Args:
            page_name (string): The name of the frame that is to be shown.
        """
        frame = self.frames[page_name]
        frame.tkraise()
        self.current_screen = page_name

    def bed_state(self):
        """ Returns the current state of the bedroom. """
        return "50%\n24°C"

    def living_state(self):
        """ Returns the current state of the living room. """
        return "90%"

    def entrance_state(self):
        """ Returns the current state of the entrance. """
        return "80%"

    def hallway_state(self):
        """ Returns the current state of the hallway. """
        return "70%"

    def kitchen_state(self):
        """ Returns the current state of the kitchen. """
        return "60%"

    def on_held_room(self, event):
        """ Defines the actions that occur after a room has been clicked.

        Args:
            event (ButtonPress event): The event that triggers the function.
        """
        # TODO

    def on_click_back(self, event):
        """ Defines the action of going to the previous window i.e. home on click.

        Args:
            event (ButtonPress event): The event that triggers the function.
        """
        # TODO

    def on_light_toggle(self):
        """ Toggles all lights on or off in the house.

        Returns:
            The new state of the lights after having been toggled
        """
        self.lights_master_state = not self.lights_master_state

        return self.lights_master_state

    def on_heating_toggle(self):
        """ Toggles all heating on or off in the house.

        Returns:
            The new state of the heating after having been toggled
        """
        self.heating_master_state = not self.heating_master_state

        return self.heating_master_state

    def set_room_light_state(self, room, state):
        """ Sets the state of the lights in a given room.

        Args:
            room (string): The room whose lights are to be set.
            state (int): A value between 0 and 100 of the new state assigned to the
                         lights in that room.
        """

    def set_room_heating_state(self, room, state):
        """ Sets the state of the lights in a given room.

        Args:
            room (string): The room whose lights are to be set.
            state (int): An arbitrary value between of the target heating value in
                         degrees celcius
        """

class Home(tk.Frame):
    """ Represents the home view screen and extends tk.Frame. """
    def __init__(self, parent, controller):
        # initialize the super
        tk.Frame.__init__(self, parent, bg="#303030")

        # Set the controller
        self.controller = controller

        # Used for timing button presses
        self.button_timer = 0.0

        # Image resources
        room_image = tk.PhotoImage(file="images/rooms.gif")
        self.light_toggle_img = tk.PhotoImage(file="images/light_master.gif")
        self.light_toggle_off_img = tk.PhotoImage(file="images/light_master_off.gif")
        self.heating_toggle_img = tk.PhotoImage(file="images/heating_master.gif")
        self.heating_toggle_off_img = tk.PhotoImage(file=
                                                    "images/heating_master_off.gif")

        # Create room background image
        rooms = tk.Canvas(self,
                          width=316,
                          height=236,
                          highlightthickness=0)
        rooms.place(x=42, y=42)
        rooms.create_image(0, 0, anchor="nw", image=room_image)
        rooms.image = room_image

        # Create master lights toggle switch
        self.light_toggle = tk.Canvas(self,
                             width=80,
                             height=160,
                             highlightthickness=0,
                             bg="#5d5d5d")
        self.light_toggle.place(x=400, y=0)
        self.light_toggle.create_image(0, 0,
                                       anchor="nw",
                                       image=self.light_toggle_img)
        self.light_toggle.image = self.light_toggle_img
        self.light_toggle.bind("<ButtonRelease-1>", self.toggle_lights)

        # Create master heating toggle switch
        self.heating_toggle = tk.Canvas(self,
                                        width=80,
                                        height=160,
                                        highlightthickness=0,
                                        bg="#5d5d5d")
        self.heating_toggle.place(x=400, y=160)
        self.heating_toggle.create_image(0, 0,
                                         anchor="nw",
                                         image=self.heating_toggle_img)
        self.heating_toggle.image = self.heating_toggle_img
        self.heating_toggle.bind("<ButtonRelease-1>", self.toggle_heating)

        # Create info labels
        # TODO: Change all states to stringvar
        bed_label = tk.Label(self,
                             text=self.controller.bed_state(),
                             bg="#292929",
                             fg="white",
                             font="Nova, 20")
        bed_label.place(x=90, y=76)
        bed_label.bind("<ButtonPress-1>", self.on_click_room)
        bed_label.bind("<ButtonRelease-1>", self.on_release_bedroom)

    def on_release_bedroom(self, event):
        self.on_release_room("Bed")

    def on_click_room(self, event):
        """ Defines the behavior of the clicks on a room.

            When a room is simply tapped, the lights in that room are toggled. If
            the room is held for a short period of time, then the app transitions to
            the proper screen. The function is separated between here and in the
            main controller for better sandboxing between networked functions and
            GUI functions. This function simply registers a click.

        Args:
            event (ButtonPress event): The event that triggers the function.
        """
        print(event)
        print(event.x)
        print(event.y)
        self.button_timer = time.time()
        print(self.button_timer)

    def on_release_room(self, room):
        """ Defines the behavior of a mouse release on a room.

            When the mouse or tap is released on a room, the app registers which
            room has been interacted with and does the appropriate action. If
            the room was released before 0.3 seconds, the lights in the room
            are switched off. Otherwise, the controller is told to switch to
            the specific controls of that room.

        Args:
            room (string): The name of the room, which must be the same as the
                           the name used for the frame in the controller class.
        """
        click_duration = time.time() - self.button_timer
        if click_duration < 0.3:
            # Toggle lights in the room
            print("Lights in %s has been toggled." %(room))
        else:
            # Tell controller to go to that room
            print("Telling controller to go to %s." %(room))
            self.controller.show_frame(room)
        
    def toggle_lights(self, event=None):
        """ Defines the behavior of the light toggle switch. 

        Args:
            event (ButtonPress event): The event that triggers the function.
        """
        current_state = self.controller.on_light_toggle()

        if current_state is True:
            self.light_toggle.create_image(0, 0,
                                           anchor="nw",
                                           image=self.light_toggle_img)
            self.light_toggle.image = self.light_toggle_img


        else:
            self.light_toggle.create_image(0, 0,
                                           anchor="nw",
                                           image=self.light_toggle_off_img)
            self.light_toggle.image = self.light_toggle_off_img

    def toggle_heating(self, event=None):
        """ Defines the behavior of the light toggle switch. 

        Args:
            event (ButtonPress event): The event that triggers the function.
        """
        current_state = self.controller.on_heating_toggle()

        if current_state is True:
            self.heating_toggle.create_image(0, 0,
                                             anchor="nw",
                                             image=self.heating_toggle_img)
            self.heating_toggle.image = self.heating_toggle_img


        else:
            self.heating_toggle.create_image(0, 0,
                                             anchor="nw",
                                             image=self.heating_toggle_off_img)
            self.heating_toggle.image = self.heating_toggle_off_img

class Room(tk.Frame):
    """ Represents a super class for the different rooms.

        Behavior is as such:
        - There is a label at the top of the screen that states which room it
          is.
        - There is a light selector, centered if not a heated room or shifted
          to the left if it is
        - The light selector has a plus or minus that changes the lighting level
          when tapped
        - When held down, the plus or minus on the light selector either turns
          the lights on or off
        - The heating label is offset to the right and shows the current temp
          as larger and the desired temperature as smaller text below it.
        - Pressing up or down changes the desired temperature.
        - Tapping the power button turns the heating on or off.
        - When the heating is off, the desired temperature label changes to
          "off"

    Args:
        room_name(string): The name of the room on the label.
        parent(tk widget): The parent widget that the room is a part of.
        controller(class): The controller class that does more complicated
                           behavior for the frame.
    """
    def __init__(self, room_name, parent, controller):
        tk.Frame.__init__(self, parent, bg="#303030")
        self.controller = controller
        self.room_name = room_name

        room_label = tk.Label(self,
                              text=room_name,
                              anchor="nw",
                              bg="#303030",
                              fg="white",
                              font="Nova, 50")
        room_label.place(x=30, y=10)

        heated_rooms = ["Bedroom",
                        "Living Room"]
        self.heated_room = False
        if room_name in heated_rooms:
            self.heated_room = True

        # TODO: Add lighting buttons


class Living(Room):
    """ Represents the living room and extends Room. """
    def __init__(self, parent, controller):
        super().__init__("Living Room", parent, controller)


class Bed(Room):
    """ Represents the bedroom and extends Room. """
    def __init__(self, parent, controller):
        super().__init__("Bedroom", parent, controller)


class Entrance(Room):
    """ Represents the entrance and extends Room. """
    def __init__(self, parent, controller):
        super().__init__("Entrance", parent, controller)


class Hallway(Room):
    """ Represents the hallway and extends Room. """
    def __init__(self, parent, controller):
        super().__init__("Hallway", parent, controller)


class Kitchen(Room):
    """ Represents the kitchen and extends Room. """
    def __init__(self, parent, controller):
        super().__init__("Kitchen", parent, controller)


if __name__ == '__main__':
    print('Starting up')
    h = HACP()
