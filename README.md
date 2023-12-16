`pip install uwsgi`

Manually run with UWSGI for testing:
`/home/pi/.local./bin/uwsgi --ini plantwatering.ini`

Use cloudflared to make the website publicly accessible: https://pimylifeup.com/raspberry-pi-cloudflare-tunnel/
(Make sure to also follow the steps to start it on boot)

To start uwsgi on boot:

`sudo nano /etc/systemd/system/plantwatering.service`
with content:

    [Unit]
    Description=uWSGI instance to serve the plantwatering project
    After=network.target
    
    [Service]
    User=pi
    Group=pi
    WorkingDirectory=/home/pi/Desktop/plantwatering-flask
    ExecStart=/home/pi/.local/bin/uwsgi --ini plantwatering.ini
    # default is 90. For some reason sometimes stopping the service doesn't work until that timeout triggers a kill
    TimeoutStopSec=15
    
    [Install]
    WantedBy=multi-user.target


`sudo systemctl enable plantwatering`

`sudo systemctl start plantwatering`
