/**
 * @param {File} file
 * @param {string} language
 * @returns {void}
 */
async function STT(file, language) {
	if (file == undefined) {
		return false;
	};

	const formdata = new FormData();
	formdata.append("file", file);
	formdata.append("language", language);

	document.getElementsByName("submit")[0].disabled = true;
	document.body.style.cursor = "wait";
	document.getElementById("Result").classList.add("Loading");

	const r = await fetch("/api/tools/stt/stt", {method: "POST", body: formdata});

	document.getElementsByName("submit")[0].disabled = false;
	document.body.style.cursor = "default";
	document.getElementById("Result").classList.remove("Loading");

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
		const result = await r2.text();
		document.getElementById("Result").text = result;
		document.getElementById("Result").classList.add("HasResult");
	};
};