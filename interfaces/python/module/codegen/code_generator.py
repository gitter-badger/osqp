# from osqp import __path__
from __future__ import print_function
import osqp
import os.path
import shutil as sh
from subprocess import call
from glob import glob
from platform import system
import sys

# Import time
import time


# import utilities
from . import utils


def codegen(work, target_dir, python_ext_name, project_type, embedded,
            force_rewrite, loop_unrolling):
    """
    Generate code
    """

    # Import OSQP path
    osqp_path = osqp.__path__[0]

    # Path of osqp module
    files_to_generate_path = os.path.join(osqp_path,
                                          'codegen', 'files_to_generate')

    # Module extension
    if system() == 'Linux' or system() == 'Darwin':
        module_ext = '.so'
    else:
        module_ext = '.pyd'

    # Check if interface already exists
    resp = None   # Initialize response
    if os.path.isdir(target_dir):
        if force_rewrite:
            sh.rmtree(target_dir)
        else:
            while resp != 'n' and resp != 'y':
                resp = input("Directory \"%s\" already exists." %
                             target_dir +
                             " Do you want to replace it? [y/n] ")
                if resp == 'y':
                    sh.rmtree(target_dir)

    # Check if python module already exists
    resp = None  # Initialize response
    if any(glob('%s*' % python_ext_name + module_ext)):
        module_name = glob('%s*' % python_ext_name + module_ext)[0]
        if force_rewrite:
            os.remove(module_name)
        else:
            while resp != 'n' and resp != 'y':
                resp = input("Python module \"%s\" already exists." %
                             module_name +
                             " Do you want to replace it? [y/n] ")
                if resp == 'y':
                    os.remove(module_name)

    # Make target directory
    sys.stdout.write("Creating target directories... \t\t\t\t\t")
    sys.stdout.flush()
    target_dir = os.path.abspath(target_dir)
    target_include_dir = os.path.join(target_dir, 'include')
    target_src_dir = os.path.join(target_dir, 'src')

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    if not os.path.exists(target_include_dir):
            os.mkdir(target_include_dir)
    if not os.path.exists(target_src_dir):
        os.makedirs(os.path.join(target_src_dir, 'osqp'))
    print("[done]")

    # Copy source files to target directory
    sys.stdout.write("Copying OSQP sources... \t\t\t\t\t")
    sys.stdout.flush()
    c_sources = glob(os.path.join(osqp_path, 'codegen', 'sources',
                                  'src', '*.c'))
    for source in c_sources:
        if loop_unrolling:
            if source != 'ldl.c':  # Do not copy ldl. We will generate it
                sh.copy(source, os.path.join(target_src_dir, 'osqp'))
        else:
            sh.copy(source, os.path.join(target_src_dir, 'osqp'))

    c_headers = glob(os.path.join(osqp_path, 'codegen', 'sources',
                                  'include', '*.h'))
    for header in c_headers:
        sh.copy(header, target_include_dir)
    print("[done]")

    # Variables created from the workspace
    sys.stdout.write("Generating customized code... \t\t\t\t\t")
    sys.stdout.flush()
    template_vars = {'data':            work['data'],
                     'settings':        work['settings'],
                     'priv':            work['priv'],
                     'scaling':         work['scaling'],
                     'embedded_flag':   embedded,
                     'python_ext_name': python_ext_name}

    if loop_unrolling:
        # Render ldl.c file
        utils.render_ldl(template_vars, os.path.join(target_src_dir,
                                                     'osqp', 'ldl.c'))

    # Render workspace
    utils.render_workspace(template_vars,
                           os.path.join(target_include_dir, 'workspace.h'))

    # Render setup.py
    utils.render_setuppy(template_vars,
                         os.path.join(target_src_dir, 'setup.py'))

    # Render emosqpmodule.c
    utils.render_emosqpmodule(template_vars,
                              os.path.join(target_src_dir,
                                           '%smodule.c' % python_ext_name))

    # Copy example.c
    sh.copy(os.path.join(files_to_generate_path, 'example.c'), target_src_dir)

    # Copy CMakelists.txt
    sh.copy(os.path.join(files_to_generate_path, 'CMakeLists.txt'), target_dir)

    print("[done]")

    # Compile python interface
    sys.stdout.write("Compiling Python wrapper... \t\t\t\t\t")
    sys.stdout.flush()
    current_dir = os.getcwd()
    os.chdir(target_src_dir)
    call(['python', 'setup.py', '--quiet', 'build_ext', '--inplace'])
    print("[done]")

    # Copy compiled solver
    sys.stdout.write("Copying code-generated Python solver to current" +
                     "directory... \t")
    sys.stdout.flush()
    module_name = glob('%s*' % python_ext_name + module_ext)
    if not any(module_name):
        raise ValueError('No python module generated! ' +
                         'Some errors have occurred.')
    module_name = module_name[0]
    sh.copy(module_name, current_dir)
    os.chdir(current_dir)
    print("[done]")



    # python setup.py build_ext --inplace --quiet


    # Generate project
    # cwd = os.getcwd()
    # os.chdir(target_dir)
    # call(["cmake", "-DEMBEDDED=%i" % embedded, ".."])
    # os.chdir(cwd)

    #render(target_src_dir, template_vars, 'osqp_cg_data.c.jinja',
    #       'osqp_cg_data.c')
    #render(target_dir, template_vars, 'example_problem.c.jinja',
    #       'example_problem.c')
