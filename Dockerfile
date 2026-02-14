FROM ubuntu:latest
LABEL authors="andrejlesnov"

ENTRYPOINT ["top", "-b"]