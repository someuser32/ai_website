/**
 * @param {string} text
 * @param {string} model
 * @returns {void}
 */
async function GPT(text, model) {
	const formdata = new FormData();
	formdata.append("text", text);
	formdata.append("model", model);

	document.getElementsByName("submit")[0].disabled = true;
	document.body.style.cursor = "wait";
	document.getElementById("Result").classList.add("Loading");

	const r = await fetch("/api/tools/gpt/gpt", {method: "POST", body: formdata});

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
		document.getElementById("Result").innerHTML = marked.parse(result);
		document.getElementById("Result").classList.add("HasResult");
	};
};