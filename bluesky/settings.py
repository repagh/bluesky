# Select the gui implementation. options: 'qtgl', 'pygame'
# Try the pygame implementation if you are having issues with qtgl.
gui = 'qtgl'

# Select the performance model. options: 'bluesky', 'bada'
performance_model = 'bluesky'

# Indicate the datafile path
data_path = 'data'

# Verbose internal logging
verbose = False

# Indicate the logfile path
log_path = 'output'

# Indicate the scenario path
scenario_path = 'scenario'

# Indicate the path for the aircraft performance data
perf_path = data_path + '/coefficients/BS_aircraft'

# Indicate the path for the BADA aircraft performance data (leave empty if BADA is not available)
perf_path_bada = data_path + '/coefficients/BADA'

# Indicate the location of the airport database
airport_file = data_path + '/global/airports.dat'

# Indicate the start location of the radar screen (e.g. [lat, lon], or airport ICAO code)
start_location = 'EHAM'

# Simulation timestep [seconds]
simdt = 0.05

# Snaplog dt [seconds]
snapdt = 30.0

# Instlog dt [seconds]
instdt = 30.0

# Skylog dt [seconds]
skydt = 60.0

# Selective snap log dt [seconds]
selsnapdt = 5.0

# Prefer compiled BlueSky modules (cgeo, casas)
prefer_compiled = True

# Limit the max number of cpu nodes for parallel simulation
max_nnodes = 999

#=========================================================================
#=  ASAS default settings
#=========================================================================

# ASAS lookahead time [sec]
asas_dtlookahead = 300.0

# ASAS update interval [sec]
asas_dt = 1.0

# ASAS horizontal PZ margin [nm]
asas_pzr = 5.0

# ASAS vertical PZ margin [ft]
asas_pzh = 1000.0

# ASAS safety margin [-]
asas_mar = 1.05

#=============================================================================
#=   QTGL Gui specific settings below
#=   Pygame Gui options in /data/graphics/scr_cfg.dat
#=============================================================================

# Radarscreen font size in pixels
text_size = 13

# Radarscreen airport symbol size in pixels
apt_size = 10

# Radarscreen waypoint symbol size in pixels
wpt_size = 10

# Radarscreen aircraft symbol size in pixels
ac_size = 16

# Stack and command line text color
stack_text_color = 0, 255, 0

# Stack and command line background color
stack_background_color = 102, 102, 102

#=========================================================================
#=  Settings for the BlueSky telnet server
#=========================================================================
telnet_port = 8888

#=========================================================================
#=  Configure the following to stream raw data from a mode-s / ADS-B
#=  TCP server.
#=========================================================================

# Mode-S / ADS-B server hostname / ip
modeS_host = ''

# Mode-S /ADS-B server port
modeS_port = 0

# END OF SETTINGS


# Import config settings from settings.cfg if this exists, if it doesn't create an initial config file
def init(gui='ask'):
    import os, sys, shutil
    configfile = 'settings.cfg'
    # If BlueSky is run from a compiled bundle instead of from source, adjust the startup path
    # and change the path of configurable files to $home/bluesky
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
        bsdir = os.path.join(os.path.expanduser('~'), 'bluesky')
        configfile = os.path.join(bsdir, 'settings.cfg')
        if not os.path.isdir(bsdir):
            os.makedirs(os.path.join(bsdir, 'output'))
        if not os.path.isdir(os.path.join(bsdir, 'scenario')):
            shutil.copytree('scenario', os.path.join(bsdir, 'scenario'))
        if not os.path.isfile(os.path.join(bsdir, 'settings.cfg')):
            with open('settings.cfg', 'r') as fin, \
                 open(os.path.join(bsdir, 'settings.cfg'), 'w') as fout:
                for line in fin:
                    if line[:8] == 'log_path':
                        line = "log_path = '" + os.path.join(bsdir, 'output').replace('\\', '/') + "'"
                    if line[:13] == 'scenario_path':
                        line = "scenario_path = '" + os.path.join(bsdir, 'scenario').replace('\\', '/') + "'"
                    fout.write(line + '\n')

    for i in range(len(sys.argv)):
        if sys.argv[i] == '--config-file':
            configfile = sys.argv[i + 1]
            break

    if not os.path.isfile(configfile):
        print
        print 'No config file settings.cfg found in your BlueSky starting directory!'
        print
        print 'This config file contains several default settings related to the simulation loop and the graphics.'
        print 'A default version will be generated, which you can change if necessary before the next time you run BlueSky.'
        print
        if gui == 'ask':
            print 'BlueSky has several user interfaces to choose from. Please select which one to start by default.'
            print 'You can always change this behavior by changing the settings.cfg file.'
            print
            print '1. QtGL:    This is the most current interface of BlueSky, but requires a graphics card that supports at least OpenGL 3.3.'
            print '2. Pygame:  Use this version if your pc doesn\'t support OpenGL 3.3.'
            print '3. Console: Run a console-only version of BlueSky. This is useful if you want to do batch simulations on a remote server.'
            print
            ans = input('Default UI version: ')
            if ans == 1:
                gui = 'qtgl'
            elif ans == 2:
                gui = 'pygame'
            elif ans == 3:
                gui = 'console'
        lines = ''

        with open(os.path.dirname(__file__).replace("\\", "/") + '/settings.py') as fin:
            line = fin.readline().strip('\n')
            while line[:5] != '# END':
                lines += line + '\n'
                line = fin.readline().strip('\n')

        with open(configfile, 'w') as fout:
            fout.write(lines)
    else:
        print 'Reading config from settings.cfg'

    execfile(configfile, globals())
    if not gui == 'ask':
        globals()['gui'] = gui
