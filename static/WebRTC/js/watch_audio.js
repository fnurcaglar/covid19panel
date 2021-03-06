/*global socket, video, config*/
let peerConnection;

socket.on('offer', function(id, description) {
	peerConnection = new RTCPeerConnection(config);
	peerConnection.setRemoteDescription(description)
	.then(() => peerConnection.createAnswer())
	.then(sdp => peerConnection.setLocalDescription(sdp))
	.then(function () {
		socket.emit('answer', id, peerConnection.localDescription);
	});
	peerConnection.ontrack = function(event) {
		audio.srcObject = event.streams[0];
	};
	peerConnection.onicecandidate = function(event) {
		if (event.candidate) {
			socket.emit('candidate', id, event.candidate);
		}
	};
});

socket.on('candidate', function(id, candidate) {
  peerConnection.addIceCandidate(new RTCIceCandidate(candidate))
  .catch(e => console.error(e));
  console.log('Candidate Gönderildi: ' + id);
});

socket.on('connect', function() {
	socket.emit('watcher');
});

socket.on('broadcaster', function() {
  socket.emit('watcher');
  console.log('Gelen : Broadcaster , Giden : Watcher');
});

socket.on('bye', function() {
	peerConnection.close();
});
