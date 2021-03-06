.. _build_from_sources:


Build from sources
==================

Install GCC and CMake
----------------------

The main compilation directives are specified using

- `GCC compiler <https://gcc.gnu.org/>`_ to build the binaries
- `CMake <https://cmake.org/>`__ to create the Makefiles


Linux
^^^^^
Both :code:`gcc` :code:`cmake` commands are already installed by default.

Mac OS
^^^^^^

Install Xcode and command line tools
""""""""""""""""""""""""""""""""""""

#. Install the latest release of `Xcode <https://developer.apple.com/download/>`_.

#. Install the command line tools by executing from the terminal

    .. code:: bash

        xcode-select --install

Install CMake via Homebrew
"""""""""""""""""""""""""""

#. Install `Homebrew <https://brew.sh/>`_ and update its packages to the latest version.

#. Install cmake by executing

    .. code:: bash

        brew install cmake


Windows
^^^^^^^
#. Install `TDM 64bit GCC <http://tdm-gcc.tdragon.net/download>`_

#. Install the latest binaries of `CMake <https://cmake.org/download/#latest>`__ for Windows 64bit



Build the binaries
------------------

Run the following commands from the terminal

#. Clone the repository, create :code:`build` directory and change directory

    .. code:: bash

       git clone https://github.com/oxfordcontrol/osqp
       cd osqp
       mkdir build
       cd build


#. Create Makefiles

    - In Linux and Mac OS run

        .. code:: bash

            cmake -G "Unix Makefiles" ..

    - In Windows run

        .. code:: bash

            cmake -G "MinGW Makefiles" ..


#. Compile OSQP

    .. code:: bash

       cmake --build .
