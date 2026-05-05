#!/usr/bin/env python3
from pydbus import SystemBus
from pydbus.generic import signal
from gi.repository import GLib, Gio
import os
import psutil

XML = """
<node>
    <interface name='org.freedesktop.UPower.PowerProfiles'>
        <property name='ActiveProfile' type='s' access='readwrite'/>
        <property name='Profiles' type='aa{sv}' access='read'/>
        <signal name='PropertiesChanged'>
            <arg type='s' name='interface_name'/>
            <arg type='a{sv}' name='changed_properties'/>
            <arg type='as' name='invalidated_properties'/>
        </signal>
    </interface>
    <interface name='net.hadess.PowerProfiles'>
        <property name='ActiveProfile' type='s' access='readwrite'/>
        <property name='Profiles' type='aa{sv}' access='read'/>
    </interface>
</node>
"""

class PowerManager:
    dbus = XML
    PropertiesChanged = signal()

    def __init__(self, bus_connection):
        self._active = "balanced"
        self.con = bus_connection
        self._profiles = [
            {'Profile': GLib.Variant('s', 'performance'), 'Driver': GLib.Variant('s', 'custom')},
            {'Profile': GLib.Variant('s', 'balanced'), 'Driver': GLib.Variant('s', 'custom')},
            {'Profile': GLib.Variant('s', 'power-saver'), 'Driver': GLib.Variant('s', 'custom')}
        ]

    @property
    def ActiveProfile(self):
        return self._active

    @ActiveProfile.setter
    def ActiveProfile(self, value):
        if value != self._active:
            self.update_system(value)
            
    def emit_signal(self, value):
        # Segnal args
        interface_name = GLib.Variant('s', "org.freedesktop.UPower.PowerProfiles")
        changed_props = GLib.Variant('a{sv}', {
            "ActiveProfile": GLib.Variant('s', value)
        })
        invalidated_props = GLib.Variant('as', [])
        
        signal_params = GLib.Variant('(sa{sv}as)', (
            "org.freedesktop.UPower.PowerProfiles", 
            {"ActiveProfile": GLib.Variant('s', value)}, 
            []
        ))

        # Send on system dbus
        try:
            self.con.emit_signal(
                None, # Broadcast
                "/org/freedesktop/UPower/PowerProfiles", # path from logs
                "org.freedesktop.DBus.Properties", # signal interface
                "PropertiesChanged", # signal name
                signal_params
            )
            print("Notify sendend using GIO")
        except Exception as e:
            print(f"Errore Gio: {e}")


    def update_system(self, value):
        self._active = value
        print(f"Applicazione profilo: {value}")

        match value:
            case 'balanced':
                os.system("tuned-adm profile balanced")
            case "performance":
                os.system("tuned-adm profile hpc-compute")
            case "power-saver":
                os.system("tuned-adm profile laptop-battery-powersave")
        
        self.emit_signal(value)

    @property
    def Profiles(self):
        return self._profiles

if __name__ == "__main__":
    bus_con = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
    
    bus = SystemBus()
    manager = PowerManager(bus_con)
    
    # Publish to path
    bus.publish("org.freedesktop.UPower.PowerProfiles", manager)
    bus.publish("net.hadess.PowerProfiles", manager)

    #manager.update_system("balanced")

    loop = GLib.MainLoop()

    def check_battery_status():
        is_plugged = psutil.sensors_battery().power_plugged
        target_profile = "performance" if is_plugged else "power-saver"

        if manager.ActiveProfile != target_profile:
            manager.update_system(target_profile)
        
        return True

    check_battery_status()
    GLib.timeout_add(2000, check_battery_status)
    loop.run()