# Transactions

## Add Transactions

Transactions describe the behavior of a Service. The Transaction Repository supports HTTP(s) stateless transactions. SOAP over HTTP(s) Transactions are supported as long as you provide the required headers.

In a Transaction, you provide criteria by which a request matches URLs, headers, query parameters, cookies, credentials, or request body, and then a response that the virtual service returns when a match is detected. The Request criteria can be a fully formed request, like a valid GET call, or a regular expression that returns a match for multiple potential requests. To learn more about matching and strategies for creating requests, see [Request Matching Examples](skill-blazemeter-service-virtualization://references/transactions.md).

The easiest way to add Transactions is uploading files in a supported format. You can also manually add and edit Transactions, or record them.

**Use when**: Adding transactions to the repository from files or manually or editing, cloning, configuring request matching examples, nested path formats, and live system endpoints.

### Supported Formats

The following file formats are supported:
- **Swagger 2.0** (JSON and YAML)
- **Swagger 3.0/Open API** (JSON and YAML) - To import multiple Swagger files in a zip file, ensure that the main file in the zip is called `index.json` or `index.yaml`
- **HAR files**
- **RR Pairs** - Upload RR pairs as a zip file with one or more pairs. File formats must follow the *name*-req and *name*-rsp format, where the name string is the same across pairs. For example: `login-req.txt` and `login-rsp.txt`
- **WSDL** (WSDL or zip for multiple files) - To import multiple WSDL files in a zip format, ensure that the main file in the zip is called `index.wsdl`
- **Exported Transactions JSON file** - Created from the export operation from the **Service** drop-down list. To learn more, see [Export Service with all Transactions](skill-blazemeter-service-virtualization://references/management.md)
- **JSON file** created from the BlazeMeter Proxy Recorder
- **WireMock and Mocklab definitions** in JSON format

### Add Transactions from a File

You can add Transactions from a variety of sources. You can edit those Transactions after you import them to tune the matching criteria. To learn more about the Request and Response fields, see [Adding Transactions Manually](skill-blazemeter-service-virtualization://references/transactions.md).

Follow these steps:

1. Log into your BlazeMeter account and click the **Service Virtualization** tab.
2. Click **Asset Catalog**.
3. Drag your file into the upload area, or click the area to browse for the file you want. This file should contain all of the Transactions that you want to use for your virtual service. To upload multiple Swagger files using a zip file, the main file in the zip file must be named `index.json` or `index.yaml`. The Import Transactions dialog opens.
4. Select the Service that you want to add these Transactions to. To create a new Service: Click **Select Service**. Enter the name for your new Service and click **Add Service**.
5. If you want to assign one or more tags to these Transactions, type the tag name(s) in the **Tags** field and press **Enter**. To enter multiple tags, press **Enter** after each tag name.
6. Click **Import**. The Transactions are added to the transaction repository as part of the selected service.

### Edit Transactions

When you import files into the transaction repository, the Transactions in the file are imported exactly as they appear in the file. You will often want or need to make those Transactions more useful by updating the URL to broaden the matching criteria, or duplicate the Transaction to add a similar Transaction that was not available in the file.

**Follow these steps:**

1. In the main menu, navigate to the **Service Virtualization** tab and click **Virtual Services**.
2. Click the Open Details button to expand a virtual service. You can see a list of transactions in your catalog and in the particular virtual service.
3. Click the **Edit Transaction** button next to the transaction that you want to edit. You can edit the transaction in your catalog, as well as in this virtual service.
4. (Optional) If you want to preserve the existing Transaction, you can clone it. See [Clone Transactions](skill-blazemeter-service-virtualization://references/transactions.md).
5. Update **Name**, **Service**, and **Description** as needed.
6. If you want to assign one or more tags to these transactions, type the tag name(s) in the **Tags** field and press **Enter**. To enter multiple tags, press **Enter** after each tag name.
7. In the **Request Matcher** tab, make changes to the existing request data. For example, you can change a direct URL into a regular expression that will match multiple similar requests. Or you can add parameters or other additional matching criteria to a request. To learn more about modifying request data, see [Request Matching Examples](skill-blazemeter-service-virtualization://references/transactions.md).
8. Click **Save**. The updated Transaction is saved and available for adding into a virtual service or Template.

### Clone Transactions

**Follow these steps:**

1. Log into your BlazeMeter account and click the **Service Virtualization** tab.
2. Click the **Asset Catalog** tab.
3. Click the **Transactions** tab.
4. In the **Actions** column, click the **Clone Transactions** button. A duplicate of the Transaction is created.

You can expand the new Transaction and make any required edits there.

### Add Transactions Manually

You can manually add Transactions to the repository to account for Transactions that might not be represented in a file or specification. Cloning a similar Transaction is the simplest way to add a new Transaction without importing, but you can create a Transaction from scratch if a good reference point is not available.

**Follow these steps:**

1. Log into your BlazeMeter account and click the **Service Virtualization** tab.
2. Click **Asset Catalog**.
3. Click the **+** button to **Add Transaction**. The Transaction details page opens.
4. Enter a name for the Transaction in the **Name** field.
5. Select the Service you want to add this Transaction to from the **Service** drop-down. To create a new Service: Click **Select Service**. Enter the name for your new Service and click **Add Service**.
6. If you want to assign one or more tags to these transactions, type the tag name(s) in the **Tags** field and press **Enter**. To enter multiple tags, press **Enter** after each tag name.
7. Enter a **Description** for the Transaction.

**In the Request Matcher tab:**

1. Select the type of Transaction you want to add. The following transaction types are supported: GET, POST, PUT, DELETE, PATCH, OPTIONS, TRACE, HEAD, CONNECT, ANY.
2. Select the proper option on the right of the URL field: Select **Equals** if you are entering a specific URL in the field that you only want to match when that specific request URL is received. Select **Matches regex** if you are entering a URL with regular expression elements that you want to match when the request URL fulfills the regex matching criteria.
3. Enter the URL or regular expression in the **URL** field. If you are editing an imported Transaction, you can change the URL to a regular expression to make the Transaction match against a broader set of requests. For help with URL matching, see [Request Matching Examples](skill-blazemeter-service-virtualization://references/transactions.md).
4. Click **Add** in each of the following tabs to add the details of your Transaction if you want to match against any of these entities in your request: For detailed help and examples, see [Request Matching Examples](skill-blazemeter-service-virtualization://references/transactions.md).
   - **Headers** - As a best practice, avoid using the "host" header in any request matching criteria, as it can adversely affect transaction matching.
   - **Query Parameters**
   - **Cookies**
   - **Credentials**
   - **Body** - equals, equals (case insensitive), contains text, matches regex, does not match regex, is absent, equals to XML, equals to JSON, matches XPath, matches XPath from CDATA, matches JSON Path, WSDL Schema Validation

**In the Response tab:**

1. Select the **Status Code** that the transaction will return with the response when a match occurs.
2. (Optional) Click the **Plus** to add one or more **Conditional Status Code**s. The previously selected default status code will become the **Fallback Status Code**, verify and adjust it if necessary:
   - **Conditional Status Code**: Select a status code that will be returned only when a given condition occurs.
   - **Expression**: Enter a parameter upon which the condition depends.
   - **Operator**: Select a comparison operator for the condition: equals, equals (case insensitive), contains text, matches regex, does not match regex, equals to JSON, matches JSON Path, equals to XML, matches XPath, matches XPath from CDATA, greater than, less than.
   - **Value**: Enter the comparison value.
3. Enter the full response body in the **Body** field.
4. (Optional) Add **Response Headers**. Use the **Edit Wizard** to define [dynamic response values](skill-blazemeter-service-virtualization://references/transactions.md).
5. (Optional) Provide **Proxy URL** values.
6. (Optional) Specify a **Think Time** to simulate realistic delays. To learn more, see [Simulating Irregular Response Latencies (Think Time)](skill-blazemeter-service-virtualization://references/transactions.md).
7. (Optional) Under **Redirect to Live System**, define the URL of your **Live System Endpoint**. All requests that match *this transaction* are conditionally redirected to the specified live system. To learn more about these use cases, see [Live System Endpoint](skill-blazemeter-service-virtualization://references/transactions.md).
8. (Optional) Under **SSL Authentication**, Select an **SSL Authentication**: No Authentication, 1-way SSL, 2-way SSL. Select an existing **Keystore** or upload a new one. Provide the **Keystore Password** and the password used to access individual keys in the keystore. (Optional) To define how to identify during SSL/TLS communication using an alias for a `private key entry` defined in your keystore, select the **Alias** and provide an **Alias Password**.
9. Click **Save**. The Transaction is added to the transaction repository.

### Request Matching Examples

Adding or editing the requests in your Transactions to match against the appropriate range of potential requests that you might use for testing helps make your virtual services powerful and efficient.

This topic includes guidance and examples for entering matching criteria for each one of the request matcher inputs:

#### URL

The URL is the primary request URL. You can format the URL in a variety of ways for matching purposes, including:
- A complete request URL that will only match when the virtual service receives that exact request. Use the Equals setting for this type of request. Any parameters must be entered in the Query Parameters section.
- A partial request URL with regular expression text that will return a match for any request that matches the expression criteria. Use the Matches regex setting for this type of request.
- A complete request URL that serves as the root of a request with parameters or other information that you include in the other matching fields. For example, you can include a root URL, and then enter parameter matching criteria in the Query Parameters section that uses regular expressions.

**Examples:**

The following URL returns a direct match of the AWS S3 API GET request for an object named report.json:

This URL returns a match for a petstore API GET request that includes the string 'dog' in its path:

**Matches:**
- https://petstore.blazemeter.com/api/pets/dogs
- https://petstore.blazemeter.com/api/pets/animals/dog
- https://petstore.blazemeter.com/api/pets/animals/dogs/small

**Does Not Match:**
- https://petstore.blazemeter.com/api/pets/cats
- https://petstore.blazemeter.com/api/pets/Dogs

The RegEx matches are case sensitive.

#### Headers

Use the Headers field to define all headers that must be present to return a match. The header value can be an exact value or a regular expression.

When you define multiple headers, all headers much be present for the request to match. If headers are optional, deselect their **Required** checkbox.

**Example:**

This URL returns a match for a petstore GET request when an `Accept` header is included with the exact value of `application/json`.

#### Query Parameters

Use query parameters to define a range of parameters that will result in a match. You can include multiple parameters, and the parameters can be exact values or regular expressions.

When you define multiple parameters, all parameters much be present for the request to match. If parameters are optional, deselect their **Required** checkbox.

When you use an equals matcher with query parameters, the incoming value is decoded before the comparison is made. Therefore, if you are trying to match on a value that is encoded within a URL, like "`http://notreal/?status=25%25%20full`", use the decoded value in the matcher ("`25% full`") instead of the encoded value in the URL.

**Example 1:**

The example request in the screenshot matches any time when the URL matches the given URL and the `search_criteria` query parameter is present with any value, including an empty value. If the optional `pet` parameter is in the request, its value must match `cat` to match, but if `pet` is not part of the request, then the value `cat` is not considered.

**Example 1 matches:**
- `https://petstore.blazemeter.com/api/pets?search_criteria=brown`
- `https://petstore.blazemeter.com/api/pets?search_criteria=white&pet=cat`
- `https://petstore.blazemeter.com/api/pets?search_criteria`

**Example 1 does not match:**
- `https://petstore.blazemeter.com/api/pets`
- `https://petstore.blazemeter.com/api/pets?pet=dog`
- `https://petstore.blazemeter.com/api/pets?search_criteria=white&pet=dog`
- `https://petstore.blazemeter.com/api/pets?page=1`

**Example 2:**

The second example matches any request when the URL matches the URL and the search_criteria parameter contains the values `white` or `black`, defined through the standard regular expression `(white|black)`.

**Example 2 matches:**
- `https://petstore.blazemeter.com/api/pets?search_criteria=black`
- `https://petstore.blazemeter.com/api/pets?search_criteria=white`

**Example 2 does not match:**
- `https://petstore.blazemeter.com/api/pets?search_criteria=brown`
- `https://petstore.blazemeter.com/api/pets`

**Example 3:**

The third example matches a request that contains the values white or black in the search_criteria query parameter (defined as regular expression) *and* does *not* contain the query parameter `store`.

**Example 3 matches:**
- `https://petstore.blazemeter.com/api/pets?search_criteria=black`
- `https://petstore.blazemeter.com/api/pets?search_criteria=white&page=1`

**Example 3 does not match:**
- `https://petstore.blazemeter.com/api/pets?search_criteria=white&store=london`
- `https://petstore.blazemeter.com/api/pets?store=london`
- `https://petstore.blazemeter.com/api/pets?page=1`

#### Cookies

Include cookies if the request needs to pass certain cookies to return a match.

#### Credentials

Include credentials if the request needs to include specific credentials to return a match.

#### Body

Include body text in the Body section if the request needs to include specific text in the request body to return a match. You can include multiple match conditions that are important to you without having to define the entire request body.

For example, you might include a match condition looking for an XPATH state, and a second match condition looking for a status code in the body. In this scenario, the entire request body doesn't have to match - only the XPATH state and status code that you specified. This is a more efficient method for defining the criteria that matter to you, because if you simply included the entire request body instead, any small deviation in the body content would cause the transaction to not match.

To match the content of XML or JSON documents *semantically*, while ignoring the format, use the **Equals XML** or **Equals JSON** matchers. These matchers ignore whitespace, formatting, and the order of fields. To match JSON or XML fields that contain specific values, while the rest of the fields can have *any value*, use placeholders.

**Examples:**
- Examples of JSON placeholders:`${json-unit.any-string}`, `${json-unit.any-number}`, `${json-unit.ignore}` and [other JSON Unit declarations](https://github.com/lukas-krecan/JsonUnit#typeplc).

The following JSON Body Matcher requires a string match for "name": "John", and accepts any content for the membership and email fields:
```json
{ "name": "John", "membership": "${json-unit.any-string}", "email": "${json-unit.ignore-element}" }
```

- Examples of XML placeholders: `${xmlunit.isNumber}`, `${xmlunit.ignore}` and [other declarations from XML Unit](https://github.com/xmlunit/user-guide/wiki/Placeholders).
- Examples how to add a WSDL schema file (xsd) for validation: Either copy and paste the xsd into the text area. Click the arrow and drag and drop the xsd file into the text area. Click the arrow and upload the xsd file.

To learn more, see [How to Do Advanced Request Matching With BlazeMeter](https://www.blazemeter.com/blog/advanced-request-matching).

---

## Helper Wizards for Request Matching and Dynamic Response Creation

Helper wizards for XPath and JSON Path help you generate XPaths and JSON Paths for request matchers in a transaction so you don't have to enter the path manually. In the request body matcher, define conditions on the request of various types such as XML, JSON, RegEx, matches XPath, matches JSON Path and so on. The helper wizard for responses helps you create dynamic values to pull the information from the request and render it in the response, so you do not have to worry about entering the syntax manually.

**Use when**: Generating XPaths and JSON Paths for request matchers or creating dynamic values in responses without manual syntax entry.

For general information about how to match requests and define responses, see [Adding Transactions](skill-blazemeter-service-virtualization://references/transactions.md).

### Add a Request Matcher Helper to an Existing Transaction

Follow these steps:

1. Go to **Service Virtualization** tab and click **Asset Catalog**
2. In the **Transactions** tab, expand an existing transaction
3. In the **Request Matcher** section, click the **Body** tab
4. Click **+** to define a body matcher
5. Select **matches XPath** or **matches JSON Path**

Use the **Selection Wizard** to define paths. The following procedure is valid for both XML XPath matching and JSON Paths:

1. Click **Selection Wizard**
2. Paste your XML in the **Sample XML** / **Sample JSON** text field
3. Click **Build Tree List**. Under **Nodes Tree List**, a tree-based selector is generated. If you are editing transactions created from a RR-pair import, sample content is automatically taken from the Equals XML or Equals JSON body matchers. The wizard throws an error when the XML is invalid and if it does not follow standards
4. Select the checkboxes of one or more **Nodes** for which you want to generate an XPath or JSON Path. For each selected node, define match type and value
5. From the **Match Type** dropdown, select one of the following options for each selected element:
   - **Specific** - matches the exact element that you provide in the **Match Value** text field
   - **Anything** - verifies only the element's existence in your request. When you select Anything, the wizard disables the **Match Value** field
   - **RegEx** - identifies matching elements by a valid custom regular expression. The input field does not perform any validation, so validate the regex in another tool
6. The **Match Value** column is pre-populated with values that are present in your sample XML. Edit the values as needed
7. (Optional) For each Node, define **Attribute Matching** if applicable:
   - **Match Type**: No Matching, Specific, Anything, Regex. By default, attributes are ignored (No Matching)
   - **Match Value**: The value or regex that the attribute should match
8. (Optional) Enable **Ignore Namespace** to allow matching across namespaces. Example: If enabled, it generates `ElementA/ElementB`. If disabled, it generates `MyNamespace:ElementA/MyNamespace:ElementB`
9. Click **Select** to confirm. The wizard generates an XPath or JSON Path for the matching logic. The sample payload is saved and retained along with the transaction

### Adding Multiple Request Matchers

- You can add more than one request matcher and the request has to pass all the matching conditions to be considered as a match
- You need to paste the sample XML/JSON that is used to display the tree only in the first matcher. The sample carries over to the subsequent matchers so you don't have to paste it again each time
- After you update your sample XML/JSON, any change in the sample XML/JSON is reflected in the other matchers, but it does not update the XPaths and JSON Paths already generated
- After you update your sample XML/JSON, open the wizard again to update your matchers

### Adding Dynamic Values to Responses

The 'Edit Wizard' helps you create dynamic values (Magic Strings) in the response content. Magic strings are basically references to information/data from an incoming request that will be replaced with actual values in the response from the service. The wizard switches automatically between XPath and JSON path based on the type of request body. For all other http related entities, the wizard will generate its appropriate magic strings syntax of the request data.

Follow these steps:

1. Go to **Service Virtualization** tab and click **Asset Catalog**
2. In the **Transactions** tab, expand an existing transaction
3. In the **Response** section, click the **Body** tab
4. Type or paste your response content in the text area. If the content is a valid JSON or XML, an **Edit Wizard** link shows on the right
5. Click the **Edit Wizard** link. A pop-up window with the response content that you entered in the text area shows. The text field contains the original values you entered and an **Expression** button next to each field to set a dynamic value on that field
6. Click the **Expression** button. A detailed subsection displays all the request information that was found in the transaction. This includes Request Body, Request Query Parameters, Request Headers, Request Cookies and Common Parameters
7. Map the request information to the appropriate fields
8. Click **Save**. The original response in the text area is replaced and the magic strings that were generated based on your selection are used

If you have used XPath or JSON expressions to create matchers, the node display is kept in sync with these existing matchers.

### Best Practices for XML Content in Request and Response Wizard

For request matching to work correctly, add element values with special characters in a CDATA section.

Here are some examples of characters that require a CDATA section:
- `"` (double quotes)
- `<` (less than)
- `>` (greater than)
- `&` (ampersand)
- `'` (apostrophe)

An example of how to wrap element values with special characters within CDATA:
```xml
<![CDATA[A & B are equal]]>
```

---

### Nested Path Formats for Request Matchers

Transactions now support a new in-house format of XPath and JSONPath matchers. This format can be used to check if an element matching the XPath or JSONPath matches a specific value or to a Regex so you can use Regular Expressions together with XPath and JSONPath. The structure of this new format looks like:

`[[ PATH, Function ]]`

The only available functions supported right now are "equalTo" (to match a specific value) and "matching" (to evaluate against a Regex).

**Examples:**

**XPath:**
- `[[ /company/employee/name/text(), equalTo(John) ]]` - Finds an element named "John"
- `[[ /company/employee/name/text(), matching(.*)]]` - Finds an element with any name

**JSONPath:**
- `[[ $.company.employee.name, equalTo(John) ]]` - Finds an element named "John"
- `[[ $.company.employee.name, matching(.*)]]` - Finds an element with any name

**Note:** The XPath and JSONPath request wizards have been changed to generate paths according to this new in-house format.

### Return a Response Collection from BlazeMeter Test Data

As a tester who is creating a "GET all" type request as a virtual service transaction, you need to return collections of data.

For example, you have mock data for five accounts. For a "GET account by id" transaction, and for five different IDs in the request, you expect five different responses. And for a transaction "GET all accounts", you expect it to return a collection of all five accounts.

Virtual services use a templating library that supports "with" and "for each" loop constructs.

**To retrieve all users (all rows in a dataset):**
```
{
"users" :
[
${#each (blazeData 'users') as |user|}
{ "id": ${user.id}, "firstname": ${user.firstname}, "lastname": ${user.lastname} }
${#unless @last}, ${/unless}
${/each}
]
}
```

**To retrieve all users with an offset and a limit:**
```
${#with (blazeData 'users' 'skip $request.query.offset' 'limit $request.query.limit') as |dataset|}
${#assign 'totalSize'}${blazeDataSize 'users'}${/assign}
{
"users" :
[
${#each dataset as |user| }
{ "id": "${user.id}", "firstname": "${user.firstname}", "lastname": "${user.lastname}", }
${#unless @last}, ${/unless}
${/each}
],
"pagination" :
{
"total_records": ${totalSize},
"current_page": ${math (math request.query.offset '/' request.query.limit) '+' 1},
"total_pages": ${math totalSize '/' request.query.limit},
"next_page": ${math (math request.query.offset '/' request.query.limit) '+' 2},
"prev_page": ${math request.query.offset '/' request.query.limit}
}
}
${/with}
```

**To show all possible parameters with a limit of 2 and id > 5:**
```
{
"users" :
[
${#each (blazeData 'users' 'limit 2' 'where id > 5' 'skip 2' 'order by lastname desc') as |user|}
{ "firstname": ${user.firstname}, "lastname": ${user.lastname}, }
${#unless @last}, ${/unless}
${/each}
]
}
```

### Live System Endpoint

You cannot or do not want to virtualize 100% of the service, but only the endpoints that you are testing. BlazeMeter offers the possibility to redirect remaining requests to the live service. You can hard-code the name of the Live System endpoint or use dynamic variables in the endpoint definition.

You have two options:

**On virtual service level**, you can redirect all unmatched requests to the live system:
- If you select **Redirect to live system** in the **No Matching Requests** field, a new field **Live System Endpoint** appears. Enter the live URL. The field also supports custom parameters defined in the Configurations tab and in the Test Data pane. The following example uses Configuration parameters: `https://${config.server}:${config.port}`. In the following example, `$(config.host}` is defined on the Configurations tab while `${path}` and `${gvalue}` are Test Data Parameters: `https://${config.host}/${path}/${gvalue}`. From now on, all requests that are not matched by a transaction are forwarded to the endpoint specified.

**On the Transaction level**, you can redirect requests to the live system that match specific Transactions:
- You can use the Request Matchers of Transactions as condition to redirect matching requests to the live system. In the Transaction editor, open the Response tab, and provide the URL of the **Live System Endpoint** on the **Redirect to live system** tab to enable this behavior. The field also accepts test data parameters.
- If you enable **Failover Mode** and the live service fails, the transaction fails gracefully and returns the transaction response.
- You can select an **SSL Authentication**: No Authentication, 1-way SSL, 2-way SSL. Select an existing **Keystore** or upload a new one. Provide the **Keystore Password** and the password used to access individual keys in the keystore. (Optional) To define how to identify during SSL/TLS communication using an alias for a `private key entry` defined in your keystore, select the **Alias** and provide an **Alias Password**.

Enter the URL in the following format:
```
http[s]://<HOST>[:<PORT>][/BASE_PATH]
```

Schema and host are required and everything else is optional.

**Examples:**
- If the **Live System Endpoint** contains value `https://live:5443/ser1`, the incoming request with `https://mock/ping` will be forwarded to `https://live:5443/ser1/ping`.
- If the **Live System Endpoint** contains value `https://live:5443`, the incoming request with `https://mock/ping` will be forwarded to `https://live:5443/ping`.

If needed, provide client certificates when calling live endpoints in virtual services, on transactions level, in webhooks and in HTTP processing actions. Every uploaded certificate is stored in the **Certificate Store** and can be reused later.

---

## Simulate Irregular Response Latencies (Think Time)

One benefit of using virtual services when testing is to introduce irregular behavior that's difficult to get a real web service to produce on demand. A test script rushes through the test steps at the same speed every time, but in BlazeMeter, a transaction can also have a fixed or random-length delay before the response is returned.

BlazeMeter's **Think Time** option introduces a delay that can be used as a factor to simulate slow human responses or network latency. The delay can be a fixed value or can be sampled from a random distribution which makes it easy for you to simulate different types of downstream latencies.

**Use when**: Simulating irregular response latencies, slow human responses, or network latency in virtual services.

### Accessing Think Time

There are several ways how to access the **Think Time** tab to add a delay to a transaction:

- Go to the **Asset Catalog** tab, open the transaction, and edit the **Response Parameters**
- Go to the **Service Virtualization** tab, open a virtual service, and go to the **Parameters** tab

### Think Time Options

For each transaction response, you have the following options:

#### No Delay / Don't use transaction delay

Sets the Think Time to 0 milliseconds. This is the default.

#### Fixed Delay

Lets you define a fixed response delay in milliseconds.

#### Random Uniform Delay

A uniform distribution simulates a stable latency with a fixed amount of jitter.

**Example**: To simulate a stable latency of 20ms +/- 5ms, use lower = 15 and upper = 25.

This option takes two parameters:
- **lower** - The lower bound of the range, inclusive
- **upper** - The upper bound of the range, inclusive

#### Random Lognormal Delay

A lognormal distribution is a pretty good approximation of long-tailed latencies centered on the 50th percentile.

This option takes two parameters:
- **median** - The 50th percentile of latencies
- **sigma** - Standard deviation. The larger the value, the longer the tail

---

## Add Parameter Options and Dynamic Responses

Add parameter options and dynamic responses to transactions to allow for more dynamic, realistic response data. You can reference values in a Transaction request to ensure that they are repeated appropriately in the response body. For example, if your Transaction is requesting a name, you can configure the response to return a random name.

**Use when**: Adding parameter options and dynamic responses to transactions or creating dynamic, realistic response data based on request values.

### Overview

There are two important components to creating dynamic responses:

- The parameters that control which data is returned, often based on request values
- [Helpers](#supported-helper-functions) that control the format of the returned data

### Import Transactions with Dynamic Responses

BlazeMeter supports preserving dynamic data from imported WireMock Transactions. WireMock uses Handlebar helper functions to dynamically generate responses, and BlazeMeter supports those functions. WireMock uses `{{...}}` notation, while BlazeMeter uses `${...}` notation; however, BlazeMeter automatically adjusts the WireMock notation during import.

BlazeMeter also supports dynamic responses from imported RR pairs, as long as they use the supported `${...}` notation.

For other source formats, like HAR, Swagger, and WSDL, import with dynamic responses data is not supported.

### Add Dynamic Responses to a Transaction

When you add dynamic responses to an imported or manually created Transaction, you enrich the response data with information from the request. The referenced information can be either in a query parameter, the request header, a request cookie, or the request body.

Follow these steps:

1. Open a Transaction in the **Asset Catalog**
2. Examine the Request data for potential values you want to parameterize and return in the response
3. Edit the Response Body to reference these values. All dynamic responses must be contained within `${...}` notation. To learn more, see [Dynamic Response Examples](#dynamic-response-examples). If you want to see a static response with a dollar curly bracket symbol (like `${XYZ}`), use the backslash as an escape symbol in the response. For example, if you want to display the response `${xyz}` at runtime, use the syntax `\${xyz}` in the Transaction's response body
4. To return values in the response based on request data, use one of the following helpers:
   - `request.query.<parametername>` - Returns the value of the specified query parameter
   - `request.headers.<headername>` - Returns the value of the specified header. Within the response header, we are only evaluating the Value section. The Name in the header is not part of the dynamic response
   - `request.cookies.<cookieid>` - Returns the value of the specified cookie
   - `request.body` - Returns the full request body
   - Other helpers are available to configure formatting, conditional responses, numeric data, and more. For a list of all available Helpers, see [Supported Helper Functions](#supported-helper-functions)
5. Save the Transaction

You can give certain parameters random values, while others can return an exact value from the request. For example, if a request is asking to create a user account, you can configure the response to return the requested data in the response.

### Dynamic Response Examples

Here are a few simple examples of dynamic response usage:

#### Return Request Query Parameter Values

Consider a marketing system with lead information. You want to return records matching a specific type of lead.

This Transaction looks up leads with a status of HOT:
```
http://localhost:64755/leads?status=HOT
```

The following Transaction response configuration will return response information with the desired status. This configuration sets the status value to whatever you specify in the Transaction.

#### Return Request Header Values

This example uses the Accept request header to send either a JSON or XML response based on the response time:

```json
${#assign "mediaType"}${request.headers.Accept}${/assign}
${#eq mediaType 'application/json'}
{
"users":[
{
"id":1,
"name":"Mario Speedwagon",
"status":"${request.query.status}"
}
]
}
${/eq}
${#eq mediaType 'application/xml'}
<?xml version="1.0" encoding="UTF-8"?>
<root>
<users>
<id>1</id>
<name>Mario Speedwagon</name>
<status>${request.query.status}</status>
</users>
</root>
${/eq}
```

#### User Name Lookup - GET Request

This Transaction looks up a user name based on an ID number. The Request URL in BlazeMeter would look like this:
```
/contact/.*
```

To return a realistic ID and name value in the response, you would add the following to the Response Body. The `request.path` entry tells the response to use the first value in the request path as the value for the id parameter. For the firstName parameter, the dynamic response creates a random alphabetic value of ten characters.

#### Account Creation - POST Request

This Transaction creates an account using a POST request with the required account data. You want the response to return the requested data in the following format:

```json
{
"id" : 3461,
"firstName" : "John" //The first letter should be capital
"lastName" : "DOE" //The whole string should be in upper case
"phone" : "(XXX)-XX-9999" // Only the last 4 digits needs to be visible
}
```

The inputForm argument specifically references the parameters from the request. Each of the three parameters also includes a helper that puts the output in the desired format.

### Supported Helper Functions

Helpers let you control the format, appearance, and other factors related to the output date of a dynamic response. BlazeMeter supports the following helpers:

#### Request Helpers

| Name | Description | Example |
|------|-------------|---------|
| `request.query.<key>` | Returns the value of the query parameter with the specified key | `${request.query.status}` Returns the value of "status" query parameter |
| `request.headers.<key>` | Returns the value of the request header with the specified key | `${request.header.Accept}` Returns the value of the request header "Accept" |
| `request.cookies.<key>` | Returns the value of the cookie with the specified key | `${request.cookies.JSESSIONID}` Returns the value of the request header "JSESSIONID" |
| `request.body` | Returns the value of the body | `${request.body}` Returns the full request body |

#### String Helpers

BlazeMeter supports many string helpers including: `capitalizeFirst`, `center`, `cut`, `defaultlfEmpty`, `join`, `ljust`, `rjust`, `substring`, `lower`, `upper`, `slugify`, `stringFormat`, `stripTags`, `capitalize`, `abbreviate`, `wordWrap`, `replace`, `yesno`, `numberFormat`.

#### Number Helpers

| Name | Description | Example |
|------|-------------|---------|
| `isEven` | Returns a value only if the first argument is even. Otherwise, return null | `${isEven 2 "Hello"}` Returns "Hello" |
| `isOdd` | Returns a value only if the first argument is odd. Otherwise, return null | `${isOdd 3 "World"}` Returns "World" |
| `stripes` | Returns a different value if the passed argument is odd or even | `${stripes 2 "Hello" "World"}` Returns "Hello" |

#### Conditional Helpers

BlazeMeter supports conditional helpers including: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `and`, `or`, `not`.

#### Assign Helpers

| Name | Description | Example |
|------|-------------|---------|
| `assign` | Creates auxiliary variables | `${#assign "title"}Hello World${/assign} ${title}` Returns "Hello World" |

#### WireMock Helpers

BlazeMeter supports WireMock helpers to support import from open source. By default, these helpers use `{{...}}` in WireMock. BlazeMeter automatically fixes imported Transactions to use the supported `${...}` notation, but if you are manually adding these to a Transaction, use the proper BlazeMeter supported notation for them to work.

BlazeMeter supports the following WireMock helpers: `xPath`, `soapXPath`, `jsonPath`, `randomValue`, `hostname`, `date`, `now`, `parseDate`, `trim`, `base64`, `urlEncode`, `formData`, `regexExtract`, `size`.

To learn more about these helpers, see [wiremock.org/docs/response-templating](https://wiremock.org/docs/response-templating/).

#### Response Helper

| Name | Description | Example |
|------|-------------|---------|
| `response.body` | Returns the value that is specified in the Transaction→Response→Body field. Use this helper anywhere in the transactions, including HTTP calls and Webhook calls | Transaction → Response → Body contains `name=${config.myName}`. Use this value in the body of the HTTP call or Webhook call as `${response.body}` |

---

## Add Processing Actions

Add Processing Actions (Webhooks, HTTP Calls, State Update) to transactions for simulating state updates, long-running tasks, and asynchronous requests.

**Use when**: Adding Processing Actions to transactions for simulating state updates, long-running tasks, and asynchronous requests or configuring Webhooks, HTTP Calls, and State Update actions.

### Usage

When do you use processing actions? For example, instead of polling the status of a job submitted to your web service, you want it to report its progress back to a client, once per second, so the client can display a progress bar to the user. The web service sends asynchronous requests to a callback URL of your choice. To simulate similar behaviors in a BlazeMeter virtual service, you configure *Processing Actions*.

- Processing Actions can reference values returned in responses of external services. To learn more, see the [Supported Helper Functions](skill-blazemeter-service-virtualization://references/transactions.md) section
- Processing Actions are optional. If defined, they are triggered after the request is matched, and before the response is sent. The webhook trigger additionally starts a timer
- The supported Processing Actions are Webhook, HTTP Call, and State Update
- You can use the response of a HTTP Call processing action in another processing action (HTTP Call, Webhook, State Update) or as a part of the **Redirect to Live** at the transaction level
- To chain actions, reorder them as needed by dragging the handle on the left side of the Action up or down

If you have defined a proxy on the Service Virtualization level, then its HTTP Actions and Webhooks use the same proxy when making outbound calls. If you do not want those calls to go through the proxy server, add your exceptions in the **No Proxy** section, similar to:
- `www.domain.com`
- `*.domain.com`
- `.domain.com`
- `www.domain.com,.domain2.com,a.domain3.com`

### HTTP Calls

A virtual service can trigger an HTTP request and then use the obtained response in the current transaction response body. The HTTP call is a synchronous call, this means, the virtual service waits for the HTTP call to finish before it sends back the response to the client.

**How to define a HTTP Call Processing Action:**

1. Go to the **Assets Catalog** tab and create or edit a **Transaction**
2. In the **Processing Actions** tab, click the **Plus** button to add one or more **HTTP Call**s
3. Define the HTTP Call:
   - In the **Name** field, give it a descriptive name
   - (Optional) Define one or more **Condition**s. This processing action only triggers if all conditions are true:
     - **Expression**: Enter a property in `${PropertyName}` format
     - **Operator**: Enter a comparison operator: equals, equals (case insensitive), contains text, matches regex, does not match regex, equals to JSON, matches JSON Path, equals to XML, matches XPath, greater than, less than
     - **Value**: Enter the comparison value that triggers the action
   - In the **URL** field, select a method (for example, GET) and define a request URL that returns a response. This field accepts variables configured in the Configurations tab (such as `${config.host}`) as well as Test Data parameters. Example: `https://${config.host}/call/${path}/${value}`
   - (Optional) Select an **SSL Authentication**: No Authentication, 1-way SSL, 2-way SSL. Select an existing **Keystore** or upload a new one. Provide the **Keystore Password** and the password used to access individual keys in the keystore. (Optional) To define how to identify during SSL/TLS communication using an alias for a `private key entry` defined in your keystore, select the **Alias** and provide an **Alias Password**
   - (Optional) Define **Query Parameters**
   - (Optional) Define **Header** values
   - (Optional) Define the **Body** value
4. Click **Save**
5. Use the response value in the transaction response body with the following syntax. Replace myHttpCallname with your HTTP Call's name to distinguish multiple calls. The syntax supports any [handlebar from Wiremock](https://docs.wiremock.io/response-templating/basics/): `${httpcalls.*myHttpCallName*.response.body}`
6. Assign this transaction to a virtual service
7. Run the virtual service and submit the test job to trigger the virtual service

Now you can review the log.

**Considerations:**
- A single transaction can have up to 20 different HTTP Calls associated with it

### Webhooks

**When do I use Think Time and when a webhook?**

The difference is that Think Time sends only the virtual service's *response* with a delay. Using a webhook, the virtual service on its own can schedule sending multiple whole *requests* asynchronously.

**Considerations:**
- A single transaction can have up to 20 different webhook definitions associated with it
- A running virtual service can keep up to 1000 webhook calls scheduled at the same time

**Example Webhook scenario:**

In this sample scenario, an API call submits a job, and the client needs to be informed asynchronously whether the job has been queued, when it has finished or failed, and so on. You want to test whether your system tracks the job status correctly -- therefore you want your virtual service to reflect that same behavior and simulate posting asynchronous reactions at certain intervals.

The overall process looks like this:

1. If the transaction matches, the virtual service responds, "The job was submitted", as usual
2. Five seconds later, the virtual service triggers the "job queued" webhook. The webhook posts the status to the provided callback URL `${request.query.callback_url}`
3. Ten seconds later, the virtual service triggers the "job finished" webhook. The webhook posts to the provided callback URL `${request.query.callback_url}`
4. And so on

**How to define a Webhook Processing Action:**

Typically, you provide the callback URL in a query parameter, in the request body, or in the header of the request that starts a job. It is a good practice to match the callback URL in a transaction to ensure they are present.

1. Go to the **Assets Catalog** tab and create or edit a **Transaction**
2. In the **Request Matcher** tab, include a matcher that ensures that the callback URL is provided. For example, use the **matches regex** operator with a value of "`.+`" on the callback_url parameter to verify that the callback_url value is present and non-empty
3. In the **Response** tab, you can reference values, as usual. For example, you can define the response body as `"Job ${jsonPath request.body '$.job_id'} submitted"`
4. In the **Processing Actions** tab, click the **Plus** button to add one or more webhooks
5. Define the webhook:
   - In the **Name** field, give it a descriptive name
   - In the **Trigger After** field, either specify a constant time in milliseconds, or enable the **Random Delay Between** checkbox and enter a min and max value in milliseconds
   - (Optional) Define one or more **Condition**s. This processing action only triggers if all conditions are true:
     - **Expression**: Enter a property in `${PropertyName}` format
     - **Operator**: Enter a comparison operator: equals, equals (case insensitive), contains text, matches regex, does not match regex, equals to JSON, matches JSON Path, equals to XML, matches XPath, greater than, less than
     - **Value**: Enter the comparison value that triggers the action
   - In the **Callback URL** field, select the method, for example, POST
   - In the **Callback URL** field, define the URL. This field accepts variables configured in the Configurations tab (such as `${config.host}`) as well as Test Data parameters. Example: `https://${config.host}/call/${path}/${value}`
   - (Optional) Select an **SSL Authentication**: No Authentication, 1-way SSL, 2-way SSL. Select an existing **Keystore** or upload a new one. Provide the **Keystore Password** and the password used to access individual keys in the keystore. (Optional) To define how to identify during SSL/TLS communication using an alias for a `private key entry` defined in your keystore, select the **Alias** and provide an **Alias Password**
   - (Optional) Define **Query Parameters**
   - (Optional) Define **Header** values
   - (Optional) Define the **Body** value
6. Click **Save**
7. Assign this transaction to a virtual service
8. Run the virtual service and submit the test job to trigger the virtual service

Now you can review the log.

### State Update

When a transaction matches, a virtual service cannot only return a value, but also modify existing data parameters in your Service Data. This processing action is useful to store a virtual service's state or even, for example, to maintain a global counter as part of a test run. Virtual services that trigger State Updates are marked with a "stateful" tag.

This updated state persists even after you stop and restart your virtual service. To reset the state, *update* your virtual service and then also choose to update your data.

**What is global scope?**

In addition to accessing data parameters in data entities, State Updates can also access data parameters with a global scope. Global data parameters are available to the whole service and are listed in the **Global Scope** section in your **Service Data** pane. You create global parameters by clicking the blue Plus button there.

**How to define a State Update Processing Action:**

You create a State Update processing action inside the transaction that triggers it.

**Follow these steps:**

1. Navigate to the **Service Virtualization** tab, select **Assets Catalog** and select a Service
2. Verify that the Service has Service Data attached. If not, create or load a Data Entity now
3. Create a transaction or open an existing one
4. In the **Processing Actions** tab of the Transaction, click the **Plus** button to add one or more **State Updates**

In the **State Change Definition** window, define which data parameter you want to update:

1. In the **Name** field, give the Processing Action a descriptive name
2. (Optional) Define one or more **Condition**s. This processing action only triggers if all conditions are true:
   - **Expression**: Enter a property in `${PropertyName}` format
   - **Operator**: Enter a comparison operator: equals, equals (case insensitive), contains text, matches regex, does not match regex, equals to JSON, matches JSON Path, equals to XML, matches XPath, greater than, less than
   - **Value**: Enter the comparison value that triggers the action
3. In the **State Change Type** field, select one of the following actions:
   - **Store Object** — If the transaction matches, add a row of values to the data entity. Select a **Data Entity**. Click the **Plus** button to add the **Selected Data Parameters** in which you want to store values. Enter the **Value to Store** to add for the Data Parameter
   - **Update Object** — If the transaction matches, update a specific value in an existing row in the data entity. Select a **Data Entity**. To define which rows of the Data Parameters you want to update, fill in the **Filter by Data Parameter** fields. Select a data parameter column, a comparison operator, and a comparison value. Click the **Plus** button to add the **Selected Data Parameters** in which you want to store values. Enter a **Value to Store** that will overwrite the existing value of the Data Parameter
   - **Delete Object** — If the transaction matches, delete a specific column value in an existing row in the data entity. Select a **Data Entity**. To define which row and column of the Data Parameters you want to delete, fill in the **Filter by Data Parameter** fields. Select a data parameter column, a comparison operator, and a comparison value
   - **Update Value** — If the transaction matches, update a global value. Select or create a global data parameter. Define a **Value**
   - **Increment Value** — If the transaction matches, increment or decrement a global value. Select or create a global data parameter. Enter a positive step value to increment to counter. Enter a negative value to decrement the counter
4. Click **Save**
5. Assign this transaction to a virtual service. The virtual service is marked with a "stateful" tag
6. Run the virtual service and submit the test job to trigger the virtual service

The operator in the **Filter by Data Parameter** fields supports the following comparison for strings and numbers, respectively:
- Equals
- Less than
- Greater than
- Starts With
- Ends With
- In — Returns true if the value matches an item in a list. Provide a comma-separated list of values

### View the Logs

1. Go to the **Service Virtualization** tab
2. Open the virtual service and verify that the transaction is attached
3. Go to the **Analytics** tab
4. On the **Inspection** tab, review the log of incoming requests to the virtual service:
   - Verify that the call was made
   - Verify that the call was matched by the transaction that triggers the Processing Action
   - Verify the response
5. On the respective Processing Action tab, review the logs of the outgoing Processing Actions:
   - Verify which calls were triggered, their method, and URL
   - Verify the time stamps when they were triggered
   - Select an entry to inspect query parameters used, headers, and body value

---

---

## Transaction Repository and Transaction Types

The Asset Catalog tab on the Service Virtualization tab contains all imported Transactions that you can use to create a virtual service.

**Use when**: Understanding the Transaction Repository, transaction types, or working with preconfigured transactions and transaction formats.

### Overview

A Transaction is a request/response pair that is associated with a given Service. For example, in the Swagger Petstore, GET /pet/{petId} and the associated response is a Transaction. A request in a Transaction can be a full, valid request, like the Petstore example, or an expression that can be matched to a broader range of real requests.

You can add transactions [from a file](#add-transactions-from-a-file), [from Wiremock](#share-transactions-between-virtual-services-and-wiremock), or [by adding them manually](#add-transactions-manually). Every time you add a Transaction, it is stored in the Transaction Repository. The Transaction Repository keeps a record of all Transactions and supports a variety of formats. When you create a virtual service, you are simply grouping together Transactions from the repository.

The Transactions tab lists all of the Transactions that are available to you. You can filter the list of Transactions by Service name to make it easier to find the specific Transaction that you're looking for. You can also search for any tags that you assigned to your Transactions, by the Transaction name, or by the request URL.

### Preconfigured Transactions

BlazeMeter comes with four preconfigured groups of Transactions to help illustrate how the product works and to get you started with assets for the following common third-party services:

- **AWS S3**: Provides sample Transactions for testing the AWS S3 cloud storage service. Transactions are included for testing object additions, deletions, copies, searches, and negative scenarios.
- **Facebook Login**: Provides sample Transactions for testing the integrated Facebook login functionality in your application. Transactions include a mixture of positive and negative scenarios, identified by tags, that cover the most common outcomes when attempting a Facebook login.
- **Salesforce Login**: Provides sample transactions for testing the integrated Salesforce login functionality in your application. Transactions include a mixture of positive and negative scenarios, identified by tags, that cover the most common outcomes when attempting an integrated Salesforce login.
- **Open Banking**: Provides sample transactions for testing services in your application that use the standard Open Banking APIs. The Open Banking Sample service includes transactions for a variety of operations, such as loan offers, balance inquiries, and account information. Duplicate these transactions to virtualize testing scenarios for open banking operations.

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Transaction Repository and Transaction Types**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-transaction-repository-transaction-types`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-transaction-repository-transaction-types"]}`

---

## Validation Sandbox

Validate transactions and matchers to ensure they work correctly before deploying virtual services, including testing request matching logic and response generation.

**Use when**: Validating transactions and matchers before deploying virtual services, testing request matching logic, or ensuring response generation works correctly.

### Overview

The Validation Sandbox allows you to test and validate your transactions and matchers before deploying them in a virtual service. This helps ensure that your request matching logic works correctly and that responses are generated as expected.

### Validation Process

1. **Test Request Matching**: Validate that your request matchers correctly identify incoming requests
2. **Test Response Generation**: Verify that responses are generated correctly based on the matching criteria
3. **Test Dynamic Responses**: Ensure that dynamic response generation works as expected
4. **Test Processing Actions**: Validate that processing actions (webhooks, HTTP calls, state updates) execute correctly

### Best Practices

- **Test Before Deploying**: Always validate transactions in the sandbox before deploying them to a virtual service
- **Test Edge Cases**: Test various request scenarios to ensure matchers work correctly
- **Verify Response Format**: Ensure responses match the expected format and structure
- **Test Dynamic Values**: Validate that dynamic values in responses are generated correctly

### Documentation References

For detailed information about validation sandbox, use the BlazeMeter MCP help tools:

**Validation Sandbox**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-validation-sandbox.htm`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-validation-sandbox.htm"]}`

---

## Share Transactions between Virtual Services and Wiremock

You can add stubs from external mocking tools to use those definitions as virtual services in BlazeMeter.

**Use when**: Integrating Wiremock/Mocklab with BlazeMeter Service Virtualization, sharing transactions between tools, or exporting/importing transaction definitions.

The following external tools are supported:

- **Wiremock/Mocklab**: [Wiremock](https://wiremock.org/)

You can integrate Transactions between virtual services and Wiremock in the following ways:

- [Add transactions from Wiremock to the transaction repository by exporting them to a JSON file](#exporting-transactions-to-a-json-file)
- [Add transactions from Wiremock to the transaction repository by uploading them directly from the code](#upload-transactions-to-a-transaction-repository-from-code)
- [Refer to transactions in the transaction repository in your Wiremock code](#reference-transaction-repository-from-code)

### Prerequisites for In-Code Sharing between Virtual Services and Wiremock

To interact with the Transaction repository directly from your Wiremock code, ensure that you meet the following prerequisites.

These prerequisites are not required if you are simply [uploading JSON files exported from Wiremock](#exporting-transactions-to-a-json-file).

#### Wiremock Prerequisites

The Wiremock extension library is required to connect with BlazeMeter virtual services:

**Maven:**
```xml
<repositories>
  <!-- your other repositories -->
  <repository>
    <id>blazemeter</id>
    <name>blazemeter</name>
    <url>http://blazemeter.jfrog.io/artifactory/blazemeter-public/</url>
  </repository>
</repositories>
<dependency>
  <groupId>com.perforce.blazemeter-wiremock-extension</groupId>
  <artifactId>blazemeter-wiremock-extension</artifactId>
  <version>1.0.3</version>
</dependency>
```

**Gradle:**
```gradle
repositories {
  maven {
    url "http://blazemeter.jfrog.io/artifactory/blazemeter-public/"
  }
}
dependencies {
  compile 'com.perforce.blazemeter-wiremock-extension:blazemeter-wiremock-extension:1.0.3'
}
```

Only version 1.0.3 of BlazeMeter-WireMock extension supports ability to upload transactions from code to BlazeMeter Asset Catalog and to download transactions from BlazeMeter Asset Catalog to code.

### Exporting Transactions to a JSON File

Export virtual endpoint definitions from your code into a JSON transaction file, which you can then import into the Transaction Repository through the Service Virtualization UI. Using this method, developers using mocking tools can share the artifacts they created in their code with other team members who can load them into the Service Virtualization UI, augment them as needed, and run them as virtual services hosting the content imported from the code.

**Wiremock code samples:**
```java
public class WiremockExportExampleTest {
  @Rule
  public WireMockRule wireMockRule = new WireMockRule(wireMockConfig().port(8081));
  
  WiremockTxnRepoStore store = new WiremockTxnRepoStore.StoreBuilder()
    .withTestInstance(this)
    .withWireMockServerOrRule(wireMockRule)
    .exportAsDslFile("/tmp/dsl")
    .build();
  
  @Test
  public void wiremockExportExampleTest() {
    stubFor(get(urlEqualTo("/cities"))
      .willReturn(aResponse()
        .withStatus(200)
        .withBody("...cities...")));
    
    /* rest of the test */
  }
}
```

The vanilla Wiremock library lets you export a JSON DSL file using the `WireMock.saveAllMappings();` method. Any file exported using this approach could be imported to Service Virtualization.

After you export the definitions into JSON, you can [add them as Transactions from a file](#add-transactions-from-a-file) to the Transaction Repository.

### Upload Transactions to a Transaction Repository from Code

You can directly upload in-code definitions of virtual endpoints to the Transaction Repository. Once the test with these definitions runs, they are converted from their in-code form into Transaction format and uploaded to the repository.

This is another way that developers using Wiremock can share the artifacts they created in code with other team members, who can use and augment them in the UI as virtual services.

To learn more about the apiKey and apiSecret variables, see [BlazeMeter API Keys](skill-blazemeter-api-reference://references/authentication.md).

**Wiremock code samples:**
```java
@TransactionCloudRepository(
  workspaces = {"Default Workspace"},
  apiKey = "...",
  apiSecret = "...",
  uri = "https://mock.blazemeter.com"
)
public class WiremockUploadExampleTest {
  @Rule
  public WireMockRule wireMockRule = new WireMockRule(wireMockConfig().port(8081));
  
  private WiremockTxnRepoStore store = new WiremockTxnRepoStore.StoreBuilder()
    .withTestInstance(this)
    .withWireMockServerOrRule(wireMockRule)
    .uploadDslToTransactionRepository("Default Workspace", "Default Service")
    .build();
  
  @Test
  public void wiremockUploadExampleTest() {
    stubFor(get(urlEqualTo("/cities"))
      .willReturn(aResponse()
        .withStatus(200)
        .withBody("...cities...")));
    
    /* rest of the test */
  }
}
```

When you use this method, the Transactions included in the test are automatically loaded into the Transaction Repository.

### Reference Transaction Repository from Code

For Transactions that already exist in the Repository, you can reference them directly from the code in your mocking tools. This lets developers use Transaction definitions that other team members created in their code.

To learn more about the apiKey and apiSecret variables, see [BlazeMeter API Keys](skill-blazemeter-api-reference://references/authentication.md).

**Wiremock Code Samples:**
```java
@TransactionCloudRepository(
  workspaces = {"Default Workspace"},
  apiKey = "...",
  apiSecret = "...",
  uri = "https://mock.blazemeter.com"
)
public class WiremockRepoExampleTest {
  @Rule
  public WireMockRule wireMockRule = new WireMockRule(
    wireMockConfig().port(8081));
  
  private WiremockTxnRepoStore store = new WiremockTxnRepoStore.StoreBuilder()
    .withTestInstance(this)
    .withWireMockServerOrRule(wireMockRule)
    .build();
  
  @Test
  public void wiremockRepoExampleTest() {
    // virtualization based on Transactions from Repository
    store.useTransaction("Example transaction", "Default Service");
    /* rest of the test */
  }
}
```

### Documentation References

For detailed information, use the BlazeMeter MCP help tools:

**Share Transactions between Virtual Services and Wiremock**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `mock-service-sharing-transactions-wiremock`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-sharing-transactions-wiremock"]}`

---

## Documentation References

For detailed information about transactions, use the BlazeMeter MCP help tools:

**Transactions**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `mock-service-add-transactions` (add transactions)
  - `mock-service-add-parameter-options-and-dynamic-responses` (parameter options and dynamic responses)
  - `mock-service-add-processing-actions` (processing actions)
  - `mock-service-helper-wizards-request-matching-dynamic-response-creation` (helper wizards)
  - `mock-service-think-time-irregular-response-latency` (think time)
  - `mock-service-transaction-repository-transaction-types` (transaction repository)
  - `mock-service-validation-sandbox.htm` (validation sandbox)
  - `mock-service-sharing-transactions-wiremock` (Wiremock integration)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["mock-service-add-transactions", "mock-service-add-parameter-options-and-dynamic-responses", "mock-service-add-processing-actions", "mock-service-helper-wizards-request-matching-dynamic-response-creation", "mock-service-think-time-irregular-response-latency", "mock-service-transaction-repository-transaction-types", "mock-service-validation-sandbox.htm", "mock-service-sharing-transactions-wiremock"]}`

