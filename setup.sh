cp .xinitrc ~/.xinitrc
cp .bash_profile ~/.bash_profile
sudo apt update -qq
sudo apt install --no-install-recommends -y xserver-xorg-video-all xserver-xorg-input-all xserver-xorg-core xinit x11-xserver-utils cockpit python3 python3-pip python3-dev chromium-browser unclutter
sudo cp ./control.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable --now control
sudo systemctl enable --now cockpit.socket
sudo pip3 install "gql[all]"
sudo pip3 install pyusb
sudo cp ./1-field.rules /etc/udev/rules.d
sudo groupadd dialout
sudo usermod -aG dialout admin
sudo reboot