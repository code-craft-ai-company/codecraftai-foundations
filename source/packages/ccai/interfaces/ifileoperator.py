"""
    .. module:: ifileoperator
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Protocol for abstracting file-system operations.
"""

from typing import Protocol, List

__all__ = ["IFileOperator"]


class IFileOperator(Protocol):
    """Protocol for abstracting file system operations."""
    
    def write_text(self, path: str, content: str, elevated: bool = False) -> None:
        """Write text to a file, replacing it if it exists."""
        
    def delete(self, path: str, elevated: bool = False) -> None:
        """Delete a file."""
        
    def read_text(self, path: str, elevated: bool = False) -> str:
        """Read the contents of a file as a string."""
        
    def list_dir(self, path: str, elevated: bool = False) -> List[str]:
        """List the names of all entries in a directory."""
        
    def exists(self, path: str, elevated: bool = False) -> bool:
        """Check if a file or directory exists."""
