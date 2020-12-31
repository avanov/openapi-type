from enum import Enum

from typing import Literal, NewType
from typing import Mapping
from typing import Any, NamedTuple, Optional, Sequence, FrozenSet, Union

from inflection import camelize
from typeit import TypeConstructor, flags

from pyrsistent import pmap, pvector
from pyrsistent.typing import PVector, PMap


__all__ = ('parse_spec', 'serialize_spec', 'OpenAPI')


class IntegerValue(NamedTuple):
    type: Literal['integer']
    format: str = ''
    example: Optional[int] = None


class StringValue(NamedTuple):
    type: Literal['string']
    format: str = ''
    description: str = ''
    enum: PVector[str] = pvector()
    example: str = ''


class BooleanValue(NamedTuple):
    type: Literal['boolean']


Ref = NewType('Ref', str)


class Reference(NamedTuple):
    ref: Ref


class ObjectValue(NamedTuple):
    type: Literal['object']
    properties: Mapping[str, 'SchemaValue']  # type: ignore
    xml: Mapping[str, Any] = pmap()


class ArrayValue(NamedTuple):
    type: Literal['array']
    items: 'SchemaValue'  # type: ignore


SchemaValue = Union[StringValue, IntegerValue, BooleanValue, Reference, ObjectValue, ArrayValue]  # type: ignore


class ObjectSchema(NamedTuple):
    type: Literal['object']
    properties: Mapping[str, SchemaValue]
    required: FrozenSet[str] = frozenset()
    description: str = ''


class ArraySchema(NamedTuple):
    type: Literal['array']
    items: SchemaValue


class ResponseRef(NamedTuple):
    """ Values that are referenced as $response.body#/some/path
    """
    operation_id: str
    parameters: Mapping[str, str]


class ObjectRef(NamedTuple):
    """ Values that are referenced as #/components/schemas/<SomeType>
    """
    ref: str


class ProductSchemaType(NamedTuple):
    all_of: Sequence['SchemaType']  # type: ignore


SchemaType = Union[ObjectSchema, ArraySchema, ResponseRef, Reference, ProductSchemaType]  # type: ignore


class Components(NamedTuple):
    schemas: Mapping[str, SchemaType]
    links: Mapping[str, SchemaType] = pmap()
    request_bodies: Mapping[str, Any] = pmap()
    security_schemes: Mapping[str, Any] = pmap()


class ServerVar(NamedTuple):
    default: str
    enum: Sequence[str]
    description: str = ''


class Server(NamedTuple):
    url: str
    description: str = ''
    variables: Mapping[str, ServerVar] = pmap()


class InfoLicense(NamedTuple):
    name: str
    url: str = ''


class InfoContact(NamedTuple):
    name: Optional[str]
    email: Optional[str]
    url: Optional[str]


class Info(NamedTuple):
    version: str
    """ API version
    """
    title: str
    license: Optional[InfoLicense]
    contact: Optional[InfoContact]
    terms_of_service: str = ''
    description: str = ''


class SpecFormat(Enum):
    V3_0_0 = '3.0.0'
    V3_0_1 = '3.0.1'
    V3_0_2 = '3.0.2'


class OperationParameter(NamedTuple):
    name: str
    in_: str
    schema: SchemaValue
    required: bool = False
    description: str = ''
    style: str = ''


HTTPCode = NewType('HTTPCode', str)
HeaderName = NewType('HeaderName', str)


class MediaTypeTag(Enum):
    """ Response content type
    """
    JSON = 'application/json'
    XML = 'application/xml'
    TEXT = 'text/plain'
    FORM_URLENCODED = 'application/x-www-form-urlencoded'
    BINARY_STREAM = 'application/octet-stream'


class Header(NamedTuple):
    """ response header
    """
    schema: SchemaValue
    description: str = ''


class MediaType(NamedTuple):
    """ https://swagger.io/specification/#media-type-object
    """
    schema: PMap[str, Any] = pmap()
    example: PMap[str, Any] = pmap()
    examples: Mapping[str, Any] = pmap()
    encoding: Mapping[str, Any] = pmap()


class Response(NamedTuple):
    """ Response of an endpoint
    """
    content: PMap[MediaTypeTag, MediaType] = pmap()
    headers: PMap[HeaderName, Header] = pmap()
    description: str = ''


class ExternalDoc(NamedTuple):
    url: str
    description: str = ''


class RequestBody(NamedTuple):
    """ https://swagger.io/specification/#request-body-object
    """
    content: Mapping[MediaTypeTag, Any]
    description: str = ''
    required: bool = False


class Operation(NamedTuple):
    """ https://swagger.io/specification/#operation-object
    """
    responses: Mapping[HTTPCode, Response]
    external_docs: Optional[ExternalDoc]
    summary: str = ''
    operation_id: str = ''
    parameters: FrozenSet[Union[OperationParameter, Reference]] = frozenset()
    request_body: Union[None, RequestBody, Reference] = None
    description: str = ''
    tags: FrozenSet[str] = frozenset()
    callbacks: Mapping[str, Mapping[str, Any]] = pmap()
    security: Optional[Any] = None


class PathItem(NamedTuple):
    """ Describes endpoint methods
    """
    head: Optional[Operation]
    get: Optional[Operation]
    post: Optional[Operation]
    put: Optional[Operation]
    patch: Optional[Operation]
    delete: Optional[Operation]
    trace: Optional[Operation]
    servers: Sequence[Server] = pvector()
    ref: Ref = Ref('')
    summary: str = ''
    description: str = ''


SecurityName = NewType('SecurityName', str)


class SpecTag(NamedTuple):
    name: str
    external_docs: Optional[ExternalDoc]
    description: str = ''


class OpenAPI(NamedTuple):
    openapi: SpecFormat
    """ Spec format version
    """
    info: Info
    """ Various metadata
    """
    paths: Mapping[str, PathItem]
    components: Components = Components(schemas=pmap(), links=pmap())
    servers: Sequence[Server] = pvector()
    security: Sequence[Mapping[SecurityName, Sequence[str]]] = pvector()
    tags: Sequence[SpecTag] = pvector()
    external_docs: Optional[ExternalDoc] = None


overrides = {
    OperationParameter.in_: 'in',
    Reference.ref: '$ref',
    PathItem.ref: '$ref',
}
_camelcase_attribute_names = flags.GlobalNameOverride(lambda x: camelize(x, uppercase_first_letter=False))

TypeGen = TypeConstructor & overrides & _camelcase_attribute_names

parse_spec, serialize_spec = TypeGen ^ OpenAPI
