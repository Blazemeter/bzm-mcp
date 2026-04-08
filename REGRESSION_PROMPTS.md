# BlazeMeter MCP Server - Regression Test Prompts

A curated set of natural-language prompts designed to trigger **every action of every tool** exposed by the BlazeMeter MCP server. Copy-paste each prompt into your MCP-connected AI assistant to verify that the corresponding tool action is invoked and returns a valid response.

> **Prerequisites**: A valid BlazeMeter API key must be configured. Replace placeholder IDs (`{account_id}`, `{workspace_id}`, etc.) with real values from your account before running.

---

## 1. User (`blazemeter_user`)

### 1.1 read

```
Show me my current BlazeMeter user information, including my default account, workspace, and project.
```

---

## 2. Account (`blazemeter_account`)

### 2.1 read

```
Read the details of my BlazeMeter account with ID {account_id}.
```

### 2.2 list

```
List all my BlazeMeter accounts.
```

---

## 3. Workspace (`blazemeter_workspaces`)

### 3.1 read

```
Get the detailed information for workspace ID {workspace_id}.
```

### 3.2 list

```
List all workspaces in account ID {account_id}.
```

### 3.3 read_locations

```
Show me the available load test locations for workspace ID {workspace_id}.
```

---

## 4. Project (`blazemeter_project`)

### 4.1 read

```
Read the details of project ID {project_id}, including how many tests it has.
```

### 4.2 list

```
List all projects in workspace ID {workspace_id}.
```

---

## 5. Tests (`blazemeter_tests`)

### 5.1 read

```
Read the detailed configuration of test ID {test_id}.
```

### 5.2 create

```
Create a new test called "MCP Regression Test" in project ID {project_id}.
```

### 5.3 list

```
List the first 10 tests in project ID {project_id}.
```

### 5.4 configure_load

```
Configure test ID {test_id} with 50 concurrent users, a 2 minute hold-for duration, and a 1 minute ramp-up using jmeter executor.
```

### 5.5 configure_locations

```
Configure test ID {test_id} to distribute load across two locations: us-east4-a at 50% and us-west1-a at 50%.
```

### 5.6 upload_assets

```
Upload the file /path/to/script.jmx to test ID {test_id} and set it as the main script.
```

### 5.7 delete

```
Delete test ID {test_id}.
```

---

## 6. Execution (`blazemeter_execution`)

### 6.1 start

```
Start a run of test ID {test_id}.
```

### 6.2 read

```
Show me the status and details of execution ID {execution_id}.
```

### 6.3 list

```
List the last 5 executions for test ID {test_id}.
```

### 6.4 read_summary

```
Get the summary report for execution ID {execution_id}.
```

### 6.5 read_errors

```
Show me the error report for execution ID {execution_id}.
```

### 6.6 read_request_stats

```
Get the request statistics report for execution ID {execution_id}.
```

### 6.7 read_all_reports

```
Get all reports (summary, errors, and request stats) for execution ID {execution_id}.
```

### 6.8 read_anomalies_stats

```
Show me the anomaly statistics for execution ID {execution_id}.
```

### 6.9 ai_analysis

```
Trigger an AI analysis for execution ID {execution_id} and tell me the results.
```

---

## 7. Billing (`blazemeter_billing`)

### 7.1 calculate_cost_from_config

```
Calculate the cost for a performance test with 100 concurrent users running for 10 minutes using the virtualUserHours allowance type.
```

---

## 8. Help (`blazemeter_help`)

### 8.1 list_help_categories

```
List all available BlazeMeter help documentation categories.
```

### 8.2 list_help_category_content

```
List all help articles in the "guide" subcategory of the "root_category" category.
```

### 8.3 read_help_info

```
Read the BlazeMeter help article about API keys. Use category "root_category", subcategory "guide", and help ID "api-blazemeter-api-keys".
```

### 8.4 batch

```
In a single call, fetch these two BlazeMeter help articles: "api-blazemeter-api-keys" and "administration-ai-consent", both from category "root_category" and subcategory "guide".
```

---

## 9. Skills (`blazemeter_skills`)

### 9.1 list_skills

```
List all available BlazeMeter skills.
```

### 9.2 read_skill

```
Read the skill definition for "blazemeter-performance-testing".
```

### 9.3 list_skill_resources

```
List all resources available in the "blazemeter-administration" skill.
```

### 9.4 read_skill_resource_uri

```
Read the skill resource at URI "blazemeter-skill-blazemeter-administration://references/ai-consent.md".
```

### 9.5 read_skill_resource_uri_list

```
Read these two skill resources at once: "blazemeter-skill-blazemeter-administration://references/ai-consent.md" and "blazemeter-skill-blazemeter-administration://references/workspaces-projects.md".
```

### 9.6 batch

```
In a single call, list all skills and read the "blazemeter-performance-testing" skill definition.
```

---

## Full Workflow Regression

The following prompt chains an end-to-end workflow across multiple tools. Run it as a single conversation to validate the full hierarchy:

```
1. Show me my BlazeMeter user info.
2. List all my accounts.
3. Pick the first account and list its workspaces.
4. Pick the first workspace and show me its details and available locations.
5. List the projects in that workspace.
6. Pick the first project and list its tests.
7. Read the details of the first test.
8. Calculate the cost if I were to run that test with 50 users for 5 minutes using virtualUserHours allowance.
9. List the last 3 executions for that test.
10. If there's an execution, get all reports for it and trigger an AI analysis.
```
