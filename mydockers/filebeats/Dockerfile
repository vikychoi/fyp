FROM docker.elastic.co/beats/filebeat:7.10.1
USER filebeat
COPY --chown=filebeat filebeat.yml /usr/share/filebeat/filebeat.yml
RUN chmod go-w /usr/share/filebeat/filebeat.yml

