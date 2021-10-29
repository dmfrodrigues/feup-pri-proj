TMP=tmp

EURLEX_DOCUMENT_FILES = eurlex/document-0.json eurlex/document-1000.json eurlex/document-2000.json eurlex/document-3000.json eurlex/document-4000.json \
eurlex/document-5000.json eurlex/document-6000.json eurlex/document-7000.json eurlex/document-8000.json eurlex/document-9000.json \
eurlex/document-10000.json eurlex/document-11000.json eurlex/document-12000.json eurlex/document-13000.json eurlex/document-14000.json \
eurlex/document-15000.json eurlex/document-16000.json eurlex/document-17000.json eurlex/document-18000.json eurlex/document-19000.json \
eurlex/document-20000.json eurlex/document-21000.json eurlex/document-22000.json eurlex/document-23000.json eurlex/document-24000.json \
eurlex/document-25000.json eurlex/document-26000.json eurlex/document-27000.json eurlex/document-28000.json eurlex/document-29000.json \
eurlex/document-30000.json eurlex/document-31000.json eurlex/document-32000.json eurlex/document-33000.json eurlex/document-34000.json \
eurlex/document-35000.json eurlex/document-36000.json eurlex/document-37000.json eurlex/document-38000.json eurlex/document-39000.json \
eurlex/document-40000.json eurlex/document-41000.json eurlex/document-42000.json eurlex/document-43000.json eurlex/document-44000.json \
eurlex/document-45000.json eurlex/document-46000.json eurlex/document-47000.json eurlex/document-48000.json eurlex/document-49000.json \
eurlex/document-50000.json eurlex/document-51000.json eurlex/document-52000.json eurlex/document-53000.json eurlex/document-54000.json \
eurlex/document-55000.json eurlex/document-56000.json eurlex/document-57000.json eurlex/document-58000.json eurlex/document-59000.json \
eurlex/document-60000.json eurlex/document-61000.json eurlex/document-62000.json eurlex/document-63000.json eurlex/document-64000.json \
eurlex/document-65000.json eurlex/document-66000.json eurlex/document-67000.json eurlex/document-68000.json eurlex/document-69000.json \
eurlex/document-70000.json eurlex/document-71000.json eurlex/document-72000.json eurlex/document-73000.json eurlex/document-74000.json \
eurlex/document-75000.json eurlex/document-76000.json eurlex/document-77000.json eurlex/document-78000.json eurlex/document-79000.json \
eurlex/document-80000.json eurlex/document-81000.json eurlex/document-82000.json eurlex/document-83000.json eurlex/document-84000.json \
eurlex/document-85000.json eurlex/document-86000.json eurlex/document-87000.json eurlex/document-88000.json eurlex/document-89000.json \
eurlex/document-90000.json eurlex/document-91000.json eurlex/document-92000.json eurlex/document-93000.json eurlex/document-94000.json \
eurlex/document-95000.json eurlex/document-96000.json eurlex/document-97000.json eurlex/document-98000.json eurlex/document-99000.json \
eurlex/document-100000.json eurlex/document-101000.json eurlex/document-102000.json eurlex/document-103000.json eurlex/document-104000.json \
eurlex/document-105000.json eurlex/document-106000.json eurlex/document-107000.json eurlex/document-108000.json eurlex/document-109000.json \
eurlex/document-110000.json eurlex/document-111000.json eurlex/document-112000.json eurlex/document-113000.json eurlex/document-114000.json \
eurlex/document-115000.json eurlex/document-116000.json eurlex/document-117000.json eurlex/document-118000.json eurlex/document-119000.json \
eurlex/document-120000.json eurlex/document-121000.json eurlex/document-122000.json eurlex/document-123000.json eurlex/document-124000.json \
eurlex/document-125000.json eurlex/document-126000.json eurlex/document-127000.json eurlex/document-128000.json eurlex/document-129000.json \
eurlex/document-130000.json eurlex/document-131000.json eurlex/document-132000.json eurlex/document-133000.json eurlex/document-134000.json \
eurlex/document-135000.json eurlex/document-136000.json eurlex/document-137000.json eurlex/document-138000.json eurlex/document-139000.json

eurlex/document.json: $(EURLEX_DOCUMENT_FILES)
	echo Hello

eurlex/document-%.json: | eurlex
	curl -s http://api.epdb.eu/eurlex/document/?offset=$(*F) --output $@

# Directories
eurlex:
	mkdir -p eurlex

