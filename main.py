import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def main():
    filename = './notebooks/note.ipynb'
    with open(filename) as file:
        nb_in = nbformat.read(file, nbformat.NO_CONVERT)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb_in)


if __name__ == '__main__':
    main()
