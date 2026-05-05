# Maintainer: Peppe289 <gsperanza204@gmail.com>
pkgname=custom-power-manager-git
pkgver=1.0
pkgrel=1
pkgdesc="Custom Power Profiles Manager for Noctalia/Niri with auto battery switch"
arch=('any')
url="https://github.com/Peppe289/power-profiles-bridge"
license=('MIT')
depends=('python' 'python-psutil' 'python-gobject' 'python-pydbus' 'tuned')
source=("git+${url}.git"
        "custom-profile.service"
        "net.hadess.PowerProfiles.conf")
sha256sums=('SKIP' 'SKIP' 'SKIP')

provides=('power-profiles-daemon')
conflicts=('power-profiles-daemon')

package() {
  install -Dm755 "${srcdir}/power-profiles-bridge/main.py" "${pkgdir}/usr/bin/custom-power-manager"

  install -Dm644 "${srcdir}/net.hadess.PowerProfiles.conf" \
    "${pkgdir}/usr/share/dbus-1/system.d/net.hadess.PowerProfiles.conf"

  install -Dm644 "${srcdir}/custom-profile.service" \
    "${pkgdir}/usr/lib/systemd/system/custom-power-manager.service"

  echo "[D-BUS Service]
Name=net.hadess.PowerProfiles
Exec=/usr/bin/custom-power-manager
User=root" > net.hadess.PowerProfiles.service

  install -Dm644 net.hadess.PowerProfiles.service \
    "${pkgdir}/usr/share/dbus-1/system-services/net.hadess.PowerProfiles.service"
}