FROM tiangolo/uwsgi-nginx:python3.7

ENV LISTEN_PORT 8080
EXPOSE 8080

COPY ./app /app
WORKDIR /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

RUN chmod +x ./wait-for-it.sh

CMD ["./wait-for-it.sh", "-h", "10.5.0.5", "db:3306", "--", "/start.sh"]
