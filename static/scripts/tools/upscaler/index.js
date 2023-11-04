/**
 * @param {File} file
 * @param {number} scale
 * @param {string} model
 * @returns {void}
 */
function Upscale(file, scale, model) {
	if (file == undefined) {
		return false;
	};
	const socket = new WebSocket(`ws://${location.host}/websocket/tools/upscaler/upscale`);
	let send_json = false;
	socket.addEventListener("open", (event) => {
		socket.send(file);
	});
	socket.addEventListener("message", (event) => {
		if (!send_json) {
			const msg = JSON.parse(event.data);
			if (msg["status"] == "success") {
				send_json = true;
				socket.send(JSON.stringify({
					"scale": scale,
					"model": model,
				}));
			} else if (msg["status"] == "error") {
				if (msg["reason"] != undefined) {
					alert(msg["reason"]);
				};
				document.getElementsByName("submit")[0].disabled = false;
				document.body.style.cursor = "default";
				document.getElementById("ResultImage").classList.remove("Loading");
			};
		} else {
			if (event.data instanceof Blob) {
				const reader = new FileReader();
				reader.addEventListener("load", () => {
					document.getElementsByName("result-image")[0].src = reader.result;
					document.getElementById("ResultImage").classList.add("HasImage");
				});
				reader.readAsDataURL(new File([event.data], "upscaled.png", {type: "image/png", lastModified: event.data.lastModified}));
			} else {
				const msg = JSON.parse(event.data);
				if (msg["status"].toLowerCase() == "error") {
					if (msg["reason"] != undefined) {
						alert(msg["reason"]);
					};
				};
			};
			document.getElementsByName("submit")[0].disabled = false;
			document.body.style.cursor = "default";
			document.getElementById("ResultImage").classList.remove("Loading");
		};
	});
	document.getElementsByName("submit")[0].disabled = true;
	document.body.style.cursor = "wait";
	document.getElementById("ResultImage").classList.add("Loading");
};