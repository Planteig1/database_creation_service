FROM python:slim

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENV FILEPATH_ROOMS="/app/data/international_names_with_rooms_1000.xlsx"
ENV FILEPATH_DRINKS="/app/data/drinks_menu_with_sales.xlsx"

CMD [ "python", "app.py" ]
