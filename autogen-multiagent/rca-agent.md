

```mermaid
graph
   start-->I(Incident<br>Extractor)<-->KQP
   I-->C(Classifier)
   C-->Writer
   KQP(KQL<br>Query<br>Planner)<-->Q1
   KQP<-->Q2
```