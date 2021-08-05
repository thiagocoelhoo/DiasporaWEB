import asyncio
import json
import datetime

import websockets
from websockets.client import WebSocketClientProtocol
from aiortc import (
    RTCPeerConnection,
    RTCConfiguration,
    RTCIceServer,
    RTCSessionDescription,
    RTCIceCandidate
)
from aiortc.contrib.media import MediaPlayer, MediaRelay

relay = None
webcam = None


async def create_peer_connection():
    """Create and config rtcpeerconnection"""
    
    ice_server = RTCIceServer(urls='stun:stun.l.google.com:19302')
    config = RTCConfiguration(iceServers=[ice_server])
    pc = RTCPeerConnection(config)

    @pc.on('track')
    async def on_track(event):
        print(event)
    
    # Add tracks to peer connection
    # print(create_local_tracks())
    pc.addTrack(create_local_tracks())
    # pc.addTransceiver('video', direction='sendonly')

    @pc.on('datachannel')
    async def on_datachannel(event):
        print('ondatachannel ->', event)
    
    return pc


def create_local_tracks():
    global relay, webcam

    options = {'framerate': '30', 'video_size': '640x480'}
    webcam = MediaPlayer('/dev/video0', format='v4l2', options=options)
    relay = MediaRelay()

    return relay.subscribe(webcam.video)


async def on_message(message: str, pc: RTCPeerConnection, ws: WebSocketClientProtocol):
    data = json.loads(message)

    if data['action'] == 'offer':
        # Set remote description

        offer_json = data['message']
        offer = RTCSessionDescription(
            sdp=offer_json['sdp'],
            type=offer_json['type']
        )

        await pc.setRemoteDescription(offer)
            
        # Create answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        
        response = json.dumps({
            'action': 'answer',
            'message': {
                'sdp': answer.sdp,
                'type': answer.type
            }
        })

        # Send answer

        await ws.send(response)
    elif data['action'] == 'candidate':
        # candidate_json = data['candidate']
        # pc.addIceCandidate(candidate)
        pass


async def main():
    uri = 'ws://127.0.0.1:8000/consumers/videostream'

    async with websockets.connect(uri) as ws:
        pc = await create_peer_connection()
        async for message in ws:
            print('new message -', datetime.datetime.now())
            await on_message(message, pc, ws)


asyncio.run(main())
