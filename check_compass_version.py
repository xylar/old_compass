#!/usr/bin/env python

import compass
import os
import argparse
import configparser


def main():
    # Define and process input arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-o", "--core", dest="core",
                        help="Core that contains configurations",
                        metavar="CORE")
    parser.add_argument("-f", "--config_file", dest="config_file",
                        required=True,
                        help="Configuration file for test case setup",
                        metavar="FILE")

    args = parser.parse_args()

    if not os.path.exists(args.config_file):
        parser.error(" Configuration file '{}' does not exist. Please create "
                     "and setup before running again.".format(
                         args.config_file))

    config = configparser.ConfigParser()
    config.read(args.config_file)

    mpas_model = config.get('paths', 'mpas_model')

    filename = os.path.join(mpas_model, 'src/core_{}/compass_version'.format(
        args.core))
    with open(filename) as f:
        mpas_model_compass_version = f.readline().strip('\n')

    compass_version = compass.__version__

    if not compass_version.startswith(mpas_model_compass_version.strip('.*')):
        print('compass version: {}'.format(compass_version))
        print('required version from MPAS-Model: {}'.format(
            mpas_model_compass_version))
        raise ValueError('Incompatible COMPASS versions.')


if __name__ == "__main__":
    main()

# vim: foldmethod=marker ai ts=4 sts=4 et sw=4 ft=python
