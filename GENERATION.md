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
