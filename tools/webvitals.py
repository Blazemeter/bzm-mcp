import io
import json
import zipfile
import requests
from fastmcp import FastMCP

# Initialize or reference your existing FastMCP instance
mcp = FastMCP("BlazeMeter-MCP")


@mcp.tool()
def gather_web_vitals(master_id: int, api_key: str, api_secret: str) -> str:
    """
    Gathers Web Vitals data from all active sessions assigned to a specific BlazeMeter Master ID.
    Downloads the artifact zip file for each session, extracts 'webvitals.json',
    and renames the content map using the session's geographical execution location.

    Args:
        master_id: The unique ID of the BlazeMeter master report run (e.g., 82160037).
        api_key: Your BlazeMeter API key / username token.
        api_secret: Your BlazeMeter API secret key.
    """
    base_url = "https://a.blazemeter.com/api/v4"
    auth = (api_key, api_secret)

    # Initialize an authorized HTTP session
    session = requests.Session()
    session.auth = auth
    session.headers.update({"Accept": "application/json"})

    results_summary = {}

    try:
        # Step 1: Fetch Master Details to extract associated Session IDs
        master_url = f"{base_url}/masters/{master_id}"
        master_response = session.get(master_url)

        if master_response.status_code != 200:
            return f"Error: Failed to fetch master {master_id}. Status Code: {master_response.status_code}"

        master_data = master_response.json()
        sessions_list = master_data.get("result", {}).get("sessionsId", [])

        if not sessions_list:
            return f"No sessions found linked to Master ID {master_id}."

        # Step 2: Loop over every session discovered in the master suite
        for s_id in sessions_list:
            # A. Query the individual session metadata to find its structural deployment location
            session_meta_url = f"{base_url}/sessions/{s_id}"
            meta_res = session.get(session_meta_url)

            location_name = "unknown-location"
            if meta_res.status_code == 200:
                meta_json = meta_res.json()
                # Safely drill down to find result -> configuration -> location
                location_name = meta_json.get("result", {}).get("configuration", {}).get("location", s_id)

            # B. Call the files endpoint to locate 'artifacts.zip'
            files_url = f"{base_url}/sessions/{s_id}/files"
            files_res = session.get(files_url)

            if files_res.status_code != 200:
                results_summary[s_id] = f"Could not retrieve files catalog (HTTP {files_res.status_code})"
                continue

            files_data = files_res.json()
            all_files = files_data.get("result", {}).get("files", [])

            # Locate the pre-authenticated download link for artifacts.zip
            artifact_link = None
            for file_entry in all_files:
                if file_entry.get("name") == "artifacts.zip":
                    artifact_link = file_entry.get("link")
                    break

            if not artifact_link:
                results_summary[s_id] = f"No 'artifacts.zip' found in this session's artifacts catalog."
                continue

            # C. Download the zip archive completely into system RAM
            zip_download_res = session.get(artifact_link)
            if zip_download_res.status_code != 200:
                results_summary[s_id] = "Failed to download the artifact archive file payload."
                continue

            # D. Extract webvitals.json directly out of the binary memory stream
            try:
                with zipfile.ZipFile(io.BytesIO(zip_download_res.content)) as z:
                    # Look for the webvitals file inside the root of the archive file tree
                    if "webvitals.json" in z.namelist():
                        with z.open("webvitals.json") as f:
                            raw_vitals_content = f.read().decode("utf-8")
                            parsed_json = json.loads(raw_vitals_content)

                            # Map the data payload using the target geographical location key
                            labeled_key = f"webvitals_{location_name}.json"
                            results_summary[labeled_key] = parsed_json
                    else:
                        results_summary[s_id] = f"Target 'webvitals.json' file is missing inside artifacts.zip."
            except zipfile.BadZipFile:
                results_summary[s_id] = "Downloaded artifacts archive file was corrupted or incomplete."
            except json.JSONDecodeError:
                results_summary[s_id] = "Extracted webvitals.json payload contains unparsable text formats."

        # Return the aggregated JSON payload back to the Model Context Protocol Client
        return json.dumps({
            "master_id": master_id,
            "status": "completed",
            "extracted_vitals": results_summary
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"An unhandled execution error occurred while mapping web vitals: {str(e)}"
        })