/*global socket, video, config*/
const peerConnections = {};

/** @type {MediaStreamConstraints} */
const constraints = {
	audio: true,
	video: false
};


navigator.mediaDevices.getUserMedia(constraints)
.then(function(stream) {
	audio.srcObject = stream;
	socket.emit('broadcaster');
}).catch(error => console.error(error));


socket.on('answer', function(id, description) {
	peerConnections[id].setRemoteDescription(description);
	console.log("Remote Description Ayarlandı")
});

socket.on('watcher', function(id) {
	console.log('Watcher ID : ' + id);
	const peerConnection = new RTCPeerConnection(config);
	peerConnections[id] = peerConnection;
	let stream = audio.srcObject;
        stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));
	peerConnection.createOffer()
	.then(sdp => peerConnection.setLocalDescription(sdp))
	.then(function () {
		socket.emit('offer', id, peerConnection.localDescription);
		console.log('Broadcaster Local Desc Gönderildi : ' + id);
	});
	peerConnection.onicecandidate = function(event) {
		if (event.candidate) {
			socket.emit('candidate', id, event.candidate);
			console.log('Candidate Gönderildi: ' + id);
		}
	};
});

socket.on('candidate', function(id, candidate) {
	peerConnections[id].addIceCandidate(new RTCIceCandidate(candidate));
});

socket.on('bye', function(id) {
	peerConnections[id] && peerConnections[id].close();
	delete peerConnections[id];
});
