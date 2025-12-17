# Test Action Library

## Test Action Library

Manage shared Objects, Group Actions, and Actions in the Test Action Library for GUI Functional and Browser Performance tests.

**Use when**: Managing shared Objects, Group Actions, and Actions in the Test Action Library or reusing test components across multiple tests.

### Overview

The Test Action Library is where you store predefined Group Actions and Objects for GUI Functional and Browser Performance scenarios. You can create a GUI Functional test or a Browser Performance Test by dragging and dropping predefined Actions into a Test Scenario. This *scriptless* testing approach is the preferred method for testers who do not want to write scripts manually.

For more information about how to create Actions and Objects, see [Creating Scriptless GUI Functional Tests](https://help.blazemeter.com/docs/guide/functional-create-scriptless-test.html).

### What are Objects, Actions, and Group Actions?

- **Actions** are user interactions such as "click", "select", or "type". The Test Action Library does not contain Actions because they are a fixed set that cannot be edited. For the full list of Actions, see [Taurus Actions for GUI Functional Testing](https://help.blazemeter.com/docs/guide/functional-taurus-actions-scriptless.html).
- **Group Actions** are your custom sets of test actions that commonly occur together in your test scenarios. For example, you can define a Group Action that contains the common sequence of Actions of going to the login page, typing user name and password, and clicking submit. Group Actions are shared with your workspace. You manage your Group Actions in the Test Action Library.
- **Objects** are the GUI elements of the application under test, such as buttons or text fields, to which you apply test actions. Objects are defined by one or more locators. If the first locator is not found, BlazeMeter tries the other locators. Edit the object to reorder the priority of its locators. BlazeMeter generates default names for new Objects based on their locators. If an Object name already exists, BlazeMeter appends an incrementally numbered suffix, such as "`Object [CSS: input[name=\"q\"]; Name: q](2)`". Objects are shared with your workspace. You manage Objects in the Test Action Library.

**Note**: Group Actions are shared with your workspace. You manage your Group Actions in the Test Action Library. Objects are shared with your workspace. You manage Objects in the Test Action Library.

---

## Management

Manage shared Objects and Group Actions in the Test Action Library, including editing, deleting, finding usages, and organizing reusable test components.

**Use when**: Managing shared Objects and Group Actions in the Test Action Library or editing, deleting, finding usages, and organizing reusable test components.

### How to Edit Shared Objects, Actions, and Group Actions?

You cannot edit [Actions](https://help.blazemeter.com/docs/guide/functional-taurus-actions-scriptless.html) because they are a fixed set.

Before editing Group Actions or Objects, you want to identify where these shared resources are used, so you can estimate the impact of your changes:

1. Go to the Test Action Library.
2. Search the Test Action Library for specific Group Actions or Objects. Click the Filter button to only show rows that fulfil criteria such as Type, Created or Updated date range, Created by user, Updated by user, Created from URL, or Test Name. Click the table headings to sort the table by criteria such as Name, Type, Base URL, Usage (in how many tests is this shared Object or Group being used?), Created date, Created by user, or Last Updated date.
3. Expand the Group Action or Object to see more details. For each Group Action, you can view the contained Actions and their default values. For each Object, you see a screenshot and its locator, so you can easily recognize it. For all entries, you see the list of affected scenarios that use this Group Action or Object.

**To edit an Object:**

1. Find and expand the Object in the Test Action Library.
2. Open a scenario that uses the Object in the Scenario Editor.
3. Edit the Object locators. You have the following options:
   - **Replace the Object**: Enable the Object Picker. Switch to the application under test in the same browser. Select a UI element to create an object or to reuse an existing object from the library.
   - **Update Object locators**: Open the Object dropdown. Hover the pointer over the Object and click Edit. The Edit Object dialog opens. Edit the object's locators manually. Inside the Edit Object Dialog, enable the Object Picker, switch to the application under test, and select a UI element to update existing locators quickly.
4. Debug-run your test to verify that your changes work.
5. If the Object is used in more than one scenario, debug-run the other scenarios as well to verify the changes.

**Note**: For each Object, you see a screenshot and its locator, so you can easily recognize it. For all entries, you see the list of affected scenarios that use this Group Action or Object.

**To edit a Group Action:**

1. Find and expand the Group Action in the Test Action Library.
2. Open a scenario that uses the Group Action.
3. Edit the Group Action in the Scenario Editor. The changes are saved locally.
4. Debug-run your test to verify that your changes work.
5. (Optional) Click **Override Group Action**. BlazeMeter saves your changes to the Test Action Library and updates the Group in other tests that reuse it.

**Note**: For each Group Action, you can view the contained Actions and their default values. The changes are saved locally until you click **Override Group Action**.

### How to Delete an Object or Group Action?

The Delete button is only available for Objects and Group Actions that are not used in any scenarios.

1. Find and expand the item in the Test Action Library.
2. If the **Usage** value is larger than zero, open each scenario in the Scenario Editor and remove the item.
3. As soon as the **Usage** value for the item is zero, the **Delete** button becomes available in the Test Action Library.

---

## Custom JavaScript Actions

The [Scriptless Scenario Editor](skill-blazemeter-functional-testing://references/gui-tests.md) supports several [actions](https://help.blazemeter.com/docs/guide/functional-taurus-actions-scriptless.html) which you as a developer can use to execute custom JavaScript code snippets in your GUI Functional Tests:

- **Assert Eval** action
- **Script Eval** action
- **Store Eval** action

The option to execute custom JavaScript code during a test makes Scriptless Testing very extensible and lets advanced users overcome limitations that a purely "scriptless" approach might bring.

All Taurus actions also support `${Taurus Variables}` that you can reference directly in your JavaScript code.

**Use when**: Implementing custom JavaScript actions for scriptless testing, executing custom JavaScript code snippets in GUI Functional Tests, or extending scriptless testing capabilities with advanced JavaScript functionality.

### Data Types and Return Statements

All of the actions available in Scriptless GUI Functional Tests run in the context of the web page you are testing, and you can access the `document` of the page in order to perform operations. For more information, see [JS Document, W3C Schools](https://www.w3schools.com/js/js_htmldom_document.asp).

Write actions that are wrapped with a return statement by using immediately invoked function expressions (IIFE).

```javascript
(function() {
  // Code goes here...
})();
```

IIFEs are a very basic wrapper that create the function and call it right away. The inner function in this example can contain a return statement that is properly handled, and the returned result is propagated.

#### How Data Types Are Resolved

By default, variables in scripting actions are either of type number or string. In the following example, you use the `storeEval` action to save the number 5 in a variable named `sum`.

Depending on how you use this variable `sum`, its type is resolved differently. For example, if you use it in a string context:

```
'${sum}' + ' items'
```

then, after expansion, the variable resolves to a string:

```
'5' + ' items'
```

In this case, the strings are concatenated using the plus operator to `'5 items'`.

On the other hand, if you have a numeric context:

```
${sum} + 10
```

then, after expansion, the variable resolves to a number:

```
5 + 10
```

And the numbers are added using the plus operator, resulting in `15`.

The same type resolution rule applies to comparison operators.

#### Working With Complex Data Types

In BlazeMeter, there is no complex data type, instead you serialize JSON data into a string, and then deserialize it back in another code snippet. In this example, you have used the `storeEval` action to create the variable `person`, and you serialize the array using the following script:

```javascript
(function() {
  const person = {name: 'John', surname: 'Doe'};
  return JSON.stringify(person);
})();
```

Later on, you can deserialize the data and use the array fields in another action:

```javascript
(function() {
  const person = JSON.parse('${person}');
  console.log(person.name); // Will print 'John'
  console.log(person.surname); // Will print 'Doe'
})();
```

### JavaScript Actions

#### ScriptEval

**Description:**

ScriptEval is the basic action for running custom JavaScript code. The action does not return a value. You can consider it equivalent to returning 'void' in programming languages.

**Syntax:**

For ScriptEval, the entire expression is evaluated, but a common best practice is to have the first line be a call to a function that is defined below, or to an anonymous function:

```javascript
myFunction();
function myFunction(){
  document.getElementById("buttonID").setAttribute("disabled", true);
  //you can add as many instructions here as needed
}
```

In the simple example above, the custom action sets the `disabled` attribute of a button to true so you can verify with another action that the button is no longer clickable.

BlazeMeter evaluates the function `myFunction();` which starts executing the instructions.

**Usage:**

Almost all interaction with the page in JavaScript is done through the [JS Document (see W3C Schools).](https://www.w3schools.com/js/js_htmldom_document.asp) In all actions, you can reference `${Taurus Variables}` directly inside the code. These variables may come from a test data parameter or a CSV file, or they may have been set by other actions.

Here is an example where you set the innerText of the button to a string:

```javascript
myFunction();
function myFunction(){
  document.getElementById("buttonID").innerText = "${variableName}";
}
```

Taurus replaces the variable `${variableName}` with the value just before the step is executed.

#### StoreEval

**Description:**

StoreEval is the basic action for running custom code, and it stores the return value of the script in a `${Taurus Variable}` so that you can use the output of a script in the rest of your test.

**Syntax:**

For StoreEval, BlazeMeter prefixes your code with an implicit `return` call. Otherwise, the syntax is the same as the other actions. For example, you enter the following code snippet:

```javascript
myFunction();
function myFunction(){
  document.getElementById("buttonID").setAttribute("disabled", true);
  //you can add as many instructions here as needed
}
```

And BlazeMeter prefixes it implicitly with a `return` statement:

```javascript
return myFunction();
function myFunction(){
  document.getElementById("buttonID").setAttribute("disabled", true);
}
```

However, if you add the `return` statement yourself and entered the following code:

```javascript
return myFunction();
function myFunction(){
  document.getElementById("buttonID").setAttribute("disabled", true);
}
```

Then BlazeMeter would treat it as a duplicated `return` statement:

```javascript
return return myFunction();
function myFunction(){
  document.getElementById("buttonID").setAttribute("disabled", true);
}
```

The main thing that's different for StoreEval is that it takes an extra parameter, the name of the variable to store the result from the script.

**Usage:**

In this example, you store the return value from the script in the variable `outputText`. Then, in a later Type action, you *use* the variable reference `${outputText}` to type the returned value into an address field. Note that when you *declare* the variable `outputText` in the StoreEval Action, you do not wrap it in `${ .. }` characters.

In this example, BlazeMeter executes the first line as `return myFunction();`. And inside myFunction() it executes the line:

```javascript
return document.getElementById("buttonID").innerText;
```

The function returns the innerText of the button. The action returns the value and stores it in the variable `outputText` which you can then reference as `${outputText}` elsewhere.

#### AssertEval

**Description:**

AssertEval is a shortcut that evaluates a custom JavaScript code snippet and asserts that the result returns true. If it does not return true, the action is interpreted as an unmet assertion and the test fails.

**Syntax & Usage:**

When `myFunction()` is evaluated, it either returns true or false. In this example, the result depends on the presence of a button with a certain text:

```javascript
myFunction();
function myFunction(){
  if(document.getElementById("buttonID").innerText = "Expected Text")
  {return true;}
  else
  {return false;}
}
```

Simply verifying whether text exists on the web page can more easily be accomplished by the Assert Text action. This is just a trivial example of how a custom JavaScript returning a true or false value lets you pass or fail an assertion.

### Worked Examples

The following two examples show how custom JavaScript functions can read any values that are not directly accessible named Objects, and how they can modify any value while the script is running, for example, to calculate intermediate values or to normalize text.

#### Example 1: Working With Values From Basic Tables

The web page you want to test contains a regular HTML table. In this first worked example, you want to calculate the sum of the numeric values in the third column of this table so you can compare it in an assertion later:

| a | x | 1 |
|---|---|---|
| b | y | 2 |
| c | z | 3 |

The following code snippet selects cells from the third column, and then applies a custom calculation script to the cells' innerText contents:

```javascript
(function() {
  const col3 = document.querySelectorAll('table tr td:nth-child(3)');
  return Array.from(col3).reduce((res, x) => res + Number(x.innerText), 0);
})();
```

You use this custom script in a `storeEval` action and declare the variable `sum` to store the result. This way, you can reference the calculated value later as `${sum}` in another action. In the example below, you use the result in a conditional if-then-else statement. Since the `reduce` function returned a number, you can use the result with numeric comparison operators such as `if ${sum} > 5`.

#### Example 2: Verify a Value in a Complex Table

In the second worked example, you want to verify that a particular value in an HTML table is correct. The table is however irregular and columns and values are sometimes included and sometimes omitted, which means the precise position of values in the HTML document changes depending on circumstances. This causes issues with identifying the Object reliably since, if you attempted to reference it like a static object, you would often read the wrong value.

**Solution: Theory**

While the data isn't in a consistent place each time, you notice an implicit relationship between labels (keys) and values. In this example, `MLR Year` is the key and the number `2019` is its value. Similarly, `Exclusion Exception` is the key and the text `Does not apply` is its value, and so on.

You can use this consistency to identify a particular value in the table with a minimum level of reliability.

**Devising a custom function:**

You want to devise a custom JavaScript function that takes a pair of key and expected value, and returns true if the value for that key found in the table is the expected value, and false otherwise.

More formally:

```
F(Key,Value) -> True/False
```

1. If the key is in the table: If the value for that key is the expected value, return true. If the value for that key is not the expected value, return false.
2. If the key is not in the table: Return false

**Complete Function:**

```javascript
valueVerifier("${Key}", "${Value}");
function valueVerifier(key, value) {
  let table = document.getElementsByTagName("table").item(0);
  let tableBody = table.getElementsByTagName("tbody").item(0);
  let rows = tableBody.getElementsByTagName("tr");
  for (let row of rows) {
    let cols = row.getElementsByTagName("td");
    for (let colIndex = 0; colIndex < cols.length; colIndex++) {
      let col = row.getElementsByTagName("td").item(colIndex);
      if (col.textContent.includes(key)) {
        if (colIndex + 1 < cols.length) {
          let nextColVal = row.getElementsByTagName("td").item(colIndex + 1).textContent;
          if (nextColVal.includes(value)) { return true; }
        }
      }
    }
  }
  return false;
}
```

**Debugging:**

The simplest way to debug a piece of JavaScript like this is by using Chrome Dev Tools on the target web page. For more information, see [Chrome DevTools](https://developer.chrome.com/docs/devtools/).

To open the Dev Tools, press F12 in Chrome. On the Dev Tools pane, paste the entire code snippet into the Console tab and press enter. It returns true or false depending on whether it found the key value pair in the first table.

If you add the line `debugger;`, it triggers a breakpoint in the Chrome debugger. The Chrome Debugger helps you see the exact state of the scope and code at that point, and lets you step through the code line by line.

### Best Practices

- Use IIFEs (Immediately Invoked Function Expressions) for return statements
- Understand data type resolution (number vs string context)
- Serialize/deserialize complex data types using JSON
- Use ScriptEval for actions that don't return values
- Use StoreEval for actions that need to store return values
- Use AssertEval for assertions that need custom logic
- Reference `${Taurus Variables}` directly in JavaScript code
- Debug JavaScript snippets using Chrome Dev Tools
- Use `debugger;` statement for breakpoints
- Test JavaScript snippets in Chrome console before using in tests
- Remember that BlazeMeter implicitly adds `return` for StoreEval
- Use functions for complex logic, call them on the first line
- Wrap `${Taurus Variables}` in double quotes when used as strings

---

## Taurus Actions for Scriptless Testing

When creating a Scriptless GUI Test or a Browser Performance Test, you can use a set of predefined test actions, such as opening a web page, selecting dropdown items, submitting forms, typing text, and clicking buttons. Scriptless Tests additionally support control structures such as conditionals and loops.

**Use when**: Using predefined Taurus actions in Scriptless GUI Tests, learning about available actions and control structures, or implementing complex test scenarios with loops and conditionals.

### Overview

All available actions and control structures are explained in this article. An object is a set of locators for finding a GUI element, such as a button, field, or menu item. A child object is an iterable object that is defined relative to another object, such as cells in table rows. (Only applicable within for-each loops.)

### Actions

GUI Functional Testing supports the following predefined Taurus actions and arguments:

- **Answer Dialog** - Intercepts a synchronously displayed JavaScript dialog, and sends a response
- **Assert Dialog** - Verifies whether a JavaScript dialog was open in the previous step
- **Assert Eval** - Verifies that the evaluation of a JavaScript expression returns a true value
- **Assert Text** - Verifies whether a given string exists in an element on the web page
- **Assert Title** - Verifies that the current page title is set to a given string
- **Assert Value** - Verifies the status of a UI element that can be set to a value, such as a checkbox or radio button
- **Click** - Simulates a single left-click by a user on, for example, a link or button
- **Close Window** - Closes a browser window
- **Context Click** - Simulates a user right-clicking, typically used to open a context menu
- **Double Click** - Simulates a double left-click by a user
- **Drag** - Simulates a drag-and-drop action by a user
- **Echo String** - Lets you print debug information to the console of the test runner
- **Edit Content** - Simulates editing the rich text content of an element
- **Go** - Navigates to a web page in the current web browser window
- **Keys** - Simulates a user pressing a key with focus on an object
- **Maximize Window** - Resizes the current browser window to the maximum size
- **Mouse Down** - Holds down the mouse button on an object
- **Mouse Move** - Moves the mouse pointer to an object
- **Mouse Up** - Releases the mouse button on an object
- **Mouse Over** - Hovers the mouse pointer over an object
- **Mouse Out** - Moves the mouse pointer away from an object
- **Open Window** - Opens a new web browser window and navigates to a URL
- **Pause For** - Simulates a slow user interaction, or you can use it to wait for content to load
- **Publish / Unpublish** - Lets you publish or clean up test data in the test environment using Data Targets
- **Resize Window** - Simulates a user changing the window size
- **Script Eval** - Lets you define and run custom actions written in JavaScript
- **Select** - Selects a menu item from a drop-down menu
- **Store Eval** - Evaluates a JavaScript and stores the results of evaluation in a variable
- **Store String** - Saves any hard-coded string into a variable
- **Store Text** - Saves the HTML InnerText of an element into a variable
- **Store Title** - Saves the current page title into a variable
- **Store Value** - Stores the value attribute of an input element into a variable
- **Submit** - Simulates a user clicking the submit button on a form
- **Switch Frame** - Changes focus to another frame or iframe
- **Switch Window** - Simulates a user switching between several open windows
- **Type** - Simulates a user typing a string into a text field
- **Type Secret** - Simulates a user typing a secret value into a masked form field
- **Wait For** - Waits either for a UI Element to change its state or for a timeout to expire

### Control Structures

If necessary, you can branch scenarios, or repeat sets of actions. GUI Functional Testing supports the following control structures:

- **If Else** - The If-Else Condition lets you branch the sequence of steps depending on a condition that is either true or false
- **For Loop** - The For Loop lets you repeat actions while counting down or up; the actions in the body can reference the counter value
- **Loop Over Data** - The Loop Over Data action lets you repeat actions in the current iteration while iterating over a range values in a Data Parameter
- **For Each Loop** - The For Each action lets you repeat actions while iterating over a list of elements, such as menu items, button groups, or even cells in table rows

### Advanced Use Case: Loop For Each Child Object

Optionally, define secondary **Child Objects** for the Iterator to loop over. The concept of Child Objects is only applicable within a For Each action.

- Each parent can have several different child objects defined
- Each Child Object has one or more locators
- The Child Object locator is relative to one instance of the object identified by the iterator (parent locator)

**Example scenario:** Iterate over cells in table rows to assert a value

1. Open your GUI Functional test and add a **For Each** action
2. As iterator, select an existing parent object or create a new one. In this example, the parents are table rows, so we use an object with an XPath of //tr
3. Edit the parent object
4. Click **Add Child Objects** and define locators relative to the parent. In this example, the Child Objects are cells in the fifth column of each row, so we enter an XPath of /td[5]
5. Click **Edit** again to save changes to the parent object
6. Define the For Each Loop body. In this example, we add an **Assert Text** action. As Object, select the parent object. Clear the searchbar if necessary, and then select the Child Object
7. Run the test. BlazeMeter repeats the test actions for the fifth cell of each row

### Documentation References

For detailed information about Taurus Actions for Scriptless Testing, use the BlazeMeter MCP help tools:

**Taurus Actions for Scriptless Testing**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-taurus-actions-scriptless`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-taurus-actions-scriptless"]}`

---

## Documentation References

For detailed information about the Test Action Library, use the BlazeMeter MCP help tools:

**Test Action Library**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-test-action-library`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-test-action-library"]}`

**Custom JavaScript Actions**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-custom-javascript-actions`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-custom-javascript-actions"]}`

**Taurus Actions for Scriptless Testing**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `functional-taurus-actions-scriptless`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["functional-taurus-actions-scriptless"]}`

