import os  

def test_mpi(num_rank):
    file = 'qutrunk/test/gate/mpi/'

    for root, dirs, files in os.walk(file):
        if root != file:
            break

        for file in files:
            if file == 'main.py':
                continue
            path = os.path.join(root, file)
            cmd = "mpiexec -n {} python {}".format(num_rank, path)
            os.system(cmd)

if __name__ == "__main__":
    test_mpi(2)