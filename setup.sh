#!/bin/bash 

# Creating a temporary working directory

WORK_DIR=$(mktemp -d)
trap 'echo "Cleaning TMP folder"; rm -rf "$WORK_DIR"' EXIT

# Creating data and output directories 

technologyFolders=("ATAC-Seq" "Chip-Seq" "RNA-Seq")
contentInFolder=("Fastq" "GenomeFasta" "BEDFile" "GenomeIndexFolder")

for dataFolder in "${technologyFolders[@]}";
do
	mkdir -p "data/${dataFolder}"
	mkdir -p "output/${dataFolder}"
	
	for iteratedContent in "${contentInFolder[@]}";
	do
		mkdir -p "data/${dataFolder}/${iteratedContent}"
	done
	
	if [[ "${dataFolder}" == "RNA-Seq" ]];
	then
		mkdir -p "data/${dataFolder}/GTFFiles"
		mkdir -p "data/${dataFolder}/GenomeFasta/mm10"
		mkdir -p "data/${dataFolder}/GenomeFasta/hg38"
	fi
done

# Chip-Seq / ATAC-Seq
# Downloading the genome fasta files 

## For Mouse

wget -P $WORK_DIR https://ftp.ensembl.org/pub/release-100/fasta/mus_musculus/dna/Mus_musculus.GRCm38.dna.primary_assembly.fa.gz
gunzip "$WORK_DIR/Mus_musculus.GRCm38.dna.primary_assembly.fa.gz"

## For Human 

wget -P $WORK_DIR  https://ftp.ensembl.org/pub/release-109/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
gunzip "$WORK_DIR/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"


# Downloading the genome gtf files

## For Mouse

wget -P $WORK_DIR https://ftp.ensembl.org/pub/release-100/gtf/mus_musculus/Mus_musculus.GRCm38.100.gtf.gz
gunzip "$WORK_DIR/Mus_musculus.GRCm38.100.gtf.gz"

## For Human 

wget -P $WORK_DIR https://ftp.ensembl.org/pub/release-109/gtf/homo_sapiens/Homo_sapiens.GRCh38.109.gtf.gz
gunzip "$WORK_DIR/Homo_sapiens.GRCh38.109.gtf.gz"

# RNA-Seq

# Downloading the genome fasta files

## For Mouse

wget -P $WORK_DIR https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M10/GRCm38.primary_assembly.genome.fa.gz
gunzip "$WORK_DIR/GRCm38.primary_assembly.genome.fa.gz"


## For Human 

wget -P $WORK_DIR https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_40/GRCh38.primary_assembly.genome.fa.gz
gunzip "$WORK_DIR/GRCh38.primary_assembly.genome.fa.gz"


# Downloading the genome gtf files

## For Mouse

wget -P $WORK_DIR https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M10/gencode.vM10.annotation.gtf.gz
gunzip "$WORK_DIR/gencode.vM10.annotation.gtf.gz"

## For Human 

wget -P $WORK_DIR https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_40/gencode.v40.annotation.gtf.gz 
gunzip "$WORK_DIR/gencode.v40.annotation.gtf.gz"


# Moving the files into different data folders

for dataFolder in "${technologyFolders[@]}";
do
	if [[ "${dataFolder}" != "RNA-Seq" ]];
	then
		cp "$WORK_DIR/Mus_musculus.GRCm38.dna.primary_assembly.fa" "data/${dataFolder}/GenomeFasta"
		cp "$WORK_DIR/Homo_sapiens.GRCh38.dna.primary_assembly.fa" "data/${dataFolder}/GenomeFasta"
		
		# Using gtf2bed for conversion
		gtf2bed < "$WORK_DIR/Mus_musculus.GRCm38.100.gtf" > "data/${dataFolder}/BEDFile/Mus_musculus.GRCm38.100.bed"
		gtf2bed < "$WORK_DIR/Homo_sapiens.GRCh38.109.gtf" > "data/${dataFolder}/BEDFile/Homo_sapiens.GRCh38.109.bed"
		
	else
		mv "$WORK_DIR/GRCm38.primary_assembly.genome.fa" "data/${dataFolder}/GenomeFasta/mm10"
		mv "$WORK_DIR/GRCh38.primary_assembly.genome.fa" "data/${dataFolder}/GenomeFasta/hg38"
		
		# Copying gtf files to destination
		mv "$WORK_DIR/gencode.vM10.annotation.gtf" "data/${dataFolder}/GTFFiles"
		mv "$WORK_DIR/gencode.v40.annotation.gtf" "data/${dataFolder}/GTFFiles"
		
		# Using gtf2bed for conversion
		gtf2bed < "data/${dataFolder}/GTFFiles/gencode.vM10.annotation.gtf" > "data/${dataFolder}/BEDFile/gencode.vM10.annotation.bed"
		gtf2bed < "data/${dataFolder}/GTFFiles/gencode.v40.annotation.gtf" > "data/${dataFolder}/BEDFile/gencode.v40.annotation.bed" 
	fi

done



exit $?
