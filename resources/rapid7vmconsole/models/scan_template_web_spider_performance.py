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


class ScanTemplateWebSpiderPerformance(object):
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
        'http_daemons_to_skip': 'list[str]',
        'maximum_directory_levels': 'int',
        'maximum_foreign_hosts': 'int',
        'maximum_link_depth': 'int',
        'maximum_pages': 'int',
        'maximum_retries': 'int',
        'maximum_time': 'str',
        'response_timeout': 'str',
        'threads_per_server': 'int'
    }

    attribute_map = {
        'http_daemons_to_skip': 'httpDaemonsToSkip',
        'maximum_directory_levels': 'maximumDirectoryLevels',
        'maximum_foreign_hosts': 'maximumForeignHosts',
        'maximum_link_depth': 'maximumLinkDepth',
        'maximum_pages': 'maximumPages',
        'maximum_retries': 'maximumRetries',
        'maximum_time': 'maximumTime',
        'response_timeout': 'responseTimeout',
        'threads_per_server': 'threadsPerServer'
    }

    def __init__(self, http_daemons_to_skip=None, maximum_directory_levels=None, maximum_foreign_hosts=None, maximum_link_depth=None, maximum_pages=None, maximum_retries=None, maximum_time=None, response_timeout=None, threads_per_server=None):  # noqa: E501
        """ScanTemplateWebSpiderPerformance - a model defined in Swagger"""  # noqa: E501

        self._http_daemons_to_skip = None
        self._maximum_directory_levels = None
        self._maximum_foreign_hosts = None
        self._maximum_link_depth = None
        self._maximum_pages = None
        self._maximum_retries = None
        self._maximum_time = None
        self._response_timeout = None
        self._threads_per_server = None
        self.discriminator = None

        if http_daemons_to_skip is not None:
            self.http_daemons_to_skip = http_daemons_to_skip
        if maximum_directory_levels is not None:
            self.maximum_directory_levels = maximum_directory_levels
        if maximum_foreign_hosts is not None:
            self.maximum_foreign_hosts = maximum_foreign_hosts
        if maximum_link_depth is not None:
            self.maximum_link_depth = maximum_link_depth
        if maximum_pages is not None:
            self.maximum_pages = maximum_pages
        if maximum_retries is not None:
            self.maximum_retries = maximum_retries
        if maximum_time is not None:
            self.maximum_time = maximum_time
        if response_timeout is not None:
            self.response_timeout = response_timeout
        if threads_per_server is not None:
            self.threads_per_server = threads_per_server

    @property
    def http_daemons_to_skip(self):
        """Gets the http_daemons_to_skip of this ScanTemplateWebSpiderPerformance.  # noqa: E501

        The names of HTTP Daemons (HTTPd) to skip when spidering. For example, `\"CUPS\"`.  # noqa: E501

        :return: The http_daemons_to_skip of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :rtype: list[str]
        """
        return self._http_daemons_to_skip

    @http_daemons_to_skip.setter
    def http_daemons_to_skip(self, http_daemons_to_skip):
        """Sets the http_daemons_to_skip of this ScanTemplateWebSpiderPerformance.

        The names of HTTP Daemons (HTTPd) to skip when spidering. For example, `\"CUPS\"`.  # noqa: E501

        :param http_daemons_to_skip: The http_daemons_to_skip of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :type: list[str]
        """

        self._http_daemons_to_skip = http_daemons_to_skip

    @property
    def maximum_directory_levels(self):
        """Gets the maximum_directory_levels of this ScanTemplateWebSpiderPerformance.  # noqa: E501

        The directory depth limit for web spidering. Limiting directory depth can save significant time, especially with large sites. A value of `0` signifies unlimited directory traversal. Defaults to `6`.  # noqa: E501

        :return: The maximum_directory_levels of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :rtype: int
        """
        return self._maximum_directory_levels

    @maximum_directory_levels.setter
    def maximum_directory_levels(self, maximum_directory_levels):
        """Sets the maximum_directory_levels of this ScanTemplateWebSpiderPerformance.

        The directory depth limit for web spidering. Limiting directory depth can save significant time, especially with large sites. A value of `0` signifies unlimited directory traversal. Defaults to `6`.  # noqa: E501

        :param maximum_directory_levels: The maximum_directory_levels of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :type: int
        """
        if maximum_directory_levels is not None and maximum_directory_levels > 100:  # noqa: E501
            raise ValueError("Invalid value for `maximum_directory_levels`, must be a value less than or equal to `100`")  # noqa: E501
        if maximum_directory_levels is not None and maximum_directory_levels < 1:  # noqa: E501
            raise ValueError("Invalid value for `maximum_directory_levels`, must be a value greater than or equal to `1`")  # noqa: E501

        self._maximum_directory_levels = maximum_directory_levels

    @property
    def maximum_foreign_hosts(self):
        """Gets the maximum_foreign_hosts of this ScanTemplateWebSpiderPerformance.  # noqa: E501

        The maximum number of unique host names that the spider may resolve. This function adds substantial time to the spidering process, especially with large Web sites, because of frequent cross-link checking involved. Defaults to `100`.  # noqa: E501

        :return: The maximum_foreign_hosts of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :rtype: int
        """
        return self._maximum_foreign_hosts

    @maximum_foreign_hosts.setter
    def maximum_foreign_hosts(self, maximum_foreign_hosts):
        """Sets the maximum_foreign_hosts of this ScanTemplateWebSpiderPerformance.

        The maximum number of unique host names that the spider may resolve. This function adds substantial time to the spidering process, especially with large Web sites, because of frequent cross-link checking involved. Defaults to `100`.  # noqa: E501

        :param maximum_foreign_hosts: The maximum_foreign_hosts of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :type: int
        """

        self._maximum_foreign_hosts = maximum_foreign_hosts

    @property
    def maximum_link_depth(self):
        """Gets the maximum_link_depth of this ScanTemplateWebSpiderPerformance.  # noqa: E501

        The maximum depth of links to traverse when spidering. Defaults to `6`.  # noqa: E501

        :return: The maximum_link_depth of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :rtype: int
        """
        return self._maximum_link_depth

    @maximum_link_depth.setter
    def maximum_link_depth(self, maximum_link_depth):
        """Sets the maximum_link_depth of this ScanTemplateWebSpiderPerformance.

        The maximum depth of links to traverse when spidering. Defaults to `6`.  # noqa: E501

        :param maximum_link_depth: The maximum_link_depth of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :type: int
        """
        if maximum_link_depth is not None and maximum_link_depth > 100:  # noqa: E501
            raise ValueError("Invalid value for `maximum_link_depth`, must be a value less than or equal to `100`")  # noqa: E501
        if maximum_link_depth is not None and maximum_link_depth < 0:  # noqa: E501
            raise ValueError("Invalid value for `maximum_link_depth`, must be a value greater than or equal to `0`")  # noqa: E501

        self._maximum_link_depth = maximum_link_depth

    @property
    def maximum_pages(self):
        """Gets the maximum_pages of this ScanTemplateWebSpiderPerformance.  # noqa: E501

        The maximum the number of pages that are spidered. This is a time-saving measure for large sites. Defaults to `3000`.  # noqa: E501

        :return: The maximum_pages of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :rtype: int
        """
        return self._maximum_pages

    @maximum_pages.setter
    def maximum_pages(self, maximum_pages):
        """Sets the maximum_pages of this ScanTemplateWebSpiderPerformance.

        The maximum the number of pages that are spidered. This is a time-saving measure for large sites. Defaults to `3000`.  # noqa: E501

        :param maximum_pages: The maximum_pages of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :type: int
        """
        if maximum_pages is not None and maximum_pages > 1000000:  # noqa: E501
            raise ValueError("Invalid value for `maximum_pages`, must be a value less than or equal to `1000000`")  # noqa: E501
        if maximum_pages is not None and maximum_pages < 0:  # noqa: E501
            raise ValueError("Invalid value for `maximum_pages`, must be a value greater than or equal to `0`")  # noqa: E501

        self._maximum_pages = maximum_pages

    @property
    def maximum_retries(self):
        """Gets the maximum_retries of this ScanTemplateWebSpiderPerformance.  # noqa: E501

        The maximum the number of times to retry a request after a failure. A value of `0` means no retry attempts are made. Defaults to `2`.  # noqa: E501

        :return: The maximum_retries of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :rtype: int
        """
        return self._maximum_retries

    @maximum_retries.setter
    def maximum_retries(self, maximum_retries):
        """Sets the maximum_retries of this ScanTemplateWebSpiderPerformance.

        The maximum the number of times to retry a request after a failure. A value of `0` means no retry attempts are made. Defaults to `2`.  # noqa: E501

        :param maximum_retries: The maximum_retries of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :type: int
        """
        if maximum_retries is not None and maximum_retries > 999:  # noqa: E501
            raise ValueError("Invalid value for `maximum_retries`, must be a value less than or equal to `999`")  # noqa: E501
        if maximum_retries is not None and maximum_retries < 0:  # noqa: E501
            raise ValueError("Invalid value for `maximum_retries`, must be a value greater than or equal to `0`")  # noqa: E501

        self._maximum_retries = maximum_retries

    @property
    def maximum_time(self):
        """Gets the maximum_time of this ScanTemplateWebSpiderPerformance.  # noqa: E501

        The maximum length of time to web spider. This limit prevents scans from taking longer than the allotted scan schedule. A value of `PT0S` means no limit is applied. The acceptable range is `PT1M` to `PT16666.6667H`.  # noqa: E501

        :return: The maximum_time of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :rtype: str
        """
        return self._maximum_time

    @maximum_time.setter
    def maximum_time(self, maximum_time):
        """Sets the maximum_time of this ScanTemplateWebSpiderPerformance.

        The maximum length of time to web spider. This limit prevents scans from taking longer than the allotted scan schedule. A value of `PT0S` means no limit is applied. The acceptable range is `PT1M` to `PT16666.6667H`.  # noqa: E501

        :param maximum_time: The maximum_time of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :type: str
        """

        self._maximum_time = maximum_time

    @property
    def response_timeout(self):
        """Gets the response_timeout of this ScanTemplateWebSpiderPerformance.  # noqa: E501

        The duration to wait for a response from a target web server. The value is specified as a ISO8601 duration and can range from `PT0S` (0ms) to `P1H` (1 hour). Defaults to `PT2M`.  # noqa: E501

        :return: The response_timeout of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :rtype: str
        """
        return self._response_timeout

    @response_timeout.setter
    def response_timeout(self, response_timeout):
        """Sets the response_timeout of this ScanTemplateWebSpiderPerformance.

        The duration to wait for a response from a target web server. The value is specified as a ISO8601 duration and can range from `PT0S` (0ms) to `P1H` (1 hour). Defaults to `PT2M`.  # noqa: E501

        :param response_timeout: The response_timeout of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :type: str
        """

        self._response_timeout = response_timeout

    @property
    def threads_per_server(self):
        """Gets the threads_per_server of this ScanTemplateWebSpiderPerformance.  # noqa: E501

        The number of threads to use per web server being spidered. Defaults to `3`.  # noqa: E501

        :return: The threads_per_server of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :rtype: int
        """
        return self._threads_per_server

    @threads_per_server.setter
    def threads_per_server(self, threads_per_server):
        """Sets the threads_per_server of this ScanTemplateWebSpiderPerformance.

        The number of threads to use per web server being spidered. Defaults to `3`.  # noqa: E501

        :param threads_per_server: The threads_per_server of this ScanTemplateWebSpiderPerformance.  # noqa: E501
        :type: int
        """
        if threads_per_server is not None and threads_per_server > 999:  # noqa: E501
            raise ValueError("Invalid value for `threads_per_server`, must be a value less than or equal to `999`")  # noqa: E501
        if threads_per_server is not None and threads_per_server < 0:  # noqa: E501
            raise ValueError("Invalid value for `threads_per_server`, must be a value greater than or equal to `0`")  # noqa: E501

        self._threads_per_server = threads_per_server

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
        if issubclass(ScanTemplateWebSpiderPerformance, dict):
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
        if not isinstance(other, ScanTemplateWebSpiderPerformance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
