# Test Data Pro

## Test Data Pro

Use Test Data Pro for large-scale test data generation, including AI-driven data profiler, AI-Assisted Function Builder, and generating seedlists from categories or examples.

**Use when**: Using Test Data Pro for large-scale test data generation or working with AI-driven data profiler, AI-Assisted Function Builder, and generating seedlists from categories or examples.

### Overview

Do you need large-scale test data for categories that are not included in the default seedlists? BlazeMeter provides [built-in data creators](https://help.blazemeter.com/docs/guide/test-data-profiler.html) that can replace hard-coded static values in your tests. Use the standard synthetic data functions and seedlists to generate test data from common categories, using mathematical operations or formulas.

For cases beyond the rule-based approaches, BlazeMeter relies on machine learning models to profile and generate test data according to your needs. A large language model (LLM) understands requests in human language, that means, you can ask it to identify the category of provided examples and to generate more examples of the same type — or, just let BlazeMeter make the requests for you!

AI-driven test data generation is useful in the following situations:
- I have a CSV file with examples and need more of the same type
- I can describe the kind of test data I need
- I can name the category, but I have no examples
- I have examples, but I can't name the category

### I Have a CSV File with Examples and Need More of the Same Type

You are extending an existing BlazeMeter test that has a CSV file attached. Looking at the content of some columns, you don't know what these data types are, nor can you easily describe what you see to search for more examples. How do you get more test data of the same type?

1. Open the test that has the CSV attached and open the **Test Data** pane
2. Open the CSV file entity and select **… > Create Data Automatically**. The **Data Creation Wizard** opens
3. Click **Next** and review the suggestions. The first step of the wizard is the **Data Profiler**. The profiler tries to identify the type of data in each column and suggests a rule-based function or built-in seedlist to replace columns. To learn more, see [Data Profiler](https://help.blazemeter.com/docs/guide/test-data-profiler.html). If the standard profiler cannot determine obvious categories, it passes the request on to the **AI-driven Data Profiler**. A trained Large Language Model identifies the category and lists more examples of the same type
4. Accept or decline the suggestions, or edit them if needed

Complete the [Data Creation Wizard](https://help.blazemeter.com/docs/guide/test-data-profiler.html) as usual.

### I Can Describe the Kind of Test Data I Need

Don't have time to browse the list of built-in data generator functions? Or you've browsed all the seedlists and didn't find a suitable one? From the Test Data pane, you can open the **AI-Assisted Test Data Function Builder** and describe which seedlist you need in words.

1. Open the test and create a Data Entity
2. Add a Data Parameter as usual, but in the value field, click the **Use AI** button. The **AI-Assisted Test Data Function Builder** opens
3. Enter a phrase that describes what type of test data you need

The wizard suggests a suitable data generator function for you, including arguments.

**Examples:**
- "random numbers from 10 to 20" suggests: `randInt(10, 20)`
- "Canadian postal codes" suggests: `regExp("[A-Z][0-9][A-Z] [0-9][A-Z][0-9]")`
- "The last day of the month" suggests: `lastDay(now())`
- "next month" suggests: `addMonths(now(), 1)`
- "A unique ID" suggests: `uuidGenerator()`

**Supported Data Generator Functions are:**
- `regExp(), sequenceGenerator(), uuidGenerator()`
- `randInt(), randText(), randDigits(), randRange(), addRand()`
- `randlov(), perclist(), seedlist(), percval()`
- `abs(), add(), divide(), multiply(), mod(), exp(), convBase()`
- `date(), time(), datetime(), dateOfBirth(), dayOfWeek(), lastDay()`
- `addRandDays(), randDate(), randTime()`
- `addSecondsToDateTime(), addMillisecs(), addSecondsToTime(), addDays(), addMonths(), addYears(), daysAfter(), secondsAfter()`
- `elfProef(), randCreditCard()`
- `length(), lower(), upper(), wordcap(), mid()`
- `anySeedlist(), similarValues()`

### I Can Name the Category, but I Have No Examples

If you can name the category of data you need, and you assume it's not among the built-in seed lists, BlazeMeter can generate any requested seedlist for you.

Create a Data Parameter as usual and set the value to the following function:
```
anySeedlist("your category")
```

This AI-driven Data Creator function returns 10 keywords or names from the same domain or category. It's as if any seed list was ready at your disposal!

**Examples:**
- `anySeedlist("car brands")` returns "Mazda", "Tesla", "Audi", "Mercedes-Benz", "BMW", "Nissan", "Chevrolet", and so on
- `anySeedlist("Polymers")` returns "polyethylene", "polystyrene", "polyurethane", "polyisoprene"

### I Have Examples, but I Can't Name the Category

The hard-coded test you are looking at used the example strings polyethylene, neoprene, nylon, silicone; you know they are chemicals or molecules, but what is the category called? Is there even a built-in seed list that contains similar values? Sometimes you don't know the terminology to look up more valid examples.

In this case, create a Data Parameter as usual. As its value, provide your keywords in the following format:
```
similarValues("keyword1","keyword2","keyword3"...)
```

This AI-driven Data Profiler function identifies the category of your keywords and return more keywords of the same type!

**Examples:**
- `similarValues("Coca-cola", "Fanta", "Sprite")` returns: "Sunkist", "Crush", "Schweppes", "Mirinda", "7UP", "Dr. Pepper"
- `similarValues("polyethylene", "polystyrene", "neoprene", "nylon", "silicone", "polyisoprene")` returns: "polyurethane", "polyvinyl chloride", "polypropylene"

---

## Test Data Pro FAQ

Understand Test Data Pro AI features, including AI consent settings, data storage, opt-out behavior, data generation limits, caching, and best practices for confidential test data.

**Use when**: Understanding Test Data Pro AI features or configuring AI consent settings, data storage, opt-out behavior, and data generation limits.

### What Type of AI is Being Utilized for Test Data Generation?

BlazeMeter utilizes Microsoft Cognitive Services. The AI-driven features employ OpenAI's services.

### How Can I Determine if AI Features are Enabled or Disabled? Whom Should I Contact?

For inquiries concerning account-wide AI consent settings, consult your organization's BlazeMeter account administrator.

When you start the Data Creation Wizard, a global toggle element indicates whether the AI features are enabled or not. If your Admin disables the AI features, the Data Profiler and Test Data Creator continue to work, but only the standard rule-based functions remain available.

### How Do I Opt Out of or Opt In to These AI-Driven Features?

Your BlazeMeter Account administrators determine whether the account opts in or opts out in the global **Account Settings**.

### What Type of Uploaded Data Does Perforce Store?

BlazeMeter stores all data in your test data model within your workspace, which you have full control over: CSV files are stored as individual files, and function parameters are stored as test parameters.

### What are the AI Features for Test Data Generation?

The BlazeMeter test data integration has the capability to provide more accurate data profiling, as well as a wider range of generated data. OpenAI usage conditions are applicable, implying that test data generated by the AI service might include inaccuracies or unintended content beyond our control.

**AI-driven test data generation is useful in the following situations:**
- I have a CSV file with examples and need more of the same type
- I can describe the kind of test data I need
- I can name the category, but I have no examples
- I have examples, but I can't name the category

### What Happens if I Choose to Opt Out Later? Do Tests that Depend on the AI-Driven Data Creator Functions Suddenly Cease to Function?

No, these tests do not stop working after opting out. AI functions tied to user consent are only utilized when *generating* test data, and the results are cached. That's the extent of it.

Additionally, there are other AI functions that don't require user data, and therefore, they consistently function with your tests. Disabling the AI features does not impact the non-AI parts of the Data Creation Wizard.

### Do These Features Require Additional Setup, Training, or Configuration?

No, the user interface guides you. [User training](https://university.blazemeter.com/learn/courses/512/test-data-pro) for Test Data Pro is available, but not required.

### Could the Test Data Generated by AI be Too 'Real'?

The generated test data is plausible and in a valid format, yet fictional. On the surface, the test data generators offer authentic-seeming data, such as real city names, ZIP codes, first names, last names, banks with RSSD IDs, and more. For instance, it can produce data that resembles actual credit card numbers or Social Security Numbers (SSNs) by employing the publicly-known formulas.

However, at a granular level, the generated test data is fabricated in the sense that it does not consist of personally identifiable information (PII). Random names, credit card numbers, addresses, phone numbers, SSNs, and the like, are independently generated and are not linked to any specific individual. Any resemblance to real persons is purely coincidental.

### What are the Best Practices Concerning Confidential Test Data?

Only submit anonymized data for profiling. For testing, utilize exclusively anonymized or synthetic data. Avoid employing production data or any content that comprises confidential or personally identifiable information (PII) as test data. This guideline extends to CSV files and sample data uploaded to the Data Profiler and Test Data Creator as well: Refrain from uploading files that include confidential data or PII.

### Does the Data Creation Wizard Return Different Output When AI is Enabled and When Not?

If you cancel the AI enablement, the Data Profiler and Test Data Creator continue to work, and only their built-in rules-based suggestions remain activated.

### What are the Limits (Number of Rows)? How Long Does it Take to Generate Large Amounts of AI-Driven Test Data?

There is no limit to the number of rows. There is only a time limit of 5 minutes. You can generate as large an amount as can be transmitted from the AI service in 5 minutes.

### Does BlazeMeter Send a Request for Each Data Row? How Long are the AI-Generated Values Cached? How Many Data Rows are Cached?

BlazeMeter does not send a request for each individual data row. Rather, it retrieves 10 rows per each request. AI-generated values are not subject to caching. If necessary, BlazeMeter directly save these values into the test data model.

### Can I Utilize Data Parameters in AI Functions like `anySeedlist()` and `similarValues()`?

Yes.

### Can We Customize or Fine-Tune the ML (Machine Learning) Models for Our Specific Needs?

No, the models are pretrained.

---

## Documentation References

For detailed information about Test Data Pro, use the BlazeMeter MCP help tools:

**Test Data Pro**:
- **Category**: `root_category`
- **Subcategory**: `guide`
- **Help ID**: `test-data-pro` (Test Data Pro), `test-data-pro-faq` (FAQ)
- **Read help**: Use `blazemeter_help` with action `read_help_info`, args: `{"category_id": "root_category", "subcategory_id": "guide", "help_id_list": ["test-data-pro", "test-data-pro-faq"]}`

