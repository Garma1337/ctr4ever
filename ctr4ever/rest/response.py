# coding=utf-8

class Response(object):

    def __init__(self, data, status_code: int = 200) -> None:
        self._data = data
        self._status_code = status_code

    def get_data(self):
        return self._data

    def get_status_code(self) -> int:
        return self._status_code

    def to_dictionary(self) -> dict:
        return {
            'data': self._data,
            'status_code': self._status_code
        }


class EmptyResponse(Response):

    def __init__(self) -> None:
        super().__init__('', 204)


class ErrorResponse(Response):

    def __init__(self, error: str, status_code: int = 200) -> None:
        super().__init__({'success': False, 'error': error }, status_code)


class SuccessResponse(Response):

    def __init__(self, data, status_code: int = 200) -> None:
        data['success'] = True
        super().__init__(data, status_code)
