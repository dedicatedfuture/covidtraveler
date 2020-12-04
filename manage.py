"""! @brief COVID Traveler Warning Project"""
##
# @mainpage COVID Traveler Warning Project
#
# @section description_main Description
# COVID  Traveler Warning provides information regarding COVID-19 statistics
# at the county and state level that are useful for a traveler. By entering a zip code
# of a destination, the application will return county and state level statistics, as 
# well as useful informational messages.
#
# @section notes_main Notes
# - This is version 1.0 and is limited to zip code searches.
#
# Copyright (c) 2020 COVID Traveler Warning Team.  All rights reserved.

##
# @file manage.py
#
# @brief manage.py is the starting point for the server application that processes request for the COVID Traveler Warning website.
#
# @section description_manage Description
# This file contains the startup code that invokes the Django framework.
# Django uses the settings.py file to locate the applications internal and external resources.
#
# @section author_manage Author(s)
# - Created by Team #3 on 11/28/2020.
# - Modified by Team #3 on 11/28/2020.
#
# Copyright (c) 2020 COVID Traveler Warning Team.  All rights reserved.
import os
import sys

def main():
    """Run administrative tasks and start the COVID Traveler server."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covidtraveler.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()


