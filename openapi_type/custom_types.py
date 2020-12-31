from enum import Enum
from typing import NewType, NamedTuple, Optional, Mapping, Sequence

import typeit
from inflection import camelize
from typeit.schema import Invalid


class ContentTypeFormat(Enum):
    JSON = 'application/json'
    XML = 'application/xml'
    TEXT = 'text/plain'
    FORM_URLENCODED = 'application/x-www-form-urlencoded'
    BINARY_STREAM = 'application/octet-stream'


MediaTypeCharset = NewType('MediaTypeCharset', str)


class ContentTypeTag(NamedTuple):
    format: ContentTypeFormat
    charset: Optional[MediaTypeCharset]


class ContentTypeTagSchema(typeit.schema.primitives.Str):
    def deserialize(self, node, cstruct: str) -> ContentTypeTag:
        """ Converts input string value ``cstruct`` to ``ContentTypeTag``
        """
        try:
            tag_str = super().deserialize(node, cstruct)
        except Invalid as e:
            error = Invalid(node, "Media Type should be a string", cstruct)
            error.add(e)
            raise error

        media_format, *param = tag_str.split(';')
        try:
            typed_format = ContentTypeFormat(media_format)
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
        return ContentTypeTag(
            format=typed_format,
            charset=charset
        )

    def serialize(self, node, appstruct: ContentTypeTag) -> str:
        """ Converts ``ContentTypeTag`` back to string value suitable for JSON/YAML
        """
        rv = [appstruct.format.value]
        if appstruct.charset:
            rv.extend([';', "charset=", appstruct.charset])

        return super().serialize(node, ''.join(rv))


class RefTo(Enum):
    SCHEMAS = '#/components/schemas/'
    LINKS = '#/components/links/'


class Ref(NamedTuple):
    location: RefTo
    name: str


class RefSchema(typeit.schema.primitives.Str):
    REF_PREFIX: Sequence[str] = ['#', 'components']
    REF_LOCATIONS: Mapping[str, RefTo] = {
        'schemas': RefTo.SCHEMAS,
        'links': RefTo.LINKS,
    }

    def deserialize(self, node, cstruct: str) -> Ref:
        """ Converts input string value ``cstruct`` to ``Ref``
        """
        try:
            ref_str = super().deserialize(node, cstruct)
        except Invalid as e:
            error = Invalid(node, "Reference should be a string", cstruct)
            error.add(e)
            raise error

        try:
            *prefix, location, ref_name = ref_str.split('/')
        except (ValueError, AttributeError):
            raise Invalid(node, "Invalid reference format", ref_str)

        if prefix != self.REF_PREFIX:
            raise Invalid(node, f"Reference is not prefixed with {'/'.join(self.REF_PREFIX)}", ref_str)

        try:
            ref_location = self.REF_LOCATIONS[location]
        except KeyError:
            raise Invalid(node, "Unrecognised reference location", ref_str)

        return Ref(ref_location, ref_name)

    def serialize(self, node, appstruct: Ref) -> str:
        """ Converts ``Ref`` back to string value suitable for JSON/YAML
        """
        rv = [appstruct.location.value, appstruct.name]
        return super().serialize(node, ''.join(rv))


TypeGenerator = (typeit.TypeConstructor
                 & ContentTypeTagSchema[ContentTypeTag]  # type: ignore
                 & RefSchema[Ref]  # type: ignore
                 & typeit.flags.GlobalNameOverride(lambda x: camelize(x, uppercase_first_letter=False))
                 )
