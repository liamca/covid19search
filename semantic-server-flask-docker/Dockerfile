FROM ubuntu:18.04

COPY CMakeLists.txt ./
COPY AnnService ./AnnService/
COPY Test ./Test/
COPY Wrappers ./Wrappers/

RUN apt-get update && apt-get install -y python3-pip && apt-get install -y vim  && apt install -y git && apt install -y cython3 && apt-get -y install wget build-essential \
    # remove the following if you don't want to build the wrappers
    openjdk-8-jdk python3-pip swig

# cmake >= 3.12 is required
RUN wget "https://github.com/Kitware/CMake/releases/download/v3.14.4/cmake-3.14.4-Linux-x86_64.tar.gz" -q -O - \
        | tar -xz --strip-components=1 -C /usr/local

COPY boost/boost_1_67_0.tar.gz /
# specific version of boost
RUN wget "https://dl.bintray.com/boostorg/release/1.67.0/source/boost_1_67_0.tar.gz" -q -O - \
        | tar -xf boost_1_67_0.tar.gz && \
        cd boost_1_67_0 && \
        ./bootstrap.sh && \
        ./b2 install && \
        # update ld cache so it finds boost in /usr/local/lib
        ldconfig && \
        cd .. && rm -rf boost_1_67_0 && rm boost_1_67_0.tar.gz

# build
RUN mkdir build && cd build && cmake .. && make && cd ..

# so python can find the SPTAG module
ENV PYTHONPATH=/Release

COPY ./requirements.txt /
RUN pip3 install --upgrade cython
RUN pip3 install -r /requirements.txt

RUN python3 -m spacy download en_core_web_sm

COPY ./web-app/ /

COPY ./data/ /data/

EXPOSE 80
ENTRYPOINT ["python3"]
CMD ["app.py"]
