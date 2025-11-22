#!/usr/bin/env python
"""
Debug script to run effects_INC.py and show full traceback
"""
import os
import django
import traceback
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tg.settings')
django.setup()

try:
    # Import and run the effects script
    print("Running effects_INC.py...")
    with open('populate_db/effects_INC.py') as f:
        code = compile(f.read(), 'populate_db/effects_INC.py', 'exec')
        exec(code)
    print("Script completed successfully!")
except Exception as e:
    print("\n" + "="*70)
    print("ERROR FOUND:")
    print("="*70)
    print(f"\nError Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print("\nFull Traceback:")
    print("-"*70)
    traceback.print_exc()
    print("-"*70)

    # Try to extract the line number from the traceback
    tb = sys.exc_info()[2]
    while tb.tb_next:
        frame = tb.tb_frame
        if 'effects_INC.py' in frame.f_code.co_filename:
            print(f"\n>>> Error occurs at line {tb.tb_lineno} in effects_INC.py")
            print(f">>> In context: {frame.f_code.co_name}")
        tb = tb.tb_next

    sys.exit(1)
