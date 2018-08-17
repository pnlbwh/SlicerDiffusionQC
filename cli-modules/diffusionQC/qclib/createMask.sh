#!/bin/bash 

set -x

usage()
{
cat << EOF
Usage:
    createMask.sh [-u <.exe>] [-c <.exe>] [-b <.exe>] [-i <imageFile>] 
                  [-o <outDir>] [-p <outPrefix>] [-e <threshold [0,1]>] [-f <imageFormat>]

Creates a mask for DWI
Options:
-h          help

-u  <path>      path/to/unu.exe
-b  <path>      path/to/bet.exe
-c  <path>      path/to/ConvertBetweenFileFormats.exe

-i  <image>     .nrrd or .nii or .nii.gz  
-p  <prefix>    output file prefix        force a re-run even if a subject folder already exists
-o  <outDir>    output directory
-e  <float>     threshold in [0,1] for bet, small threshold gives tighter mask 
-f  <format>    .nrrd or .nii
EOF
}


while getopts "hu:c:b:i:p:o:e:f:" OPTION; do
    case $OPTION in
        h) usage; exit 1;;
        u) unu=$OPTARG ;;
        c) ConvertBetweenFileFormats=$OPTARG ;;
        b) bet=$OPTARG ;;
        i) dwi=$OPTARG ;;
        p) prefix=$OPTARG ;;
        o) outDir=$OPTARG ;;
        e) eta=$OPTARG ;;
        f) format=$OPTARG ;;
    esac
done

cd $outDir

tmpbse=$prefix-bse.nrrd

if [ $format == "nrrd" ]
then

	# For unu, .nrrd files are mandatory
	# Extracting b0 image
	unu slice -a 3 -p 0 -i $dwi -o $tmpbse

	ConvertBetweenFileFormats $tmpbse $tmpbse.nii.gz

	# Bet generates output as ${prefix}_mask.nii.gz
	# Change the threshold that follows -f
	bet $tmpbse.nii.gz $prefix -m -n -f 0.25 -R

	rm $tmpbse $tmpbse.nii.gz $prefix.nii.gz


else

	bet $dwi $prefix -m -n -f $eta -R

fi


set +x




