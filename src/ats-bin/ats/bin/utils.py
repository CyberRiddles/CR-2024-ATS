"""ATS launcher utilities"""

# imports
from __future__ import annotations
import os
from dataclasses import dataclass, fields


@dataclass
class LaunchArguments:
    server_ip: str
    server_port: int

    @staticmethod
    def __get_env() -> dict:
        """Retrieves the local environment variables based on the class fields"""
        # Get the arguments from the os based on this dataclass fields
        env_arguments: dict = {
            field.name: os.getenv(field.name)
            for field in fields(LaunchArguments)
            if os.getenv(field.name) is not None
        }

        # Return the arguments as dictionary
        return env_arguments

    @staticmethod
    def get_arguments() -> LaunchArguments:
        """"""
        # A dict that will store the arguments that have been retrieved
        arguments: dict = {}

        # Get environment arguments
        env_arguments: dict = LaunchArguments.__get_env()
        arguments.update(env_arguments)

        # Get config file arguments
        # <Not implemented for this puzzle>

        # Get cli arguments
        # <Not implemented for this puzzle>

        launch_arguments: LaunchArguments = LaunchArguments(**arguments)
        return launch_arguments
