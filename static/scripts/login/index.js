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
	$.post("/api/login", {
		"username": username,
		"password": password,
		"save": save != undefined ? +save : 0,
	}, function (data, textStatus, jqXHR) {
		location.reload();
	}).fail(() => {
		alert("Username or password is incorrect!")
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
	$.post("/api/register", {
		"username": username,
		"email": email,
		"password": password,
		"captcha": captcha,
	}, function (data, textStatus, jqXHR) {
		if (data["message"] != undefined) {
			alert(data["message"]);
		};
	});
};