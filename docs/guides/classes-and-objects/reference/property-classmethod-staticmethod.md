---
title: property, classmethod, staticmethod syntax
---

# `property`, `classmethod`, `staticmethod` syntax

Syntax reference for the three decorators that change how a method is called and what its first argument is.

## `@property`

Turns a method into an attribute-style access.

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        raise AttributeError("can't delete the temperature")
```

Usage:

```python
t = Temperature(22)
t.celsius          # calls the getter
t.celsius = 25     # calls the setter
del t.celsius      # calls the deleter
```

| Decorator | Role |
| --- | --- |
| `@property` | The getter. Required. |
| `@<name>.setter` | The setter. Optional — leave off for a read-only property. |
| `@<name>.deleter` | The deleter. Optional; rarely useful. |

All three decorated methods must share the *same name*. The underscored attribute (`_celsius` above) is where the real storage lives, by convention.

Read-only form:

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def diameter(self):           # no setter — read-only
        return self.radius * 2
```

## `@classmethod`

First argument is `cls`, the class itself. The most common use is an alternative constructor.

```python
class Date:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_iso(cls, s):
        year, month, day = s.split("-")
        return cls(int(year), int(month), int(day))

    @classmethod
    def today(cls):
        import datetime
        t = datetime.date.today()
        return cls(t.year, t.month, t.day)
```

Call via the class or an instance:

```python
Date.from_iso("2026-04-21")
Date.today()
```

Use `cls(...)` rather than hard-coding the class name — this way, subclasses inherit the factory correctly (`BusinessDate.from_iso(...)` returns a `BusinessDate`).

## `@staticmethod`

Takes neither `self` nor `cls` — a plain function that happens to be namespaced under the class.

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @staticmethod
    def celsius_to_fahrenheit(c):
        return c * 9 / 5 + 32

    @staticmethod
    def fahrenheit_to_celsius(f):
        return (f - 32) * 5 / 9
```

Call via the class or an instance:

```python
Temperature.celsius_to_fahrenheit(100)
```

Staticmethods have no access to `self` or `cls`. If you find yourself wanting either, use `@classmethod` or a plain method instead. If you want neither *and* the function isn't conceptually tied to the class, put it at module level — classes aren't just namespaces.

## Comparison at a glance

| Decorator | First arg | Can access instance state? | Can access class? | Typical use |
| --- | --- | --- | --- | --- |
| plain method | `self` | Yes | Via `type(self)` | Everything that needs the instance. |
| `@classmethod` | `cls` | No | Yes | Alternative constructors, operations on the class itself. |
| `@staticmethod` | (none) | No | No | Logically related utility functions. |
| `@property` | `self` | Yes | — | Computed attributes, validated attributes. |
