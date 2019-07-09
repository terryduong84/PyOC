#!/bin/bash
echo ""
echo "=========================================================="
echo "  This is made for oc5P! It relies on the use of f2py3    "
echo "  For other version, incompatibility should be expected!  "
echo "  One may want to change liboctqpy.f90 and libocpy.py     "
echo "  according to new liboctq.F90 and update Makefile-fPIC   "
echo "  to make interface with the new opencalphad version work "
echo "                                                          "
echo "          *!  Interface is made for python3 !*            "
echo "=========================================================="
echo ""

#
# Current build folder 
#
cwd=$(pwd)
#
# Back up original files before build
#
mkdir bak
cp * ./bak
#
# Prepare oc's Makefile with -fPIC flags added to gcc and gfortran
# commands. The -fPIC flags are essential for later use of f2py.
#
# Notes:
#
#       In oc5 there are 2 Makefiles: Makefile and Makefile-nogetkey
#       The used Makefile-nogetkey (below) is the simpler make.
#       One may need to change of the name of makefile when porting
#       this script to newer version of oc.
#
#       Also, when porting to newer oc, make sure the lines and line
#       variables captured in Makefile and in liboctq.F90 later are
#       correct lines to be modified. If there were other line(s)
#       picked up because they share the same pick-up patterns, make
#       them different (e.g. putting extra features/patterns as comments)
#
cd ../
make clean
cp Makefile-nogetkey Makefile-fPIC
lines=($(grep -F -n " -c " Makefile-fPIC | cut -d : -f 1))
for i in "${lines[@]}"
do
    sed -i $i's/ -c / -fPIC -c /'  Makefile-fPIC
done
#
# Compile oc5 and essential libraries
#
make -f Makefile-fPIC
#
# Copy the required libs to build folder
#
cp liboceq* ftinyopen.o tinyopen.o tinyfiledialogs.o $cwd
#
# In liqoctq.F90:
#
#  - Make sure 'character(len=2):: compnamesi' in 'tqgcom' has 
# the same length as 'character elname*2' in 'tqrfil' and 
# 'character selel(*)*2' in 'tqrpfil' for compatibility when 
# passing these variables to 'get_element_data'
#
#  - Also, check 'character(Len=2):: elenames(maxc)' in liqoctqpy.f90 
# (wrapper of liqoctq.F90) for compatible character length
#
#  - Check back above note in case of porting this script to newer oc
#    (make sure the found pattern (below) belong to the tqgcom function)
#
cd $cwd
cp ../TQ4lib/F90/liboctq.F90 ./
line=$(grep -F -n "character*24, dimension(*) :: compnames" liboctq.F90 | cut -d : -f 1) # orig.: 24 in tqgcom()
echo $line
line=$line's/24/2/' # change 24 to 2
echo $line
sed -i $line liboctq.F90
#
# Compile the TQ4 fortran interface: liboctq.F90
#
rm -f *.so liboctq.o liboctq.mod
gfortran -c -fPIC liboctq.F90
#
# Convert fortran interface to python interface
#
# Note:
#
#       liboctqpy.f90 is required for this. It is simply a wrapper 
#       of liboctq.F90 that triggers function calls
#
f2py -c --fcompiler=gnu95 --f90flags=-fPIC ftinyopen.o tinyopen.o tinyfiledialogs.o liboctq.o liboceq.a -m liboctqpy liboctqpy.f90
#
# Postprocess ... Make sure one has libocpy.py and the liboctqpy*.so
#                 in the file build as these are the API interface
#
mkdir lib
mv *.so lib/liboctqpy.so
cp libocpy.py lib
