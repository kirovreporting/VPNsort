import plistlib
import operator
import sys
import subprocess
import os

try:
    # Receiving list of source files
    files = os.popen("ls ~/Library/Preferences/ByHost/com.apple.networkConnect.*.plist").read().splitlines()
except FileNotFoundError:
    # If there are no files
    print("Seems like you don't have any VPN lists, because you don't have any com.apple.networkConnect.*.plist file in ~/Library/Preferences/Byhost/ directory")
else:
    # For every file:
    for filename in files:
        try:
            print("\nSorting "+filename)
            with open(filename,'rb') as f:
                root = plistlib.load(f)
                f.close()
            print("Making a backup...")
            try:
                subprocess.run(["cp",filename,filename+"_backup"])
            except Exception:
                print("Backup failed, work stopped. Bye!")
                sys.exit()
            else:
                print("Done")
            for key in root:
                root[key].sort(key=operator.itemgetter('UserDefinedName'))
            try:
                with open(filename, 'wb') as fp:
                    plistlib.dump(root, fp)
            except Exception:
                print("Oops, something whong has happened while writing your plist. Restoring from backup...")
                try:
                    subprocess.run(["cp", filename+"_backup", filename])
                except Exception:
                    print("Restoring failed. Please check ~/Library/Preferences/Byhost/ to restore your .plist manually. Bye!")
                    sys.exit()
                else:
                    print("Done. Bye!")
                    sys.exit()
        except plistlib.InvalidFileException:
            print("File you've tried to modify is not plist")
        else:
            print("File "+filename+" sorted")
    print("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Please, relogin and then execute \"killall SystemUIServer -HUP\"\nBye!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n")




