#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# sample.py - a sample file for using jobsched.py

import jobsched

params_list = [(2, "Tokyo"), (4, "Osaka"), (6,), (8,), (10, )]
job_sched = jobsched.JobScheduler(2, ('echo', 'Hello'), params_list, interval=2, verbose=True)
job_sched.run()
