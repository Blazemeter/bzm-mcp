import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from config.path_mapper import (
    BinaryPathMappingStrategy,
    DockerPathMappingStrategy,
    PathMapperFactory,
)


class TestBinaryPathMappingStrategy:

    def test_map_paths_no_mapping(self):
        strategy = BinaryPathMappingStrategy()
        file_paths = [
            "/Users/user/Documents/test.jmx",
            "/Users/user/Documents/blazemeter/archive.zip",
            "relative/path/test.csv"
        ]
        
        result = strategy.map_paths(file_paths)
        
        assert result == file_paths

    def test_map_paths_empty_list(self):
        strategy = BinaryPathMappingStrategy()
        result = strategy.map_paths([])
        assert result == []


class TestDockerPathMappingStrategy:

    def test_map_paths_with_source_directory(self):
        strategy = DockerPathMappingStrategy(
            source_working_directory="/Users/user/Documents",
            container_working_directory="/home/bzm-mcp/working_directory"
        )
        
        file_paths = [
            "/Users/user/Documents/test.jmx",
            "/Users/user/Documents/blazemeter/archive.zip",
            "/Users/user/Documents/subdir/test.csv"
        ]
        
        result = strategy.map_paths(file_paths)
        
        expected = [
            "/home/bzm-mcp/working_directory/test.jmx",
            "/home/bzm-mcp/working_directory/blazemeter/archive.zip",
            "/home/bzm-mcp/working_directory/subdir/test.csv"
        ]
        
        assert result == expected

    def test_map_paths_with_trailing_slashes(self):
        strategy = DockerPathMappingStrategy(
            source_working_directory="/Users/user/Documents/",
            container_working_directory="/home/bzm-mcp/working_directory/"
        )
        
        file_paths = ["/Users/user/Documents/test.jmx"]
        result = strategy.map_paths(file_paths)
        
        expected = ["/home/bzm-mcp/working_directory/test.jmx"]
        assert result == expected

    def test_map_paths_outside_source_directory(self):
        strategy = DockerPathMappingStrategy(
            source_working_directory="/Users/user/Documents",
            container_working_directory="/home/bzm-mcp/working_directory"
        )
        
        file_paths = [
            "/Users/user/Documents/test.jmx", 
            "/Users/user/other/file.txt",     
            "relative/path/test.csv"           
        ]
        
        result = strategy.map_paths(file_paths)
        
        expected = [
            "/home/bzm-mcp/working_directory/test.jmx",
            "/Users/user/other/file.txt", 
            "relative/path/test.csv"      
        ]
        
        assert result == expected

    def test_map_paths_with_absolute_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            strategy = DockerPathMappingStrategy(
                source_working_directory=temp_dir,
                container_working_directory="/home/bzm-mcp/working_directory"
            )
            
            test_file = Path(temp_dir) / "test.jmx"
            test_file.touch()
            
            file_paths = [str(test_file)]
            result = strategy.map_paths(file_paths)
            
            expected = ["/home/bzm-mcp/working_directory/test.jmx"]
            assert result == expected

    def test_map_paths_empty_list(self):
        strategy = DockerPathMappingStrategy(
            source_working_directory="/Users/user/Documents",
            container_working_directory="/home/bzm-mcp/working_directory"
        )
        
        result = strategy.map_paths([])
        assert result == []


class TestPathMapperFactory:

    @patch.dict(os.environ, {'MCP_DOCKER': 'false'})
    def test_create_strategy_binary_mode(self):
        strategy = PathMapperFactory.create_strategy()
        assert isinstance(strategy, BinaryPathMappingStrategy)

    @patch.dict(os.environ, {'MCP_DOCKER': 'true', 'SOURCE_WORKING_DIRECTORY': '/Users/user/Documents'})
    def test_create_strategy_docker_mode(self):
        strategy = PathMapperFactory.create_strategy()
        assert isinstance(strategy, DockerPathMappingStrategy)
        assert strategy.source_working_directory == '/Users/user/Documents'

    @patch.dict(os.environ, {'MCP_DOCKER': 'true'}, clear=True)
    def test_create_strategy_docker_mode_missing_env_var(self):
        with pytest.raises(ValueError, match="Working directory must be set in the Docker catalog configuration"):
            PathMapperFactory.create_strategy()


class TestPathMappingIT:

    def test_real_world_scenario(self):
        strategy = DockerPathMappingStrategy(
            source_working_directory="/Users/theUser/Documents",
            container_working_directory="/home/bzm-mcp/working_directory"
        )
        
        file_paths = [
            "/Users/theUser/Documents/test.jmx",
            "/Users/theUser/Documents/blazemeter/jmeter/archive.zip",
            "/Users/theUser/Documents/data/test-data.csv",
            "/Users/theUser/Documents/config/test-config.yaml"
        ]
        
        result = strategy.map_paths(file_paths)
        
        expected = [
            "/home/bzm-mcp/working_directory/test.jmx",
            "/home/bzm-mcp/working_directory/blazemeter/jmeter/archive.zip",
            "/home/bzm-mcp/working_directory/data/test-data.csv",
            "/home/bzm-mcp/working_directory/config/test-config.yaml"
        ]
        
        assert result == expected

    def test_mixed_path_types(self):
        strategy = DockerPathMappingStrategy(
            source_working_directory="/Users/user/Documents",
            container_working_directory="/home/bzm-mcp/working_directory"
        )
        
        file_paths = [
            "/Users/user/Documents/test.jmx",      
            "relative/test.csv",                   
            "/tmp/other/file.txt",                 
            "/Users/user/Documents/subdir/test.zip"
        ]
        
        result = strategy.map_paths(file_paths)
        
        expected = [
            "/home/bzm-mcp/working_directory/test.jmx",
            "relative/test.csv",                   # Unchanged
            "/tmp/other/file.txt",                 # Unchanged
            "/home/bzm-mcp/working_directory/subdir/test.zip"
        ]
        
        assert result == expected
