FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN apt-get -y update && apt-get -y install wget

RUN apt-get -y install gcc samtools openjdk-8-jre
ENV NSLOTS 4

# -----------------------------------------

# install BBTools


ADD bbmap_version /kb/module/

WORKDIR /kb/module

RUN BBMAP_VERSION=$(cat /kb/module/bbmap_version) \
    && BBMAP=BBMap_$BBMAP_VERSION.tar.gz \
    && wget -O $BBMAP https://sourceforge.net/projects/bbmap/files/$BBMAP/download \
    && tar -xf $BBMAP \
    && rm $BBMAP

# build BBTools small C-lib
RUN cd /kb/module/bbmap/jni \
    && make -f makefile.linux

COPY --from=metabat/metabat /usr/local/bin/jgi_summarize_bam_contig_depths /usr/local/bin/

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
