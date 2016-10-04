FROM rickyking/ds-xgboost-anaconda-jupyter

ADD src/*.py /opt/conda/lib/python2.7/site-packages/autostat/
ADD src/autostat3 /usr/bin/
RUN mkdir /work;\
pip install pandas-confusion;

WORKDIR /work
#ENTRYPOINT ["python2.7", "/usr/bin/autostat3"]


