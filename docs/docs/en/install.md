# install misspy

## prerequisite
misspy supports Python3.8 and above.

Python2 and Python3.7 and earlier are not supported.

## install

!!! If you install the development version
    New features released in future versions will require the development version to be installed until the stable version is released.
    ```
    python3 -m pip install -U misspy --pre
    ```
    Windows users:
    ```
    py -3 -m pip install -U misspy --pre
    ```
The library can be obtained from PyPI.
```
python3 -m pip install -U misspy
```
Windows users:
```
py -3 -m pip install -U misspy
```

# Basic concept
misspy is a mechanism to send API requests by method.

You can start using misspy by specifying at least the instance address.

What is returned by misspy is basically not a dictionary type, you can get the value in a way like javascript dot notation.
```
import misspy

bot = misspy.Bot("mi.example.com")

meta = bot.meta()

print(meta.name)
```