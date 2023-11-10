# OpenAI - Common Use Cases

## Common Use Cases

- Summarization & Risk Analysis
- Recommendation system
- Language Translation
- Content generation and Personalization
- Prompting and completion from your own content

### Language Translation

OpenAI can be used to develop language translation models that can translate text from one language to another.

```mermaid
flowchart LR
  A((Start))-->B([Add text<br/>to be translated])
  B-->O([Prompt<br/>OpenAI API])
  classDef blue fill:blue,color:#fefefe
  class A,B,O blue
```

Jupyter notebook:

- [Translation](https://github.com/msalemor/openai-use-cases/blob/main/notebooks/translation.ipynb)

Examples:

```python
source_language = languageCodes["en"]  # English
target_language = languageCodes["es"]  # Spanish
target_text = mock_get_extract_language("en")

prompt = f'Translate the text from {source_language} to {target_language}.\n[context]\n{target_text}'
```

> Prompt:<br/>Translate the following text from English to Spanish: Azure Container Apps is a fully managed environment that enables you to run microservices and containerized applications on a serverless platform. Common uses of Azure Container Apps include:<br/>- Deploying API endpoints<br/>- Hosting background processing applications<br/>- Handling event-driven processing<br/>- Running microservices<br/><br/>Completion:<br/>Azure Container Apps es un entorno completamente administrado que le permite ejecutar microservicios y aplicaciones en contenedores en una plataforma sin servidor. Los usos comunes de Azure Container Apps incluyen:<br/>- Desplegar puntos finales de API<br/>- Alojar aplicaciones de procesamiento en segundo plano<br/>- Manejar procesamiento impulsado por eventos<br/>- Ejecutar microservicios.

### Content Generation & Personalization

OpenAI can be used to develop personalized content and experiences for users based on their interests and behavior.

```mermaid
flowchart LR
  A((Start))-->B([Get structured<br/>properties])
  B-->D([Build a simple description<br/>from the properties])
  D-->O([Prompt<br/>OpenAI API])
  classDef blue fill:blue,color:#fefefe
  class A,B,D,O blue
```

Examples:

```python
car = mock_get_car()
car_description = get_car_description(car)

prompt = f'Create a one paragraph sales description that includes the price for a {car_description}'
```

Jupyter notebook:

- [Content generation](https://github.com/msalemor/openai-use-cases/blob/main/notebooks/personalization.ipynb)

> Prompt:<br/>Get a full sales description for a used very good condition red 2020 Ford Explorer<br/><br/>Completion:<br/>This used 2020 Ford Explorer is in very good condition and is a great choice for anyone looking for a reliable and stylish SUV. It has a bold red exterior and a comfortable interior with plenty of room for passengers and cargo. The exterior features a sleek design with a bold grille, LED headlights, and fog lights. The interior is equipped with leather seating, power windows and locks, a power liftgate, and a rearview camera. The 3.5L V6 engine provides plenty of power and the 6-speed automatic transmission ensures smooth shifting. The Ford Explorer also comes with a variety of safety features such as blind spot monitoring, lane keeping assist, and adaptive cruise control. This vehicle is perfect for anyone looking for a reliable and stylish SUV.
