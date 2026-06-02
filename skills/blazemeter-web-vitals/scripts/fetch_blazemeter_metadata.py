#!/usr/bin/env python3
"""
Fetch BlazeMeter metadata (names) for account, workspace, project, test case, and master IDs.
Updates the execution-metadata.json file with the retrieved names.
"""

import json
import base64
from pathlib import Path
from typing import Dict, Optional
import httpx


class BlazeMeterMetadataFetcher:
    """Fetch metadata from BlazeMeter API."""
    
    def __init__(self, api_id: str, api_secret: str):
        """Initialize with API credentials."""
        self.api_id = api_id
        self.api_secret = api_secret
        self.base_url = "https://a.blazemeter.com/api/v4"
        self.client = httpx.Client(timeout=30.0)
        
        # Create auth header
        auth_string = f"{api_id}:{api_secret}"
        auth_b64 = base64.b64encode(auth_string.encode()).decode()
        self.headers = {"Authorization": f"Basic {auth_b64}"}
    
    def get_account_name(self, account_id: int) -> Optional[str]:
        """Fetch account name by ID."""
        try:
            response = self.client.get(f"{self.base_url}/accounts/{account_id}", headers=self.headers)
            if response.status_code == 200:
                return response.json()["result"].get("name")
        except Exception as e:
            print(f"  ⚠ Error fetching account name: {e}")
        return None
    
    def get_workspace_name(self, workspace_id: int) -> Optional[str]:
        """Fetch workspace name by ID."""
        try:
            response = self.client.get(f"{self.base_url}/workspaces/{workspace_id}", headers=self.headers)
            if response.status_code == 200:
                return response.json()["result"].get("name")
        except Exception as e:
            print(f"  ⚠ Error fetching workspace name: {e}")
        return None
    
    def get_project_name(self, project_id: int) -> Optional[str]:
        """Fetch project name by ID."""
        try:
            response = self.client.get(f"{self.base_url}/projects/{project_id}", headers=self.headers)
            if response.status_code == 200:
                return response.json()["result"].get("name")
        except Exception as e:
            print(f"  ⚠ Error fetching project name: {e}")
        return None
    
    def get_test_name(self, test_id: int) -> Optional[str]:
        """Fetch test (test case) name by ID."""
        try:
            response = self.client.get(f"{self.base_url}/tests/{test_id}", headers=self.headers)
            if response.status_code == 200:
                return response.json()["result"].get("name")
        except Exception as e:
            print(f"  ⚠ Error fetching test name: {e}")
        return None
    
    def get_master_name(self, master_id: int) -> Optional[str]:
        """Fetch master (execution) name by ID."""
        try:
            response = self.client.get(f"{self.base_url}/masters/{master_id}", headers=self.headers)
            if response.status_code == 200:
                return response.json()["result"].get("name")
        except Exception as e:
            print(f"  ⚠ Error fetching master name: {e}")
        return None
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()


def fetch_and_update_metadata(
    execution_dir: str,
    account_id: int,
    workspace_id: int,
    project_id: int,
    test_case_id: int,
    master_id: int,
    api_key_file: str
) -> Dict:
    """
    Fetch BlazeMeter metadata and update execution-metadata.json.
    
    Args:
        execution_dir: Path to the execution directory
        account_id: BlazeMeter account ID
        workspace_id: BlazeMeter workspace ID
        project_id: BlazeMeter project ID
        test_case_id: BlazeMeter test case ID
        master_id: BlazeMeter master (execution) ID
        api_key_file: Path to API key JSON file
    
    Returns:
        Updated metadata dictionary
    """
    # Load API credentials
    with open(api_key_file) as f:
        api_creds = json.load(f)
        api_id = api_creds.get("id")
        api_secret = api_creds.get("secret")
    
    if not api_id or not api_secret:
        raise ValueError("Missing API credentials in api_key_file")
    
    # Initialize fetcher
    fetcher = BlazeMeterMetadataFetcher(api_id, api_secret)
    
    print("📡 Fetching BlazeMeter metadata...")
    
    # Fetch names
    account_name = fetcher.get_account_name(account_id)
    print(f"  ✓ Account: {account_id} → {account_name}")
    
    workspace_name = fetcher.get_workspace_name(workspace_id)
    print(f"  ✓ Workspace: {workspace_id} → {workspace_name}")
    
    project_name = fetcher.get_project_name(project_id)
    print(f"  ✓ Project: {project_id} → {project_name}")
    
    test_name = fetcher.get_test_name(test_case_id)
    print(f"  ✓ Test Case: {test_case_id} → {test_name}")
    
    master_name = fetcher.get_master_name(master_id)
    print(f"  ✓ Master: {master_id} → {master_name}")
    
    fetcher.close()
    
    # Load existing metadata
    metadata_file = Path(execution_dir) / "execution-metadata.json"
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Add names to metadata
    metadata["accountId"] = account_id
    metadata["accountName"] = account_name
    metadata["workspaceId"] = workspace_id
    metadata["workspaceName"] = workspace_name
    metadata["projectId"] = project_id
    metadata["projectName"] = project_name
    metadata["testCaseId"] = test_case_id
    metadata["testCaseName"] = test_name
    metadata["testMasterId"] = master_id
    metadata["testMasterName"] = master_name

    # Derive regions from existing session entries already stored in the metadata
    existing_sessions = metadata.get("sessions", [])
    regions = sorted({s.get("location") for s in existing_sessions if s.get("location")})
    metadata["regions"] = regions

    # Save updated metadata
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✓ Metadata updated: {metadata_file}")
    return metadata


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 7:
        print("Usage: fetch_blazemeter_metadata.py <execution_dir> <account_id> <workspace_id> <project_id> <test_case_id> <master_id> [api_key_file]")
        sys.exit(1)
    
    execution_dir = sys.argv[1]
    account_id = int(sys.argv[2])
    workspace_id = int(sys.argv[3])
    project_id = int(sys.argv[4])
    test_case_id = int(sys.argv[5])
    master_id = int(sys.argv[6])
    api_key_file = sys.argv[7] if len(sys.argv) > 7 else "/Users/wguerrero/bzm-vitals-mcp/api-key.json"
    
    try:
        metadata = fetch_and_update_metadata(
            execution_dir,
            account_id,
            workspace_id,
            project_id,
            test_case_id,
            master_id,
            api_key_file
        )
        print("\n✅ Metadata fetch completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
