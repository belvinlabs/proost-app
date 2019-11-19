from os import getenv
import collections
from datetime import datetime, timezone
import datetime as ddt
import pytz

from flask import Flask, json
from sqlalchemy.ext.declarative import DeclarativeMeta

from utils.enums import APIErrorTypes

app = Flask(__name__)


def get_nested(data, *args):
    if args and data:
        element = args[0]
        if element:
            value = data.get(element)
            return value if len(args) == 1 else get_nested(value, *args[1:])


def new_alchemy_encoder(fields_to_expand=[]):
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):

        def field_condition(self, x):
            
            return not x.startswith('_') and \
                   x != 'metadata' and \
                   x != 'query' and \
                   x != 'query_class'

        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                print()
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                # TODO filter out non supported objects like functions
                for field in [x for x in dir(obj) if self.field_condition(x)]:
                    val = obj.__getattribute__(field)
                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or (isinstance(val, list) and len(val) > 0 and isinstance(val[0].__class__, DeclarativeMeta)):
                        # unless we're expanding this field, stop here
                        if field not in fields_to_expand:
                            # not expanding this field: set it to None and continue
                            fields[field] = None
                            continue
                    if isinstance(val, datetime):
                        ts = val.timestamp()
                        temp_val = datetime.utcfromtimestamp(ts).replace(tzinfo=pytz.utc)
                        val = temp_val.isoformat()
                    fields[field] = val
                # a json-encodable dict
                return fields

            if isinstance(obj.__class__, collections.Callable):
                return None

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def dump_json(data, fields_to_expand=[]):
    indent = None
    separators = (',', ':')

    if app.config['JSONIFY_PRETTYPRINT_REGULAR'] or app.debug:
        indent = 2
        separators = (', ', ': ')

    data = json.dumps(data, cls=new_alchemy_encoder(fields_to_expand),
                      check_circular=False,
                      indent=indent,
                      separators=separators) + '\n'
    return data


def jsonify(data, fields_to_expand=[]):
    """This function wraps :func:`dumps` to add a few enhancements that make
    life easier.  It turns the JSON output into a :class:`~flask.Response`
    object with the :mimetype:`application/json` mimetype.  For convenience, it
    also converts multiple arguments into an array or multiple keyword
    arguments
    into a dict.  This means that both ``jsonify(1,2,3)`` and
    ``jsonify([1,2,3])`` serialize to ``[1,2,3]``.

    For clarity, the JSON serialization behavior has the following differences
    from :func:`dumps`:

    1. Single argument: Passed straight through to :func:`dumps`.
    2. Multiple arguments: Converted to an array before being passed to
       :func:`dumps`.
    3. Multiple keyword arguments: Converted to a dict before being passed to
       :func:`dumps`.

    Example usage::

        from flask import jsonify

        @app.route('/_get_current_user')
        def get_current_user():
            return jsonify(username=g.user.username,
                           email=g.user.email,
                           id=g.user.id)

    This will send a JSON response like this to the browser::

        {
            "username": "admin",
            "email": "admin@localhost",
            "id": 42
        }


    .. versionchanged:: 0.11
       Added support for serializing top-level arrays. This introduces a
       security risk in ancient browsers. See :ref:`json-security` for details.

    This function's response will be pretty printed if the
    ``JSONIFY_PRETTYPRINT_REGULAR`` config parameter is set to True or the
    Flask app is running in debug mode. Compressed (not pretty) formatting
    currently means no indents and no spaces after separators.

    .. versionadded:: 0.2
    """
    response_body = dump_json(data, fields_to_expand=fields_to_expand)

    return app.response_class(
        response_body,
        mimetype=app.config['JSONIFY_MIMETYPE']
    )
