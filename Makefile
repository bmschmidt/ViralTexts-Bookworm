
all: bookwormdatabase

input.txt: cl20-flover08-rep4.clinfo.gz

cl20-flover08-rep4.clinfo.gz:
	scp bschmidt@discovery4.neu.edu:/home/dasmith/work/locca/c19-b71-moa/pairs-n5u100m10/save/cl20-flover08-rep4.clinfo.gz .

bookworm:
	git clone git@github.com:bmschmidt/Presidio $@

bookwormdatabase: bookworm/files/metadata/jsoncatalog.txt bookworm/files/texts/input.txt bookworm/files/metadata/field_descriptions.json
	cd bookworm; make;

input.txt: jsoncatalog.txt

jsoncatalog.txt:
	python parseTexts.py cl20-flover08-rep4.clinfo.gz

newspaperdata.txt:
	sed 's/paper\t/name\t/g' /raid/ChronAm/newspaperdata.txt > $@

betterMetadata: newspaperdata.txt
	cd bookworm; python OneClick.py supplementMetadataFromTSV ../newspaperdata.txt
