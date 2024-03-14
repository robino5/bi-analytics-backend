from logging import getLogger

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import status

logging = getLogger("core.renderer")


class CustomRenderer(CamelCaseJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            status_code = renderer_context["response"].status_code

            code_to_msg = {
                status.HTTP_200_OK: "success",
                status.HTTP_202_ACCEPTED: "success",
                status.HTTP_201_CREATED: "success",
                status.HTTP_204_NO_CONTENT: "success",
                status.HTTP_400_BAD_REQUEST: "error",
                status.HTTP_401_UNAUTHORIZED: "error",
                status.HTTP_403_FORBIDDEN: "error",
                status.HTTP_404_NOT_FOUND: "error",
                status.HTTP_406_NOT_ACCEPTABLE: "error",
                status.HTTP_500_INTERNAL_SERVER_ERROR: "error",
            }

            response = {
                "status": code_to_msg.get(status_code),
                "code": status_code,
                "data": None,
                "message": None,
            }

            match status_code:
                case (
                    status.HTTP_200_OK
                    | status.HTTP_201_CREATED
                    | status.HTTP_204_NO_CONTENT
                    | status.HTTP_202_ACCEPTED
                ):
                    response["data"] = data
                case _:
                    if isinstance(data, dict) and data.get("detail", None):
                        response["message"] = data["detail"]
                    else:
                        response["message"] = data
            return super().render(response, accepted_media_type, renderer_context)
        except Exception as err:
            logging.exception(err)
            return super().render(
                {
                    "status": code_to_msg.get(status.HTTP_500_INTERNAL_SERVER_ERROR),
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "data": None,
                    "message": "an unexpected error happened. Please check log for more details.",
                }
            )
