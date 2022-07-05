import traceback
from colorama import init, Fore
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.permissions import BasePermission

init(autoreset=True)


def import_callable(path_or_callable):
    if hasattr(path_or_callable, "__call__"):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, str)
        package, attr = path_or_callable.rsplit(".", 1)
        return getattr(import_module(package), attr)


def generate_response(title, body):
    match title:
        case "non_field_errors":
            msg_head = ""
        case _:
            msg_head = f"{title.capitalize()} :"
    msg_body = (
        body[0].replace(".", "") if (isinstance(body, list)) else body.replace(".", "")
    )
    message = f"{msg_head} {msg_body}".strip()
    return message


def create_uniform_response(errors):
    print("this is printed", errors)
    final_message = []
    if isinstance(errors, list):
        for error in errors:
            for key, value in error.items():
                final_message.append(generate_response(key, value))
    else:
        for key, value in errors.items():
            final_message.append(generate_response(key, value))
    return {"message": "\n".join(final_message), "code": "ERROR"}


def custom_exception_handler(exc, context):
    print("exec and context --", exc, context)
    response = exception_handler(exc, context)
    if response:
        return Response(create_uniform_response(response.data), status=exc.status_code)
    print(f"{Fore.YELLOW}\n\nMessage starts here ------------\n\n")
    print(
        f"{Fore.RED}".join(
            traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        )
    )
    print(f"{Fore.YELLOW}\n\nMessage ends here ------------\n\n")
    message = {
        "code": "ERROR",
        "message": "Error occured, admin has been informed",
    }
    return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OnlyUnAuthenticated(BasePermission):
    """
    Allows access only to unauthenticated users
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)
