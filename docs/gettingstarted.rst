Getting Started
=====================

In this section we provide an overview of how to use the survey simulator. We start by generating a set of 
files containing information on the synethic planetoids that we wish to study. We take you through the process of generating
ephemerides for these synthetic bodiess using OIF (Objects in Field), and show you how to use surveySimPP. 

.. tip::
   In this quick start guide, we demonstrate how to run a single instance of OIF and surveySimPP. Both packages are designed to allow multiple instances to be run in parallel in order to accomodate simulations with very large numbers of synthetic planetesimals by breaking up the job across multiple live proccesses. We recommend first starting with the examples below, before moving on to parallel processing.


.. important::
  All the input files and configuration files used in this demonstation are available in the demo directory within the surveySimPP github repositor (survey_sim_pp/survey_simulator_post_processing/demo). Below includes instructions on how to generate these, but you can skip those setps and go straight to the run commands if you need to.

.. note::
  All input data files in this example are white-space separated format solely for the ease of reading.   

Move to the Correct Directory
---------------------------------
The command line arguments assume that the user is the downloaded surveySimPP directory::
   cd survey_sim_pp/survey_simulator_post_processing

Creating Object Files
-------------------------
The first step in the process is to generate a set of files which describe the orbital and physical parameters
of the objects that we wish to study. Here we will generate a file called 'testorb.des', which contains
the orbits of five objects::

   ObjID t_0 t_p argperi node i e q FORMAT
   6 54800.0 6340.99721 16.4209 45.79141 21.20084 0.67411 5.65043 COM
   632 54800.0 23466.22367 284.5519 217.91073 5.37133 0.4966 6.88417 COM
   6624 54800.0 26018.29348 107.05559 285.0348 22.55248 0.31532 8.0147 COM
   12733 54800.0 -35166.67218 204.92643 193.27826 31.25325 0.68699 7.76983 COM
   28311 54466.0 39984.71835 260.982851 122.344837 2.801063 0.25719962 40.02995082 COM
   39262 54466.0 54670.08858857185 80.463152617168 132.486568373398 18.303864557524 0.6625177539 1.286218727856 COM
   39265 54466.0 54075.567351641024 73.11929900858 314.32320360528 22.761089277031 0.772124864464 0.569263692349 COM
   307764 54466.0 54641.54032677078 102.019078535164 278.124566551661 10.994324503586 0.567173981581 0.504552654462 COM
   356450 54466.0 90480.35745 7.89 144.25849 8.98718 0.09654 33.01305 COM
   387449 54800.0 54026.65733 349.45493 115.41492 11.28725 0.19587 2.48289 COM

We will also generate a file called 'sspp_testset_colours.txt' which contains information about the colour and brightness of the objects::

   ObjID H u-r g-r i-r z-r y-r GS
   6 15.88 1.72 0.48 -0.11 -0.12 -0.12 0.15
   632 14.23 1.72 0.48 -0.11 -0.12 -0.12 0.15
   6624 14.23 1.72 0.48 -0.11 -0.12 -0.12 0.15
   12733 15.75 1.72 0.48 -0.11 -0.12 -0.12 0.15
   28311 7.76 2.55 0.92 -0.38 -0.59 -0.7 0.15
   39262 10.818 1.72 0.48 -0.11 -0.12 -0.12 0.15
   39265 11.678 2.13 0.65 -0.19 -0.14 -0.14 0.15
   307764 25.0 2.13 0.65 -0.19 -0.14 -0.14 0.15
   356450 7.99 2.55 0.92 -0.38 -0.59 -0.7 0.15
   387449 18.92 1.72 0.48 -0.11 -0.12 -0.12 0.15


OIF
-----------
The survey simulator post processing code relies on using an orbital calculator to generate ephemerides,
we recommend using Objects in Field, but you can use any orbital calculator as long as the outputs are 
consistent. Here we give an overview of how to use Objects in Field. If you are using another orbit calculator
then you can skip to the section on using the survey simulator.


Generate an OIF Config File 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The survey simulator post processing code comes with several command line utilities. One of these is 
a config file generator for Objects in Field. makeConfigOIF takes two required parameters, the name of 
the orbit file and the pointing database. There are several optional arguments which can be used to further 
customise your OIF usage. Details of these optional arguments can be seen in inputs.


The most basic OIF config file can be generated by typing::

   makeConfigOIF ./demo/sspp_testset_orbits.des ./demo/baseline_v2.0_1yr.db -no -1 -ndays -1 -camerafov instrument_circle.dat -spkstep 1

This will return the following::

   [CONF]
   cache dir = _cache/sspp_testset_orbits/1-10
   
   [ASTEROID]
   population model = ./demo/sspp_testset_orbits.des
   spk t0 = 60188
   ndays = 395
   object1 = 1
   nobjects = 10
   spk step = 1
   nbody = T
   input format = whitespace
   
   [SURVEY]
   survey database = ./demo/baseline_v2.0_1yr.db
   field1 = 1
   nfields = 216011
   mpcobscode file = obslist.dat
   telescope = I11
   surveydbquery = SELECT observationId,observationStartMJD,fieldRA,fieldDEC,rotSkyPos FROM observations order by observationStartMJD
   
   [CAMERA]
   threshold = 5
   camera = instrument_circle.dat

   output file = stdout
   output format = csv
 
This file will be saved as OIFconfig_test.ini in the directory it has been run within. 

Running OIF
~~~~~~~~~~~~
Now that we have an OIF config file, we can easily run OIF by typing::

   oif -f ./demo/OIFconfig_test.ini > ./demo/test_oif_output.txt
  mv sspp_testset_orbits-01-10.ini OIFconfig_test.ini
   
The first few lines returned will look something like this::

   START HEADER
   [CONF]
   cache dir = _cache/sspp_testset_orbits/1-10
   [ASTEROID]
   population model = ./demo/sspp_testset_orbits.des
   spk t0 = 60188
   ndays = 395
   object1 = 1
   nobjects = 10
   spk step = 1
   nbody = T
   input format = whitespace
   [SURVEY]
   survey database = ./demo/baseline_v2.0_1yr.db
   field1 = 1
   nfields = 216011
   mpcobscode file = obslist.dat
   telescope = I11
   surveydbquery = SELECT observationId,observationStartMJD,fieldRA,fieldDEC,rotSkyPos FROM observations order by observationStartMJD
   [CAMERA]
   threshold = 5
   camera = instrument_circle.dat
   [OUTPUT]
   output file = stdout
   output format = csv
   Survey length:
   Field 1 : 60218.001805555556
   Field n : 60582.99947369435
   Days : 365.0
   END HEADER
   ObjID,FieldID,FieldMJD,AstRange(km),AstRangeRate(km/s),AstRA(deg),AstRARate(deg/day),AstDec(deg),AstDecRate(deg/day),Ast-Sun(J2000x)(km),Ast-Sun(J2000y)(km),Ast-Sun(J2000z)(km),Ast-Sun(J2000vx)(km/s),Ast-Sun(J2000vy)(km/s),Ast-Sun(J2000vz)(km/s),Obs-Sun(J2000x)(km),Obs-Sun(J2000y)(km),Obs-Sun(J2000z)(km),Obs-Sun(J2000vx)(km/s),Obs-Sun(J2000vy)(km/s),Obs-Sun(J2000vz)(km/s),Sun-Ast-Obs(deg),V,V(H=0)
   632,38059,60277.351867,983057302.988296,-27.914,143.141481,0.024483,8.677660,-0.022025,-718755527.053,707115399.940,202146766.832,-9.461,-9.435,-3.858,58803455.841,124187416.914,53827633.096,-28.129,10.565,4.677,8.010336,28.838,8.838
   632,46306,60289.319749,955259166.375772,-25.916,143.290960,-0.003491,8.469810,-0.012344,-728491905.519,697311952.040,198144183.848,-9.369,-9.524,-3.883,28969257.489,132531884.873,57445740.529,-30.037,5.053,2.290,7.422641,28.748,8.748
   632,46328,60289.330920,955234165.662179,-25.887,143.290920,-0.003562,8.469672,-0.012355,-728500949.842,697302758.025,198140435.373,-9.369,-9.524,-3.883,28940272.325,132536748.654,57447949.381,-30.022,5.025,2.287,7.421909,28.748,8.748
   632,48406,60292.334497,948632591.573514,-25.159,143.275797,-0.010595,8.436174,-0.009812,-730929572.603,694827991.907,197131809.209,-9.346,-9.547,-3.889,21194286.022,133717766.728,57960238.222,-30.274,3.559,1.661,7.219795,28.724,8.724
   632,48432,60292.346208,948607150.833510,-25.127,143.275672,-0.010647,8.436059,-0.009824,-730939030.057,694818331.543,197127873.378,-9.346,-9.547,-3.890,21163663.520,133721354.533,57961917.731,-30.254,3.533,1.659,7.218942,28.724,8.724
   632,49105,60293.342276,946459498.864074,-24.881,143.266024,-0.012946,8.426666,-0.008965,-731743091.175,693996357.947,196793023.849,-9.338,-9.554,-3.892,18580786.934,134029746.520,58095614.789,-30.327,3.053,1.450,7.147094,28.715,8.715
   632,50469,60295.348632,942200588.209358,-24.322,143.239649,-0.017554,8.410343,-0.007257,-733360678.321,692338765.443,196118002.537,-9.323,-9.569,-3.896,13361661.832,134524609.291,58310240.323,-30.416,2.061,1.028,6.995151,28.698,8.698


This generates the ephemerides for the objects we are looking for. This information will be used when running the SSPP.
Save this information as a file called 'test_oif_output.txt'.

.. warning::
   Only one instance of OIF can be run per output directory. Make sure to have different output pathways if you are running multiple instances on the same compute node. 
 
surveySimPP
-----------------------------------------

Now that we have the information about the ephemerides, we can begin to run the survey simulator to 
check if these objects are observable by the LSST.

Generate a surveySimPP Config File 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The key information about the simulation paramteres are held in the post processing configuration file.
There is a configuration file generator build into the survey simulator, which can be run using::
   
  makeConfigPP ./demo/PPConfig_test.ini --ephformat csv --trailinglosseson True
 
which will generate a default config file, named config.ini. There are several optional parameters that
can be added (see inputs). The config file will look something like this::

   # Configuration file for Solar System Post Processing package.
   
   
   [INPUTFILES]
   
   # Paths of input files (orbit, colour, cometary, pointing simulation output) 
   # are given at the command line with the following flags:
   # -c or --config                    Input configuration file name
   # -m or --comet                     Comet parameter file name
   # -l or --colour or --color         Colour file name
   # -o or --orbit                     Orbit file name
   # -p or --pointing                  Pointing simulation output file name 
   # -b or --brightness or --phase     Brightness and phase parameter file name
    
   # Type of input ephemerides: default = oif. Options: currently only oif.
   ephemerides_type=oif
   
   # Location of pointing database.
   pointingdatabase = ./demo/baseline_v2.0_1yr.db
   #./data/test/baseline_10yrs_10klines.db 
   #'./data/baseline_v1.3_10yrs.db'# 
   # ./demo/baseline_v2.0_10yrs.db
   
   # Path to camera footprint file, if using.
   footprintPath= ./data/detectors_corners.csv
   
   # Database query for extracting data for pointing database.
   # Change this at your peril!
   ppsqldbquery = SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId
   
   # Input ephemerides format (by separator): csv,whitespace,hdf5
   ephFormat=csv
   
   # Format for orbit/colour/brightness/cometary data files: comma, csv or whitespace
   auxFormat=whitespace
   
   
   #### GENERAL PARAMETERS ####
   
   
   [OBJECTS]
   # Flag for cometary activity. If not none, cometary parameters must be specified at the command line.
   # Options: none, comet. Default: none.
   cometactivity = none
   
   
   [FILTERS]
   
   # Observing filters of interest.
   # Should be given in the following order: main filter in which H is calculated, then 
   # resolved filters. These must have colour offsets specified in physical parameters file.
   # E.g.: if observing filters are r,g,i,z, physical parameters file must have H column 
   # calculated in r, then also 'g-r', 'i-r', 'z-r' columns.
   # Should be separated by comma.
   observing_filters= r,g,i,z
   
   
   [PHASE]
   
   # Define the used input phase function. Options: HG, HG1G2, HG12, linear, none. 
   # Default : HG
   phasefunction = HG
   
   
   [PERFORMANCE]
   
   # Whether trailing loss calculation is switched on. Options: True, False.
   # Relevant for close-approaching NEOs.
   # Default: True.
   trailingLossesOn = True
   
   # Choose between surface area equivalent or actual camera footprint, including chip gaps.
   # Options: circle, footprint.
   # Default: footprint.
   cameraModel = footprint
   
   
   [FILTERINGPARAMETERS]
   
   # Fraction of detector surface area which contains CCD -- simulates chip gaps
   # for the circular footprint. Comment out if using camera footprint. 
   # Default: 0.9.
   # fillfactor = 0.9
   
   # Limit of brightness: detection with brightness higher than this are omitted (assuming saturation).
   # Must be a float.
   # Default == 16.0
   brightLimit = 16.0
   
   # SNR limit: drop observations below this SNR threshold. Omit for default 2.0 SNR cut.
   # Mutually exclusive with the magnitude threshold. Must be a float.
   #SNRLimit = 2.0
   
   # Magnitude threshold: drop observations below this magnitude. Omit for no magnitude cut.
   # Mutually exclusive with the SNR limit. Must be a float.
   #magLimit = 22.0
   
   # Detection efficiency fading function on or off. Uses the fading function as outlined in 
   # Chelsey and Vereš (2017) to remove observations. 
   # Default: True.
   fadingFunctionOn = True
   
   # Width parameter for fading function. Default is 0.1 after Chelsey and Vereš (2017).
   # Should be greater than zero and less than 0.5.
   fadingFunctionWidth = 0.1
   
   # Below are FIVE variables needed to run the SSP linking filter. Comment all
   # five out if you do not wish to run the SSP linking filter.
   
   # SSP detection efficiency. Which fraction of the detections will
   # the automated solar system processing pipeline recognise? Float.
   # Default: 0.95
   SSPDetectionEfficiency = 0.95
   
   # Length of tracklets. How many observations during one night are required to produce 
   # a valid tracklet? Must be an int.
   # Default: 2
   minTracklet = 2
   
   # Number of tracklets for detection. How many tracklets are required
   # to classify as a detection? Must be an int.
   # Default: 3
   noTracklets = 3
   
   # Interval of tracklets (days). In what amount of time does the aforementioned
   # number of tracklets needs to be discovered to constitute a complete detection?
   # Default: 15.0. Must be a float.
   trackletInterval = 15.0
   
   # Minimum separation for SSP inside the tracklet (in arcseconds) to distinguish between 
   # two images to recognise the motion between images.
   # Default: 0.5.
   inSepThreshold = 0.5
   
   
   [GENERAL]
   
   # size of chunk of objects to be processed serially
   sizeSerialChunk = 10
   
   
   [OUTPUTFORMAT]
   
   # Path for output file and stem is given at the command line with the following flags:
   # -u or --outfile                   Output file path.
   # -t or --stem                      Output file stem.
   
   # Output format. Options [csv  | separatelyCSV | sqlite3 | hdf5 ].
   outputformat = csv
   
   # Size of output. Controls which columns are in the output files. 
   # Options are "default" only. More may be added later.
   outputsize = default
   
   # Decimal places RA and Dec should be rounded to in output. Default is 7.
   position_decimals = 7
   
   # Decimal places magnitudes should be rounded to in output. Default is 3. 
   magnitude_decimals = 3
   

Running surveySimPP
~~~~~~~~~~~~~~~~~~~~~~~

Finally, we have all the information required to run the survey simulator. This can be done by typing::

   surveySimPP -c ./demo/PPConfig_test.ini -p ./demo/sspp_testset_colours.txt -o ./demo/sspp_testset_orbits.des -e ./demo/example_oif_output.txt -u ./data/out/ -t testrun_e2e 

The first several lines of  output will look something like::

   ObjID,FieldMJD,fieldRA,fieldDec,AstRA(deg),AstDec(deg),AstrometricSigma(deg),optFilter,observedPSFMag,observedTrailedSourceMag,PhotometricSigmaPSF(mag),PhotometricSigmaTrailedSource(mag),fiveSigmaDepth,fiveSigmaDepthAtSource
   632,60315.2441,141.4554595,8.1858813,142.5089358,8.434994,1.36e-05,r,22.607,22.722,0.084,0.084,23.783,23.771
   632,60315.26793,141.4554595,8.1858813,142.5075236,8.4352135,1.17e-05,i,22.587,22.509,0.09,0.09,23.595,23.583
   632,60322.248,141.0466609,9.4406351,142.0713696,8.5214621,7.9e-06,g,23.138,23.16,0.06,0.06,24.591,24.558
   632,60322.2717,141.0466609,9.4406351,142.0697072,8.5218264,5.9e-06,r,22.762,22.64,0.051,0.051,24.315,24.282
   632,60328.19755,141.6678165,7.1548011,141.64208,8.6235416,1.79e-05,z,22.517,22.556,0.139,0.139,22.962,22.918
   632,60328.25587,140.9158928,9.8725584,141.6375209,8.6246736,1.03e-05,i,22.423,22.368,0.08,0.079,23.619,23.579
   632,60328.27875,140.9158928,9.8725584,141.6357097,8.6251096,1.76e-05,z,22.729,22.423,0.136,0.136,22.982,22.943
   632,60328.30071,141.6678165,7.1548011,141.634002,8.6255457,1.71e-05,z,22.506,22.552,0.134,0.133,23.006,22.962
   632,60329.25405,142.8361496,7.6203923,141.5610457,8.6442007,9.4e-06,g,23.129,23.081,0.065,0.065,24.462,24.39
   632,60340.20215,140.7268621,9.0201761,140.6614046,8.8967256,1.04e-05,i,22.395,22.27,0.089,0.089,23.291,23.291
   632,60340.22599,140.7268621,9.0201761,140.6593039,8.8973371,1.37e-05,z,22.461,22.368,0.119,0.119,22.942,22.942
   632,60344.1987,140.326146,7.7906532,140.314112,9.0038707,3.22e-05,g,23.158,23.076,0.111,0.111,23.583,23.563
   632,60344.22335,140.326146,7.7906532,140.3118898,9.0045278,9.6e-06,r,22.345,22.586,0.061,0.061,23.802,23.782
   632,60344.27754,140.326146,7.7906532,140.307012,9.0060477,2.74e-05,i,22.111,22.477,0.121,0.121,22.894,22.875
   632,60344.30119,140.326146,7.7906532,140.3048883,9.0066966,2.52e-05,z,22.157,22.296,0.152,0.152,22.616,22.596
   632,60345.18907,140.2280447,8.5837329,140.2272922,9.0314101,1.23e-05,r,22.345,22.448,0.067,0.067,23.668,23.668
   632,60346.16835,141.2076529,9.0398667,140.1413377,9.0589925,1.68e-05,r,22.27,22.395,0.079,0.079,23.477,23.466
   632,60348.25973,140.0293005,8.965671,139.9570249,9.1190653,6.9e-06,r,22.447,22.326,0.049,0.049,24.011,24.011
   632,60351.19357,139.8492054,8.6320566,139.6992239,9.2054883,7.3e-06,g,22.816,22.853,0.05,0.05,24.472,24.472
   632,60351.21734,139.8492054,8.6320566,139.6970959,9.2061844,5.7e-06,r,22.414,22.32,0.043,0.043,24.163,24.163
   632,60356.23982,139.7624114,10.611928,139.2607587,9.3586028,3.09e-05,z,22.276,22.303,0.167,0.167,22.542,22.511
   632,60366.0856,137.8508484,9.4076278,138.4526989,9.6644812,3.53e-05,z,22.248,22.441,0.234,0.233,22.242,22.242
   632,60377.14141,135.9939995,10.2602506,137.6736389,9.9991782,8.7e-06,i,22.612,22.701,0.076,0.076,23.784,23.703
   632,60384.12561,137.578367,10.4153852,137.2810625,10.1951391,9e-06,r,22.692,22.733,0.067,0.067,24.041,24.041
   632,60397.0945,137.6294414,10.4654572,136.8071117,10.5053467,2.82e-05,i,22.715,22.781,0.18,0.18,22.89,22.887
   632,60397.11835,137.6294414,10.4654572,136.8065221,10.5058448,2.86e-05,z,22.447,22.321,0.21,0.209,22.697,22.694
   632,60399.0693,137.5007909,9.6835542,136.7666383,10.5451375,2.45e-05,r,22.901,22.642,0.138,0.138,23.341,23.327
   632,60399.09351,137.5007909,9.6835542,136.7661228,10.5456264,1.57e-05,i,22.846,22.781,0.124,0.124,23.356,23.343
   632,60404.02967,136.6652419,10.7150041,136.703629,10.635411,1.48e-05,r,23.031,22.856,0.093,0.093,23.834,23.834
   632,60407.01166,137.9003026,10.4601787,136.6928919,10.6825895,1.01e-05,r,23.012,22.954,0.078,0.078,24.083,24.064
   632,60407.03549,137.9003026,10.4601787,136.6928541,10.6829441,1.08e-05,i,22.884,22.873,0.094,0.094,23.755,23.735
   632,60419.97412,138.2254847,11.0456903,136.8872669,10.8206369,4.34e-05,i,22.218,22.964,0.272,0.272,22.592,22.563
   632,60426.97045,137.6919103,9.2401203,137.1521501,10.84754,2.4e-05,r,23.096,23.018,0.136,0.136,23.638,23.552
   632,60426.98127,137.6919103,9.2401203,137.1526965,10.8474947,2.59e-05,i,22.967,22.818,0.158,0.158,23.348,23.263
   632,60432.96527,138.1759203,10.3996733,137.4653145,10.8432948,1.47e-05,r,23.093,23.366,0.108,0.108,23.861,23.858
   632,60432.97609,138.1759203,10.3996733,137.4659096,10.8432426,1.12e-05,i,23.105,23.082,0.104,0.104,23.8,23.797
   632,60435.95804,136.7133685,10.5177289,137.6504775,10.8316439,1.94e-05,r,23.373,23.434,0.137,0.137,23.608,23.6
   39265,60370.38399,192.6418095,-32.5378881,193.6750982,-32.7017699,2.8e-06,i,18.027,18.016,0.004,0.004,23.121,23.116
   
.. warning::
   Only one instance of surveySimPP can be run per output directory. Make sure to have different output pathways if you are running multiple instances on the same compute node. 

.. note::
   surveySimPP outputs a log file and error file. If all has gone well, the error file will be empty. The log file has the configuration parameters outputted to it as a record of the run setup. 
