using System.Text.Json;
using System.Text.Json.Serialization;
//using ToonFormat;

// Request request = new(
//     Context: "The essay discusses the impact of climate change on polar bear populations, highlighting recent research findings and conservation efforts.",
//     CriteriaItems:
//     [
//         new CriteriaItem("Clarity", "The text should be clear and easy to understand."),
//         new CriteriaItem("Relevance", "The content should be relevant to the topic of climate change and polar bears."),
//         new CriteriaItem("Evidence", "The text should provide evidence to support its claims."),
//         new CriteriaItem("Organization", "The information should be well-organized and logically structured."),
//         new CriteriaItem("Grammar", "The text should be free from grammatical errors.")
//     ]
// );

string json = @"
{
    ""Context"": ""The essay discusses the impact of climate change on polar bear populations, highlighting recent research findings and conservation efforts."",
    ""CriteriaItems"": [
        { ""Criteria"": ""Clarity"", ""Description"": ""The text should be clear and easy to understand."", ""weight"": 0.4 },
        { ""Criteria"": ""Relevance"", ""Description"": ""The content should be relevant to the topic of climate change and polar bears."", ""weight"": 0.2 },
        { ""Criteria"": ""Evidence"", ""Description"": ""The text should provide evidence to support its claims."", ""weight"": 0.2 },
        { ""Criteria"": ""Organization"", ""Description"": ""The information should be well-organized and logically structured."", ""weight"": 0.1 },
        { ""Criteria"": ""Grammar"", ""Description"": ""The text should be free from grammatical errors."", ""weight"": 0.1 }
    ]
}
";
Request request = JsonSerializer.Deserialize<Request>(json)!;

var response = await EvaluateRubricAsync(request);
Console.WriteLine("Evaluation Response:");
JsonSerializerOptions jsonSerializerOptions = new() { WriteIndented = true };
Console.WriteLine(JsonSerializer.Serialize(response.Result, jsonSerializerOptions));


/// <summary>
/// Evaluates a give text against specified criteria.
/// </summary>
/// <param name="request">The request containing the text and criteria items.</param>
/// <returns>A task that represents the asynchronous operation. The task result contains the evaluation response.</returns>
async Task<Response> EvaluateRubricAsync(Request request)
{
  const string promptTemplate = @"Evaluate the given text against the following criteria: 
<CRITERIA_LIST>

Text to evaluate:
```text
<CONTEXT>
```

Evaluation rules:
- Evaluate each criterion on a scale from 0 to 5, where 0 means 'does not meet the criterion at all' and 5 means 'fully meets the criterion'. Provide a brief rationale for each score.
- Use the weights provided for each criterion to calculate a weighted score.
- Provide the sum of all weighted scores and a rationale based on the individual criterion scores.

No epilogue or prologue. Respond in the following JSON format only:
{
    ""context"": string,
    ""overallWeightedScore"": number (0-5),
    ""scoreRationale"": string,
    ""criteriaScores"": [
        <CRITERIA_OBJECTS>
    ]
}
";

  var criteriaList = string.Join("\n", request.CriteriaItems.Select(ci => $"- {ci.Criteria} ({ci.Weight}): {ci.Description}"));
  var criteriaJSONObjects = string.Join(",\n        ", request.CriteriaItems.Select(ci => $@"{{
            ""criteria"": ""{ci.Criteria}"",
            ""weight"": {ci.Weight},
            ""score"": number (0-5),
            ""weightedScore"": number (0.0-5.0),
            ""scoreRationale"": string
        }}"));
  //string toon = Toon.Encode(request.CriteriaItems);


  var prompt = promptTemplate.Replace("<CRITERIA_LIST>", criteriaList)
                             .Replace("<CONTEXT>", request.Context)
                             .Replace("<CRITERIA_OBJECTS>", criteriaJSONObjects);

  Console.WriteLine($"Generated Prompt:\n{prompt}");
  File.WriteAllText("prompt.txt", prompt);
  await Task.Delay(100); // Simulate async work


  // TODO: Replace this mock response with actual call to an LLM
  const string mockResponse = @"
{
  ""context"": ""Evaluation of a technical document for clarity and relevance."",
  ""overallWeightedScore"": 4,
  ""scoreRationale"": ""The document is well-structured and mostly clear, with minor issues in grammar."",
  ""criteriaScores"": [
    {
      ""criteria"": ""Clarity"",
      ""score"": 4,
      ""weightedScore"": 1.6,
      ""scoreRationale"": ""The content is generally clear, but some sentences are overly complex.""
    },
    {
      ""criteria"": ""Relevance"",
      ""score"": 5,
      ""weightedScore"": 1.0,
      ""scoreRationale"": ""All sections are highly relevant to the topic.""
    },
    {
      ""criteria"": ""Evidence"",
      ""score"": 3,
      ""weightedScore"": 0.6,
      ""scoreRationale"": ""Some claims lack supporting data or references.""
    },
    {
      ""criteria"": ""Organization"",
      ""score"": 4,
      ""weightedScore"": 0.4,
      ""scoreRationale"": ""Logical flow is maintained, but headings could be more descriptive.""
    },
    {
      ""criteria"": ""Grammar"",
      ""score"": 4,
      ""weightedScore"": 0.4,
      ""scoreRationale"": ""Minor grammatical errors detected, but overall readable.""
    }
  ]
}";

  // Create a JSON dynamic object to represent the response
  var jsonResponse = JsonSerializer.Deserialize<dynamic>(mockResponse);
  return new Response(jsonResponse);
}

/// <summary>
/// Lists the properties of an object and their values.
/// </summary>
record CriteriaItem(
  [property: JsonPropertyName("criteria")] string Criteria,
  [property: JsonPropertyName("description")] string Description,
  [property: JsonPropertyName("weight")] double Weight = 0.0
);

/// <summary>
/// Request to evaluate text against criteria.
/// </summary>
record Request(
  [property: JsonPropertyName("context")] string Context,
  [property: JsonPropertyName("criteriaItems")] IEnumerable<CriteriaItem> CriteriaItems
);

/// <summary>
/// Response from the evaluation.
/// </summary>
record Response(
  [property: JsonPropertyName("result")] dynamic? Result
);
