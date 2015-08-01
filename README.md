# Find My Raspberry

## Server

	pip install flask
	PORT=8858 python server.py

Your can use `hostname -i` to find your server IP in most times.

## Client(Run on your own raspberry)

	SERVER=http://<your-server-ip>:8858/api/findme python findme.py

## LICENSE
[MIT](LICENSE)
