#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SANDBOX EXPORT - Save workspace before sandbox shutdown
Exports entire workspace to a single compressed archive that can be
stored on host and quickly imported in next sandbox session.
"""

import os
import json
import zipfile
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Set
import shutil
import sys
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class SandboxExporter:
    """Export workspace for host storage"""
    
    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path(__file__).parent
        self.ignore_patterns = self._load_ignore_patterns()
        self.export_dir = Path.home() / "Desktop"  # Export to desktop for easy host access
        
    def _load_ignore_patterns(self) -> Set[str]:
        """Load ignore patterns from .sandboxignore"""
        ignore_file = self.workspace_root / ".sandboxignore"
        patterns = set()
        
        if ignore_file.exists():
            with open(ignore_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.add(line)
        
        # Always ignore these
        patterns.update([
            '__pycache__',
            '*.pyc',
            '.git',
            'venv',
            'env',
            '.venv'
        ])
        
        return patterns
    
    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        path_str = str(path.relative_to(self.workspace_root))
        
        for pattern in self.ignore_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                if path_str.startswith(pattern.rstrip('/')):
                    return True
            elif '*' in pattern:
                # Wildcard pattern
                import fnmatch
                if fnmatch.fnmatch(path_str, pattern):
                    return True
            else:
                # Exact match
                if pattern in path_str:
                    return True
        
        return False
    
    def create_manifest(self) -> dict:
        """Create export manifest with metadata"""
        from MEMORY_CORE.memory_manager import get_memory
        
        memory = get_memory()
        
        return {
            "export_timestamp": datetime.now().isoformat(),
            "workspace_root": str(self.workspace_root),
            "workspace_name": self.workspace_root.name,
            "python_version": sys.version,
            "session_id": memory.session_id,
            "export_version": "1.0",
            "host_instructions": {
                "storage": "Store this file somewhere safe on host",
                "restore": "Copy to new sandbox Documents folder and run SANDBOX_IMPORT.py",
                "size_optimized": "Cache and temp files excluded"
            }
        }
    
    def export_workspace(self, output_name: str = None) -> Path:
        """
        Export entire workspace to compressed archive
        
        Returns path to created archive
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not output_name:
            output_name = f"Datacenter_Export_{timestamp}.zip"
        
        output_path = self.export_dir / output_name
        
        print("=" * 78)
        print("SANDBOX WORKSPACE EXPORT")
        print("=" * 78)
        print()
        print("Preparing workspace for host storage...")
        print()
        
        # Save final checkpoint
        print(">>> Creating final checkpoint...")
        try:
            from MEMORY_CORE.memory_manager import get_memory
            memory = get_memory()
            memory.remember("sandbox_export", {
                "timestamp": datetime.now().isoformat(),
                "export_file": output_name
            }, "export")
            print("    OK - Checkpoint saved")
        except Exception as e:
            print(f"    WARNING - Checkpoint warning: {e}")
        
        # Create archive
        print(f"\n>>> Creating archive: {output_name}")
        print(f"    Output: {output_path}")
        print()
        
        files_added = 0
        files_skipped = 0
        total_size = 0
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for root, dirs, files in os.walk(self.workspace_root):
                root_path = Path(root)
                
                # Filter directories
                dirs[:] = [d for d in dirs if not self.should_ignore(root_path / d)]
                
                for file in files:
                    file_path = root_path / file
                    
                    if self.should_ignore(file_path):
                        files_skipped += 1
                        continue
                    
                    try:
                        arcname = file_path.relative_to(self.workspace_root)
                        zipf.write(file_path, arcname)
                        files_added += 1
                        total_size += file_path.stat().st_size
                        
                        if files_added % 50 == 0:
                            print(f"    >>> {files_added} files added...")
                    
                    except Exception as e:
                        print(f"    WARNING - Skipped {file_path.name}: {e}")
                        files_skipped += 1
        
        # Calculate final size
        archive_size = output_path.stat().st_size
        compression_ratio = (1 - archive_size / total_size) * 100 if total_size > 0 else 0
        
        print("\n" + "=" * 78)
        print("EXPORT COMPLETE!")
        print("=" * 78)
        print(f"Archive: {output_path.name}")
        print(f"Location: {output_path.parent}")
        print(f"Files included: {files_added}")
        print(f"Files skipped: {files_skipped}")
        print(f"Original size: {total_size / 1024 / 1024:.1f} MB")
        print(f"Archive size: {archive_size / 1024 / 1024:.1f} MB")
        print(f"Compression: {compression_ratio:.1f}%")
        print()
        print("=" * 78)
        print("NEXT STEPS FOR HOST:")
        print("=" * 78)
        print(f"1. Find file on Desktop: {output_path.name}")
        print("2. Copy to safe location on host computer")
        print("3. In new sandbox: Copy file to Documents folder")
        print("4. Run: python SANDBOX_IMPORT.py")
        print()
        print("File is on your DESKTOP for easy access!")
        print("=" * 78)
        
        return output_path


def main():
    """Main export function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Export workspace for sandbox preservation")
    parser.add_argument('--output', '-o', help='Output filename', default=None)
    parser.add_argument('--quick', '-q', action='store_true', help='Quick export (less compression)')
    
    args = parser.parse_args()
    
    exporter = SandboxExporter()
    archive_path = exporter.export_workspace(args.output)
    
    print(f"\n🎉 Workspace exported successfully!")
    print(f"\n🔐 SHA-256: {calculate_checksum(archive_path)}")


def calculate_checksum(file_path: Path) -> str:
    """Calculate SHA-256 checksum for verification"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()[:16]


if __name__ == "__main__":
    main()
