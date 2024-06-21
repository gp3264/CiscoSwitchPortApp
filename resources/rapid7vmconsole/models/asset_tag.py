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


class AssetTag(object):
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
        'color': 'str',
        'created': 'str',
        'id': 'int',
        'links': 'list[Link]',
        'name': 'str',
        'risk_modifier': 'object',
        'search_criteria': 'SearchCriteria',
        'source': 'str',
        'sources': 'list[TagAssetSource]',
        'type': 'str'
    }

    attribute_map = {
        'color': 'color',
        'created': 'created',
        'id': 'id',
        'links': 'links',
        'name': 'name',
        'risk_modifier': 'riskModifier',
        'search_criteria': 'searchCriteria',
        'source': 'source',
        'sources': 'sources',
        'type': 'type'
    }

    def __init__(self, color=None, created=None, id=None, links=None, name=None, risk_modifier=None, search_criteria=None, source=None, sources=None, type=None):  # noqa: E501
        """AssetTag - a model defined in Swagger"""  # noqa: E501

        self._color = None
        self._created = None
        self._id = None
        self._links = None
        self._name = None
        self._risk_modifier = None
        self._search_criteria = None
        self._source = None
        self._sources = None
        self._type = None
        self.discriminator = None

        if color is not None:
            self.color = color
        if created is not None:
            self.created = created
        if id is not None:
            self.id = id
        if links is not None:
            self.links = links
        self.name = name
        if risk_modifier is not None:
            self.risk_modifier = risk_modifier
        if search_criteria is not None:
            self.search_criteria = search_criteria
        if source is not None:
            self.source = source
        if sources is not None:
            self.sources = sources
        self.type = type

    @property
    def color(self):
        """Gets the color of this AssetTag.  # noqa: E501

        The color to use when rendering the tag in a user interface.  # noqa: E501

        :return: The color of this AssetTag.  # noqa: E501
        :rtype: str
        """
        return self._color

    @color.setter
    def color(self, color):
        """Sets the color of this AssetTag.

        The color to use when rendering the tag in a user interface.  # noqa: E501

        :param color: The color of this AssetTag.  # noqa: E501
        :type: str
        """
        allowed_values = ["default", "blue", "green", "orange", "red", "purple"]  # noqa: E501
        if color not in allowed_values:
            raise ValueError(
                "Invalid value for `color` ({0}), must be one of {1}"  # noqa: E501
                .format(color, allowed_values)
            )

        self._color = color

    @property
    def created(self):
        """Gets the created of this AssetTag.  # noqa: E501

        The date and time the tag was created.  # noqa: E501

        :return: The created of this AssetTag.  # noqa: E501
        :rtype: str
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this AssetTag.

        The date and time the tag was created.  # noqa: E501

        :param created: The created of this AssetTag.  # noqa: E501
        :type: str
        """

        self._created = created

    @property
    def id(self):
        """Gets the id of this AssetTag.  # noqa: E501

        The identifier of the tag.  # noqa: E501

        :return: The id of this AssetTag.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AssetTag.

        The identifier of the tag.  # noqa: E501

        :param id: The id of this AssetTag.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def links(self):
        """Gets the links of this AssetTag.  # noqa: E501

        Hypermedia links to corresponding or related resources.  # noqa: E501

        :return: The links of this AssetTag.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this AssetTag.

        Hypermedia links to corresponding or related resources.  # noqa: E501

        :param links: The links of this AssetTag.  # noqa: E501
        :type: list[Link]
        """

        self._links = links

    @property
    def name(self):
        """Gets the name of this AssetTag.  # noqa: E501

        The name (label) of the tab.  # noqa: E501

        :return: The name of this AssetTag.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AssetTag.

        The name (label) of the tab.  # noqa: E501

        :param name: The name of this AssetTag.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def risk_modifier(self):
        """Gets the risk_modifier of this AssetTag.  # noqa: E501

        The amount to adjust risk of an asset tagged with this tag.   # noqa: E501

        :return: The risk_modifier of this AssetTag.  # noqa: E501
        :rtype: object
        """
        return self._risk_modifier

    @risk_modifier.setter
    def risk_modifier(self, risk_modifier):
        """Sets the risk_modifier of this AssetTag.

        The amount to adjust risk of an asset tagged with this tag.   # noqa: E501

        :param risk_modifier: The risk_modifier of this AssetTag.  # noqa: E501
        :type: object
        """

        self._risk_modifier = risk_modifier

    @property
    def search_criteria(self):
        """Gets the search_criteria of this AssetTag.  # noqa: E501


        :return: The search_criteria of this AssetTag.  # noqa: E501
        :rtype: SearchCriteria
        """
        return self._search_criteria

    @search_criteria.setter
    def search_criteria(self, search_criteria):
        """Sets the search_criteria of this AssetTag.


        :param search_criteria: The search_criteria of this AssetTag.  # noqa: E501
        :type: SearchCriteria
        """

        self._search_criteria = search_criteria

    @property
    def source(self):
        """Gets the source of this AssetTag.  # noqa: E501

        The source of the tag.  # noqa: E501

        :return: The source of this AssetTag.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this AssetTag.

        The source of the tag.  # noqa: E501

        :param source: The source of this AssetTag.  # noqa: E501
        :type: str
        """
        allowed_values = ["built-in", "custom"]  # noqa: E501
        if source not in allowed_values:
            raise ValueError(
                "Invalid value for `source` ({0}), must be one of {1}"  # noqa: E501
                .format(source, allowed_values)
            )

        self._source = source

    @property
    def sources(self):
        """Gets the sources of this AssetTag.  # noqa: E501

        The source(s) by which a tag is-applied to an asset.  # noqa: E501

        :return: The sources of this AssetTag.  # noqa: E501
        :rtype: list[TagAssetSource]
        """
        return self._sources

    @sources.setter
    def sources(self, sources):
        """Sets the sources of this AssetTag.

        The source(s) by which a tag is-applied to an asset.  # noqa: E501

        :param sources: The sources of this AssetTag.  # noqa: E501
        :type: list[TagAssetSource]
        """

        self._sources = sources

    @property
    def type(self):
        """Gets the type of this AssetTag.  # noqa: E501

        The type of the tag.  # noqa: E501

        :return: The type of this AssetTag.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this AssetTag.

        The type of the tag.  # noqa: E501

        :param type: The type of this AssetTag.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["custom", "location", "owner", "criticality"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if issubclass(AssetTag, dict):
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
        if not isinstance(other, AssetTag):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
