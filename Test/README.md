The test data in this directory is managed using [git-lfs](https://git-lfs.github.com/).

Download all data with

    > git lfs pull --exclude=

New data should be added with the following sequence:

    > git lfs track Test/Baseline/NEWDATA.ext
    > git add Test/Baseline/NEWDATA.ext
    > git add .gitattributes
    > git commit

To run the test from the Slicer extension build directory, use `ctest`. To run the test on the command-line,
see the top level README.
