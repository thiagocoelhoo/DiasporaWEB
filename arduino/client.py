"""
Script responsável por se connectar ao arduino por meio
de comunicação serial e, também, responsável por se
connectar ao servidor por meio de websockets.
"""

import asyncio
import json

import websockets
import aioserial


async def main():
	uri = 'ws://127.0.0.1:8000/consumers/arduino'
	serial = aioserial.AioSerial('/dev/ttyACM0')
	headers = {}
	async with websockets.connect(uri, extra_headers=headers) as websocket:
		while True:
			raw_data = await serial.readline_async()
			try:
				data = json.loads(raw_data.decode(errors='ignore'))
				print(raw_data)
				await websocket.send(json.dumps(data))
				await asyncio.sleep(0.1)
			except:
				pass


asyncio.run(main())

