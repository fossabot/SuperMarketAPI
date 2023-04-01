

FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# build container --> docker build -t market-api .
# run container --> docker run -dp 5005:5000 market-api