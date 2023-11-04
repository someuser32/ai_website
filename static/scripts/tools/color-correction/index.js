/**
 * @param {File} file
 * @param {Array<number>} args
 * @returns {void}
 */
async function Correct(file, ...args) {
	if (file == undefined) {
		return false;
	};

	const formdata = new FormData();
	formdata.append("file", file);
	const form_keys = ["temperature", "hue", "brightness", "contrast", "saturation", "gamma", "exposure_offset", "vignette", "noise", "sharpness", "hdr"];
	for (let i=0; i<form_keys.length; i++) {
		formdata.append(form_keys[i], args[i]);
	};

	document.getElementsByName("submit")[0].disabled = true;
	document.body.style.cursor = "wait";
	document.getElementById("ResultImage").classList.add("Loading");

	const r = await fetch("/api/tools/color-correction/correct", {method: "POST", body: formdata});

	document.getElementsByName("submit")[0].disabled = false;
	document.body.style.cursor = "default";
	document.getElementById("ResultImage").classList.remove("Loading");

	if (r.status != 200) {
		alert(r.statusText);
		return false;
	};

	const r2 = r.clone();
	try {
		const json = await r.json();
		if (json["status"] != "success") {
			if (json["reason"] != undefined) {
				alert(json["reason"]);
			};
		};
	} catch (e) {
		const blob = await r2.blob();
		const reader = new FileReader();
		reader.addEventListener("load", () => {
			document.getElementsByName("result-image")[0].src = reader.result;
			document.getElementById("ResultImage").classList.add("HasImage");
		});
		reader.readAsDataURL(new File([blob], "color_corrected.png", {type: blob.type, lastModified: blob.lastModified}));
	};
};