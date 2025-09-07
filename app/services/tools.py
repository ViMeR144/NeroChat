import math
import re
from typing import List, Dict, Optional

SAFE_MATH_PATTERN = re.compile(r"^[0-9\s\+\-\*\/\(\)\.,^%]+$")


def maybe_solve_math(messages: List[Dict[str, str]]) -> Optional[str]:
	text = messages[-1]["content"] if messages else ""
	if not text:
		return None
	if not SAFE_MATH_PATTERN.match(text):
		return None
	try:
		# Replace commas with dots for decimal compatibility
		expr = text.replace(",", ".")
		# Disallow dangerous names by limiting globals
		allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
		allowed_names.update({"__builtins__": {}})
		result = eval(expr, allowed_names, {})
		return f"[math] {text} = {result}"
	except Exception:
		return None

