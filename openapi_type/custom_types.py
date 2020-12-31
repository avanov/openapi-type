from enum import Enum
from typing import NewType, NamedTuple, Optional

import typeit
from inflection import camelize
from typeit.schema import Invalid


class MediaTypeFormat(Enum):
    JSON = 'application/json'
    XML = 'application/xml'
    TEXT = 'text/plain'
    FORM_URLENCODED = 'application/x-www-form-urlencoded'
    BINARY_STREAM = 'application/octet-stream'


MediaTypeCharset = NewType('MediaTypeCharset', str)


class MediaTypeTag(NamedTuple):
    format: MediaTypeFormat
    charset: Optional[MediaTypeCharset]


class MediaTypeTagSchema(typeit.schema.primitives.Str):
    def deserialize(self, node, cstruct: str) -> MediaTypeTag:
        """ Converts input string value ``cstruct`` to ``MediaTypeTag``
        """
        try:
            tag_str = super().deserialize(node, cstruct)
        except Invalid as e:
            error = Invalid(node, "Media Type should be a string", cstruct)
            error.add(e)
            raise error

        media_format, *param = tag_str.split(';')
        try:
            typed_format = MediaTypeFormat(media_format)
        except ValueError:
            raise Invalid(node, f"Unsupported Media Type format: {media_format}", media_format)

        if param:
            param = [x for x in param[0].split('charset=') if x.strip()]
            if param:
                charset = param[0]
            else:
                charset = None
        else:
            charset = None
        return MediaTypeTag(
            format=typed_format,
            charset=charset
        )

    def serialize(self, node, appstruct: MediaTypeTag) -> str:
        """ Converts ``MediaTypeTag`` back to string value suitable for JSON/YAML
        """
        rv = [appstruct.format.value]
        if appstruct.charset:
            rv.extend([';', "charset=", appstruct.charset])

        return super().serialize(node, ''.join(rv))


TypeGenerator = ( typeit.TypeConstructor
                & MediaTypeTagSchema[MediaTypeTag]  # type: ignore
                & typeit.flags.GlobalNameOverride(lambda x: camelize(x, uppercase_first_letter=False))
                )

