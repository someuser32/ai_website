/**
 * @param {string} username
 * @param {string} password
 * @returns {void}
 */
function Login(username, password) {
	if (username == "" || password == "") {
		return;
	};
	$.post("/api/login", {
		"username": username,
		"password": password,
	}, function (data, textStatus, jqXHR) {
		if (data["message"] != undefined) {
			alert(data["message"]);
		};
	}, "json").fail(() => {
		console.log("fail");
	});
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
		return;
	};
	$.post("/api/login", {
		"username": username,
		"email": email,
		"password": password,
		"captcha": captcha,
		"is_registration": 1,
	}, function (data, textStatus, jqXHR) {
		if (data["message"] != undefined) {
			alert(data["message"]);
		};
	}, "json");
};