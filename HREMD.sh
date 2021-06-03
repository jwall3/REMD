#!/bin/bash
module load gcc
module load mpiP/3.4.1/gcc493

export PATH=/home/project/13001327/stuwilli/Software/plumed-2.6.1/bin:$PATH
export LD_LIBRARY_PATH=/home/project/13001327/stuwilli/Software/plumed-2.6.1/lib:$LD_LIBRARY_PATH

export PATH=/home/project/13001327/stuwilli/Software/gromacs-2019/bin:$PATH

# mdrun_mpi
export PATH=/home/project/13001327/stuwilli/Software/gromacs-2019_mpi/bin:$PATH

### RUN EM AND NVT on 1.
mpirun mdrun_mpi -v -deffnm em -plumed plumed.dat -dlb no >stdout.$PBS_JOBID
mpirun mdrun_mpi -v -deffnm nvt -plumed plumed.dat  -dlb no >stdout.$PBS_JOBID

### CREATE THE REPLICAS
# 9 Replicas
nrep=9
# "effective" temperature range
tmin=300
tmax=1000


# clean dir
rm -fr \#*
rm -r R*

for((i=0;i<nrep;i++))
do
 echo this is i $i
# move to dir
 mkdir R$i;cp aladi_si.gro R$i;cp nvt* R$i;cp em* R$i; cp md* R$i;cp npt* R$i;cp processed.top R$i;cp plumed.dat R$i
done

python3 lamda.py

for((i=0;i<nrep;i++))
do
 echo this is i $i
 cd R$i
# process topol
  grep -v "mpiP:" topol$i.top > topol__$i.top;grep -v "MPI startup" topol__$i.top > topol_$i.top
  gmx grompp -f nvt.mdp -c nvt.gro -p topol_$i.top -o md.tpr
 cd ..
done
######RUN REMD
mpirun -np 9 mdrun_mpi -v  -deffnm md -plumed plumed.dat -multidir R0 R1 R2 R3 R4 R5 R6 R7 R8 -replex 100 -nsteps 15000000000 -maxh 1 -hrex -dlb no >stdout.$PBS_JOBID
