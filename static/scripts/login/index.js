/**
 * @param {string} username
 * @param {string} password
 * @param {boolean?} save
 * @returns {void}
 */
function Login(username, password, save) {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "/api/login", true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.onreadystatechange = (event) => {
		if (xhr.readyState != 4) {
			return;
		};
		switch (xhr.status) {
			case 200:
				location.reload();
				break;

			case 401:
				alert(JSON.parse(xhr.responseText)["detail"]);
				document.getElementsByName("submit")[0].disabled = false;
				break;

			default:
				break;
		};
	};
	xhr.send($.param({
		"username": username,
		"password": password,
		"save": save != undefined ? +save : 0,
	}));
	document.getElementsByName("submit")[0].disabled = true;
	return true;
};

/**
 * @param {string} username
 * @param {string} email
 * @param {string} password
 * @param {string} captcha
 * @returns {void}
 */
function Register(username, email, password, captcha) {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "/api/register", true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = (event) => {
		if (xhr.readyState != 4) {
			return;
		};
		switch (xhr.status) {
			case 200:
				location.reload();
				break;

			case 400:
				RefreshCaptcha();
				alert(JSON.parse(xhr.responseText)["detail"]);
				document.getElementsByName("submit")[0].disabled = false;
				break;

			default:
				break;
		};
	};
	xhr.send(JSON.stringify({
		"username": username,
		"email": email,
		"password": password,
		"captcha": captcha,
	}));
	document.getElementsByName("submit")[0].disabled = true;
	return true;
};

/**
 * @returns {void}
 */
function RefreshCaptcha() {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "/api/refresh_captcha", true);
	xhr.setRequestHeader("Content-Type", "application/text");
	xhr.onreadystatechange = (event) => {
		if (xhr.readyState != 4) {
			return;
		};
		switch (xhr.status) {
			case 200:
				document.getElementsByName("captcha-img")[0].src = xhr.responseText;
				break;

			default:
				break;
		};
	};
	xhr.send(JSON.stringify({}));
};