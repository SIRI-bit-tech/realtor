#!/bin/bash
gunicorn realtor_project.wsgi:application --bind 0.0.0.0:10000 