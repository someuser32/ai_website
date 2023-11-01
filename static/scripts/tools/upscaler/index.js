/**
 * @param {File} file
 * @param {number} scale
 * @param {string} model
 * @returns {void}
 */
function Upscale(file, scale, model) {
	const socket = new WebSocket(`ws://${location.host}/websocket/tools/upscaler/upscale`);
	let send_json = false;
	socket.addEventListener("open", (event) => {
		socket.send(file);
	});
	socket.addEventListener("message", (event) => {
		if (!send_json) {
			send_json = true;
			socket.send(JSON.stringify({
				"scale": scale,
				"model": model,
			}));
		} else {
			if (event.data instanceof Blob) {
				const blob = new Blob([event.data]);
				const url = URL.createObjectURL(blob);
				console.log(url)
				document.getElementsByName("upscaled-image")[0].src = url;
			} else {
				const msg = JSON.parse(event.data);
				if (msg["status"].toLowerCase() == "error") {
					if (msg["reason"] != undefined) {
						alert(msg["reason"]);
					};
				};
			};
			document.getElementsByName("submit")[0].disabled = false;
		};
	});
	document.getElementsByName("submit")[0].disabled = true;
};