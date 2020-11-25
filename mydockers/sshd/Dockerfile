FROM arm32v6/alpine:latest

# add openssh and clean
RUN apk add --update openssh \
&& rm  -rf /tmp/* /var/cache/apk/*
# add entrypoint script
ADD docker-entrypoint.sh /usr/local/bin
#make sure we get fresh keys
RUN rm -rf /etc/ssh/ssh_host_rsa_key /etc/ssh/ssh_host_dsa_key
RUN sed -i -E 's/^root.*$/root:$6$A6poINBsKceAi3RD$gIMPsdw12v0q7xsPpfuRiGs75I5qba.WXewZB9I1\/Qb2aIGylES7miXy4qjI0PtiMKNiYvOcE1hRui9.gqwvc\/:18540:0:::::/g' /etc/shadow

RUN ["chmod","+x","/usr/local/bin/docker-entrypoint.sh"]
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
RUN sed -i -E 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

CMD ["/usr/sbin/sshd","-D"]
