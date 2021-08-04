var pc;
var dc;
var videoStreamSocket;
var config = {iceServers: [{urls: 'stun:stun.l.google.com:19302'}]};
var videoElement = document.getElementById('video');

function start() {
  videoStreamSocket = new WebSocket('ws://127.0.0.1:8000/consumers/videostream');
  pc = new RTCPeerConnection(config);
  
  pc.ontrack = function (event) {
    console.log('Track:', event);
    videoElement.srcObject = event.streams[0];
  };

  pc.onicecandidate = function (event) {
    let data = {
      action: 'candidate',
      candidate: event.candidate
    };
    // console.log(event.candidate);
    videoStreamSocket.send(JSON.stringify(data));
  };

  videoStreamSocket.onopen = send_offer;
  videoStreamSocket.onmessage = onMessageHandler;
}

async function send_offer() {
  // Add tranceivers / create data channel
  
  // dc = pc.createDataChannel('chat');
  pc.addTransceiver('video', {direction:'recvonly'});

  // Create offer and set local description
  let offer = await pc.createOffer();
  await pc.setLocalDescription(offer);

  // Send offer
  let data = {
    action: 'offer',
    message: pc.localDescription
  }

  videoStreamSocket.send(JSON.stringify(data));
}

function onMessageHandler(event) {
  data = JSON.parse(event.data);
  console.log(data);
  if (data.action === 'answer') {
    pc.setRemoteDescription(data.message);
  }
}
