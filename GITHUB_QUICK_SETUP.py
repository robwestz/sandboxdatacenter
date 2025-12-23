#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Quick Setup - Snabb GitHub-initialisering
Helps set up GitHub repo för Datacenter workspace
"""

import subprocess
import sys
from pathlib import Path

class GitHubSetup:
    """GitHub repository setup helper"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent
        
    def check_git(self) -> bool:
        """Check if git is installed"""
        try:
            result = subprocess.run(["git", "--version"], capture_output=True)
            if result.returncode == 0:
                print("[OK] Git is installed")
                return True
            else:
                print("[FAIL] Git not found")
                return False
        except FileNotFoundError:
            print("[FAIL] Git not installed. Download from https://git-scm.com/")
            return False
    
    def check_gitignore(self) -> bool:
        """Verify .gitignore exists"""
        gitignore = self.workspace / ".gitignore"
        if gitignore.exists():
            print("[OK] .gitignore found")
            return True
        else:
            print("[FAIL] .gitignore missing")
            return False
    
    def initialize_repo(self) -> bool:
        """Initialize git repository"""
        try:
            # Check if already initialized
            git_dir = self.workspace / ".git"
            if git_dir.exists():
                print("[OK] Repository already initialized")
                return True
            
            # Initialize
            result = subprocess.run(
                ["git", "init"],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("[OK] Repository initialized")
                return True
            else:
                print(f"[FAIL] Git init failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            return False
    
    def configure_git(self, name: str = None, email: str = None) -> bool:
        """Configure git user"""
        try:
            if not name:
                name = input("Enter your name: ").strip()
            if not email:
                email = input("Enter your email: ").strip()
            
            # Set user name
            subprocess.run(
                ["git", "config", "user.name", name],
                cwd=self.workspace,
                capture_output=True
            )
            
            # Set user email
            subprocess.run(
                ["git", "config", "user.email", email],
                cwd=self.workspace,
                capture_output=True
            )
            
            print(f"[OK] Configured: {name} <{email}>")
            return True
            
        except Exception as e:
            print(f"[FAIL] Configuration error: {e}")
            return False
    
    def add_remote(self, url: str = None) -> bool:
        """Add GitHub remote"""
        try:
            if not url:
                url = input("Enter GitHub repo URL (https://github.com/username/repo.git): ").strip()
            
            # Check if remote already exists
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                existing_url = result.stdout.strip()
                if existing_url == url:
                    print(f"[OK] Remote already set: {url}")
                    return True
                else:
                    print(f"[INFO] Changing remote from {existing_url} to {url}")
                    subprocess.run(
                        ["git", "remote", "remove", "origin"],
                        cwd=self.workspace,
                        capture_output=True
                    )
            
            # Add remote
            result = subprocess.run(
                ["git", "remote", "add", "origin", url],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"[OK] Remote added: {url}")
                return True
            else:
                print(f"[FAIL] Failed to add remote: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            return False
    
    def stage_files(self) -> bool:
        """Stage files for commit"""
        try:
            result = subprocess.run(
                ["git", "add", "."],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("[OK] Files staged (respecting .gitignore)")
                return True
            else:
                print(f"[FAIL] Failed to stage: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            return False
    
    def show_status(self) -> bool:
        """Show git status"""
        try:
            result = subprocess.run(
                ["git", "status"],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("\n[GIT STATUS]")
                print(result.stdout)
                return True
            else:
                return False
                
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            return False
    
    def run_setup(self):
        """Run complete setup"""
        print("\n" + "=" * 78)
        print("GITHUB SETUP FOR DATACENTER")
        print("=" * 78 + "\n")
        
        # Check prerequisites
        if not self.check_git():
            return False
        
        if not self.check_gitignore():
            print("[WARN] .gitignore not found, but continuing...")
        
        # Initialize repository
        if not self.initialize_repo():
            return False
        
        # Configure git
        if not self.configure_git():
            return False
        
        # Add remote
        if not self.add_remote():
            print("[INFO] Skipping remote setup (can do manually)")
        
        # Stage files
        if not self.stage_files():
            return False
        
        # Show status
        self.show_status()
        
        print("\n" + "=" * 78)
        print("SETUP COMPLETE")
        print("=" * 78 + "\n")
        
        print("Next steps:")
        print("1. Review staged files above (respects .gitignore)")
        print("2. Commit: git commit -m 'Initial commit: Datacenter workspace'")
        print("3. Push: git push -u origin main")
        print("\nOr for quick setup:")
        print("   python GITHUB_QUICK_SETUP.py --commit")
        
        return True


def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GitHub setup for Datacenter")
    parser.add_argument('--commit', action='store_true', help='Auto-commit after setup')
    parser.add_argument('--name', help='Git user name')
    parser.add_argument('--email', help='Git user email')
    parser.add_argument('--repo', help='GitHub repo URL')
    
    args = parser.parse_args()
    
    setup = GitHubSetup()
    
    if not setup.run_setup():
        sys.exit(1)
    
    if args.commit:
        print("\n[INFO] Committing changes...")
        try:
            result = subprocess.run(
                ["git", "commit", "-m", "Initial commit: Datacenter workspace with sandbox system"],
                cwd=setup.workspace,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("[OK] Committed successfully")
                print("\n[INFO] Ready to push!")
                print("Run: git push -u origin main")
            else:
                print(f"[INFO] Nothing to commit (already committed?)")
                
        except Exception as e:
            print(f"[FAIL] Commit failed: {e}")


if __name__ == "__main__":
    main()
