pip install uwsgi

/home/pi/.local./bin/uwsgi --ini plantwatering.ini

Use cloudflared to make the website publicly accessible: https://pimylifeup.com/raspberry-pi-cloudflare-tunnel/

cloudflared tunnel run --url 127.0.0.1:80 plantwatering