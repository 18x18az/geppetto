cp .xinitrc ~/.xinitrc
sudo cp ./control.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable --now control
