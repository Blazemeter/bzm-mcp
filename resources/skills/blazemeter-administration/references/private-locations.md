# Private Locations Management

## Administration Manage Private Locations

Manage private locations across workspaces as an account admin, including sharing, unsharing, and deleting private locations, with validation for tests using those locations. As an Account Admin, you can manage all the Private Locations in your BlazeMeter account. Viewing all your Private Locations in one place allows you to optimize the use of your resources, by sharing and unsharing Private Locations across Workspaces. Additionally, you can permanently delete Private Locations within your account.

**Use when**: Managing private locations across workspaces as an account admin or when sharing, unsharing, and deleting private locations with validation for tests using those locations.

### Access Account-Level Private Location Management

Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**. To view the details of private locations in your account, navigate to **Settings > Account > Locations Manager > Private Locations**.

### Share Private Locations

To share a Private Location with other workspaces within your account, follow these steps:

1. Log into your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings > Account > Locations Manager**. A list of all Private Locations in your account appears. You can search and filter Private Locations by name
4. Select a Private Location, then click the share icon. A list of available workspaces displays
5. Select one or more workspaces, then click **Share with (n) Workspaces** (where n = number of workspaces selected)

All the existing shared Workspaces will be marked in the table as Shared. In addition, the calculation of n includes all Workspaces that will be shared. If a Workspace is already shared, it cannot be selected but it will be included in the total number of shared workspaces (n).

**Result:** The selected workspaces are added to the selected Private Location on the **Private Locations** page.

### Unshare Private Locations

To unshare a Private Location from Workspaces, follow these steps:

1. Log into your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings > Account > Private Locations**. A list of all Private Locations in your account appears. You can search or filter Private Locations by name. By default, the **Private Location** page displays up to five Workspace names in a private location table row. If more than five Workspaces are shared with a Private Location, a link appears on the right indicating the number of shared workspaces that are hidden (not shown)
4. To unshare, do one of the following:
   - Click the X icon next to a Workspace name
   - Click either an **(n) more** link (where n = number of hidden workspaces) or an **Unshare** button. A list of all the shared Workspaces displays. Select one or more Workspaces, then click **Remove share from (n) Workspaces** (where n = number of workspaces selected)

If the selected private locations are assigned to tests configured in one or more of the selected Workspaces, the following message displays:

*Before you can unshare, you first need to reconfigure the tests assigned to the selected Private Location to run in alternative locations.*

To do that, follow these steps:

1. Click **Show me a list of tests that are using this Private Location**. The **Advanced Search** page opens with a list of tests that are using the selected Private Location
2. Click the name of the relevant test(s) and scroll down to **Locations**
3. Change the location(s) as needed
4. Return to the Private Location page and repeat step 3

**Result:** The selected workspaces are unshared from the selected Private Location on the **Private Locations** page.

### Delete Private Locations

You can delete Private Locations whether they are shared or unshared.

To delete a private location, follow these steps:

1. Log into your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings > Account > Private Locations**. A list of all Private Locations in your account appears. You can search or filter private locations by name
4. Select a private location row
5. Click the trash can icon on the right of the selected private location row. A popup displays
6. Click **Delete**. The selected private location is permanently deleted

If the selected private locations are assigned to tests configured in the selected workspaces, the following message displays:

*Before you can delete, you first need to reconfigure the tests assigned to the selected Private Location to run in alternative locations.*

1. Click **Show me a list of tests that are using this Private Location**. The **Advanced Search** page opens with a list of tests that are using the selected Private Location
2. Click the name of the relevant test(s) and scroll down to **Locations**
3. Change the location(s) as needed
4. Return to the Private Location page and click Delete

**Important:** This action *does not* delete an installed agent. To manually delete an agent, see [Removing an Agent](https://help.blazemeter.com/docs/guide/private-locations-remove-agent.html).

**Note**: Sharing private locations across workspaces allows centralized management and resource optimization. Account administrators can ensure consistent testing infrastructure across multiple workspaces while maintaining proper access control.

---

## Administration Manage Cloud Providers

As an Account Admin, you can manage the cloud providers for each workspace in your BlazeMeter account. Viewing all your cloud providers lets you optimize the use of your resources, by enabling or disabling cloud providers across Workspaces.

BlazeMeter allows you to simulate virtual user traffic from various global locations. This feature promotes easy scalability, allowing testers to simulate thousands or even millions of users effortlessly. It also lets you conduct testing from multiple cloud servers strategically located worldwide to identify potential performance bottlenecks specific to certain regions.

By default, all workspaces can use all cloud locations.

**Use when**: Managing cloud providers for workspaces as an account admin or when enabling or disabling cloud providers across workspaces to optimize resource usage.

### View Cloud Providers

1. Log in to your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings > Account** and click **Locations Manager**
4. Click **Cloud Providers**. The **Cloud Providers** list displays

Access the **Cloud Providers** list is where you can search for workspaces, filter to show all/all that are disabled/all enabled, and click to enable/disable cloud locations for these workspaces.

### Enable or Disable Cloud Providers

To enable or disable cloud providers per workspace, follow these steps:

1. Log into your BlazeMeter account
2. Click the **Cog** icon at the top right of the BlazeMeter UI to open the **Settings**
3. Navigate to **Settings > Account > Location Manager**
4. Click **Cloud Providers**. The **Cloud Providers** list opens
5. In the required table row, click the **Edit** button
6. Select the **Enabled** or **Disabled** options for the listed workspaces as needed

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Administration Manage Cloud Providers**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-manage-cloud-locations.html.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-manage-cloud-locations.html.htm"]}`

**Administration Manage Private Locations**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `administration-manage-private-locations`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["administration-manage-private-locations"]}`

