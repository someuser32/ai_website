// /**
//  * @param {string} email
//  * @returns {boolean}
//  */
// function IsEmailValid(email) {
// 	const regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
// 	return !!email.match(regex);
// };

/**
 * @param {Element} element
 * @param {string|Array<string>} extensions
 * @param {DragEvent} event
 * @param {Function} callback
 * @returns {boolean}
 */
function FileDrop(element, extensions, event, callback) {
	const files = (event.dataTransfer.items ? [...event.dataTransfer.items].filter((item, i, a) => (item.kind == "file")).map((item, i, a) => (item.getAsFile())) : [...event.dataTransfer.files]).filter((file, i, a) => (extensions == "*" || extensions == undefined || extensions == null || extensions.some((ext) => (file.name.endsWith(ext)))));
	if (files.length == 0) {
		return false;
	};
	if (!callback(element, files)) {
		return false;
	};
	event.preventDefault();
	return true;
};

/**
 * @param {Element} element
 * @param {string|Array<string>} extensions
 * @param {Function} callback
 * @returns {void}
 */
function FileClick(element, extensions, callback) {
	const input = document.createElement("input");
	input.style.display = "none";
	input.setAttribute("type", "file");
	input.setAttribute("accept", extensions.join(","));
	input.addEventListener("change", () => {
		if (input.files.length > 0) {
			callback(element, input.files);
		};
	});
	input.click();
	input.remove();
};

/**
 * @param {Element} element
 * @param {Array<File>} files
 * @returns {boolean}
 */
function ImageFiles(element, files) {
	const img = [...element.children].find((child) => (child.tagName.toLowerCase() == "img"));
	const reader = new FileReader();
	reader.addEventListener("load", () => {
		img.src = reader.result;
		element.classList.add("HasImage");
	});
	reader.readAsDataURL(new File([files[0]], files[0].name, {type: files[0].type, lastModified: files[0].lastModified}));
	element.uploaded_files = files;
	return true;
};