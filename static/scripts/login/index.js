/**
 * @param {string} username
 * @param {string} password
 * @param {boolean?} save
 * @returns {void}
 */
async function Login(username, password, save) {
	const formdata = new FormData();
	formdata.append("username", username);
	formdata.append("password", password);
	formdata.append("save", save != undefined ? +save : 0);

	document.getElementsByName("submit")[0].disabled = true;
	document.body.style.cursor = "wait";

	const r = await fetch("/api/login", {method: "POST", body: formdata, headers: [["Content-Type", "application/x-www-form-urlencoded"]]});
	switch (r.status) {
		case 200:
			location.reload();
			break;

		case 401:
			const json = await r.json();
			alert(json["detail"]);
			document.getElementById("submit")[0].disabled = false;
			break;

		default:
			break;
	};

	document.body.style.cursor = "default";
	return true;
};

/**
 * @param {string} username
 * @param {string} email
 * @param {string} password
 * @param {string} captcha
 * @returns {void}
 */
async function Register(username, email, password, captcha) {
	const formdata = new FormData();
	formdata.append("username", username);
	formdata.append("email", email);
	formdata.append("password", password);
	formdata.append("captcha", captcha);

	document.getElementsByName("submit")[0].disabled = true;
	document.body.style.cursor = "wait";

	const r = await fetch("/api/register", {method: "POST", body: formdata});
	switch (r.status) {
		case 200:
			location.reload();
			break;

		case 400:
			await RefreshCaptcha();
			const json = await r.json();
			alert(json["detail"]);
			document.getElementById("submit")[0].disabled = false;
			break;

		default:
			break;
	};

	document.body.style.cursor = "default";
	return true;
};

/**
 * @returns {void}
 */
async function RefreshCaptcha() {
	const r = await fetch("/api/refresh_captcha", {method: "POST"});
	if (r.status == 200) {
		document.getElementsByName("captcha-img")[0].src = await r.text();
	};
};