from dataclasses import dataclass, field
from decimal import Decimal


@dataclass()
class arg_range:
	start : int | float
	stop : int | float
	step : int | float = 1
	default : int | float | None = None
	name : str = ""
	range : tuple[int | float] = field(init=False)

	def __post_init__(self):
		if self.start > self.stop and self.step > 0:
			raise ValueError
		elif self.start < self.stop and self.step < 0:
			raise ValueError
		elif self.start != self.stop and self.step == 0:
			raise ValueError
		if self.default is None:
			self.default = self.start
		range, stop, step = set(), Decimal(str(self.stop)), Decimal(str(self.step))
		i = Decimal(str(self.start))
		while i <= stop:
			range.add(float(i))
			i += step
		self.range = tuple(range)

	def __contains__(self, __key: object) -> bool:
		if not isinstance(__key, (int, float)):
			return False
		return self.start <= __key <= self.stop
