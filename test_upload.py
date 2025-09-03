#!/usr/bin/env python3
import asyncio
import os
import sys
sys.path.append('.')

from config.token import BzmToken
from tools.test_manager import TestManager

test_id = 15008368
file_paths = [
        "/Users/diego/Documents/batch_convertsions/output/ws1/loadrunner_script/loadrunner_script.zip",
        "/Users/diego/Documents/batch_convertsions/output/ws1/loadrunner_script/225dd2a4-e4d3-48c3-811c-ddf9e09c5860_exec.yaml"
    ]
main_script = "/Users/diego/Documents/batch_convertsions/output/ws1/loadrunner_script/225dd2a4-e4d3-48c3-811c-ddf9e09c5860_exec.yaml"

async def test_upload():
    api_key = os.getenv('BLAZEMETER_API_KEY')
    if not api_key:
        print("Please set BLAZEMETER_API_KEY environment variable")
        return
    
    if ':' not in api_key:
        print("API key should be in format: key_id:key_secret")
        return
    
    key_id, key_secret = api_key.split(':', 1)
    token = BzmToken(key_id, key_secret)
    
    print("Checking files:")
    for file_path in file_paths:
        exists = os.path.exists(file_path)
        print(f"  {file_path}: {'EXISTS' if exists else 'NOT FOUND'}")
    
    test_manager = TestManager(token)
    
    try:
        print(f"\nStarting upload for test {test_id}...")
        result = await test_manager.upload_assets(test_id, file_paths, main_script)
        print(f"Upload result: {result}")
    except Exception as e:
        print(f"Error during upload: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_upload())
