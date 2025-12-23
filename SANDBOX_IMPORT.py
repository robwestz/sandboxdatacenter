#!/usr/bin/env python3
"""
🚀 SANDBOX IMPORT - Restore workspace in new sandbox session
Extracts workspace from archive and resumes exactly where you left off.
"""

import os
import json
import zipfile
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional
import sys
import subprocess

class SandboxImporter:
    """Import and restore workspace from archive"""
    
    def __init__(self, target_root: Path = None):
        self.target_root = target_root or Path(__file__).parent
        self.temp_manifest = None
        
    def find_archive(self) -> Optional[Path]:
        """Find most recent export archive"""
        # Check current directory
        archives = list(Path.cwd().glob("Datacenter_Export_*.zip"))
        
        # Check Documents folder
        docs = Path.home() / "Documents"
        archives.extend(docs.glob("Datacenter_Export_*.zip"))
        
        # Check Desktop
        desktop = Path.home() / "Desktop"
        archives.extend(desktop.glob("Datacenter_Export_*.zip"))
        
        if not archives:
            return None
        
        # Return most recent
        return max(archives, key=lambda p: p.stat().st_mtime)
    
    def verify_archive(self, archive_path: Path) -> bool:
        """Verify archive integrity"""
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                # Check if archive is valid
                bad_file = zipf.testzip()
                if bad_file:
                    print(f"❌ Corrupt file in archive: {bad_file}")
                    return False
                
                # Check for manifest
                if '.sandbox_manifest.json' not in zipf.namelist():
                    print("⚠️  No manifest found - archive may be incomplete")
                    return True  # Continue anyway
                
                return True
        except zipfile.BadZipFile:
            print("❌ Archive is corrupted or not a valid zip file")
            return False
    
    def import_workspace(self, archive_path: Path = None, force: bool = False) -> bool:
        """
        Import workspace from archive
        
        Args:
            archive_path: Path to archive file (auto-detected if None)
            force: Force import even if target exists
        
        Returns:
            True if successful
        """
        print("╔══════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                          ║")
        print("║                     🚀 SANDBOX WORKSPACE IMPORT 🚀                      ║")
        print("║                                                                          ║")
        print("║                Restoring workspace from previous session...             ║")
        print("║                                                                          ║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        print()
        
        # Find archive
        if not archive_path:
            print("🔍 Searching for export archive...")
            archive_path = self.find_archive()
            
            if not archive_path:
                print("❌ No export archive found!")
                print("\n📋 Please:")
                print("   1. Copy Datacenter_Export_*.zip to this folder")
                print("   2. Run: python SANDBOX_IMPORT.py path/to/archive.zip")
                return False
            
            print(f"   ✅ Found: {archive_path.name}")
        
        archive_path = Path(archive_path)
        
        if not archive_path.exists():
            print(f"❌ Archive not found: {archive_path}")
            return False
        
        # Verify archive
        print("\n🔐 Verifying archive integrity...")
        if not self.verify_archive(archive_path):
            return False
        print("   ✅ Archive is valid")
        
        # Check if target already has content
        if list(self.target_root.glob("*")) and not force:
            print("\n⚠️  Target directory already has content!")
            response = input("   Continue and merge? (y/N): ")
            if response.lower() != 'y':
                print("   Import cancelled")
                return False
        
        # Extract archive
        print(f"\n📦 Extracting to: {self.target_root}")
        files_extracted = 0
        
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            members = zipf.namelist()
            total_files = len(members)
            
            for i, member in enumerate(members, 1):
                zipf.extract(member, self.target_root)
                files_extracted += 1
                
                if i % 50 == 0:
                    progress = (i / total_files) * 100
                    print(f"   📄 Extracting: {progress:.0f}% ({i}/{total_files})", end='\r')
        
        print(f"\n   ✅ Extracted {files_extracted} files")
        
        # Load manifest
        manifest_path = self.target_root / ".sandbox_manifest.json"
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
                self.temp_manifest = manifest
                
            print(f"\n📋 Restored from session:")
            print(f"   Timestamp: {manifest.get('export_timestamp', 'unknown')}")
            print(f"   Session ID: {manifest.get('session_id', 'unknown')}")
        
        # Restore Python environment
        print("\n🐍 Setting up Python environment...")
        self.restore_environment()
        
        # Activate memory system
        print("\n🧠 Activating memory system...")
        self.activate_memory()
        
        print("\n" + "="*78)
        print("✅ IMPORT COMPLETE!")
        print("="*78)
        print("🎉 Workspace restored successfully!")
        print()
        print("📋 NEXT STEPS:")
        print("="*78)
        print("1. Verify memory: python TEST_MEMORY.py")
        print("2. Activate system: python ACTIVATE_MEMORY.py")
        print("3. Continue working where you left off!")
        print()
        print("💡 Your workspace is ready - all context preserved!")
        print("="*78)
        
        return True
    
    def restore_environment(self):
        """Restore Python environment"""
        requirements = self.target_root / "requirements.txt"
        
        if requirements.exists():
            print("   📦 Installing dependencies...")
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(requirements), "-q"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    print("   ✅ Dependencies installed")
                else:
                    print("   ⚠️  Some dependencies may have failed")
                    if result.stderr:
                        print(f"   Error: {result.stderr[:200]}")
            except subprocess.TimeoutExpired:
                print("   ⚠️  Installation timed out (you can install manually)")
            except Exception as e:
                print(f"   ⚠️  Could not auto-install: {e}")
                print(f"   Run manually: pip install -r requirements.txt")
        else:
            print("   ⚠️  No requirements.txt found")
    
    def activate_memory(self):
        """Activate memory system"""
        activate_script = self.target_root / "ACTIVATE_MEMORY.py"
        
        if activate_script.exists():
            try:
                # Just verify it exists, don't run yet
                print("   ✅ Memory system ready")
                print("   Run: python ACTIVATE_MEMORY.py")
            except Exception as e:
                print(f"   ⚠️  Memory system: {e}")
        else:
            print("   ⚠️  ACTIVATE_MEMORY.py not found")


def main():
    """Main import function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Import workspace from sandbox export")
    parser.add_argument('archive', nargs='?', help='Path to export archive', default=None)
    parser.add_argument('--force', '-f', action='store_true', help='Force import over existing content')
    parser.add_argument('--target', '-t', help='Target directory', default=None)
    
    args = parser.parse_args()
    
    target = Path(args.target) if args.target else None
    importer = SandboxImporter(target)
    
    success = importer.import_workspace(args.archive, args.force)
    
    if success:
        print("\n🎊 Ready to continue your work!")
    else:
        print("\n💡 Import failed - check errors above")
        sys.exit(1)


if __name__ == "__main__":
    main()
