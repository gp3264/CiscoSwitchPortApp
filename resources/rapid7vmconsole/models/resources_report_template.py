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


class ResourcesReportTemplate(object):
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
        'links': 'list[Link]',
        'resources': 'list[ReportTemplate]'
    }

    attribute_map = {
        'links': 'links',
        'resources': 'resources'
    }

    def __init__(self, links=None, resources=None):  # noqa: E501
        """ResourcesReportTemplate - a model defined in Swagger"""  # noqa: E501

        self._links = None
        self._resources = None
        self.discriminator = None

        if links is not None:
            self.links = links
        if resources is not None:
            self.resources = resources

    @property
    def links(self):
        """Gets the links of this ResourcesReportTemplate.  # noqa: E501

        Hypermedia links to corresponding or related resources.  # noqa: E501

        :return: The links of this ResourcesReportTemplate.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this ResourcesReportTemplate.

        Hypermedia links to corresponding or related resources.  # noqa: E501

        :param links: The links of this ResourcesReportTemplate.  # noqa: E501
        :type: list[Link]
        """

        self._links = links

    @property
    def resources(self):
        """Gets the resources of this ResourcesReportTemplate.  # noqa: E501

        The resources returned.  # noqa: E501

        :return: The resources of this ResourcesReportTemplate.  # noqa: E501
        :rtype: list[ReportTemplate]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this ResourcesReportTemplate.

        The resources returned.  # noqa: E501

        :param resources: The resources of this ResourcesReportTemplate.  # noqa: E501
        :type: list[ReportTemplate]
        """

        self._resources = resources

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
        if issubclass(ResourcesReportTemplate, dict):
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
        if not isinstance(other, ResourcesReportTemplate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
