import logging
import os

# Constants
LOGGING_LEVEL = logging.DEBUG
LOG_LEVEL_INFO = logging.INFO
LOG_LEVEL_ERROR = logging.ERROR
LOG_LEVEL_WARN = logging.WARNING
LOG_LEVEL_DEBUG = logging.DEBUG
LOG_DIR:str = "../logs"
CUSTOM_FORMAT:str = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
DATE_FORMAT:str = '%Y-%m-%d %H:%M:%S'

DEFAULT_CLASS_NAME='Default_Class_Name'
DEFAULT_NUM_SPACES:int = 4
DEFAULT_MULTILINE_STR:str = 'Default Line1\nDefault Line2'
DEFAULT_SEPERATOR = '\n'
DEFAULT_INPUT_STR:str = "Default Line A"



class UtilityLogger:
    """
    
    Common Wrapper Class Factory for Log creation
    
    Glenn Phillips gphillips@mdot.state.md.us
    September 17, 2023
    
    """

    def __init__(self,
                 logger_name: str=DEFAULT_CLASS_NAME,
                 log_level: str=LOGGING_LEVEL,
                 log_dir: str=LOG_DIR,
                 formatter: str=CUSTOM_FORMAT,
                 date_format: str=DATE_FORMAT):
        """
        Utility Logger Constructor 
        
        :param logger_name:
        :param log_level:
        :param log_dir:
        :param formatter:
        :param date_format:
        """
        self.logger_name = logger_name
        self.log_level = log_level
        self._log_dir = log_dir
        self.date_format = date_format
 
        self.formatter = self._set_formatter(formatter, date_format)
        
        self._set_console_output(False)
        self._configure_logger()
    
    def _configure_logger(self,):
        """
        Configure the _logger   
        :param self:
        """

        # self._logger = logging.getLogger(self.logger_name)
        self._logger = logging.Logger(self.logger_name)
        self._logger.setLevel(self.log_level)
        self._logger.propagate = False
        
        # Create a console handler and set its level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(self.formatter)
        
        # Create a file handler if _log_dir is provided
        if self._log_dir:
            log_file = os.path.join(self._log_dir, f"{self.logger_name}.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(self.formatter)
            self._logger.addHandler(file_handler)
            self._logger.propagate = False
        
        # Add the console handler to the _logger if console output is enabled
        if self.console_enabled:
            self._logger.addHandler(console_handler)
    
    @property
    def logger(self) -> logging.Logger:
        """
        get _logger instance
        
        :param self:
        :return configured _logger instance:
        """
        return self._logger
    
    @logger.setter
    def logger(self, logger_object:logging.Logger) -> None:
        """

        
        :param logger_object:
        """
        self._logger = logger_object
    
    @property
    def log_dir(self) -> str:
        """

        :param self :
        """
        return self._log_dir
    
    @log_dir.setter
    def log_dir(self, log_dir: str):
        """
        Sets log directory
        
        :param log_dir:
        """
        self._log_dir = log_dir
        # Reconfigure the _logger with the updated _log_dir
        self._configure_logger()
        
    def log(self, log_level:str=LOGGING_LEVEL, msg:str=DEFAULT_INPUT_STR) -> None:
        """
        Sends log message to internal _logger instance.
 
        :param log_level: use constants from logging
        :param msg:
        """
        self._logger.log(log_level, msg)

    def log_exception(self, message:str) -> None:
        """
        Send exception to _logger
        
        :param message: the exception and the message to send to the logger
        """
        self._logger.exception(message)
        
    def _set_console_output(self, enabled:str=False) -> None:
        """
        Set console output
        
        :param enabled:
        """
        self.console_enabled = enabled

    def _set_formatter(self, custom_format:str=CUSTOM_FORMAT,
                              date_format:str=DATE_FORMAT) -> logging.Formatter:
        """
        
        :param custom_format:
        :param date_format:
        """
        
        if custom_format is None:
            custom_format = CUSTOM_FORMAT
        if date_format is None:
            date_format = DATE_FORMAT
        resulting_formatter = logging.Formatter(custom_format, date_format)             
        return resulting_formatter
    
    def _append_spaces(self, input_string:str=DEFAULT_INPUT_STR, num_spaces:int=DEFAULT_NUM_SPACES) -> None:
        """
        Appends a specified number of spaces to a string.
    
        @param input_string: The input string.
        @param num_spaces: The number of spaces to append.
        @return: The input string with the specified number of spaces appended.
        """
        if num_spaces < 0:
            raise ValueError("Number of spaces should be non-negative.")
        
        spaces = ' ' * num_spaces
        return spaces + input_string
    
    def multline_log(self, 
                     log_level:str=LOG_LEVEL_INFO,
                     msg:str=DEFAULT_MULTILINE_STR, 
                     sep:str=DEFAULT_SEPERATOR, 
                     num_indent:int=DEFAULT_NUM_SPACES) -> None:
        """
         Make a multi line entry in the log for a single event
                
        :param log_level:
        :param msg:
        :param sep:
        :param num_indent:
        """
        if log_level is None:
            log_level = LOG_LEVEL_DEBUG
        
        if sep is None:
            sep = DEFAULT_SEPERATOR
            
        if num_indent is None:
            num_indent = DEFAULT_NUM_SPACES
            
        if msg is None:
            msg:str = DEFAULT_INPUT_STR
        
        lines:list = msg.split(sep)
     
        for line in lines:
            self._logger.log(log_level, self._append_spaces(line, num_indent))
        return
            
    def box_message(self, input_string:str=DEFAULT_INPUT_STR) -> str:
        """
        Encapsulate text in a box
        
        :param input_string:
        """
        if not input_string:
            return "Input string is empty."

        lines = input_string.splitlines()
        max_line_length = max(len(line) for line in lines)
        box_width = max_line_length + 4  # Add 2 spaces on each side and 2 '|' characters.
    
        box = []
        box.append('+' + '-' * box_width + '+')
    
        for line in lines:
            box.append(f'| {line.ljust(max_line_length)}   |')
    
        box.append('+' + '-' * box_width + '+')
    
        return '\n'.join(box)

    @staticmethod
    def quick_functionality_test():
        """
        Static Method to test basic functions
        """
            # can use "UtilityLoggerExample" self.__class__.__name__
        logger_utility = UtilityLogger("UtilityLoggerExample {}".format("_MAIN"), logging.DEBUG, "./", None, None)
        
        # Get a _logger for 'MyClass'
        logger = logger_utility.logger
        
        # Now you can use this _logger to log messages
        logger.debug("This is a debug message.")
        logger.info("This is an info message.")
        logger.warning("This is a warning message.")
        logger.error("This is an error message.")
        logger.critical("This is a critical message.")
        logger.log(logging.ERROR, "log method 1 Error Line")
        logger.log(logging.ERROR, "log method 2 Error Line")
        
        try:
            # Simulate an exception
            raise ValueError("An example error occurred.")
        except ValueError as e:
            # Log the exception traceback using the new method
            logger_utility.log_exception(f"An exception occurred:{e.args}")
            logger_utility.multline_log(logging.CRITICAL, logger_utility.box_message(str(e.args)))
            
        logger_utility.multline_log(logging.DEBUG, msg=None, sep=None, num_indent=None)
        test_msg = "TEST Line 1\nTEST Line 2 TEST Line 2\nTEST Line 3 TEST Line 3 TEST Line 3\n"
        test_msg = logger_utility.box_message(test_msg)
        logger_utility.multline_log(logging.DEBUG, test_msg, sep=None, num_indent=None)
        logger_utility.multline_log(logging.DEBUG, msg=test_msg, sep=None, num_indent=None)
        logger_utility.multline_log(logging.INFO, msg=test_msg, sep=None, num_indent=None)
        logger_utility.multline_log(logging.WARN, msg=test_msg, sep=None, num_indent=None)
        logger_utility.multline_log(logging.CRITICAL, msg=test_msg, sep=None, num_indent=None)
        
        
if __name__ == "__main__":
    """
    Main for Quick functionality test 
    """
    UtilityLogger.quick_functionality_test()
    
