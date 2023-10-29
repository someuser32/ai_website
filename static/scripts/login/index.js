/**
 * @param {string} username
 * @param {string} password
 * @param {boolean?} save
 * @returns {void}
 */
function Login(username, password, save) {
	if (username == "" || password == "") {
		return;
	};
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "/api/login", true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = (event) => {
		if (xhr.readyState != 4) {
			return;
		};
		switch (xhr.status) {
			case 200:
				location.reload();
				break;

			case 403:
				alert(xhr.responseText["detail"]);
				break;

			default:
				break;
		};
	};
	xhr.send(JSON.stringify({
		"username": username,
		"password": password,
		"save": save != undefined ? +save : 0,
	}));
};

/**
 * @param {string} username
 * @param {string} email
 * @param {string} password
 * @param {string} captcha
 * @returns {void}
 */
function Register(username, email, password, captcha) {
	if (username == "" || email == "" || password == "" || captcha == "") {
		alert("You are missed required fields!");
		return;
	};
	if (!IsEmailValid(email)) {
		alert("Invalid email!");
		return;
	};
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
				alert(JSON.parse(xhr.responseText)["detail"]);
				RefreshCaptcha();
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