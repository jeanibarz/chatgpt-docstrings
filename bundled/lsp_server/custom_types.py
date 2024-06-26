import enum

import attrs


@enum.unique
class TelemetryTypes(str, enum.Enum):
    Info = "info"
    Error = "error"


@attrs.define
class TelemetryParams:
    type: TelemetryTypes = attrs.field(  # noqa
        validator=attrs.validators.instance_of(TelemetryTypes)
    )
    name: str = attrs.field(validator=attrs.validators.instance_of(str))
    data: dict = attrs.field(validator=attrs.validators.instance_of(dict))
