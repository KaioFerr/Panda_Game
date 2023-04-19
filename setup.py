import cx_Freeze

executables = [cx_Freeze.Executable('Panda_Game.py')]
cx_Freeze.setup(

    name = "Panda Game",
    options = {'build_exe': {'packages': ['pygame'],
                             'include_files': ['imagem', 'sons']}},
    executables = executables

)