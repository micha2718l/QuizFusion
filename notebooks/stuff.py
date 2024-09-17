from typing import Any
import pint

ureg = pint.UnitRegistry()
pint.set_application_registry(ureg)


class Unit(pint.Unit):
    def __format__(self, format_spec):
        return super().__format__("~L")

    def add_unit(unit):
        ureg.define(unit)


class Value(pint.Quantity):
    def __new__(cls, value=1, unit="", sigfigs=3, pre_zeros=0):
        # Create a new instance of the class using the pint.Quantity factory
        # This is why we need to use super().__new__ instead of super().__init__
        obj = super().__new__(cls, value, unit)
        obj.sigfigs = sigfigs
        obj.pre_zeros = pre_zeros
        return obj

    def __format__(self, format_spec):
        clean = False

        if format_spec:
            if format_spec[0] == "C":
                clean = True
                format_spec = format_spec[1:]
            if len(format_spec) > 1:
                self.sigfigs = int(format_spec)
        unit = self.units
        if isinstance(unit, pint.Unit):
            match self.units:
                case ureg.degree:
                    unit = r"^\circ"
                case _:
                    unit = f"{unit:~L}"
        out = f"{'0'*self.pre_zeros}{self.magnitude:#.{self.sigfigs}g} {unit}"
        return out if clean else f"${out}$"

    def __repr__(self):
        return self.__format__(None)

    def __str__(self):
        return self.__repr__()
