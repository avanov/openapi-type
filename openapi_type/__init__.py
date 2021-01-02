from enum import Enum

from typing import Literal, NewType
from typing import Mapping
from typing import Any, NamedTuple, Optional, Sequence, FrozenSet, Union

from pyrsistent import pmap, pvector
from pyrsistent.typing import PVector, PMap

from .custom_types import TypeGenerator, ContentTypeTag, Ref


__all__ = ('parse_spec', 'serialize_spec', 'OpenAPI')


class IntegerValue(NamedTuple):
    type: Literal['integer']
    format: str = ''
    example: Optional[int] = None
    default: Optional[int] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None


class FloatValue(NamedTuple):
    type: Literal['number']
    format: str = ''
    example: Optional[float] = None
    default: Optional[float] = None


class StringValue(NamedTuple):
    type: Literal['string']
    format: str = ''
    description: str = ''
    enum: PVector[str] = pvector()
    default: Optional[str] = None
    example: str = ''


class BooleanValue(NamedTuple):
    type: Literal['boolean']
    default: Optional[bool] = None


class Reference(NamedTuple):
    ref: Ref


RecursiveAttrs = Mapping[str, 'SchemaValue']  # type: ignore


class ObjectValue(NamedTuple):
    type: Literal['object']
    properties: RecursiveAttrs
    xml: Mapping[str, Any] = pmap()


class ObjectWithAdditionalProperties(NamedTuple):
    type: Literal['object']
    additional_properties: Mapping[str, Any]


class ArrayValue(NamedTuple):
    type: Literal['array']
    items: 'SchemaValue'  # type: ignore


SchemaValue = Union[StringValue,       # type: ignore
                    IntegerValue,
                    FloatValue,
                    BooleanValue,
                    Reference,
                    ObjectValue,
                    ArrayValue,
                    ObjectWithAdditionalProperties]


class ObjectSchema(NamedTuple):
    type: Literal['object']
    properties: RecursiveAttrs
    required: FrozenSet[str] = frozenset()
    description: str = ''


class InlinedObjectSchema(NamedTuple):
    properties: RecursiveAttrs
    required: FrozenSet[str]
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


SchemaType = Union[StringValue, ObjectSchema, ArraySchema, ResponseRef, Reference, ProductSchemaType, ObjectWithAdditionalProperties, InlinedObjectSchema]  # type: ignore


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


class ParamLocation(Enum):
    QUERY = 'query'
    HEADER = 'header'
    PATH = 'path'
    COOKIE = 'cookie'


class OperationParameter(NamedTuple):
    name: str
    in_: ParamLocation
    schema: SchemaValue
    required: bool = False
    description: str = ''
    style: str = ''


HTTPCode = NewType('HTTPCode', str)
HeaderName = NewType('HeaderName', str)


class Header(NamedTuple):
    """ response header
    """
    schema: SchemaValue
    description: str = ''


class MediaType(NamedTuple):
    """ https://swagger.io/specification/#media-type-object
    """
    schema: Optional[SchemaType] = None
    example: PMap[str, Any] = pmap()
    examples: Mapping[str, Any] = pmap()
    encoding: Mapping[str, Any] = pmap()


class Response(NamedTuple):
    """ Response of an endpoint
    """
    content: PMap[ContentTypeTag, MediaType] = pmap()
    headers: PMap[HeaderName, Header] = pmap()
    description: str = ''


class ExternalDoc(NamedTuple):
    url: str
    description: str = ''


class RequestBody(NamedTuple):
    """ https://swagger.io/specification/#request-body-object
    """
    content: Mapping[ContentTypeTag, Any]
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
    ref: Optional[Ref] = None
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


parse_spec, serialize_spec = TypeGenerator & overrides ^ OpenAPI
