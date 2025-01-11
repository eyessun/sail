# utils/response.py

from rest_framework.response import Response
from rest_framework import status

def success_response(data=None, message="success", code=0, total=None, page=None, page_size=None):
    """
    返回成功的标准格式
    :param data: 返回的数据
    :param message: 返回的信息
    :param code: 状态码（默认0表示成功）
    :param total: （分页时使用）总数据条数
    :param page: （分页时使用）当前页码
    :param page_size: （分页时使用）每页数据条数
    :return: Response对象
    """
    response = {
        "code": code,
        "message": message,
        "data": data,
        "total": total,
        "page": page,
        "pageSize": page_size
    }
    return Response(response, status=status.HTTP_200_OK)

def error_response(message="error", code=1000, data=None):
    """
    返回失败的标准格式
    :param message: 错误信息
    :param code: 错误码（默认1000表示通用错误）
    :param data: 返回的额外数据（默认None）
    :return: Response对象
    """
    response = {
        "code": code,
        "message": message,
        "data": data
    }
    return Response(response, status=status.HTTP_400_BAD_REQUEST)
