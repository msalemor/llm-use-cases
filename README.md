# OpenAI - Common Use Cases

## Common Use Cases

- Summarization & risk Analysis
- Recommendation system
- Language transation
- Content generation and Personalization
- Prompting and complition from your own content

### Summarization, Risk Analysis, Action Items

```mermaid
flowchart LR
  A((Start))-->B([Add text to<br/>be analyzed as context])
  B-->O([Prompt<br/>OpenAI API])
  classDef blue fill:blue,color:#fefefe
  class A,B,O blue
```

Jupyter notebook:

- [Analysis](https://github.com/msalemor/openai-use-cases/blob/main/notebooks/analysis.ipynb)

Examples:

```python
contract = mock_get_contract("LEASE_AGREEMENT")
prompt = f'Summarize and list risks.\n[context]\n{contract}'
```

- Sample 1:

  > Prompt:<br/>Summarize and list risks.<br/><br/>Content:<br/>RESIDENTIAL LEASE AGREEMENT<br/>
  > RENT. The Tenant shall pay to Landlord the sum of $1,500 per month (hereinafter referred to as "Rent") for the duration of the Term of the Lease. The Rent shall be payable on or before every day of the month (hereinafter referred to as the "Due Date"), notwithstanding that the said date falls on a weekend or holiday.<br/>
  > A. Late Rent. If Rent is not paid within days of the Due Date, the Rent shall be considered past due, and a late fee of a $50 or 5% of the Rent past due shall be applied for every day Rent is late or O occurrence Rent is late.<br/>B. Returned Checks. In the event that a check intended as payment for Rent is dishonored for whatever reason, the same shall be considered as Late Rent with the late fee being payable on the same.<br/><br/>Completion:<br/>Summary:<br/>The residential lease agreement states that the tenant must pay $1,500 per month on or before the due date, with a late fee of $50 or 5% of the rent past due if payment is not made within days of the due date. If a check intended as payment is dishonored, it will also be considered as late rent with the late fee being payable on the same.<br/>Risks:<br/>- Risk of incurring late fees if rent is not paid on time.<br/>- Risk of incurring additional fees if a check intended as payment is dishonored.<br/>- Risk of potential legal action if rent is consistently paid late or not at all.

- Sample 2:
  > Prompt:<br/>What is my best investment?<br/><br/>Context:<br/>Portfolio:<br/>- 100 shares of MSFT at $100. Today's price is $295.<br/>- 100 shares of TSLA at $1000. Today's price is $153.<br/><br/>Completion:<br/>Based on the current prices, your best investment would be the 100 shares of MSFT that you own. The value of your MSFT shares has increased significantly since you purchased them, and they are now worth $29,500 (100 shares x $295 per share), compared to the $10,000 you originally invested. On the other hand, your TSLA shares have decreased in value and are now worth $15,300 (100 shares x $153 per share), which is a loss of $84,700 from your original investment of $100,000. However, it's important to note that past performance is not a guarantee of future results, and it's always a good idea to do your own research and consult with a financial advisor before making any investment decisions.

### Recommendation System

OpenAI can be used to develop recommendation systems that can suggest products, services, or content to users based on their preferences and behavior.

```mermaid
flowchart LR
  A((Start))-->B{From curated<br/>content}
  B--No-->O([OpenAI])
  B--Yes-->D([Add curated<br/>content as context])
  D-->O
  classDef blue fill:blue,color:#fefefe
  class A,B,O,D blue
```

Jupyter notebook:

- [Recommendation](https://github.com/msalemor/openai-use-cases/blob/main/notebooks/recommendation.ipynb)

Examples:

- Without context

```python
prompt = "List the best restaurants in Miami, FL."
```

- With context

```python
target_text=""
for restaurant in mock_get_restaurant_list("MIA"):
    target_text += f"{restaurant}\n"

prompt = f'List two top restaurants in Miami, FL\n{target_text}'
```

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
