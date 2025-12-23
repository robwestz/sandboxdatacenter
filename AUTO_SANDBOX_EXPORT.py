#!/usr/bin/env python3
"""
⏰ AUTO SANDBOX EXPORT - Automatic export before shutdown
Monitors system and triggers export when sandbox is about to close.
Can also be scheduled to run periodically.
"""

import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import threading
import signal

class AutoExporter:
    """Automatic workspace export system"""
    
    def __init__(self, interval_minutes: int = 30):
        self.interval_minutes = interval_minutes
        self.running = False
        self.last_export = None
        self.export_count = 0
        
    def export_now(self, reason: str = "manual") -> bool:
        """Trigger export immediately"""
        print(f"\n⏰ Auto-export triggered: {reason}")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            result = subprocess.run(
                [sys.executable, "SANDBOX_EXPORT.py"],
                cwd=Path(__file__).parent,
                capture_output=False,
                timeout=300
            )
            
            if result.returncode == 0:
                self.last_export = datetime.now()
                self.export_count += 1
                print(f"   ✅ Export #{self.export_count} completed")
                return True
            else:
                print(f"   ❌ Export failed with code {result.returncode}")
                return False
                
        except Exception as e:
            print(f"   ❌ Export error: {e}")
            return False
    
    def watch_mode(self):
        """Watch mode - export at intervals"""
        print("╔══════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                          ║")
        print("║                  ⏰ AUTO SANDBOX EXPORT - WATCH MODE ⏰                  ║")
        print("║                                                                          ║")
        print(f"║              Exporting every {self.interval_minutes} minutes                          ║")
        print("║                                                                          ║")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        print()
        print("💡 This will keep your workspace backed up automatically")
        print(f"📊 Export interval: {self.interval_minutes} minutes")
        print("⌨️  Press Ctrl+C to stop")
        print()
        
        self.running = True
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            while self.running:
                # Wait for interval
                for i in range(self.interval_minutes * 60):
                    if not self.running:
                        break
                    time.sleep(1)
                    
                    # Show countdown every minute
                    remaining = (self.interval_minutes * 60 - i) // 60
                    if i > 0 and i % 60 == 0:
                        print(f"   ⏳ Next export in {remaining} minutes...", end='\r')
                
                if self.running:
                    print()  # New line before export
                    self.export_now("scheduled")
                    
        except KeyboardInterrupt:
            print("\n\n⏸️  Watch mode stopped by user")
            self.shutdown()
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n\n🛑 Received signal {signum}")
        self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown with final export"""
        print("="*78)
        print("🛑 SHUTTING DOWN - FINAL EXPORT")
        print("="*78)
        
        self.running = False
        
        # Do final export
        success = self.export_now("shutdown")
        
        if success:
            print("\n✅ Workspace safely backed up!")
            print("💾 Archive is on Desktop - save to host!")
        else:
            print("\n⚠️  Final export failed - try manual export")
            print("   Run: python SANDBOX_EXPORT.py")
        
        print("\n👋 Goodbye! Your work is preserved.")
        sys.exit(0)


def main():
    """Main auto-export function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automatic sandbox export")
    parser.add_argument('--watch', '-w', action='store_true', 
                       help='Watch mode - export at regular intervals')
    parser.add_argument('--interval', '-i', type=int, default=30,
                       help='Export interval in minutes (default: 30)')
    parser.add_argument('--now', '-n', action='store_true',
                       help='Export immediately and exit')
    
    args = parser.parse_args()
    
    exporter = AutoExporter(interval_minutes=args.interval)
    
    if args.now:
        # Single export
        success = exporter.export_now("manual")
        sys.exit(0 if success else 1)
    
    elif args.watch:
        # Watch mode
        exporter.watch_mode()
    
    else:
        # Show usage
        print("⏰ AUTO SANDBOX EXPORT")
        print()
        print("Usage:")
        print("  python AUTO_SANDBOX_EXPORT.py --now          # Export now")
        print("  python AUTO_SANDBOX_EXPORT.py --watch        # Watch mode (30 min)")
        print("  python AUTO_SANDBOX_EXPORT.py --watch -i 15  # Watch mode (15 min)")
        print()
        print("💡 Tip: Run in watch mode in a separate terminal")
        print("        Your workspace will be auto-saved!")


if __name__ == "__main__":
    main()
