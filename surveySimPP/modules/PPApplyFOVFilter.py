from . import PPFootprintFilter
import logging
import numpy as np
from astropy.coordinates import SkyCoord


def PPApplyFOVFilter(observations, configs, rng, verbose=False):
    """
    Wrapper function for PPFootprintFilter and PPFilterDetectionEfficiency. Checks to see
    whether a camera footprint filter should be applied or if a simple fraction of the
    circular footprint should be used, then applies the required filter.

    Parameters:
    -----------
    observations (Pandas dataframe): dataframe of observations.

    configs (dictionary): dictionary of variables from config file.

    rng (numpy Generator): numpy random number generator object.

    verbose (boolean): Verbose mode on or off.

    Returns:
    -----------
    observations (Pandas dataframe): dataframe of observations after FOV filters have been applied.
    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if configs['camera_model'] == 'footprint':
        verboselog('Applying sensor footprint filter...')
        footprintf = PPFootprintFilter.Footprint(configs['footprint_path'])
        onSensor, detectorIDs = footprintf.applyFootprint(observations)

        observations = observations.iloc[onSensor].copy()
        observations["detectorID"] = detectorIDs

        observations = observations.sort_index()

    if configs['camera_model'] == 'circle':
        verboselog('FOV is circular...')
        if configs['circle_radius']:
            verboselog('Circle radius is set. Applying circular footprint filter...')
            observations = PPCircleFootprint(observations, configs['circle_radius'])
        if configs['fill_factor']:
            verboselog('Fill factor is set. Removing random observations to mimic chip gaps.')
            observations = PPSimpleSensorArea(observations, rng, configs['fill_factor'])

    return observations


def PPGetSeparation(obj_RA, obj_Dec, cen_RA, cen_Dec):
    """
    Function to calculate the distance of an object from the field centre.

    Parameters:
    -----------
    obj_RA (float): RA of object in decimal degrees.

    obj_Dec (float): Dec of object in decimal degrees.

    cen_RA (float): RA of field centre in decimal degrees.

    cen_Dec (float): Dec of field centre in decimal degrees.

    Returns:
    -----------
    sep_degree (float): The separation of the object from the centre of the field, in decimal
    degrees.

    """

    obj_coord = SkyCoord(ra=obj_RA, dec=obj_Dec, unit="deg")
    cen_coord = SkyCoord(ra=cen_RA, dec=cen_Dec, unit="deg")

    sep = obj_coord.separation(cen_coord)

    return sep.degree


def PPCircleFootprint(observations, circle_radius):
    """Simple function which removes objects which lay outside of a circle
    of given radius centred on the field centre.

    Parameters:
    -----------
    observations (Pandas dataframe): dataframe of observations.

    circle_radius (float): radius of circle footprint in degrees.

    Returns:
    ----------
    new_observations (Pandas dataframe): dataframe of observations with all lying
    beyond the circle radius dropped.

    """

    # note the slightly convoluted syntax in this function seems to be necessary
    # to avoid the dreaded chained indexing Pandas warnings.

    object_separation = observations.apply(lambda x: PPGetSeparation(x["AstRA(deg)"],
                                                                     x["AstDec(deg)"],
                                                                     x.fieldRA,
                                                                     x.fieldDec),
                                           axis=1)

    observations['object_separation'] = object_separation
    new_observations = observations[observations['object_separation'] < circle_radius]

    new_observations.reset_index(drop=True, inplace=True)
    new_observations = new_observations.drop('object_separation', axis=1)

    return new_observations


def PPSimpleSensorArea(ephemsdf, rng, fillfactor=0.9):
    """
    Randomly removes a number of observations proportional to the
    fraction of the field not covered by the detector.

    Parameters:
    -----------
    ephemsdf (Pandas dataframe): dataframe containing observations.

    rng (numpy Generator): numpy random number generator object.

    fillfactor (float): fraction of FOV covered by the sensor.

    Returns:
    ----------
    ephemsOut (Pandas dataframe): dataframe of observations with fraction removed.

    """

    n = len(ephemsdf)

    randomNum = rng.random(n)
    fillArray = np.zeros(n) + fillfactor
    dropObs = np.where(randomNum > fillArray)[0]

    ephemsOut = ephemsdf.drop(dropObs)
    ephemsOut = ephemsOut.reset_index(drop=True)

    return ephemsOut
