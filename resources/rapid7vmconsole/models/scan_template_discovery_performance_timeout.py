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


class ScanTemplateDiscoveryPerformanceTimeout(object):
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
        'initial': 'str',
        'maximum': 'str',
        'minimum': 'str'
    }

    attribute_map = {
        'initial': 'initial',
        'maximum': 'maximum',
        'minimum': 'minimum'
    }

    def __init__(self, initial=None, maximum=None, minimum=None):  # noqa: E501
        """ScanTemplateDiscoveryPerformanceTimeout - a model defined in Swagger"""  # noqa: E501

        self._initial = None
        self._maximum = None
        self._minimum = None
        self.discriminator = None

        if initial is not None:
            self.initial = initial
        if maximum is not None:
            self.maximum = maximum
        if minimum is not None:
            self.minimum = minimum

    @property
    def initial(self):
        """Gets the initial of this ScanTemplateDiscoveryPerformanceTimeout.  # noqa: E501

        The initial timeout to wait between retry attempts. The value is specified as a ISO8601 duration and can range from `PT0.5S` (500ms) to `P30S` (30s). Defaults to `PT0.5S`.  # noqa: E501

        :return: The initial of this ScanTemplateDiscoveryPerformanceTimeout.  # noqa: E501
        :rtype: str
        """
        return self._initial

    @initial.setter
    def initial(self, initial):
        """Sets the initial of this ScanTemplateDiscoveryPerformanceTimeout.

        The initial timeout to wait between retry attempts. The value is specified as a ISO8601 duration and can range from `PT0.5S` (500ms) to `P30S` (30s). Defaults to `PT0.5S`.  # noqa: E501

        :param initial: The initial of this ScanTemplateDiscoveryPerformanceTimeout.  # noqa: E501
        :type: str
        """

        self._initial = initial

    @property
    def maximum(self):
        """Gets the maximum of this ScanTemplateDiscoveryPerformanceTimeout.  # noqa: E501

        The maximum time to wait between retries. The value is specified as a ISO8601 duration and can range from `PT0.5S` (500ms) to `P30S` (30s). Defaults to `PT3S`.  # noqa: E501

        :return: The maximum of this ScanTemplateDiscoveryPerformanceTimeout.  # noqa: E501
        :rtype: str
        """
        return self._maximum

    @maximum.setter
    def maximum(self, maximum):
        """Sets the maximum of this ScanTemplateDiscoveryPerformanceTimeout.

        The maximum time to wait between retries. The value is specified as a ISO8601 duration and can range from `PT0.5S` (500ms) to `P30S` (30s). Defaults to `PT3S`.  # noqa: E501

        :param maximum: The maximum of this ScanTemplateDiscoveryPerformanceTimeout.  # noqa: E501
        :type: str
        """

        self._maximum = maximum

    @property
    def minimum(self):
        """Gets the minimum of this ScanTemplateDiscoveryPerformanceTimeout.  # noqa: E501

        The minimum time to wait between retries. The value is specified as a ISO8601 duration and can range from `PT0.5S` (500ms) to `P30S` (30s). Defaults to `PT0.5S`.  # noqa: E501

        :return: The minimum of this ScanTemplateDiscoveryPerformanceTimeout.  # noqa: E501
        :rtype: str
        """
        return self._minimum

    @minimum.setter
    def minimum(self, minimum):
        """Sets the minimum of this ScanTemplateDiscoveryPerformanceTimeout.

        The minimum time to wait between retries. The value is specified as a ISO8601 duration and can range from `PT0.5S` (500ms) to `P30S` (30s). Defaults to `PT0.5S`.  # noqa: E501

        :param minimum: The minimum of this ScanTemplateDiscoveryPerformanceTimeout.  # noqa: E501
        :type: str
        """

        self._minimum = minimum

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
        if issubclass(ScanTemplateDiscoveryPerformanceTimeout, dict):
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
        if not isinstance(other, ScanTemplateDiscoveryPerformanceTimeout):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
