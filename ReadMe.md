# Requirement lib:
    python==3.9.7
	opencv-python==4.5.4.60
	PyAutoGUI==0.9.53
	pywin32==302
    pyinstaller==4.7.0

# Build app to file .exe for windows:
pyinstaller main.py --noconsole --noconfirm --icon="data/nth_auto_game.ico" --name=AutoPikachu
