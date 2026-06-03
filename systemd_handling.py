from pathlib import Path
import subprocess

service_file = "/etc/systemd/system/rgb_controller.service"

if Path(service_file).is_file():
    with open(service_file, "r") as f:
        file_content = f.read()
else:
    file_content = '''[Unit]
Description=keyboard rgb controller service

[Service]
Type=simple
ExecStart=
Restart=on-failure

[Install]
WantedBy=multi-user.target'''

def update_system() -> None:
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "rgb_controller.service"])
    subprocess.run(["systemctl", "restart", "rgb_controller.service"])

def update_service(command:str) -> None:
    global file_content
    file_content = file_content.split("\n")
    for i,line in enumerate(file_content):
        if line.startswith("ExecStart"):
            file_content[i] = line[:line.index('=') + 1] + command
            break

    with open(service_file, "w") as f:
        f.write('\n'.join(file_content))

    update_system()