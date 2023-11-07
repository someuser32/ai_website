let model_speakers = {};

/**
 * @param {string} model_name
 * @param {Array<string>} speakers
 * @returns {void}
 */
function LoadModelSpeakers(model_name, speakers) {
	model_speakers[model_name] = speakers;
};

/**
 * @param {string} model_name
 * @returns {void}
 */
function OnModelChanged(model_name) {
	const speakers_dropdown = document.getElementsByName("speaker")[0];
	if (speakers_dropdown.model_name == model_name) {
		return;
	};
	speakers_dropdown.model_name = model_name;
	console.log(model_speakers[model_name])
	$('select[name="speaker"]').empty();
	for (let i=0; i<model_speakers[model_name].length; i++) {
		$('select[name="speaker"]').append($("<option></option>").attr("value", model_speakers[model_name][i]).text(model_speakers[model_name][i]));
	};
};

/**
 * @param {string} text
 * @param {string} model
 * @param {string} speaker
 * @param {number} pitch
 * @returns {void}
 */
async function TTS(text, model, speaker, pitch) {
	const formdata = new FormData();
	formdata.append("text", text);
	formdata.append("model", model);
	formdata.append("speaker", speaker);
	formdata.append("pitch", pitch);

	document.getElementsByName("submit")[0].disabled = true;
	document.body.style.cursor = "wait";
	document.getElementById("ResultAudio").classList.add("Loading");

	const r = await fetch("/api/tools/tts/tts", {method: "POST", body: formdata});

	document.getElementsByName("submit")[0].disabled = false;
	document.body.style.cursor = "default";
	document.getElementById("ResultAudio").classList.remove("Loading");

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
			document.getElementById("ResultAudio").src = reader.result;
			document.getElementById("ResultAudio").classList.add("HasAudio");
		});
		reader.readAsDataURL(new File([blob], "audio.wav", {type: blob.type, lastModified: blob.lastModified}));
	};
};