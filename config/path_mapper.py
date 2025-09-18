"""
Path mapping strategies for handling file paths in different execution environments.
Supports both binary execution and Docker container execution modes.
"""
import os
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path


class PathMappingStrategy(ABC):
    """Abstract base class for path mapping strategies."""
    
    @abstractmethod
    def map_paths(self, file_paths: List[str]) -> List[str]:
        pass


class BinaryPathMappingStrategy(PathMappingStrategy):
    
    def map_paths(self, file_paths: List[str]) -> List[str]:
        # No mapping needed for binary execution - paths work as-is.
        return file_paths


class DockerPathMappingStrategy(PathMappingStrategy):
    
    def __init__(self, source_working_directory: str, container_working_directory: str = "/home/bzm-mcp/working_directory"):
        self.source_working_directory = str(Path(source_working_directory).resolve()).rstrip('/')
        # Don't resolve container path - it should remain as specified for container execution
        self.container_working_directory = container_working_directory.rstrip('/')
    
    def map_paths(self, file_paths: List[str]) -> List[str]:
        mapped_paths = []
        
        for file_path in file_paths:
            abs_file_path = str(Path(file_path).resolve())
            
            if abs_file_path.startswith(self.source_working_directory):
                relative_path = abs_file_path[len(self.source_working_directory):].lstrip('/')
                mapped_path = f"{self.container_working_directory}/{relative_path}"
                mapped_paths.append(mapped_path)
            else:
                # Path doesn't start with source directory - keep as-is (might be relative or outside source)
                mapped_paths.append(file_path)
        
        return mapped_paths


class PathMapperFactory:
    """Factory for creating appropriate path mapping strategies."""
    
    @staticmethod
    def create_strategy() -> PathMappingStrategy:
        is_docker = os.getenv('MCP_DOCKER', 'false').lower() == 'true'
        
        if is_docker:
            source_dir = os.getenv('SOURCE_WORKING_DIRECTORY')
            if not source_dir:
                raise ValueError(
                    "Working directory must be set in the Docker catalog configuration."
                    "Without volume mount, actions like upload assets will not work."
                    "Lack of volume mount results in missing SOURCE_WORKING_DIRECTORY environment variable"
                )
            return DockerPathMappingStrategy(source_dir)
        else:
            return BinaryPathMappingStrategy()
