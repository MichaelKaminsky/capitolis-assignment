FROM continuumio/miniconda3:4.6.14

COPY . /capitolis-assignment


WORKDIR /capitolis-assignment

RUN conda env create -f environment.yml

RUN echo "source activate base" > ~/.bashrc

ENV PATH /opt/conda/envs/capitolis-assignment/bin:$PATH
ENV PYTHONPATH /capitolis-assignment

CMD python data_pipeline.py

EXPOSE 8080

