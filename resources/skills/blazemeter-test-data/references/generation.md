# Test Data Generation

## Generator Functions

Use Test Data Generator Functions to generate synthetic test data for your tests. When you parameterize your tests, you can assign these functions as variable values instead of using static hard-coded values.

**Use when**: Generating synthetic test data using generator functions, parameterizing tests with dynamic values, or creating realistic test data programmatically.

### Terminology Used

The parameter values for Test Data Generator functions are ECMAScript 6 expressions. An expression can be numbers, text, functions, or a combination of these.

- **Functions**: A Data Generation Function accepts zero or more arguments, and returns a value. For example, the random credit card function accepts `"AMEX"` as argument, and returns a valid random American Express number
- **Variables**: After you have declared a parameter `x` in your test, you can reference its value elsewhere using `${x}` syntax
- **Numbers**: You can use numbers and familiar mathematical operators in parameters
- **Text**: Use quotation marks to define a text string. You can use plus signs to join text, numbers, function return values, and variables into one string (string concatenation)
- **Dates and Times**: Provide dates and times enclosed in quotes and in ISO 8601 (UTC) format, "YYYY-MM-DD HH:mm:ss.SSS"
- **Logical functions**: Comparisons and conditions support the Boolean values `true` and `false`
- **Lists**: You can define lists of strings using `["jelly","bread", "peanut butter"]` syntax and, similarly, you define numeric lists as `[1,2,3]`
- **Nesting**: You can nest functions and variables into one another to chain them together

### Function Categories

The following function categories are available:

- **Text Functions**: Generate new random strings, change the capitalization of a string, or tell you the length of a string (length, lorem, lower, randText, randChars, regExp, upper, wordcap)
- **List Functions**: Let you pick a random value from a list, or a substring from a string (mid, percval, randFromCSV, randFromSeedlist, randFromList, valueFromSeedlist, valueFromList, valueFromCSV, fixedDistribution, percDistribution, randDistribution)
- **Identifier Functions**: Generate random but valid credit card numbers and globally unique identifiers (randCreditCard, guid, uuidGenerator, luhn, addLuhn, customLuhn, usSsn, usSsnNew, brazilianCnpj, brazilianCpf, elfProef, italianTaxCode, spanishDni)
- **Date and Time Functions**: Let you identify the day of the week or the name of the month, generate random dates and times, or generate dates and times within ranges (addDays, addMonths, addYears, addMillisecs, addSecondsToTime, addSecondsToDateTime, addRandDays, date, parseDate, datetime, daysAfter, dateOfBirth, dob, dayOfWeek, dow, lastDay, randDate, randTime, secondsAfter, time, now)
- **Mathematical Functions**: Let you perform common mathematical operations (such as add, multiply, divide, modulo), convert bases, or generate random numbers (abs, add, addRand, convBase, divide, exp, mod, multiply, randDigits, randRange, randInt, sequenceGenerator)
- **Logical Functions**: Let you compare values and generate data according to custom conditions (ifCondition, ternary operator `?:`, booleanCompare, not, or, and)
- **Special Functions**: Additional specialized functions (valueFromJson)

### Examples

**Example: Function usage**

To generate values such as "Kim.Smith@acme.com" for an email variable, you join (concatenate) generator functions and strings together:

```
randFromSeedlist("firstnames") + "." + randFromSeedlist("lastnames") + "@acme.com"
```

**Example: Variable usage**

If you already have variables that contain part of the data, you can concatenate multiple variables. In this example, you already have the variables `firstName` and `lastName` in your Data Entity. Next, you create an `email` variable and define it as concatenation of the `${firstName}` value, a period, the `${lastName}` value, and the string `"@acme.com"`:

| Variable Name | Variable Value | Result Examples |
|---------------|----------------|-----------------|
| firstName | randFromSeedlist("firstnames") | Kim<br>Joe |
| lastName | randFromSeedlist("lastnames") | Smith<br>Kumar |
| email | ${firstName}+"."+${lastName}+"@acme.com" | Kim.Smith@acme.com<br>Joe.Kumar@acme.com |

**Advanced Example**

You can nest functions and variables as needed to fulfill complex requirements. For example, you want to generate email addresses in all lower case, from several different domains:

```
lower(${firstName}) + "." + lower(${lastName}) + "@" + randFromList(["acme.com","myorg.org"])
```

For detailed documentation of all functions, their parameters, and examples, see the [Test Data Generator Functions](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html) help documentation.

For related functions, see also:
- [Test Data Generator - Seed Lists](skill-blazemeter-test-data://references/generation.md)

---

## Generator Functions JavaScript Methods

Use built-in JavaScript methods to manipulate and transform test data generated by generator functions, including string manipulation, mathematical operations, and regular expressions.

**Use when**: Manipulating and transforming test data using JavaScript methods, performing string operations, mathematical calculations, or using regular expressions for pattern matching and replacement.

### Overview

For advanced users, the parameter definition supports a subset of common JavaScript prototype methods. Prior knowledge of JavaScript is required. These methods allow you to transform and manipulate the output of generator functions.

**Example Scenario:**

This parameter definition generates an email address like `Joe.Smith@example.com`:

```
randFromSeedlist("firstnames") + "." + randFromSeedlist("lastnames") + "@example.com"
```

However, some first names and last names contain special characters such as whitespace which are not allowed in email addresses. The following example shows how to replace all whitespaces by a period:

```
( randFromSeedlist("firstnames") + "." + randFromSeedlist("lastnames") + "@example.com" ).replace(/ /g,".")
```

The use of the `.replace()` method ensures that multi-name email addresses such as `Mark.Graca.Maria.Fuego@example.com` are generated correctly.

### Supported JavaScript Methods

The following table shows the list of supported JavaScript methods:

| JavaScript Method | Description | Examples |
|------------------|-------------|----------|
| All static properties and static methods from [Math](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math) | Offers math constants, exponents and logarithms, angle functions, min/max, floor/ceiling, and more | `${radians} / (Math.PI / 180)`<br>`Math.SQRT2`<br>`Math.trunc(42.84)`<br>`Math.floor(5.95)`<br>`Math.sin(1)` |
| All static properties from [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number) | Lets you inspect JavaScript constants and limits | `Number.MAX_VALUE`<br>`Number.MIN_VALUE`<br>`Number.POSITIVE_INFINITY` |
| `isNaN()` | Tells you whether a value is not a number | `isNaN(${var}) ? 0 : ${var}+3` |
| `parseInt()` `parseFloat()` | Converts strings to numbers | `parseInt("123")`<br>`parseFloat("83.468")` |
| `encodeURI()` `decodeURI()` `decodeURIComponent()` `encodeURIComponent()` | Converts URLs and paths to escape special characters | `encodeURI("/my path/some file")` |
| `normalize()` | Converts a Unicode string into a (human readable) string in Unicode Normalization Form | `normalize('\u0041\u006d\u00e9')` |
| `toLocaleLowerCase()`<br>`toLocaleUpperCase()` | Changes the capitalization of a string, respecting the given locale | `'İstanbul'.toLocaleLowerCase('tr')` |
| `replace()` | Searches and replaces strings or regular expressions in strings, and returns a new string | `"Joe Moe Doe".replace(/ /g,".")`<br>`"Joe Doe".replace("Joe","John")` |
| `repeat()` | Repeats text several times | `"Cheers! ".repeat(3)` |
| `padEnd()` `padStart()` | Adds characters before or after a string up to the specified length | `"123".padStart(5, '0')`<br>`"abc".padEnd(6, 'x')` |
| `concat()` | Conjoins two strings with the given character | `"hello".concat(' ', "world")` |
| `substring()` `slice()` | Returns the substring between two indices. Slice() also supports negative indices for counting backwards from the end | `"Chrome 80.0.123".substring(7)`<br>`"Chrome 80.0.123".substring(7,9)`<br>`"Chrome 80.0.123".slice(-8)`<br>`"Chrome 80.0.123".slice(7,9)` |
| `charAt()` `charCodeAt()` `codePointAt()` | Returns one character, or UTF-16 code, or Unicode code point found at the index position | `"abc".charAt(1)`<br>`"abc".charCodeAt(1)`<br>`'☃★♲'.codePointAt(1)` |
| `search()` `indexOf()` `lastIndexOf()` | Tells you the index *where* a regular expression or substring first matches a string. Returns -1 if no match was found | `"hello world".search(/[\s]+/g)`<br>`"hello world".indexOf("o")`<br>`"hello world".lastIndexOf("o")` |
| `test()` | Tells you *whether* a regular expression matches a string | `RegExp('foo*').test('fooo')` |
| `startsWith()`<br>`endsWith()`<br>`includes()` | Tells you *whether* a string contains a substring | `"abcdefg".startsWith("ab")`<br>`"abcdefg".includes("cde")`<br>`"abcdefg".endsWith("fg")` |
| `localeCompare()` | Returns 0 if the strings are the same, returns 1 if the second string is earlier in the sort order, and -1 if it's lower | `"m".localeCompare("m")`<br>`"z".localeCompare("a")`<br>`"a".localeCompare("z")` |

**Note**: Indices start counting at 0.

To learn more about method arguments, see [MDN JavaScript Documentation](https://developer.mozilla.org/en-US/docs/Web/javascript).

### Regular Expressions

Typically, you use literal search terms: For example, searching for "high-school" misses all instances of "high school". Regular expressions (RegEx), however, are a smart way to describe search text patterns. With a RegEx pattern you can look for "either 'high-school' or 'high school', but not 'high. School'".

The JavaScript methods `test()`, `search()`, and `replace()` support regular expressions as arguments. Surround the RegEx with two slashes. Symbols such as `*`, `+`, `?`, `\` have special meanings.

**Examples:**
- `"hello world".search(/[\s]+/g)` - Tell me the index of the first one or more spaces in the text "hello world"
- `RegExp('foo*').test('fooo')` - Tell me whether "fooo" matches the pattern "the word 'fo' followed by zero or more o's"
- `"Joe Moe Doe".replace(/ /g,".")` - Give me a new string with the same text, but all spaces are replaced by periods

To learn more about regular expression syntax, including links to online RegEx testers, see [MDN Regular Expressions Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions).

### Regular Expression Examples

The following table shows some examples of regular expressions:

| RegEx | Example | Meaning |
|-------|---------|---------|
| `/abc/` | `"abc"`<br>`"labcoat"` | Literally these characters in that order |
| `/ab*c/` | `"abc"` `"abbbbbbbc"` `"ac"` | One a, then maybe some bs, then one c.<br>`*` repeats the preceding character **zero or more** times |
| `/ab+c/` | `"abc"` `"abbbbbbbc"` | One a, then some bs, then one c.<br>`+` repeats the preceding character **one or more** times |
| `/sha[la]+lee/` | `"shalalee"`<br>`"shalalalalalalee"` | One sha, then some la's, then one lee.<br>Use brackets to apply a repetition symbol to the preceding **group** |
| `/^Introduction$/` | `"Introduction"` | Just this pattern on a line by itself. `^` stands for the beginning of a line. `$` stands for the end of a line |
| `/abc/g` | `"Learning my abc's wearing a labcoat"` | Search **globally**, don't stop searching after the first |
| `/abc/i` | `"ABC"` `"AbC"` `"abc"` | **Case-insensitive** search |
| `/\\w+\\s/g` | `"a "` `"sample "` | Search any words followed by one space.<br>`\w` stands for **any alphanumeric Latin character including underscore**<br>`+` repeats the preceding character **one or more** times<br>`\s` stands for **any space or tab character** |
| `/\\d{3}-\\d{2,4}/` | `273-0379` `925-221` `444-10` | Exactly 3 digits, a hyphen, then 2 to 4 digits.<br>`\d` stands for **any digit**<br>`{n}` repeats the preceding character **exactly n** times<br>`{n,m}` repeats the preceding character **at least n** and **at most m** times |
| `/ab\\*c/` `/ab\\\\c/` | `"ab*c"` `"ab\\c"` | First a, b, then literally this symbol, then one c. Use a backslash to take the following **special character literally** |
| `/.ie/` | `"pie"` `"lie"` `"tie"...` | Any letter followed by the given text "ie". `.` stands for **any one character** |

### Reference

- **Help ID**: `test-data-generator-functions-javascript`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-generator-functions-javascript"]}`

---

## Generator Functions Seed Lists

Use built-in seed lists for generating realistic test data, including names, addresses, companies, and multi-column seed lists.

**Use when**: Generating realistic test data using built-in seed lists or creating test data with names, addresses, companies, or multi-column data.

### Seed Lists

The included seed lists contain common example strings to help you generate realistic test data, such as names of weekdays, months, persons, banks, companies, places, and so on. To learn more, see the [randFromSeedList()](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html#randFromSeedList) / [randlov()](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html#randFromSeedList) or [valueFromSeedlist()](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html#h_01EP79N0D3DSTCF40JZRTXEK42) functions.

BlazeMeter ships with the following seed lists included:

**Names**
- `firstnames`, `femalenames`, `malenames`
- `lastnames`, `lastnameenglish`, `honorific-titles`
- `firstnamefemaleamerican`, `firstnamemaleamerican`
- `lastnameindian`
- `lastnameitalian`, `firstnameitalian-multicol`
- `lastnamespanish` `firstnamespanish-multicol`
- `firstnamegerman`, `lastnamegerman`, `honorific-titles-german`

**Addresses**
- `country`
- `streetnames`
- `ukpostcode-multicol`
- `usaddress-multicol`, `usaddressbig-multicol`
- `uszip-multicol`, `usstates-multicol`
- `italiancities-multicol`
- `spanishcities-multicol`
- `australianpostalcodes-multicol`
- `ukpostcodes-sample`, `uktowns`, `ukcounties`
- `germanpostalcodes`, `japan-zip-codes-full`, `swedishpostalcodes`, `indiancities`
- `escommunities`

**Miscellaneous**
- `bankaccountno`, `banknames`, `usbanks-multicol`, `usbanksbig-multicol`
- `creditcard`, `currencycode`, `swift-bic`, `iban-random`
- `companies`, `energycompanies`, `spcompanies-multicol`, `usmanufacturercompanies-multicol`, `usretailcompanies-multicol`
- `dayofweek`, `month`
- `ukcompanies-multicol`, `ukethnicity`, `ukgender`, `ukphonenumbers`, `ukreligions`, `uksortcodes`
- `escompanies-multicol`
- `emailaddresses`
- `icd10-multicol`
- `colors`, `colorsbig-multicol`
- `IPV4-multicol`, `ipv4-random`, `IPV4`, `IPV6-multicol`, `ipv6-random`, `IPV6`, `mac-random`
- `MF` (contains the values "M" and "F" to generate random male/female values)
- `YN` (contains the values "Y" and "N" to generate random yes/no values)
- `computergames`

### Multi-Column Seed Lists

Some seed lists contain several columns of congruent data, such as a street name with matching postal code, county, and city name, that you can use to test form validation or map lookup. Their names end in "*-multicol*".

The `randFromSeedlist(seedListName, column, percnull)` function has an optional column parameter to select these extra columns. By default, the function only returns the first column.

**Note**: When using `valueFromSeedlist()` with multi-column seed lists, you can retrieve matching values from the same row by using the same row index. This ensures data consistency across related columns.

**Examples:**
- `randFromSeedlist("femalenames")` Returns "Jenny"
- `randFromSeedlist("usaddress-multicol", 1)` Returns "325 Beacon St"
- `randFromSeedlist("usaddress-multicol", 2)` Returns "Boston"
- `randFromSeedlist("usaddress-multicol", 1, 20)` Returns "325 Beacon St" or null with a 20% probability
- `valueFromSeedlist("usaddress-multicol",1,4) + " " + valueFromSeedlist("usaddress-multicol",1,2)` Returns the matching values "02215 Boston" because they are both taken from row 1.

Multi-Column Seed Lists provide values such as:
- `australianpostalcodes-multicol`: AUS postal code, city/town
- `colorsbig-multicol`: Color name, hexadecimal value, red value, green value, blue value
- `icd10-multicol`: ICD-10 code, human-readable name
- `IPV4-multicol`: IPv4 addresses split into 4 columns
- `IPV6-multicol`: IPv6 addresses split into 8 columns
- `firstnameitalian-multicol`: Italian first name, gender (M or F)
- `italiancities-multicol`: Italian city, province code, province name, region code, tax code, is capital (YES or empty), min zipcode, max zipcode
- `firstnamespanish-multicol`: Spanish first name, gender (M or F)
- `spanishcities-multicol`: Spanish city name, province code, province name, community, postal codes, postal code prefix, capital (values: Capoluogo or empty)
- `escompanies-multicol`: Spanish company name, company email
- `spcompanies-multicol`: S&P500 company name, ticker symbol, industry sector
- `ukcompanies-multicol`: UK company name, street address, city, county
- `ukpostcode-multicol`: UK postal code, city, county, phone prefix
- `usaddress-multicol`: US street address, city, two-letter state abbreviation, zip code
- `usaddressbig-multicol`: US zip code, street address, city, two-letter state abbreviation, city alias, zip code
- `usbanks-multicol`: US bank name, city, state, RSSD ID
- `usbanksbig-multicol`: US bank name, short bank name, address, city, country, zip code, RSSD ID
- `usmanufacturercompanies-multicol`: US company name, ticker symbol, industry sector
- `usretailcompanies-multicol`: US company name, ticker symbol, industry sector
- `usstates-multicol`: US state name, two-letter state abbreviation
- `uszip-multicol`: US zip code, two-letter state abbreviation, city, city alias, county, area code

---

## How to Randomize

Control random test data distributions, including fixed values, random selection, probability-based, and guaranteed percentage distributions.

**Use when**: Controlling random test data distributions or implementing fixed values, random selection, or probability-based data distributions.

### Control Random Test Data Distributions

Either use fixed test data values from an ordered spreadsheet or get randomized values. You can get completely random data or influence the distribution of the returned values. You can define alternative values or functions and choose a probability for each, as long as the total of the distributions adds up to 100 percent.

**Follow these steps:**

1. After defining a Data Parameter, click **Distribution** to define values. The **Synthetic Data Generation By Distribution** window opens
2. Choose a **Distribution Mode**:
   - **Random** — Selects values pseudo-randomly. The probability for each is the same, but not guaranteed. This is the default
   - **Probability %** — Lets you define a probability for each value, the actual distribution is not guaranteed, though. This means, a 50-50 distribution might end up being 50.1% and 49.9%
   - **Guaranteed %** — Each value is selected exactly according to the given percentage distribution. For example, a 25-25-25-25 distribution selects each of the four values in turn
3. Click the **Plus** button to add alternative values or functions
4. (For **Probability %** and **Guaranteed %** modes only) Define **Distribution Settings** by entering the desired percentage for each value. The total must add up to 100%
5. Click **Save**

---

## Generate Test Data for Negative Tests and Chaos Testing

Generate test data for negative tests and chaos testing using BlazeMeter's probabilistic distribution settings to create negative and chaotic test data scenarios.

**Use when**: Generating test data for negative tests and chaos testing, testing unhappy paths, or creating unpredictable test scenarios with invalid or malformed data.

### Overview

There are only few ways for users to get a process right (the Happy Path), and countless ways of getting it wrong (the Unhappy Paths). In practice, the majority of your tests are so-called negative tests of Unhappy Paths. *Negative assertions* verify that your app is indeed catching exceptions that you know to avoid, and that it offers helpful validation or error messages and ways for users to recover gracefully.

However, even negative and positive tests merely test the well-trodden paths that users take, whereas reality is unpredictable. *Chaos testing* refers to testing unexpected errors that occur, for example, when someone sends requests in the wrong formats or when responses are delayed. Coming up with chaotic test data takes even more effort than writing tests for straight-forward Happy and Unhappy Paths.

BlazeMeter's test data integration helps you save time by generating negative and chaotic test data as part of the Probabilistic Distribution settings. You control how the negative cases are pseudo-randomly distributed.

### Generate Negative Test Data

**Steps:**

1. Open any test or virtual service transaction
2. Open the **Test Data/Service Data** pane, and open a Data Entity. If you want to switch between positive and negative, create a [Data Variant](skill-blazemeter-test-data://references/generation.md) for the negative cases now
3. Find the Data Parameter for which you need negative test data and click its **Distribution** button. The **Synthetic Data Generation By Distribution** dialog opens
4. Click the **Suggest Negative Data** button and choose a suggestion:
   - **Out of bounds numbers**: Extreme values
   - **Negative numbers where positive numbers are expected**, and vice versa
   - **Text where numbers where expected**, and vice versa
   - **Strings that are too long or too short** for the text field
   - **Malformatted text**: Wrong delimiters, or text with invalid characters
   - **Extra numbers or characters** at the beginning or the end
   - **Credit cards** with correct checksum but for the wrong vendor
   - **Times and dates** with invalid formats, or with valid formats but not the requested one
   - **Empty values**, and so on
5. If there are no suggestions for your test data, contact Support and describe your use case
6. Click **Save**

### Run Tests with Negative Data

Run the test to see how your app reacts to chaotic and negative test data.

To learn more about providing alternative values and their probabilities, see [Random Distributions](skill-blazemeter-test-data://references/generation.md).

### Documentation References

For detailed information about generating test data for negative tests and chaos testing, use the BlazeMeter MCP help tools:

**Generate Test Data for Negative Tests and Chaos Testing**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `test-data-negative-chaos-testing`
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-negative-chaos-testing"]}`

---

## Variants

Create and manage data variants for quick switching between different test data configurations in the same Data Entity.

**Use when**: Creating and managing data variants for quick switching between different test data configurations or testing multiple scenarios with the same Data Entity.

### Why Data Variants?

Data variants help you create instances of a Test Data Entity that you can quickly switch between. Think of situations where you want to re-run the same test structurally, but with different test data: For example, you want to run the same registration test with user addresses for either US users, EU users, or APC users, so you can focus on testing specific address validation features.

To run such test variants, you could create multiple Data Entities with a parallel data structure. The Data Entities would need to have the same column names but could contain different values, and you would load a different Entity for each test run. This works, the only disadvantage is, you would have to keep track of which Data Entities belong to which test or virtual service, among all the shared Data Entities.

Data Variants are an alternative that makes swapping between Data Entities quick and easy. When you load a Data Entity with Data Variants, it comes with a menu that lets you select from among its variants. Each Data Variant has the same column structure but can contain different (overridden) values. The Variants are saved and loaded together with their Data Entity.

### The Default Variant

Data Variants are derived from one base variant called "default". You cannot add, delete, or rename parameters in variants because they are the same across all variants.

If you add, delete, rename, modify a parameter in the default variant, this change propagates to all variants.

**Example:**
You have a Data Entity called "Users" that contains two Data Parameters:
- Users: age: randInt(20,80) region: "US"

You create a variant of "Users" and name it "Teenagers". In it, you override the age value to randInt(15,19). Now you have two variants with different age values:
- Users (Default) age: randInt(20,80) region: "US"
- Users (Teenagers) age: **randInt(15,19)** region: "US"

If you, in the *default* variant, change the default region to "EU", both variants reflect the change:
- Users (Default) age: randInt(20,80) region: "**EU**"
- Users (Teenagers) age: **randInt(15,19)** region: "**EU**"

### Create Data Variants

Data Variants are available in the following test types:
- Functional and Performance Tests that have a Data Entity with Data Parameters associated
- virtual services that have a Service Data Entity with Data Parameters associated

**Follow these steps:**

1. Open the Test or virtual service
2. Open the **Test Data pane** or **Service Data** pane, respectively
3. Click the Data Entity's ellipsis menu and select **Manage Data Variants**. The **Manage Data Variants of Data Entity "Name"** window opens and shows the default variant
4. Click **Add Data Variant**. A new variant is added to the list
5. Give each Variant a distinctive name so that team members know which one to select
6. Click **Save**. Your variants now appear in a menu below the Data Entity name
7. Select a data variant from the menu
8. Edit the values in each data variant as needed

Finally, select a data variant and run the test.

### Edit Data Variants

When you edit data variants, the default values from the Entity are overridden and the new values stored in the variant.

**Follow these steps:**

1. Open the Test or virtual service
2. Open the **Test Data** pane or **Service Data** pane, respectively
3. Identify the Entity and select a data variant from its menu. Edit the values in each data variant as needed. To reset a value back to the default, click **Reset Variant Override**. To add a column, switch to the default variant first

### Troubleshoot Data Variants

- If the Manage Variants menu item of a Data Entity is grayed out, add Data Parameters first
- If you try to add a new Data Parameter and get the error message "*Modify property on non default dataset is not allowed*", switch to the default Data Variant first

---

## Negative Chaos Testing

Generate test data for negative tests and chaos testing, including out-of-bounds values, malformed data, probabilistic distributions, and edge case generation. There are only few ways for users to get a process right (the Happy Path), and countless ways of getting it wrong (the Unhappy Paths). In practice, the majority of your tests are so-called negative tests of Unhappy Paths.

**Use when**: Generating test data for negative tests and chaos testing or creating out-of-bounds values, malformed data, probabilistic distributions, and edge cases.

### Overview

- **Negative assertions** verify that your app is indeed catching exceptions that you know to avoid, and that it offers helpful validation or error messages and ways for users to recover gracefully
- **Chaos testing** refers to testing unexpected errors that occur, for example, when someone sends requests in the wrong formats or when responses are delayed
- BlazeMeter's test data integration helps you save time by generating negative and chaotic test data as part of the Probabilistic Distribution settings. You control how the negative cases are pseudo-randomly distributed

### Generate Negative and Chaos Test Data

**Steps:**

1. Open any test or virtual service transaction
2. Open the **Test Data/Service Data** pane, and open a Data Entity. If you want to switch between positive and negative, create a [Data Variant](skill-blazemeter-test-data://references/generation.md) for the negative cases now
3. Find the Data Parameter for which you need negative test data and click its **Distribution** button. The **Synthetic Data Generation By Distribution** dialog opens
4. Click the **Suggest Negative Data** button and choose a suggestion:
   - **Out of bounds numbers, extreme values**: Negative numbers where positive numbers are expected, and vice versa
   - **Text where numbers where expected, and vice versa**
   - **Strings that are too long or too short** for the text field
   - **Malformatted text, wrong delimiters, or text with invalid characters**
   - **Extra numbers or characters** at the beginning or the end
   - **Credit cards with correct checksum but for the wrong vendor**
   - **Times and dates with invalid formats**, or with valid formats but not the requested one
   - **Empty values**, and so on
   
   If there are no suggestions for your test data, contact Support and describe your use case
5. Click **Save**

Run the test to see how your app reacts to chaotic and negative test data.

To learn more about providing alternative values and their probabilities, see [Random Distributions](skill-blazemeter-test-data://references/generation.md)

---

## How to Generate Synthetic Test Data

When parameterizing tests with different variable values, you can [Load Test Data from Spreadsheets](skill-blazemeter-test-data://references/core-concepts.md) or generate synthetic test data, or a combination of these sources.

Synthetic test data looks like real or random data, but you have full control over its form, and you don't have to collect it yourself.

**Advantages:**
- Synthetic test data is advantageous in tests where you need dynamic parameter values, such as relative date stamps ("today" or "last month"), fake but valid credit card numbers, random but plausible names, and so on
- BlazeMeter additionally helps you avoid invalid values: The included functions don't generate dates such as February 31, names such as `asdf%as'df`, nor credit card numbers with invalid checksums

**Use when**: Generating synthetic test data for tests, creating dynamic parameter values, or avoiding invalid test data values.

### Available Data Generator Functions

Synthetic Data Generator Functions work in the same way as functions that you are familiar with from Excel spreadsheets, such as DAYS() or CHOOSE().

The following function categories are available:

- **Text Functions**: Generate new random strings, change the capitalization of a string, or tell you the length of a string
- **List Functions**: Let you pick a random value from a list, or a substring from a string
- **Identifier Functions**: Generate random but valid credit card numbers and globally unique identifiers
- **Date and Time Functions**: Let you identify the day of the week or the name of the month, generate random dates and times, or generate dates and times within ranges
- **Mathematical Functions**: Let you perform common mathematical operation (such as add, multiply, divide, modulo), convert bases, or generate random numbers
- **Logical Functions**: Let you compare values and generate data according to custom conditions

For the full list of all functions and their parameters, see [Test Data Generator Functions](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html).

### Insert Synthetic Data Parameters From Examples

After you have recorded a test, you want to add synthetic test data. The provided example functions cover common cases such as personal data, financial data, date/time, text manipulation, JavaScript, JSON format, and Seed List examples such as street addresses or IP Addresses. You can edit and expand the inserted examples any time, as needed!

**Steps:**

1. Open a test and go to the **Configuration** tab
2. Click **Test Data**. The list of data parameters opens on the right side
3. Click the **Plus** button and select **Create New Data Parameter From Example**. The **Add Data Parameter From Example** window opens and displays common examples
4. Select an example category from the left column
5. Select an example variant where applicable
6. (Optional) Hover over an example line and click **Preview parameter value** to see an instance of generated data
7. Click **Add** to insert the example into your Test Data pane. BlazeMeter creates data parameters and initializes them with functions and values

As described in [How to Use Test Data](skill-blazemeter-test-data://references/core-concepts.md), identify the data parameter that you want to use, click **Copy Parameter Name to Clipboard**, return to the test steps, and replace the hard-coded value with the pasted parameter. You can now run your test case as usual.

**Important Notes:**
- Some inserted example parameters rely on other parameters -- multi-column seed lists rely on an index parameter; an address is a concatenation of street and postal code parameters; a drivers license ID is a concatenation of name and date parameters; and so on. Before you edit or delete an example parameter, verify that no other parameter depends on it
- Inserting example parameters *does not* overwrite existing parameters of the same name. But if there are conflicting names, the inserted example might not work

### Scenario: Insert Synthetic Test Data Manually

In the following example scenario, you have recorded a Scriptless GUI Functional test case that types the hard-coded street name "`Wall Street`" into an address field. You now want to test this field with synthetically generated street names of varying lengths, randomly alternating with 50% null values using the percnull option.

You have familiarized yourself with the list of available [Test Data Generator Functions](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html) and have chosen the `randFromSeedlist()` function with the "`streetnames`" parameter.

**Steps:**

1. Open a Scriptless GUI Functional Test and go to the **Configuration** tab
2. Click **Test Data**. The list of data parameters opens on the right side
3. Click the **Plus** button and click **Create a new data parameter**. Enter `address` as its name
4. In the **Parameter Value** field, click the **Functions** menu. Hover over the function to view its documentation. Hover over and click the "**i**" icon to see a worked example, then click the arrow to return
5. Select a function and fill in its arguments. In this example, you have searched for a function related to lists and selected `randFromSeedlist()`. You want to use the "streetnames" parameter, column 1, and set the percnull option to 50% (to return an empty string in the half the test runs). Therefore you define the Parameter Value as: `randFromSeedlist("streetnames", 1, 50)`
6. (Optional) Click **Preview** to view an example of generated test data. In our example, the `${address}` preview might show a street name like "`Quarry High Street`" or an empty string with 50% probability. Click **Preview** a second time to return to the function definition
7. Click outside the field to save your changes

As described in [How to Use Test Data](skill-blazemeter-test-data://references/core-concepts.md), identify the data parameter that you want to use, click **Copy Parameter Name to Clipboard**, return to the test step and replace the static value with the pasted parameter. In this example, you replace the hard-coded **Text** value "`Wall Street`" with `${address}`. You can now run your test case as usual.

### Scenario: Use CSV Data as Input to Synthetically Generate Data

Sometimes when you load data from a static CSV file, it is missing relevant columns. You can add missing columns synthetically: BlazeMeter can populate, for example, an e-mail address column in the format `firstname.lastname@domain.com` based on the existing first and last name columns.

### Scenario: Replace CSV Columns with Dynamic Test Data

In this scenario, you have loaded data from a static CSV file, but you also need dynamic test data. For example, you can add a dynamic date of birth column that ensures valid dates with ages between 18 and 21 *at the time the test runs*. Rename the static birthdates column, create a new parameter named birthdates, and let BlazeMeter populate its values.

### Scenario: Extend CSV Rows with Dynamic Test Data

In other scenarios, the CSV file suits your test case well and you want to keep using the static data. But for longer tests, you run out of rows. Instead of looping back to the beginning of the column and repeating values, you want to *extend* the column dynamically.

**Steps:**

1. Expand the **Test Data** pane and hover the mouse over the CSV entry
2. Click the **More Actions** menu and select **Extend CSV File**. The **Extend CSV File** window opens
3. Select a CSV column and click the pencil icon under **Extend By Value** to edit the field
4. Define the values that you want to generate synthetically. BlazeMeter suggests available [test data generation functions and arguments](https://help.blazemeter.com/docs/guide/test-data-generator-functions.html)
5. Click **Save**

### Preview Generated Test Data

There are several ways how to preview or review generated test data.

#### How to Preview Stand-Alone Values

Click the **Preview Parameter Value** button next to a parameter to preview one instance of generated data. Click the button a second time to see the editable function again.

If a previewed parameter depends on another, random parameter, they are not synchronized in the stand-alone preview.

**Example of two stand-alone values:**
- `${filename} = randText(10,15)` Preview: `"E36hvVLj4mri"`
- `${filenamewithsuffix} = ${filename}+".txt"` Preview: `"waFcYCk8TJI6Bh.txt"`

#### How to Preview Synthetic Values in Context

In the **Test Data** pane, click **Iterations** (for GUI Functional Tests) or **Data Settings** (for Performance Tests) to preview generated values. The **Data Settings** window opens and shows a table that lists the first hundred instances of test data generated for all parameters for a run, in context.

In context means that if a previewed parameter depends on another, randomized parameter, the two synthetic values are synchronized.

**Example of two dependent values that are synchronized in the preview:**
- `${filename} = randText(10,15)` **Preview:** E36hvVLj4mri
- `${filenamewithsuffix} = ${filename}+".txt"` **Preview:** E36hvVLj4mri.txt

#### How to Download Test Data for Review

You can review the synthetic data that was generated after a test was run.

**Steps:**

1. Click **Reports**, and open the test report
2. Under Summary, click **Show Test Data**
3. Review the test data used in this test
4. (Optionally) Download the test data
5. Click **Close**

---

## Documentation References

For detailed information about test data generation, use the BlazeMeter MCP help tools:

**Test Data Generation**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: 
  - `test-data-generator-functions` (generator functions)
  - `test-data-generator-functions-seedlists` (seed lists)
  - `test-data-how-to-randomize` (randomize)
  - `test-data-variants` (variants)
  - `test-data-load-from-spreadsheets` (load from spreadsheets)
  - `test-data-generate-synthetic` (generate synthetic)
  - `test-data-generator-functions-javascript` (JavaScript generator functions)
  - `test-data-negative-chaos-testing` (negative and chaos testing)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-generator-functions", "test-data-generator-functions-seedlists", "test-data-how-to-randomize", "test-data-variants", "test-data-load-from-spreadsheets", "test-data-generate-synthetic", "test-data-generator-functions-javascript", "test-data-negative-chaos-testing"]}`

