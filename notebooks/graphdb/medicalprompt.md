## Data

```text
Patient John Doe
John Doe, a 45-year-old male, has undergone multiple medical tests. On January 15, 2023, John had a Blood Test, specifically a Complete Blood Count, which yielded normal results. This test is crucial for evaluating overall health and detecting a variety of disorders, including anemia, infection, and many other diseases. Additionally, John underwent a Chest X-Ray on March 10, 2023, which showed no abnormalities. Chest X-Rays are typically used to diagnose conditions affecting the chest, its contents, and nearby structures. The results from both tests indicate that John Doe is in good health, with no immediate concerns arising from these examinations.

Patient Jane Smith
Jane Smith, a 37-year-old female, also had a Blood Test on February 20, 2023. Unlike John Doe, Jane's Blood Test results indicated high cholesterol levels. High cholesterol is a significant risk factor for cardiovascular diseases, including heart attack and stroke. This result suggests that Jane may need to make lifestyle changes or consider medical interventions to manage her cholesterol levels and reduce her risk of developing heart-related conditions.

Patient Alice Johnson
Alice Johnson, a 29-year-old female, underwent a Brain MRI on April 5, 2023. The MRI results indicated a mild concussion. Brain MRIs are highly detailed imaging tests used to diagnose brain injuries, tumors, and other neurological conditions. A mild concussion, while not typically life-threatening, can have significant short-term and long-term effects on cognitive function and overall well-being. Alice may require follow-up care and monitoring to ensure a full recovery and to prevent any potential complications.
```

## Prompt

```text
system:
You are an AI that can determine the relationships give a text related to patient information, tests, and test results. 

Rules:
- A patient may have more than one test
- Write the neo4j to create the entities and the relationships

user:
<TEXT>
```

## Result

```text
// Create Patients
CREATE (john:Patient {name: 'John Doe', age: 45, gender: 'male'})
CREATE (jane:Patient {name: 'Jane Smith', age: 37, gender: 'female'})
CREATE (alice:Patient {name: 'Alice Johnson', age: 29, gender: 'female'})

// Create Tests
CREATE (bloodTestJohn:Test {type: 'Blood Test', subtype: 'Complete Blood Count', date: date('2023-01-15')})
CREATE (chestXRayJohn:Test {type: 'Chest X-Ray', date: date('2023-03-10')})
CREATE (bloodTestJane:Test {type: 'Blood Test', date: date('2023-02-20')})
CREATE (brainMRI:Test {type: 'Brain MRI', date: date('2023-04-05')})

// Create Test Results
CREATE (bloodTestResultJohn:TestResult {result: 'normal', description: 'Complete Blood Count yielded normal results'})
CREATE (chestXRayResultJohn:TestResult {result: 'no abnormalities', description: 'Chest X-Ray showed no abnormalities'})
CREATE (bloodTestResultJane:TestResult {result: 'high cholesterol', description: 'Blood Test indicated high cholesterol levels'})
CREATE (brainMRIResult:TestResult {result: 'mild concussion', description: 'MRI indicated a mild concussion'})

// Create Relationships
CREATE (john)-[:UNDERWENT]->(bloodTestJohn)
CREATE (john)-[:UNDERWENT]->(chestXRayJohn)
CREATE (jane)-[:UNDERWENT]->(bloodTestJane)
CREATE (alice)-[:UNDERWENT]->(brainMRI)

CREATE (bloodTestJohn)-[:HAS_RESULT]->(bloodTestResultJohn)
CREATE (chestXRayJohn)-[:HAS_RESULT]->(chestXRayResultJohn)
CREATE (bloodTestJane)-[:HAS_RESULT]->(bloodTestResultJane)
CREATE (brainMRI)-[:HAS_RESULT]->(brainMRIResult)
```
