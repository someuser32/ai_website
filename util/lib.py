import re
from typing import Any, Hashable, Iterable


def is_number(i: str, /) -> bool:
	try:
		float(i)
	except (ValueError, TypeError):
		return False
	return True

def is_bool(i: str, /) -> bool:
	return i.lower() in {"true", "false"}

def parse_bool(i: str, /) -> bool | None:
	return i.lower() == "true" if is_bool(i) else None

def parse_deepdiff_keys(diff: str, /) -> list[Hashable]:
	keys : list[str] = [key[0] or key[1] for key in re.findall(r"(?<=\[)('([^'\\]*(?:\\.[^'\\]*)*)'|[\w\d]+)(?=\])", diff)]
	keys_formatted = []
	for key in keys:
		if key.startswith("'") and key.endswith("'"):
			keys_formatted.append(key[1:-1])
		elif key.isdigit():
			keys_formatted.append(int(key))
		elif is_number(key):
			keys_formatted.append(float(key))
		elif is_bool(key):
			keys_formatted.append(parse_bool(key))
		else:
			keys_formatted.append(key)
	return keys_formatted

def recursively_setvalue_from(obj: dict, obj2: dict, keys: Iterable[Hashable], /):
	obj_key = obj
	for key in keys[:-2]:
		obj_key = obj_key[key]
	obj2_key = obj2
	for key in keys:
		obj2_key = obj2_key[key]
	obj_key[keys[-1]] = obj2_key

def recursively_removekey(obj: dict, keys: Iterable[Hashable], /):
	obj_key = obj
	for key in keys[:-1]:
		obj_key = obj_key[key]
	del obj_key[keys[-1]]

def recursively_setvalue(obj: dict, value: Any, keys: Iterable[Hashable], /):
	obj_key = obj
	for key in keys[:-1]:
		obj_key = obj_key[key]
	obj_key[keys[-1]] = value

def recursively_getvalue(obj: dict, keys: Iterable[Hashable], /) -> Any:
	obj_key = obj
	for key in keys:
		obj_key = obj_key[key]
	return obj_key

def safe_typecast(old: Any, new: Any, /) -> Any:
	if isinstance(old, str) and isinstance(new, int):
		return int(old)
	elif isinstance(old, str) and isinstance(new, float):
		return float(old)
	elif isinstance(old, (int, float)) and isinstance(new, str):
		return str(old)
	elif isinstance(old, bool) and isinstance(new, int):
		return int(old)
	elif isinstance(old, int) and isinstance(new, bool):
		return bool(old)
	return new
