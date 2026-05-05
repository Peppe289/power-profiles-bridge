# Power Profiles Bridge

A lightweight, Python-based power profile manager for Arch Linux. This project serves as a custom drop-in replacement for `power-profiles-daemon`, specifically engineered to interface with Noctalia, Niri, and other environments utilizing Hadess and UPower D-Bus specifications.

# Backend Integration: Tuned

Unlike the standard daemon, this bridge uses Tuned (Adaptive System Tuning Daemon) to apply deep system optimizations.

# D-Bus Security Policies

This package installs a security policy in `/usr/share/dbus-1/system.d/`. This configuration is critical as it authorizes the script to claim the `net.hadess.PowerProfiles` and `org.freedesktop.UPower.PowerProfiles` names on the System Bus, which is otherwise restricted to root-owned processes.

# Install on Arch

```sh
git clone https://github.com/Peppe289/power-profiles-bridge.git
cd power-profiles-bridge
makepkg -si
```
