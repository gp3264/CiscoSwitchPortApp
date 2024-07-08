# coding: utf-8

"""
    Python InsightVM API Client

    OpenAPI spec version: 3
    Contact: support@rapid7.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class WebSettings(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'max_threads': 'int',
        'min_threads': 'int',
        'port': 'int',
        'session_timeout': 'str'
    }

    attribute_map = {
        'max_threads': 'maxThreads',
        'min_threads': 'minThreads',
        'port': 'port',
        'session_timeout': 'sessionTimeout'
    }

    def __init__(self, max_threads=None, min_threads=None, port=None, session_timeout=None):  # noqa: E501
        """WebSettings - a model defined in Swagger"""  # noqa: E501

        self._max_threads = None
        self._min_threads = None
        self._port = None
        self._session_timeout = None
        self.discriminator = None

        if max_threads is not None:
            self.max_threads = max_threads
        if min_threads is not None:
            self.min_threads = min_threads
        if port is not None:
            self.port = port
        if session_timeout is not None:
            self.session_timeout = session_timeout

    @property
    def max_threads(self):
        """Gets the max_threads of this WebSettings.  # noqa: E501

        The maximum number of request handling threads.  # noqa: E501

        :return: The max_threads of this WebSettings.  # noqa: E501
        :rtype: int
        """
        return self._max_threads

    @max_threads.setter
    def max_threads(self, max_threads):
        """Sets the max_threads of this WebSettings.

        The maximum number of request handling threads.  # noqa: E501

        :param max_threads: The max_threads of this WebSettings.  # noqa: E501
        :type: int
        """

        self._max_threads = max_threads

    @property
    def min_threads(self):
        """Gets the min_threads of this WebSettings.  # noqa: E501

        The minimum number of request handling threads.  # noqa: E501

        :return: The min_threads of this WebSettings.  # noqa: E501
        :rtype: int
        """
        return self._min_threads

    @min_threads.setter
    def min_threads(self, min_threads):
        """Sets the min_threads of this WebSettings.

        The minimum number of request handling threads.  # noqa: E501

        :param min_threads: The min_threads of this WebSettings.  # noqa: E501
        :type: int
        """

        self._min_threads = min_threads

    @property
    def port(self):
        """Gets the port of this WebSettings.  # noqa: E501

        The port the web server is accepting requests.  # noqa: E501

        :return: The port of this WebSettings.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this WebSettings.

        The port the web server is accepting requests.  # noqa: E501

        :param port: The port of this WebSettings.  # noqa: E501
        :type: int
        """

        self._port = port

    @property
    def session_timeout(self):
        """Gets the session_timeout of this WebSettings.  # noqa: E501

        Session timeout duration, in ISO 8601 format. For example: `\"PT10M\"`.  # noqa: E501

        :return: The session_timeout of this WebSettings.  # noqa: E501
        :rtype: str
        """
        return self._session_timeout

    @session_timeout.setter
    def session_timeout(self, session_timeout):
        """Sets the session_timeout of this WebSettings.

        Session timeout duration, in ISO 8601 format. For example: `\"PT10M\"`.  # noqa: E501

        :param session_timeout: The session_timeout of this WebSettings.  # noqa: E501
        :type: str
        """

        self._session_timeout = session_timeout

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(WebSettings, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, WebSettings):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other