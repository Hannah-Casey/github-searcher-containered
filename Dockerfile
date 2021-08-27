FROM python:3.9.4
ADD github-searcher.py /
WORKDIR /app/src
COPY . .
RUN pip3 install requests
ENTRYPOINT ["python", "./github-searcher.py"]
#CMD ["-u", "-m", "swagger_server"]
#CMD ["python", "./github-searcher.py", "--stratum-size", "100", "--github-token", "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", "--database", "res.db", "--statistics", "stats.csv", "\extension:sol"]



