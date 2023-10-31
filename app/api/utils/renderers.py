import json
from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import JSONRenderer


class RequestJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        errors = None
        errors = data.get('errors', None)
        if data and data.get('detail', '') and isinstance(data.get('detail', ''), ErrorDetail):
            errors = data['detail']
        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            data['status'] = 'failed'
            if data.get('errors', '') and isinstance(data['errors'], dict):
                error_list = format_errors(data)
                data['errors'] = error_list

            return super(RequestJSONRenderer, self).render(data)

        # Finally, we can render our data under the "user" namespace.
        data["status"] = "success"
        return json.dumps(data)


def format_errors(data):
    """
    Function that formats error messages
    Args:
        data(dict): error dict
    Returns:
        error(dict): formated errors
    """
    errors = list(data['errors'].values())
    error_list = []
    for error in errors:
        if isinstance(error, list):
            error_list.extend(error)
        else:
            nested_errors = list(error.values())
            nested_error = extract_errors(nested_errors[0])
            nested_error = nested_error if isinstance(nested_error, list) else [nested_error]
            error_list.extend(nested_error)

    return error_list


def extract_errors(nested_error):
    """
    Function that extract error message from the
    nested dict
    Args:
        nested_error(dict): nested_error dict
    Returns:
        None
    """
    if isinstance(nested_error, dict):
        errors = list(nested_error.values())
        if isinstance(errors[0], list):
            return errors[0]
        else:
            pass
    return nested_error[0] if isinstance(nested_error, list) else nested_error
